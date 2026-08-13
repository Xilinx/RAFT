#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# One capture run: select rails, poll INA sensors, stream results to file or TCP.
# Started by capture_daemon (manual start or GPIO trigger window).

from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from dataclasses import dataclass, field

from board_config import BoardConfig, SensorSpec, load_board_config
from capture_config import apply_capture_config, load_capture_config
from capture_output import DEFAULT_LOG_DIR, resolve_output_path, run_file_capture, run_tcp_server
from disk_guard import InsufficientDiskSpaceError, require_disk_space_for_output
from sampler_engine import (
    RAILS_ALL,
    RailSampleError,
    SensorBank,
    Sampler,
    catalog_msg,
    select_sensors,
)


# Parameters for one capture session (CLI or GPIO window).
@dataclass
class SessionParams:
    rails: str = RAILS_ALL
    capture_config: str | None = None
    output: str = "file"
    rate: float = 20.0
    duration: float = 0.0
    output_file: str | None = None
    file_format: str = "jsonl"
    host: str = "0.0.0.0"
    port: int = 18094
    client: str = "cli"
    log_dir: str = DEFAULT_LOG_DIR
    trigger_window: str | None = None


# Mutable session status exported in status.json.
@dataclass
class SessionStatus:
    session_id: str
    state: str = "starting"
    started_at: float = 0.0
    board: str = ""
    output: str = "file"
    output_file: str | None = None
    port: int = 18094
    rate_hz: float = 20.0
    duration: float = 0.0
    rails: list[str] = field(default_factory=list)
    rails_selector: str = RAILS_ALL
    client: str = "cli"
    sample_count: int = 0
    error: str | None = None

    # Seconds since session start (0 if not started).
    def elapsed_s(self) -> float:
        if not self.started_at:
            return 0.0
        return round(time.time() - self.started_at, 1)

    # Serialize session status for status.json and CLI output.
    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "state": self.state,
            "started_at": self.started_at,
            "elapsed_s": self.elapsed_s(),
            "board": self.board,
            "output": self.output,
            "output_file": self.output_file,
            "port": self.port,
            "rate_hz": self.rate_hz,
            "duration": self.duration,
            "rails": self.rails,
            "rails_selector": self.rails_selector,
            "client": self.client,
            "sample_count": self.sample_count,
            "error": self.error,
        }


# Load board config and resolve rails (raises ValueError if invalid).
def resolve_session_specs(p: SessionParams) -> tuple[BoardConfig, list[SensorSpec]]:
    cfg = load_board_config()
    specs = select_sensors(cfg, p.rails)
    if p.capture_config:
        cap_cfg = load_capture_config(p.capture_config)
        specs = apply_capture_config(cfg, specs, cap_cfg)
    return cfg, specs


