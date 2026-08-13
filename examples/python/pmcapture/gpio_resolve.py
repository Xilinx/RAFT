#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Maps a GPIO trigger name to chip and line (via gpioinfo / libgpiod).
# Used when arming a GPIO trigger (capture_config).

from __future__ import annotations

import glob
import subprocess


# Normalize gpiochip reference to /dev/gpiochipN path.
def _chip_path(chip_ref: str) -> str:
    if chip_ref.startswith("/dev/"):
        return chip_ref
    return f"/dev/{chip_ref}"

# List available /dev/gpiochip* device paths.
def _iter_chip_paths() -> list[str]:
    return sorted(glob.glob("/dev/gpiochip*"))

# Resolve GPIO name via libgpiod line_offset_from_id.
def _resolve_via_gpiod(name: str) -> tuple[str, int] | None:
    try:
        import gpiod
    except ImportError:
        return None

    if not hasattr(gpiod.Chip, "line_offset_from_id"):
        return None

    for path in _iter_chip_paths():
        chip = None
        try:
            chip = gpiod.Chip(path)
            offset = chip.line_offset_from_id(name)
            return path, int(offset)
        except (OSError, ValueError, LookupError):
            continue
        except Exception as exc:
            if getattr(exc, "errno", None) in (2, 22):
                continue
            raise
        finally:
            if chip is not None and hasattr(chip, "close"):
                chip.close()
    return None

# Resolve GPIO name via gpioinfo name filter.
def _resolve_via_gpioinfo_filter(name: str) -> tuple[str, int] | None:
    try:
        proc = subprocess.run(
            ["gpioinfo", name],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if proc.returncode != 0:
        return None
    parts = proc.stdout.strip().split()
    if len(parts) >= 2 and parts[1].isdigit():
        return _chip_path(parts[0]), int(parts[1])
    return None

# Parse one gpioinfo line into offset and optional name.
def _parse_gpioinfo_line(line: str) -> tuple[int, str | None] | None:
    stripped = line.strip()
    if not stripped.startswith("line"):
        return None
    try:
        _line_kw, num_part, rest = stripped.split(":", 2)
        offset = int(num_part.strip())
    except ValueError:
        return None
    rest = rest.strip()
    if rest.startswith('"'):
        end = rest.find('"', 1)
        if end > 0:
            return offset, rest[1:end]
        return offset, None
    first = rest.split(None, 1)[0]
    if first == "unnamed":
        return offset, None
    return offset, first

# Resolve GPIO name by scanning full gpioinfo output.
def _resolve_via_gpioinfo_scan(name: str) -> tuple[str, int] | None:
    try:
        proc = subprocess.run(
            ["gpioinfo"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if proc.returncode != 0:
        return None

    current_chip: str | None = None
    for raw in proc.stdout.splitlines():
        if raw.strip().startswith("gpiochip"):
            current_chip = raw.split()[0]
            continue
        if current_chip is None:
            continue
        parsed = _parse_gpioinfo_line(raw)
        if parsed is None:
            continue
        offset, line_name = parsed
        if line_name == name:
            return _chip_path(current_chip), offset
    return None

# Resolve a logical GPIO name to (chip device path, line offset).
def resolve_gpio_name(name: str) -> tuple[str, int]:
    for resolver in (
        _resolve_via_gpioinfo_filter,
        _resolve_via_gpioinfo_scan,
        _resolve_via_gpiod,
    ):
        hit = resolver(name)
        if hit is not None:
            return hit

    raise ValueError(
        f"GPIO {name!r} not found (checked gpioinfo and libgpiod on /dev/gpiochip*)"
    )
