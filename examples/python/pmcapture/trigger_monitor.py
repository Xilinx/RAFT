#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Watches a GPIO line while armed; starts capture on assert, stops on deassert.
# Created by capture_daemon on arm.

from __future__ import annotations

import logging
import threading
import time
from datetime import timedelta
from typing import Callable

from capture_config import TriggerSpec

log = logging.getLogger("trigger_monitor")


# Read GPIO line value from libgpiod request or edge event.
def _read_line_value(request, chip_offset: int, event=None):
    values = request.get_values()
    key = event.line_offset if event is not None else chip_offset
    if isinstance(values, dict):
        return values[key]
    if isinstance(values, (list, tuple)):
        if len(values) == 1:
            return values[0]
        try:
            return values[key]
        except IndexError:
            return values[0]
    try:
        return values[key]
    except (KeyError, IndexError, TypeError):
        return values[0]


# Return True when raw line value matches active level.
def _level_is_active(value, active: str) -> bool:
    if hasattr(value, "name"):
        name = value.name.lower()
        if active == "high":
            return name in ("active", "high", "1")
        return name in ("inactive", "low", "0")
    if active == "high":
        return bool(value)
    return not bool(value)


# Watch one GPIO line and invoke callbacks on assert/deassert.
class TriggerMonitor:
    # Store trigger spec and assert/deassert callbacks.
    def __init__(
        self,
        spec: TriggerSpec,
        on_assert: Callable[[], None],
        on_deassert: Callable[[], None],
    ):
        self._spec = spec
        self._on_assert = on_assert
        self._on_deassert = on_deassert
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._request = None
        self._lock = threading.Lock()
        self._gated_active = False
        self._last_edge_at = 0.0

    # Start the background GPIO edge monitor thread.
    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="trigger-gpio",
            daemon=True,
        )
        self._thread.start()

    # Stop the monitor thread and release the GPIO line request.
    def stop(self, timeout: float = 5.0) -> None:
        self._stop.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
        self._thread = None
        self._release_request()

    # Return 1/0 for active/inactive trigger level, or None if unavailable.
    def read_level(self) -> int | None:
        with self._lock:
            req = self._request
        if req is None:
            return None
        try:
            val = _read_line_value(req, self._spec.line_offset)
            return 1 if _level_is_active(val, self._spec.active) else 0
        except Exception:
            return None

    # Release libgpiod line request held by the monitor thread.
    def _release_request(self) -> None:
        with self._lock:
            req = self._request
            self._request = None
        if req is not None:
            try:
                req.release()
            except Exception as exc:
                log.debug("release trigger line: %s", exc)

    # Poll GPIO edges and invoke assert/deassert callbacks.
    def _run(self) -> None:
        import gpiod
        from gpiod.line import Direction, Edge

        spec = self._spec
        chip = spec.chip
        offset = spec.line_offset

        settings = gpiod.LineSettings(
            direction=Direction.INPUT,
            edge_detection=Edge.BOTH,
        )
        debounce_ms = spec.debounce_ms
        if debounce_ms > 0 and hasattr(settings, "debounce_period"):
            settings.debounce_period = timedelta(milliseconds=debounce_ms)

        try:
            request = gpiod.request_lines(
                chip,
                consumer="pmcapture-trigger",
                config={offset: settings},
            )
        except OSError as exc:
            log.error("failed to request GPIO %s (%s line %s): %s", spec.gpio, chip, offset, exc)
            raise

        with self._lock:
            self._request = request

        log.info(
            "trigger monitor: %s on %s line %s active=%s",
            spec.gpio,
            chip,
            offset,
            spec.active,
        )

        try:
            val = _read_line_value(request, offset)
            self._gated_active = _level_is_active(val, spec.active)
        except Exception:
            self._gated_active = False

        try:
            while not self._stop.is_set():
                if not request.wait_edge_events(timeout=timedelta(seconds=0.5)):
                    continue
                for event in request.read_edge_events():
                    now = time.monotonic()
                    if debounce_ms > 0 and (now - self._last_edge_at) * 1000.0 < debounce_ms:
                        continue
                    self._last_edge_at = now

                    try:
                        val = _read_line_value(request, offset, event)
                    except Exception:
                        continue

                    active_now = _level_is_active(val, spec.active)
                    if active_now and not self._gated_active:
                        self._gated_active = True
                        try:
                            self._on_assert()
                        except Exception:
                            log.exception("on_assert callback failed")
                    elif not active_now and self._gated_active:
                        self._gated_active = False
                        try:
                            self._on_deassert()
                        except Exception:
                            log.exception("on_deassert callback failed")
        finally:
            self._release_request()