# One running capture: sampler thread plus file or TCP output sink.
class CaptureSession:
    WATCHDOG_TIMEOUT_S = 30.0

    # Initialize session state from SessionParams.
    def __init__(self, params: SessionParams):
        self.params = params
        self.session_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        self.status = SessionStatus(
            session_id=self.session_id,
            output=params.output,
            port=params.port,
            rate_hz=params.rate,
            duration=params.duration,
            client=params.client,
        )
        self._lock = threading.Lock()
        self._worker: threading.Thread | None = None
        self._sampler: Sampler | None = None
        self._on_change = None
        self._board_cfg: BoardConfig | None = None
        self._specs: list[SensorSpec] | None = None

    # Register callback invoked when session status changes.
    def set_on_change(self, cb):
        self._on_change = cb

    # Invoke the registered status-change callback if set.
    def _notify(self):
        if self._on_change is not None:
            self._on_change()

    # Return True while the capture worker thread is alive.
    def is_running(self) -> bool:
        with self._lock:
            return self._worker is not None and self._worker.is_alive()

    # Build status dict including live sampler metrics when available.
    def status_dict(self) -> dict:
        with self._lock:
            st = self.status.to_dict()
            st["requested_rate_hz"] = st["rate_hz"]
            if self._sampler is not None:
                st["sample_count"] = self._sampler.sample_count
                st["actual_rate_hz"] = round(self._sampler.actual_rate, 1)
            return st

    # Preflight rails and spawn the capture worker thread.
    def start(self) -> None:
        with self._lock:
            if self._worker is not None and self._worker.is_alive():
                raise RuntimeError("capture session already running")
        cfg, specs = resolve_session_specs(self.params)
        rail_names = [s.name for s in specs]
        p = self.params
        if p.output == "file":
            out_path = resolve_output_path(
                p.output_file,
                p.file_format,
                p.log_dir,
                board_name=cfg.board_name,
                suffix=p.trigger_window,
            )
            require_disk_space_for_output(out_path)
        with self._lock:
            self._board_cfg = cfg
            self._specs = specs
            self.status.board = cfg.board_name
            self.status.rails = rail_names
            self.status.rails_selector = str(self.params.rails or RAILS_ALL)
            self._worker = threading.Thread(
                target=self._run, name="capture-session", daemon=True
            )
            self._worker.start()

    # Signal an active session to stop without waiting.
    def request_stop(self) -> None:
        with self._lock:
            if self._sampler is not None:
                self._sampler.stop_event.set()

    # Request stop and wait for the worker thread to finish.
    def stop(self, timeout: float = 15.0) -> None:
        self.request_stop()
        worker = None
        with self._lock:
            worker = self._worker
        if worker is not None and worker.is_alive():
            worker.join(timeout=timeout)
        with self._lock:
            if self.status.state not in ("idle", "error"):
                self.status.state = "idle"
            self._worker = None
        self._notify()

    # Worker thread: run sampler and file or TCP output until stop.
    def _run(self):
        p = self.params
        try:
            rate = max(0.1, min(50.0, p.rate))
            with self._lock:
                cfg = self._board_cfg
                specs = self._specs
            if cfg is None or specs is None:
                cfg, specs = resolve_session_specs(p)

            rail_names = [s.name for s in specs]

            with self._lock:
                self.status.board = cfg.board_name
                self.status.rails = rail_names
                self.status.rails_selector = str(p.rails or RAILS_ALL)
                self.status.rate_hz = rate
                self.status.started_at = time.time()
                self.status.state = "running"

            bank = SensorBank(specs)
            sampler = Sampler(rate, bank)
            sampler.board_name = cfg.board_name
            self._sampler = sampler
            sampler.start()
            logging.info(
                "session %s: %.1f Hz, %d rails, output=%s",
                self.session_id,
                rate,
                len(specs),
                p.output,
            )
            self._notify()

            threading.Thread(
                target=self._watchdog,
                args=(sampler,),
                daemon=True,
                name="session-watchdog",
            ).start()

            catalog = catalog_msg(cfg, specs)
            if p.output == "file":
                os.makedirs(p.log_dir, mode=0o755, exist_ok=True)
                out_path = resolve_output_path(
                    p.output_file,
                    p.file_format,
                    p.log_dir,
                    board_name=cfg.board_name,
                    suffix=p.trigger_window,
                )
                require_disk_space_for_output(out_path)
                with self._lock:
                    self.status.output_file = out_path
                self._notify()
                run_file_capture(
                    sampler,
                    catalog,
                    rail_names,
                    out_path,
                    p.file_format,
                    p.duration,
                )
            else:
                run_tcp_server(sampler, catalog, p.host, p.port, p.duration)

            if sampler.sample_error:
                logging.error("%s", sampler.sample_error)
                with self._lock:
                    self.status.state = "error"
                    self.status.error = sampler.sample_error
            else:
                with self._lock:
                    self.status.state = "idle"
                    if self._sampler is not None:
                        self.status.sample_count = self._sampler.sample_count
        except InsufficientDiskSpaceError as e:
            logging.error("%s", e)
            with self._lock:
                self.status.state = "error"
                self.status.error = str(e)
        except RailSampleError as e:
            logging.error("%s", e)
            with self._lock:
                self.status.state = "error"
                self.status.error = str(e)
        except Exception as e:
            logging.exception("capture session failed: %s", e)
            with self._lock:
                self.status.state = "error"
                self.status.error = str(e)
        finally:
            if self._sampler is not None:
                self._sampler.stop_event.set()
            self._sampler = None
            # Clear worker before notify so is_running() is False when the
            # daemon session-change callback runs (GPIO window counting).
            with self._lock:
                self._worker = None
            self._notify()

    # Stop capture if the sampler stalls or never produces a first sample.
    def _watchdog(self, sampler: Sampler):
        deadline = time.monotonic() + self.WATCHDOG_TIMEOUT_S
        while sampler.is_alive() and not sampler.stop_event.is_set():
            time.sleep(2.0)
            now = time.monotonic()
            last = sampler.last_sample_mono
            if last == 0.0:
                if now > deadline:
                    logging.error("no first sample after %.0fs", self.WATCHDOG_TIMEOUT_S)
                    sampler.stop_event.set()
                    break
                continue
            if now - last > self.WATCHDOG_TIMEOUT_S:
                logging.error("sampler stalled %.1fs", now - last)
                sampler.stop_event.set()
                break
