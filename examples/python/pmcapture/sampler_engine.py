#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Polls INA rails at the requested rate and produces V/I/W sample records.
# Used by capture_session; capture_output reads from the sampler thread.

from __future__ import annotations

import logging
import threading
import time
from collections import deque
from dataclasses import dataclass

from board_config import BoardConfig, SensorSpec, setup_import_paths

setup_import_paths()
from sensors import INA226, INA700, INA745x  # noqa: E402


# Initialized INA driver bound to one SensorSpec.
@dataclass
class ActiveSensor:
    spec: SensorSpec
    driver: object


# Raised when a configured rail cannot be read during capture.
class RailSampleError(RuntimeError):
    # Attach rail name and underlying cause to the error message.
    def __init__(self, rail_name: str, cause: Exception | str):
        self.rail_name = rail_name
        self.cause = cause
        msg = (
            "requested rail sampling is failing due to an error: "
            f"{rail_name}: {cause}"
        )
        super().__init__(msg)


# Initialize and read RAFT INA drivers from board JSON specs.
class SensorBank:
    # Preflight and initialize INA drivers for the given sensor list.
    def __init__(self, specs: list[SensorSpec]):
        self.active: list[ActiveSensor] = []
        self._init(specs)

    # Construct the RAFT INA driver for one SensorSpec.
    def _make_driver(self, spec: SensorSpec):
        pn = spec.part_name
        if pn == "INA226":
            return INA226(spec.i2c_address, spec.i2c_bus)
        if pn == "INA700":
            return INA700(spec.i2c_address, spec.i2c_bus)
        if pn in ("INA745A", "INA745B"):
            return INA745x(spec.i2c_address, spec.i2c_bus)
        raise ValueError(f"Unsupported Part_Name {spec.part_name!r}")

    # Initialize each sensor driver; raise if any fail preflight.
    def _init(self, specs: list[SensorSpec]):
        bad: list[str] = []
        for spec in specs:
            try:
                drv = self._make_driver(spec)
            except Exception as e:
                bad.append(f"  {spec.name}: driver create failed: {e}")
                continue

            mc = spec.maximum_current or 5000
            sr = spec.shunt_resistor or 2000
            pm = spec.phase_multiplier or 1

            try:
                if not drv.initSensor(mc, sr, pm):
                    bad.append(
                        f"  {spec.name} {spec.i2c_bus}/{spec.i2c_address}: init failed"
                    )
                    continue
            except Exception as e:
                bad.append(f"  {spec.name}: init error: {e}")
                continue

            self.active.append(ActiveSensor(spec=spec, driver=drv))
            logging.info(
                "preflight %-15s %-7s %s/%-6s OK",
                spec.name,
                spec.part_name,
                spec.i2c_bus,
                spec.i2c_address,
            )

        if bad:
            raise RuntimeError(
                "PREFLIGHT FAILED — sensor init errors:\n" + "\n".join(bad)
            )
        if not self.active:
            raise RuntimeError("No sensors initialized.")
        logging.info("preflight: %d/%d sensors ready", len(self.active), len(specs))

    # Read voltage, current, and power for one active rail.
    def read_rail(self, entry: ActiveSensor) -> dict:
        try:
            v = round(entry.driver.getBusVoltage(), 4)
            i = round(abs(entry.driver.getCurrent()), 4)
            w = round(entry.driver.getPower(), 4)
            if w <= 0 and v > 0 and i > 0:
                w = round(v * i, 4)
            return {"V": v, "I": i, "W": w}
        except Exception as e:
            logging.error("read %s: %s", entry.spec.name, e)
            raise RailSampleError(entry.spec.name, e) from e


