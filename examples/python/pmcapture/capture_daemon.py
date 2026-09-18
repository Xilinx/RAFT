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


# Linux pid_t is a signed 32-bit C int.  JSON will decode a larger integer,
# and os.kill() then raises OverflowError instead of OSError.  A grant that
# recorded such a pid would make every later reclaim crash, so both the
# request parser and the liveness probe reject it.
_PID_T_MAX = 0x7FFFFFFF


# Return True unless the process is known to be gone.
def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OverflowError:
        return False
    except OSError:
        # EPERM means the process exists but is owned by another user.
        return True
    return True


# Turn down an acquire or release, recording why.
#
# Refusals are logged where grants are not: a grant only means the bus
# changed hands as intended, while a refusal means a client went without the
# bus and its operation failed.  They are also rare, since the arbiter is
# idle almost all the time, so INFO keeps them in the default journal.  A
# field failure whose cause was contention leaves no other trace of who was
# holding the bus at the time.
def _refuse(cmd: str, holder: str, pid: int, error: str) -> dict:
    logging.info("%s refused for %s (pid %d): %s", cmd, holder, pid, error)
    return {"ok": False, "error": error}


# Turn down one of pmcapture's own operations -- a start, an arm, or a
# triggered capture -- and record why.
#
# The counterpart of _refuse for requests that carry no holder, since these
# arrive from the operator's CLI or from a GPIO trigger rather than from a
# client.  Contention matters just as much in this direction: "exclusive
# lock held by ..." is the operator being told that another service owns the
# bus, which is the same thing worth finding in a journal after the fact.
def _refuse_local(cmd: str, error: str) -> dict:
    logging.info("%s refused: %s", cmd, error)
    return {"ok": False, "error": error}


# Validate the holder/pid pair carried by acquire and release requests.
# A malformed request is a client bug rather than contention, so it is
# logged more loudly than a refusal and cannot always name its sender.
def _holder_from_request(req: dict, cmd: str) -> tuple[str, int, dict | None]:
    holder = str(req.get("holder") or "").strip()
    if not holder:
        logging.warning("%s rejected: request carries no holder", cmd)
        return "", 0, {"ok": False, "error": f"{cmd} requires holder"}
    pid = req.get("pid")
    if (
        isinstance(pid, bool)
        or not isinstance(pid, int)
        or pid <= 0
        or pid > _PID_T_MAX
    ):
        logging.warning(
            "%s rejected for %s: pid %r is not a positive integer",
            cmd,
            holder,
            pid,
        )
        return "", 0, {"ok": False, "error": f"{cmd} requires integer pid"}
    return holder, pid, None


