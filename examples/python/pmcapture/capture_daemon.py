#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Background service: one capture at a time, commands over a Unix socket.
# Started by systemd; controlled by the pmcapture CLI.

from __future__ import annotations

import json
import logging
import os
import signal
import socket
import threading
import time
from typing import TYPE_CHECKING

from capture_status import build_capture_visibility

if TYPE_CHECKING:
    from capture_config import TriggerSpec
    from capture_session import CaptureSession, SessionParams
    from trigger_monitor import TriggerMonitor

RUN_DIR = "/run/pmcapture"
CONTROL_SOCK = os.path.join(RUN_DIR, "control.sock")
STATUS_FILE = os.path.join(RUN_DIR, "status.json")


# Atomically write daemon status to /run/pmcapture/status.json.
def write_status(payload: dict, *, sync: bool = True) -> None:
    os.makedirs(RUN_DIR, mode=0o755, exist_ok=True)
    tmp = STATUS_FILE + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        fh.flush()
        if sync:
            os.fsync(fh.fileno())
    os.replace(tmp, STATUS_FILE)


# Read status.json; return unknown state if missing or invalid.
def read_status_file() -> dict:
    try:
        with open(STATUS_FILE, "r") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"state": "unknown", "daemon_reachable": False}


# Idle supervisor: one session slot, GPIO arm, Unix control socket.
class CaptureDaemon:
    # Initialize daemon state, session slot, and GPIO arm fields.
    def __init__(self):
        self._session: CaptureSession | None = None
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._daemon_started_at = time.time()
        self._start_in_progress = False
        # GPIO triggered capture (arm / disarm)
        self._armed = False
        self._armed_profile: SessionParams | None = None
        self._armed_trigger: TriggerSpec | None = None
        self._trigger_monitor: TriggerMonitor | None = None
        self._gpio_gated = False
        self._armed_at: float | None = None
        self._windows_completed = 0
        self._trigger_window_seq = 0
        self._daemon_error: str | None = None

    # Derive high-level daemon state from session, arm, and error flags.
    def _daemon_state(self) -> str:
        with self._lock:
            if self._daemon_error:
                return "error"
            if self._session is not None and self._session.is_running():
                return "running"
            if self._armed:
                return "armed"
            return "idle"

    # Build trigger subsection for status.json when armed.
    def _trigger_status(self) -> dict | None:
        with self._lock:
            if not self._armed or self._armed_trigger is None:
                return None
            spec = self._armed_trigger
            monitor = self._trigger_monitor
            level = monitor.read_level() if monitor is not None else None
            out = {
                "gpio": spec.gpio,
                "active": spec.active,
                "chip": spec.chip,
                "line": spec.line_offset,
                "level": level,
                "armed_at": self._armed_at,
                "windows_completed": self._windows_completed,
            }
            session_running = (
                self._session is not None and self._session.is_running()
            )
            if self._gpio_gated and not session_running:
                # Stale after failed/raced GPIO start or missed session callback.
                self._gpio_gated = False
            if self._gpio_gated and session_running:
                out["gpio_gated"] = True
            return out

    # Publish combined daemon/session/trigger status to status.json.
    def _publish_status(self, *, sync: bool = True):
        with self._lock:
            if self._session is not None and self._session.is_running():
                session = self._session.status_dict()
            else:
                session = None
            state = self._daemon_state()
            trigger = self._trigger_status()
            capture = build_capture_visibility(
                state=state,
                session=session,
                trigger=trigger,
                error=self._daemon_error,
            )
            payload = {
                "state": state,
                "sampling_active": capture["sampling_active"],
                "armed": capture["armed"],
                "capture": capture,
                "daemon_pid": os.getpid(),
                "daemon_started_at": self._daemon_started_at,
                "control_sock": CONTROL_SOCK,
                "session": session,
                "trigger": trigger,
                "error": self._daemon_error,
            }
        write_status(payload, sync=sync)

    # Refresh status when a capture session stops or changes state.
    def _on_session_change(self):
        with self._lock:
            if self._session is not None and not self._session.is_running():
                if self._gpio_gated and self._session.status.state != "error":
                    self._windows_completed += 1
                err = self._session.status.error
                if err:
                    self._daemon_error = err
                self._session = None
                self._gpio_gated = False
        self._publish_status()

    # Return busy error dict if a session start is already in progress.
    def _busy_error(self) -> dict | None:
        with self._lock:
            if self._session is not None and self._session.is_running():
                return {
                    "ok": False,
                    "error": "system busy: pmcapture capture session running",
                }
            if self._start_in_progress:
                return {
                    "ok": False,
                    "error": "system busy: capture start in progress",
                }
        return None

    # Build SessionParams from a control-socket start/arm request.
    def _params_from_request(
        self,
        req: dict,
        *,
        client: str = "cli",
        trigger_window: str | None = None,
    ) -> SessionParams:
        from capture_config import load_capture_config, merge_start_options
        from capture_session import SessionParams
        from sampler_engine import RAILS_ALL

        cap_cfg = None
        cap_path = req.get("capture_config")
        if cap_path:
            cap_cfg = load_capture_config(cap_path)

        base = {
            "rails": req.get("rails", RAILS_ALL),
            "capture_config": cap_path,
            "output": req.get("output", "file"),
            "rate": float(req.get("rate", 20.0)),
            "duration": float(req.get("duration", 0.0)),
            "output_file": req.get("output_file"),
            "file_format": req.get("file_format", "jsonl"),
            "host": req.get("host", "0.0.0.0"),
            "port": int(req.get("port", 18094)),
            "client": client,
        }
        merged = merge_start_options(base, cap_cfg)

        return SessionParams(
            rails=str(merged.get("rails", RAILS_ALL)),
            capture_config=merged.get("capture_config"),
            output=str(merged.get("output", "file")),
            rate=float(merged.get("rate", 20.0)),
            duration=float(merged.get("duration", 0.0)),
            output_file=merged.get("output_file"),
            file_format=str(merged.get("file_format", "jsonl")),
            host=str(merged.get("host", "0.0.0.0")),
            port=int(merged.get("port", 18094)),
            client=str(merged.get("client", client)),
            trigger_window=trigger_window,
        )

    # Start a capture session from SessionParams if the daemon is idle.
    def _start_session_params(self, params: SessionParams) -> dict:
        from capture_session import CaptureSession

        busy = self._busy_error()
        if busy:
            return busy

        with self._lock:
            if self._session is not None and self._session.is_running():
                return {
                    "ok": False,
                    "error": "capture already running",
                    "session": self._session.status_dict(),
                }
            self._start_in_progress = True

        session = None
        try:
            session = CaptureSession(params)
            session.set_on_change(self._on_session_change)
            session.start()
        except Exception as e:
            if session is not None:
                session.stop(timeout=5.0)
            return {"ok": False, "error": str(e)}
        finally:
            with self._lock:
                self._start_in_progress = False

        with self._lock:
            self._session = session
            self._daemon_error = None
        self._publish_status()
        return {"ok": True, "session": session.status_dict()}

    # Start an open-ended GPIO capture window on trigger assert.
    def _on_gpio_assert(self) -> None:
        from capture_session import SessionParams

        with self._lock:
            if not self._armed or self._armed_profile is None:
                return
            if self._session is not None and self._session.is_running():
                return
            if self._start_in_progress:
                return
            self._trigger_window_seq += 1
            window = f"gpio{self._trigger_window_seq}"
            profile = SessionParams(
                rails=self._armed_profile.rails,
                capture_config=self._armed_profile.capture_config,
                output="file",
                rate=self._armed_profile.rate,
                duration=0.0,
                output_file=self._armed_profile.output_file,
                file_format=self._armed_profile.file_format,
                host=self._armed_profile.host,
                port=self._armed_profile.port,
                client="gpio",
                log_dir=self._armed_profile.log_dir,
                trigger_window=window,
            )
            self._gpio_gated = True
        logging.info("GPIO assert — starting capture window %s", window)
        resp = self._start_session_params(profile)
        if not resp.get("ok"):
            logging.error("GPIO assert start failed: %s", resp.get("error"))
            with self._lock:
                self._gpio_gated = False

    # Request stop when GPIO deasserts during an active gated capture.
    def _on_gpio_deassert(self) -> None:
        with self._lock:
            if not self._gpio_gated:
                return
            session = self._session
        if session is not None and session.is_running():
            logging.info("GPIO deassert — stopping capture session")
            session.request_stop()

    # Clear arm state and stop trigger monitor (caller must hold lock).
    def _disarm_locked(self) -> None:
        monitor = self._trigger_monitor
        self._trigger_monitor = None
        self._armed = False
        self._armed_profile = None
        self._armed_trigger = None
        self._armed_at = None
        self._gpio_gated = False
        if monitor is not None:
            monitor.stop()

    # Dispatch a JSON control command from the Unix socket.
    def handle_command(self, req: dict) -> dict:
        cmd = (req.get("cmd") or "").strip().lower()
        if cmd == "ping":
            return {"ok": True, "pong": True}
        if cmd == "status":
            self._publish_status()
            with self._lock:
                running = self._session is not None and self._session.is_running()
                sess = self._session.status_dict() if running else None
                trigger = self._trigger_status()
                state = self._daemon_state()
                capture = build_capture_visibility(
                    state=state,
                    session=sess,
                    trigger=trigger,
                    error=self._daemon_error,
                )
            return {
                "ok": True,
                "state": state,
                "sampling_active": capture["sampling_active"],
                "armed": capture["armed"],
                "capture": capture,
                "session": sess,
                "trigger": trigger,
                "error": self._daemon_error,
            }
        if cmd == "disarm":
            with self._lock:
                if not self._armed:
                    self._publish_status()
                    return {"ok": True, "state": "idle", "message": "not armed"}
                session = self._session
                gpio_gated = self._gpio_gated
            if session is not None and session.is_running() and gpio_gated:
                session.stop()
            with self._lock:
                self._disarm_locked()
                self._session = None
                self._daemon_error = None
            self._publish_status()
            return {"ok": True, "state": "idle"}
        if cmd == "arm":
            from capture_config import (
                load_capture_config,
                merge_arm_trigger,
                resolve_trigger_spec,
            )
            from trigger_monitor import TriggerMonitor

            with self._lock:
                if self._armed:
                    return {"ok": False, "error": "already armed (disarm first)"}
            busy = self._busy_error()
            if busy:
                return busy

            cap_path = req.get("capture_config")
            cap_cfg = None
            if cap_path:
                try:
                    cap_cfg = load_capture_config(cap_path)
                except (OSError, ValueError) as e:
                    return {"ok": False, "error": str(e)}
            elif not req.get("gpio"):
                return {
                    "ok": False,
                    "error": "arm requires --gpio or capture_config with trigger block",
                }

            try:
                trigger = merge_arm_trigger(req, cap_cfg)
                trigger = resolve_trigger_spec(trigger)
            except (OSError, ValueError) as e:
                return {"ok": False, "error": str(e)}

            arm_req = dict(req)
            arm_req.setdefault("output", "file")
            arm_req["duration"] = 0.0
            if cap_path:
                arm_req["capture_config"] = cap_path
            try:
                profile = self._params_from_request(arm_req, client="gpio")
            except (OSError, ValueError) as e:
                return {"ok": False, "error": str(e)}
            if profile.output != "file":
                return {
                    "ok": False,
                    "error": "GPIO triggered capture requires output=file",
                }

            monitor = TriggerMonitor(
                trigger,
                on_assert=self._on_gpio_assert,
                on_deassert=self._on_gpio_deassert,
            )
            try:
                monitor.start()
            except Exception as e:
                return {"ok": False, "error": f"trigger monitor failed: {e}"}

            with self._lock:
                self._armed = True
                self._armed_profile = profile
                self._armed_trigger = trigger
                self._trigger_monitor = monitor
                self._armed_at = time.time()
                self._windows_completed = 0
                self._trigger_window_seq = 0
                self._daemon_error = None
            self._publish_status()
            return {
                "ok": True,
                "state": "armed",
                "trigger": self._trigger_status(),
            }
        if cmd == "stop":
            with self._lock:
                if self._session is None or not self._session.is_running():
                    self._publish_status()
                    return {"ok": True, "state": "idle", "message": "not running"}
                session = self._session
            session.stop()
            with self._lock:
                self._session = None
            self._publish_status()
            return {"ok": True, "state": "idle"}
        if cmd == "start":
            with self._lock:
                if self._armed:
                    return {
                        "ok": False,
                        "error": "manual start not allowed while armed (disarm first)",
                    }
            try:
                params = self._params_from_request(
                    req, client=str(req.get("client", "cli"))
                )
            except (OSError, ValueError) as e:
                return {"ok": False, "error": str(e)}
            return self._start_session_params(params)

        return {"ok": False, "error": f"unknown command: {cmd!r}"}

    # Handle one control-socket client connection in a worker thread.
    def _client_thread(self, conn: socket.socket):
        try:
            conn.settimeout(5.0)
            chunks: list[bytes] = []
            while True:
                part = conn.recv(4096)
                if not part:
                    break
                chunks.append(part)
                if b"\n" in part:
                    break
            raw = b"".join(chunks).decode("utf-8", errors="replace").strip()
            if not raw:
                resp = {"ok": False, "error": "empty request"}
            else:
                req = json.loads(raw.split("\n", 1)[0])
                resp = self.handle_command(req)
            conn.sendall((json.dumps(resp) + "\n").encode())
        except json.JSONDecodeError:
            conn.sendall(
                (json.dumps({"ok": False, "error": "invalid JSON"}) + "\n").encode()
            )
        except Exception as e:
            logging.exception("control client error: %s", e)
            try:
                conn.sendall(
                    (json.dumps({"ok": False, "error": str(e)}) + "\n").encode()
                )
            except OSError:
                pass
        finally:
            try:
                conn.close()
            except OSError:
                pass

    # Unblock accept() so the main loop can exit on shutdown.
    def _wake_listener(self, srv: socket.socket) -> None:
        try:
            srv.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    # Stop session, disarm, remove socket, and write final status.
    def _finalize_shutdown(self, srv: socket.socket, timeout: float = 5.0) -> None:
        with self._lock:
            session = self._session
            self._session = None
            self._disarm_locked()
        if session is not None:
            session.stop(timeout=timeout)
        try:
            srv.close()
        except OSError:
            pass
        try:
            os.unlink(CONTROL_SOCK)
        except OSError:
            pass
        self._publish_status(sync=False)

    # Bind control socket, accept clients, and run until SIGINT/SIGTERM.
    def serve(self):
        os.makedirs(RUN_DIR, mode=0o755, exist_ok=True)
        if os.path.exists(CONTROL_SOCK):
            try:
                os.unlink(CONTROL_SOCK)
            except OSError:
                pass

        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(CONTROL_SOCK)
        os.chmod(CONTROL_SOCK, 0o666)
        srv.listen(8)
        logging.info("pmcapture daemon idle — control socket %s", CONTROL_SOCK)
        self._publish_status()

        # Handle SIGINT/SIGTERM: stop session, disarm, and wake accept loop.
        def shutdown(signum, _frame):
            # Keep the handler minimal — Python runs it on the main thread and
            # blocks the accept loop until it returns.
            logging.info("daemon shutdown signal %s", signum)
            self._stop_event.set()
            with self._lock:
                if self._session is not None:
                    self._session.request_stop()
                self._disarm_locked()
            self._wake_listener(srv)

        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)

        srv.settimeout(0.5)
        while not self._stop_event.is_set():
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=self._client_thread,
                args=(conn,),
                daemon=True,
                name="control-client",
            ).start()

        self._finalize_shutdown(srv)


# Configure logging and enter CaptureDaemon.serve().
def run_daemon(debug: bool = False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)-5s %(message)s",
    )
    CaptureDaemon().serve()
