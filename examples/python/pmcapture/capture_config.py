#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Reads capture JSON profiles and merges them with CLI or daemon options.
# Used on start and arm by the CLI and capture_daemon.

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from board_config import BoardConfig, SensorSpec


# Resolved GPIO trigger line and active level for arm/disarm.
@dataclass
class TriggerSpec:
    gpio: str
    active: str = "high"
    debounce_ms: float = 0.0
    chip: str | None = None
    line_offset: int | None = None


# User capture profile; optional fields override daemon/CLI defaults.
@dataclass
class CaptureConfig:
    source_path: str
    rails: list[str] | None = None
    rails_selector: str | None = None
    rate_hz: float | None = None
    duration_s: float | None = None
    output: str | None = None
    output_file: str | None = None
    file_format: str | None = None
    trigger: TriggerSpec | None = None


# Parse trigger object from capture-config JSON.
def _parse_trigger_block(raw, path: str) -> TriggerSpec:
    if not isinstance(raw, dict):
        raise ValueError(f'"trigger" must be an object: {path}')
    gpio = raw.get("gpio")
    if not isinstance(gpio, str) or not gpio.strip():
        raise ValueError(f'"trigger.gpio" must be a non-empty string: {path}')
    active = str(raw.get("active", "high")).strip().lower()
    if active not in ("high", "low"):
        raise ValueError(f'"trigger.active" must be "high" or "low": {path}')
    debounce_ms = float(raw.get("debounce_ms", 0))
    chip = raw.get("chip")
    line = raw.get("line") if "line" in raw else raw.get("offset")
    return TriggerSpec(
        gpio=gpio.strip(),
        active=active,
        debounce_ms=debounce_ms,
        chip=str(chip) if chip is not None else None,
        line_offset=int(line) if line is not None else None,
    )


# Fill chip/line_offset via libgpiod utilities or explicit chip/line in config.
def resolve_trigger_spec(spec: TriggerSpec) -> TriggerSpec:
    from gpio_resolve import resolve_gpio_name

    if spec.chip and spec.line_offset is not None:
        chip = spec.chip if spec.chip.startswith("/dev/") else f"/dev/{spec.chip}"
        return TriggerSpec(
            gpio=spec.gpio,
            active=spec.active,
            debounce_ms=spec.debounce_ms,
            chip=chip,
            line_offset=int(spec.line_offset),
        )

    chip, offset = resolve_gpio_name(spec.gpio)
    return TriggerSpec(
        gpio=spec.gpio,
        active=spec.active,
        debounce_ms=spec.debounce_ms,
        chip=chip,
        line_offset=offset,
    )


# Load and validate user capture-config JSON file.
def load_capture_config(path: str) -> CaptureConfig:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Capture config not found: {path}")
    with open(path, "r") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Capture config must be a JSON object: {path}")

    rails: list[str] | None = None
    rails_selector: str | None = None
    deprecated_pool = data.get("rails_pool", data.get("rails_selection"))
    if deprecated_pool is not None:
        if not isinstance(deprecated_pool, str) or not deprecated_pool.strip():
            raise ValueError(
                f'"rails_pool" must be a non-empty string (deprecated; use '
                f'"rails": "<selector>" instead): {path}'
            )
        rails_selector = deprecated_pool.strip()

    raw = data.get("rails")
    if raw is not None:
        if isinstance(raw, str) and raw.strip():
            if rails_selector is not None:
                raise ValueError(
                    f'"rails" selector and deprecated "rails_pool" are mutually '
                    f"exclusive: {path}"
                )
            rails_selector = raw.strip()
        elif isinstance(raw, list) and raw:
            rails = []
            for i, item in enumerate(raw):
                if not isinstance(item, str) or not item.strip():
                    raise ValueError(
                        f'"rails[{i}]" must be a non-empty string: {path}'
                    )
                rails.append(item.strip())
        else:
            raise ValueError(
                f'"rails" must be a selector string (e.g. "all") or a non-empty '
                f'array of rail names: {path}'
            )

    rate_hz = data.get("rate_hz", data.get("rate"))
    duration_s = data.get("duration_s", data.get("duration"))
    output = data.get("output")
    output_file = data.get("output_file")
    file_format = data.get("file_format")

    if rate_hz is not None:
        rate_hz = float(rate_hz)
    if duration_s is not None:
        duration_s = float(duration_s)
    if output is not None and output not in ("tcp", "file"):
        raise ValueError(f'output must be "tcp" or "file": {path}')
    if file_format is not None and file_format not in ("jsonl", "csv"):
        raise ValueError(f'file_format must be "jsonl" or "csv": {path}')

    trigger = None
    if "trigger" in data:
        trigger = _parse_trigger_block(data["trigger"], path)

    return CaptureConfig(
        source_path=path,
        rails=rails,
        rails_selector=rails_selector,
        rate_hz=rate_hz,
        duration_s=duration_s,
        output=output,
        output_file=output_file,
        file_format=file_format,
        trigger=trigger,
    )


