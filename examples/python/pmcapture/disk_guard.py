#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Refuses or stops file capture when the output disk is nearly full.
# Used by capture_session and capture_output.

from __future__ import annotations

import os
import shutil

# Stop or refuse capture when less than this fraction of the filesystem is free.
MIN_FREE_DISK_RATIO = 0.01

# How often to re-check free space during an active file capture.
DISK_CHECK_INTERVAL_S = 5.0


# Raised when the output filesystem has too little free space.
class InsufficientDiskSpaceError(RuntimeError):
    pass


# Return the directory whose free space governs writes to *path*.
def storage_directory_for_path(path: str) -> str:
    abspath = os.path.abspath(os.path.expanduser(path))
    if os.path.isdir(abspath):
        return abspath
    parent = os.path.dirname(abspath)
    return parent or "/"


# Return the fraction of total space that is free (0.0–1.0).
def free_disk_ratio(directory: str) -> float:
    usage = shutil.disk_usage(directory)
    if usage.total <= 0:
        return 0.0
    return usage.free / usage.total


# Format user-visible insufficient disk space message.
def format_insufficient_disk_message(directory: str, free_ratio: float) -> str:
    min_pct = MIN_FREE_DISK_RATIO * 100.0
    free_pct = free_ratio * 100.0
    return (
        "insufficient disk space to store sampling data: "
        f"{free_pct:.2f}% free on {directory} "
        f"(need at least {min_pct:.0f}% free)"
    )


# Raise if the filesystem for *path* has less than 1% free space.
def require_disk_space_for_output(path: str) -> None:
    directory = storage_directory_for_path(path)
    ratio = free_disk_ratio(directory)
    if ratio < MIN_FREE_DISK_RATIO:
        raise InsufficientDiskSpaceError(
            format_insufficient_disk_message(directory, ratio)
        )


# Return True when free space on the output filesystem is below 1%.
def disk_space_exhausted(path: str) -> bool:
    directory = storage_directory_for_path(path)
    return free_disk_ratio(directory) < MIN_FREE_DISK_RATIO