# Background thread polling INA rails at configured rate.
class Sampler(threading.Thread):
    # Configure sampling rate and sensor bank for the background thread.
    def __init__(self, rate_hz: float, bank: SensorBank):
        super().__init__(daemon=True, name="sampler")
        self.rate_hz = rate_hz
        self.period = 1.0 / rate_hz
        self.bank = bank
        self.subscribers: list[deque] = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.last_sample_mono = 0.0
        self.actual_rate = 0.0
        self.board_name = ""
        self.sample_count = 0
        self.sample_error: str | None = None

    # Register a deque to receive sample dicts from the sampler thread.
    def add_subscriber(self) -> deque:
        q: deque = deque(maxlen=128)
        with self.lock:
            self.subscribers.append(q)
        return q

    # Unregister a subscriber deque when output sink finishes.
    def remove_subscriber(self, q: deque):
        with self.lock:
            try:
                self.subscribers.remove(q)
            except ValueError:
                pass

    # Read all active rails for one sample tick.
    def _sample_once(self) -> dict:
        ts = time.time()
        rails: dict[str, dict] = {}
        for entry in self.bank.active:
            rails[entry.spec.name] = self.bank.read_rail(entry)
        return {
            "ts": round(ts, 3),
            "rails": rails,
            "board": self.board_name,
        }

    # Poll sensors at rate_hz until stop_event is set.
    def run(self):
        next_t = time.monotonic()
        while not self.stop_event.is_set():
            try:
                sample = self._sample_once()
            except RailSampleError as e:
                logging.error("%s", e)
                self.sample_error = str(e)
                self.stop_event.set()
                break
            except Exception as e:
                logging.exception("sample error: %s", e)
                self.sample_error = (
                    "requested rail sampling is failing due to an error: "
                    f"{e}"
                )
                self.stop_event.set()
                break

            now_mono = time.monotonic()
            if self.last_sample_mono:
                inst = 1.0 / max(1e-3, now_mono - self.last_sample_mono)
                self.actual_rate = self.actual_rate * 0.9 + inst * 0.1
            self.last_sample_mono = now_mono
            sample["rate"] = round(self.actual_rate, 1)
            self.sample_count += 1

            with self.lock:
                subs = list(self.subscribers)
            for q in subs:
                try:
                    q.append(sample)
                except Exception:
                    pass

            next_t += self.period
            sleep = next_t - time.monotonic()
            if sleep > 0:
                time.sleep(sleep)
            else:
                next_t = time.monotonic()


# Build JSONL catalog object describing active rails.
def catalog_msg(cfg: BoardConfig, active: list[SensorSpec] | None = None) -> dict:
    sensors = active if active is not None else cfg.sensors
    return {
        "type": "catalog",
        "board": cfg.board_name,
        "rails": [
            {
                "name": s.name,
                "domain": s.domain,
                "nominal_v": s.nominal_v,
                "phases": s.phase_multiplier or 1,
                "bus": s.bus_num,
                "addr": s.i2c_address,
                "part": s.part_name,
            }
            for s in sensors
        ],
        "domains": cfg.domains,
    }


# Selector value: every entry in board JSON POWER SENSORS.
RAILS_ALL = "all"

# Deprecated aliases for RAILS_ALL (old docs/scripts).
_RAILS_ALL_ALIASES = frozenset({"all", "power_sensors", "power_domains"})


# Select SensorSpec list from --rails selector string.
def select_sensors(cfg: BoardConfig, rails_arg: str) -> list[SensorSpec]:
    arg = (rails_arg or RAILS_ALL).strip()
    if arg in _RAILS_ALL_ALIASES:
        return list(cfg.sensors)

    tokens = [t.strip() for t in arg.split(",") if t.strip()]
    wanted: set[str] = set()
    for token in tokens:
        if token in cfg.domain_rails:
            wanted.update(cfg.domain_rails[token])
        else:
            wanted.add(token)

    out = [s for s in cfg.sensors if s.name in wanted or s.key in wanted]
    if not out:
        domains = ", ".join(cfg.domains) if cfg.domains else "(none)"
        raise ValueError(
            f"--rails {rails_arg!r} matched zero sensors (board has {len(cfg.sensors)}). "
            f"Use default (all rails), a POWER DOMAIN name ({domains}), "
            f"or comma-separated rail names."
        )
    return out