# Trim active sensor pool to rails listed in capture config.
def apply_capture_config(
    board: BoardConfig,
    pool_specs: list[SensorSpec],
    capture: CaptureConfig,
) -> list[SensorSpec]:
    if not capture.rails:
        return pool_specs

    board_by_name = {s.name: s for s in board.sensors}
    board_by_key = {s.key: s for s in board.sensors}
    pool_by_name = {s.name: s for s in pool_specs}
    pool_by_key = {s.key: s for s in pool_specs}

    invalid: list[str] = []
    not_in_pool: list[str] = []
    out: list[SensorSpec] = []

    for rail in capture.rails:
        if rail not in board_by_name and rail not in board_by_key:
            invalid.append(rail)
            continue
        spec = pool_by_name.get(rail) or pool_by_key.get(rail)
        if spec is None:
            not_in_pool.append(rail)
            continue
        if spec not in out:
            out.append(spec)

    if invalid:
        board_rails = ", ".join(sorted(board_by_name))
        raise ValueError(
            f"Capture config rails not defined in board JSON ({board.json_path}):\n"
            f"  invalid: {', '.join(invalid)}\n"
            f"  board rails: {board_rails}"
        )
    if not_in_pool:
        pool_rails = ", ".join(sorted(pool_by_name))
        raise ValueError(
            f"Capture config rails not in --rails pool ({capture.source_path}):\n"
            f"  excluded by pool: {', '.join(not_in_pool)}\n"
            f"  pool rails: {pool_rails}"
        )
    if not out:
        raise ValueError(f"Capture config matched zero sensors: {capture.source_path}")
    return out


# Apply capture-config defaults; explicit base values win.
def merge_start_options(base: dict, capture: CaptureConfig | None) -> dict:
    if capture is None:
        return dict(base)
    merged = dict(base)
    field_map = (
        ("rails_selector", "rails"),
        ("rate_hz", "rate"),
        ("duration_s", "duration"),
        ("output", "output"),
        ("output_file", "output_file"),
        ("file_format", "file_format"),
    )
    for cfg_attr, opt_key in field_map:
        val = getattr(capture, cfg_attr, None)
        if val is not None and merged.get(opt_key) in (None, "", 0):
            merged[opt_key] = val
    if capture.rails and not merged.get("capture_config"):
        merged["capture_config"] = capture.source_path
    return merged


# Build TriggerSpec from arm request and optional capture JSON.
def merge_arm_trigger(req: dict, capture: CaptureConfig | None) -> TriggerSpec:
    cfg_trigger = capture.trigger if capture is not None else None

    gpio = req.get("gpio")
    if gpio is not None:
        gpio = str(gpio).strip()
    elif cfg_trigger is not None:
        gpio = cfg_trigger.gpio

    active_raw = req.get("trigger_active")
    if active_raw is not None:
        active = str(active_raw).strip().lower()
    elif cfg_trigger is not None:
        active = cfg_trigger.active
    else:
        active = "high"

    debounce_raw = req.get("debounce_ms")
    if debounce_raw is not None:
        debounce_ms = float(debounce_raw)
    elif cfg_trigger is not None:
        debounce_ms = cfg_trigger.debounce_ms
    else:
        debounce_ms = 0.0

    if not gpio:
        raise ValueError("arm requires --gpio or capture config with trigger block")
    if active not in ("high", "low"):
        raise ValueError('trigger active must be "high" or "low"')

    chip = cfg_trigger.chip if cfg_trigger is not None else None
    line_offset = cfg_trigger.line_offset if cfg_trigger is not None else None
    if req.get("gpio") is not None:
        chip = None
        line_offset = None

    return TriggerSpec(
        gpio=gpio,
        active=active,
        debounce_ms=debounce_ms,
        chip=chip,
        line_offset=line_offset,
    )
