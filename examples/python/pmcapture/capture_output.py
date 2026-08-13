#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Writes samples to a CSV/JSONL file or a TCP JSONL stream.
# Called from capture_session while a capture is running.

from __future__ import annotations

import csv
import json
import logging
import os
import socket
import threading
import time
from datetime import datetime

from sampler_engine import Sampler
from disk_guard import (
    DISK_CHECK_INTERVAL_S,
    InsufficientDiskSpaceError,
    disk_space_exhausted,
    format_insufficient_disk_message,
    free_disk_ratio,
    require_disk_space_for_output,
    storage_directory_for_path,
)

DEFAULT_LOG_DIR = "/data/pmcapture"


# Build auto-generated capture filename under log_dir.
def default_output_file(
    fmt: str,
    log_dir: str = DEFAULT_LOG_DIR,
    *,
    board_name: str | None = None,
    suffix: str | None = None,
) -> str:
    os.makedirs(log_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ext = "csv" if fmt == "csv" else "jsonl"
    parts = ["capture"]
    if board_name:
        parts.append(board_name)
    parts.append(stamp)
    if suffix:
        parts.append(suffix)
    return os.path.join(log_dir, f"{'_'.join(parts)}.{ext}")


# Resolve CLI output path or auto-generate under log_dir.
def resolve_output_path(
    output_file: str | None,
    file_format: str,
    log_dir: str = DEFAULT_LOG_DIR,
    *,
    board_name: str | None = None,
    suffix: str | None = None,
) -> str:
    if not output_file:
        return default_output_file(
            file_format, log_dir, board_name=board_name, suffix=suffix
        )
    path = os.path.abspath(os.path.expanduser(output_file))
    if path.endswith(os.sep) or os.path.isdir(path):
        return default_output_file(
            file_format, path.rstrip(os.sep), board_name=board_name, suffix=suffix
        )
    return path

# Append one sample row to a CSV DictWriter.
def write_csv_sample(writer, rail_names: list[str], sample: dict):
    row = {
        "ts": sample.get("ts", ""),
        "rate_hz": sample.get("rate", ""),
    }
    rails = sample.get("rails") or {}
    for name in rail_names:
        vals = rails.get(name) or {}
        row[f"{name}_V"] = vals.get("V", "")
        row[f"{name}_I"] = vals.get("I", "")
        row[f"{name}_W"] = vals.get("W", "")
    writer.writerow(row)


# Write samples to a local file until duration elapses or stop is signaled.
def run_file_capture(
    sampler: Sampler,
    catalog: dict,
    rail_names: list[str],
    path: str,
    file_format: str,
    duration: float,
    on_complete=None,
) -> int:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    require_disk_space_for_output(path)
    deadline = time.monotonic() + duration if duration > 0 else None
    q = sampler.add_subscriber()
    count = 0
    storage_dir = storage_directory_for_path(path)
    last_disk_check = time.monotonic()

    logging.info("capturing to %s (%s)", path, file_format)
    if duration > 0:
        logging.info("capture duration: %.1f s", duration)

    try:
        with open(path, "w", newline="") as fh:
            if file_format == "csv":
                fieldnames = ["ts", "rate_hz"]
                for name in rail_names:
                    fieldnames.extend([f"{name}_V", f"{name}_I", f"{name}_W"])
                writer = csv.DictWriter(fh, fieldnames=fieldnames)
                writer.writeheader()
                fh.flush()
            else:
                fh.write(json.dumps(catalog) + "\n")
                fh.flush()

            while not sampler.stop_event.is_set():
                if deadline is not None and time.monotonic() >= deadline:
                    logging.info("capture duration complete")
                    break
                now = time.monotonic()
                if now - last_disk_check >= DISK_CHECK_INTERVAL_S:
                    last_disk_check = now
                    if disk_space_exhausted(path):
                        ratio = free_disk_ratio(storage_dir)
                        msg = format_insufficient_disk_message(storage_dir, ratio)
                        logging.error("stopping capture: %s", msg)
                        sampler.stop_event.set()
                        raise InsufficientDiskSpaceError(msg)
                wrote = False
                while q:
                    sample = q.popleft()
                    if file_format == "csv":
                        write_csv_sample(writer, rail_names, sample)
                    else:
                        fh.write(json.dumps(sample) + "\n")
                    count += 1
                    wrote = True
                if wrote:
                    fh.flush()
                time.sleep(0.001)
    finally:
        sampler.remove_subscriber(q)
        logging.info("wrote %d samples to %s", count, path)
        if on_complete is not None:
            on_complete(count)
    return count

# Stream catalog and samples to one TCP client connection.
def _serve_client(sock: socket.socket, addr, sampler: Sampler, catalog: dict):
    logging.info("client connected: %s", addr)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        for opt, val in (("TCP_KEEPIDLE", 15), ("TCP_KEEPINTVL", 5), ("TCP_KEEPCNT", 3)):
            const = getattr(socket, opt, None)
            if const is not None:
                sock.setsockopt(socket.IPPROTO_TCP, const, val)
    except OSError:
        pass
    sock.settimeout(2.0)
    q = sampler.add_subscriber()
    try:
        sock.sendall((json.dumps(catalog) + "\n").encode())
        while not sampler.stop_event.is_set():
            sent_any = False
            while q:
                msg = q.popleft()
                try:
                    sock.sendall((json.dumps(msg) + "\n").encode())
                    sent_any = True
                except (BrokenPipeError, ConnectionResetError):
                    return
                except socket.timeout:
                    break
            if not sent_any:
                try:
                    sock.settimeout(0.05)
                    chunk = sock.recv(64)
                    if not chunk:
                        return
                except socket.timeout:
                    pass
                except OSError:
                    return
                time.sleep(0.02)
    finally:
        sampler.remove_subscriber(q)
        try:
            sock.close()
        except OSError:
            pass
        logging.info("client disconnected: %s", addr)

# Stop TCP capture after configured duration elapses.
def _duration_watchdog(sampler: Sampler, srv: socket.socket | None, duration: float):
    if duration <= 0:
        return
    time.sleep(duration)
    if sampler.stop_event.is_set():
        return
    logging.info("capture duration %.1f s elapsed — stopping", duration)
    sampler.stop_event.set()
    if srv is not None:
        try:
            srv.close()
        except OSError:
            pass

# Accept TCP clients and stream JSONL samples until stop.
def run_tcp_server(
    sampler: Sampler,
    catalog: dict,
    host: str,
    port: int,
    duration: float,
) -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(8)
    logging.info("listening on %s:%d (tcp)", host, port)
    if duration > 0:
        logging.info("capture duration: %.1f s", duration)
        threading.Thread(
            target=_duration_watchdog,
            args=(sampler, srv, duration),
            daemon=True,
            name="duration",
        ).start()

    try:
        while not sampler.stop_event.is_set():
            srv.settimeout(0.5)
            try:
                sock, addr = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=_serve_client,
                args=(sock, addr, sampler, catalog),
                daemon=True,
            ).start()
    finally:
        try:
            srv.close()
        except OSError:
            pass