# Idle supervisor: one session slot, GPIO arm, Unix control socket.
class CaptureDaemon:
    # Initialize daemon state, session slot, and GPIO arm fields.
    def __init__(self):
        self._session: CaptureSession | None = None
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._daemon_started_at = time.time()
        self._start_in_progress = False
        self._arm_in_progress = False
        # Exclusive window granted to another SC service (see "acquire").
        self._exclusive: dict | None = None
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
    # The exclusive holder is deliberately absent: it changes once per bus
    # transaction, so a snapshot file would be stale far more often than
    # correct.  Read it live from the "status" command instead.
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

    # Return the exclusive holder, reclaiming it if its process is gone.
    # Caller must hold the lock.
    def _exclusive_holder_locked(self) -> dict | None:
        holder = self._exclusive
        if holder is None:
            return None
        pid = holder.get("pid")
        if isinstance(pid, int) and not _pid_alive(pid):
            logging.warning(
                "reclaiming exclusive lock from dead holder %s (pid %d)",
                holder.get("holder"),
                pid,
            )
            self._exclusive = None
            return None
        return holder

    # Why the daemon cannot take the bus, or None if it is idle.
    #
    # Caller must hold the lock.  Operations that go on to claim the bus have
    # to test and reserve without releasing it: checking here and committing
    # under a second lock would let an "acquire" land in between and hand a
    # client the bus while the start or arm went ahead anyway.
    #
    # Armed is not in this helper.  A GPIO-triggered start is supposed to run
    # while armed, and it uses this helper.  Manual start and acquire each
    # refuse armed on their own, in the same critical section as their claim.
    def _busy_reason_locked(self) -> str | None:
        holder = self._exclusive_holder_locked()
        if holder is not None:
            return (
                "system busy: exclusive lock held by "
                f"{holder['holder']} (pid {holder['pid']})"
            )
        if self._session is not None and self._session.is_running():
            return "system busy: pmcapture capture session running"
        if self._start_in_progress:
            return "system busy: capture start in progress"
        if self._arm_in_progress:
            return "system busy: pmcapture arm in progress"
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
    # cmd names the caller for the log line when the start is refused.
    def _start_session_params(self, params: SessionParams, cmd: str = "start") -> dict:
        # Test and reserve together.  _start_in_progress is what makes a
        # concurrent "acquire" back off, so it has to be set before the lock is
        # released, not after a separate busy check.
        with self._lock:
            running_status = None
            reason = None
            if self._session is not None and self._session.is_running():
                running_status = self._session.status_dict()
            elif cmd == "start" and self._armed:
                # Manual start only.  A GPIO-triggered start is supposed to
                # run while armed; that path calls this helper as
                # "triggered capture".  The check lives here, in the same
                # section that sets _start_in_progress, because start loads
                # its config before it reserves and an arm that finishes in
                # that stretch must still be seen.
                reason = "manual start not allowed while armed (disarm first)"
            else:
                reason = self._busy_reason_locked()
                if reason is None:
                    self._start_in_progress = True
        if running_status is not None:
            resp = _refuse_local(cmd, "capture already running")
            resp["session"] = running_status
            return resp
        if reason is not None:
            return _refuse_local(cmd, reason)

        from capture_session import CaptureSession

        session = None
        started = False
        try:
            session = CaptureSession(params)
            session.set_on_change(self._on_session_change)
            session.start()
            started = True
        except Exception as e:
            if session is not None:
                session.stop(timeout=5.0)
            return {"ok": False, "error": str(e)}
        finally:
            # Publish the session and drop the reservation in one critical
            # section.  The sampler is already on the bus once start() returns,
            # so releasing the reservation first would leave an instant where
            # the daemon looks idle and an "acquire" would be granted.
            with self._lock:
                if started:
                    self._session = session
                    self._daemon_error = None
                self._start_in_progress = False
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
        resp = self._start_session_params(profile, cmd="triggered capture")
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

    # Clear arm state and detach the trigger monitor (caller must hold lock).
    #
    # The monitor is returned rather than stopped here: stop() joins the
    # watcher thread, and on a trigger edge that thread is inside
    # _on_gpio_assert waiting for this same lock, so joining under the lock
    # would block both until the join timeout expired and stall every client
    # acquire behind it.  Callers stop it after releasing the lock.
    def _disarm_locked(self):
        monitor = self._trigger_monitor
        self._trigger_monitor = None
        self._armed = False
        self._armed_profile = None
        self._armed_trigger = None
        self._armed_at = None
        self._gpio_gated = False
        return monitor

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
                exclusive = self._exclusive_holder_locked()
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
                "exclusive": dict(exclusive) if exclusive else None,
                "error": self._daemon_error,
            }
        if cmd == "acquire":
            holder, pid, err = _holder_from_request(req, "acquire")
            if err is not None:
                return err
            refusal = None
            granted = None
            with self._lock:
                current = self._exclusive_holder_locked()
                if current is not None:
                    if current["holder"] == holder and current["pid"] == pid:
                        # Repeat acquire from the same caller is a no-op.
                        return {
                            "ok": True,
                            "exclusive": dict(current),
                            "message": "already held",
                        }
                    refusal = (
                        "system busy: exclusive lock held by "
                        f"{current['holder']} (pid {current['pid']})"
                    )
                else:
                    # Same states start and arm refuse on, plus armed:
                    # a trigger can assert at any moment, so a client
                    # window is not granted while the daemon is waiting
                    # for one.
                    refusal = self._busy_reason_locked()
                    if self._armed and refusal is None:
                        refusal = (
                            "system busy: pmcapture armed for triggered "
                            "capture (disarm first)"
                        )
                    if refusal is None:
                        # Grants happen only from idle.
                        granted = {
                            "holder": holder,
                            "pid": pid,
                            "since": time.time(),
                        }
                        self._exclusive = granted

            # Both outcomes are logged outside the critical section, so the
            # test-and-set stays free of I/O and one client's journal write
            # cannot delay another client's acquire.
            if refusal is not None:
                return _refuse("acquire", holder, pid, refusal)
            # Debug level on purpose.  The daemon sits idle almost all the
            # time, which is exactly when windows are granted, so logging each
            # one would add a grant and a release line for every client
            # operation.  Use --debug to trace them.
            logging.debug("exclusive lock granted to %s (pid %d)", holder, pid)
            return {"ok": True, "exclusive": dict(granted)}
        if cmd == "release":
            holder, pid, err = _holder_from_request(req, "release")
            if err is not None:
                return err
            refusal = None
            with self._lock:
                current = self._exclusive_holder_locked()
                if current is None:
                    return {"ok": True, "message": "not locked"}
                if current["holder"] != holder or current["pid"] != pid:
                    refusal = (
                        "exclusive lock held by "
                        f"{current['holder']} (pid {current['pid']})"
                    )
                else:
                    self._exclusive = None

            if refusal is not None:
                return _refuse("release", holder, pid, refusal)
            logging.debug("exclusive lock released by %s (pid %d)", holder, pid)
            return {"ok": True, "message": "released"}
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
                monitor = self._disarm_locked()
                self._session = None
                self._daemon_error = None
            if monitor is not None:
                monitor.stop()
            self._publish_status()
            return {"ok": True, "state": "idle"}
        if cmd == "arm":
            from capture_config import (
                load_capture_config,
                merge_arm_trigger,
                resolve_trigger_spec,
            )
            from trigger_monitor import TriggerMonitor

            # Arm reserves the bus before it does any of its slow setup.
            # Loading the capture config, resolving the trigger and requesting
            # the GPIO line all run unlocked, so without _arm_in_progress an
            # "acquire" arriving in that stretch would be granted and the arm
            # would still commit, leaving a client holding the bus while the
            # daemon is armed.
            with self._lock:
                if self._armed:
                    reason = "already armed (disarm first)"
                else:
                    reason = self._busy_reason_locked()
                    if reason is None:
                        self._arm_in_progress = True
            if reason is not None:
                return _refuse_local("arm", reason)

            try:
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
                    # Drop the reservation here, in the same step that publishes
                    # _armed.  The GPIO watcher is already running, and a
                    # triggered start uses _busy_reason_locked(), which treats
                    # _arm_in_progress as busy.  Leaving the flag set until
                    # finally would drop a trigger edge that lands in between.
                    self._arm_in_progress = False
            finally:
                # Failure paths never set _armed, so this is what drops the
                # reservation.  Success already dropped it above.
                with self._lock:
                    self._arm_in_progress = False
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
            try:
                params = self._params_from_request(
                    req, client=str(req.get("client", "cli"))
                )
            except (OSError, ValueError) as e:
                return {"ok": False, "error": str(e)}
            # Armed is re-checked inside _start_session_params, in the same
            # step that sets _start_in_progress, because config load above
            # runs unlocked.
            return self._start_session_params(params)

        return {"ok": False, "error": f"unknown command: {cmd!r}"}

    # Record that a reply never reached the client that asked for it, and
    # take back a window the client never learned it had.
    #
    # A client's own timeout is shorter than this end's, so a send that fails
    # means it gave up first.  Clients fail closed, so a grant they never
    # heard about is not in use, and a running capture is not in doubt.  What
    # does need undoing is that grant: the client cannot send a release for a
    # window it never heard about, and both clients are long-lived services
    # whose pids stay alive, so the dead-holder reclaim would never fire and
    # the window would be held for the life of the process, refusing every
    # capture.  Taking it back is safe only for a grant this connection just
    # made.  An "already held" reply means the same process already owns the
    # window and may be on the bus; dropping that hold would let someone else
    # in underneath it.
    def _reply_undelivered(self, req: dict, resp: dict, err: OSError) -> None:
        cmd = ""
        if isinstance(req, dict):
            cmd = (req.get("cmd") or "").strip().lower()
        logging.warning("%s reply undelivered: %s", cmd or "request", err)
        if cmd != "acquire" or not isinstance(resp, dict) or not resp.get("ok"):
            return
        if resp.get("message") == "already held":
            return

        holder, pid, err_resp = _holder_from_request(req, "acquire")
        if err_resp is not None:
            return

        with self._lock:
            current = self._exclusive
            if current is None:
                return
            # Only ever take back this client's own window.
            if current.get("holder") != holder or current.get("pid") != pid:
                return
            self._exclusive = None

        logging.warning(
            "exclusive lock taken back from %s (pid %d): its grant was never "
            "delivered, so it failed the operation rather than using the bus",
            holder,
            pid,
        )

    # Handle one control-socket client connection in a worker thread.
    def _client_thread(self, conn: socket.socket):
        req: dict = {}
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
            try:
                conn.sendall((json.dumps(resp) + "\n").encode())
            except OSError as err:
                self._reply_undelivered(req, resp, err)
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
            self._exclusive = None
            monitor = self._disarm_locked()
        if monitor is not None:
            monitor.stop()
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
                monitor = self._disarm_locked()
            if monitor is not None:
                monitor.stop()
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
