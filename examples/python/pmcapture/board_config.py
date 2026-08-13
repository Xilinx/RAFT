#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Reads RAFT board JSON and builds the INA rail list for the running board.
# Used when a capture session starts (capture_session).

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass, field

log = logging.getLogger("board_config")


# Resolve RAFT install root from env, installed path, or source tree.
def resolve_raft_dir() -> str:
    env = os.environ.get("RAFT_DIR", "").strip()
    if env:
        return env.rstrip("/") + "/"
    if os.path.isdir("/usr/share/raft/xserver"):
        return "/usr/share/raft/"
    # Source tree: examples/python/pmcapture -> RAFT root
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", "..")) + "/"


RAFT_DIR = resolve_raft_dir()
BOARD_DIR = os.path.join(RAFT_DIR, "xserver/raft_services/power_management/board")

_UTILS_DIR = os.path.join(RAFT_DIR, "xserver/utils")
if _UTILS_DIR not in sys.path:
    sys.path.insert(0, _UTILS_DIR)

import board_identity  # noqa: E402


# Resolve board JSON path using RAFT board identity (sc-board-id or EEPROM).
def board_json_path() -> str:
    try:
        product_name, product_revision = board_identity.get_board_identity()
    except board_identity.BoardIdentityError as exc:
        raise SystemExit(str(exc)) from exc

    path = board_identity.resolve_board_json_path(
        BOARD_DIR, product_name, product_revision
    )
    if path is None:
        raise SystemExit(
            f"Board JSON not found for {product_name}"
            + (f"-{product_revision}" if product_revision else "")
        )
    return path


# One INA rail entry parsed from board JSON POWER SENSORS.
@dataclass
class SensorSpec:
    key: str
    name: str
    part_name: str
    i2c_bus: str
    i2c_address: str
    domain: str
    nominal_v: float
    maximum_current: int | None
    shunt_resistor: int | None
    phase_multiplier: int | None

    # I2C bus number extracted from the device path (e.g. /dev/i2c-5 -> 5).
    @property
    def bus_num(self) -> int:
        return int(self.i2c_bus.rsplit("-", 1)[-1])


# Parsed board JSON: sensors, domains, and metadata.
@dataclass
class BoardConfig:
    board_name: str
    json_path: str
    features: list[str] = field(default_factory=list)
    sensors: list[SensorSpec] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    domain_rails: dict[str, list[str]] = field(default_factory=dict)


# Return POWER SENSORS block; board JSON may use POWER SENSORS or POWER_SENSORS.
def _power_sensors_block(board_data: dict) -> dict:
    return board_data.get("POWER SENSORS") or board_data.get("POWER_SENSORS", {})


# Map a rail name to its POWER DOMAIN label.
def _domain_for_rail(rail_name: str, domain_rails: dict[str, list[str]]) -> str:
    for domain, rails in domain_rails.items():
        if rail_name in rails:
            return domain
    return "Other"


# Load and validate board JSON for the installed platform.
def load_board_config() -> BoardConfig:
    try:
        product_name, _product_revision = board_identity.get_board_identity()
    except board_identity.BoardIdentityError as exc:
        raise SystemExit(str(exc)) from exc

    path = board_json_path()
    if not os.path.isfile(path):
        raise SystemExit(f"Board JSON not found: {path}")

    with open(path, "r") as f:
        json_data = json.load(f)

    name = product_name
    if name not in json_data:
        raise SystemExit(f"Board key {name!r} not in {path}")

    board_data = json_data[name]
    features = board_data.get("FEATURE", {}).get("List", [])

    domain_rails: dict[str, list[str]] = {}
    domains: list[str] = []
    if "POWER DOMAIN" in board_data:
        for _key, val in board_data["POWER DOMAIN"].items():
            dname = val["Name"]
            rails = list(val.get("Rails", []))
            domain_rails[dname] = rails
            domains.append(dname)

    typical_v: dict[str, float] = {}
    for _k, v in board_data.get("VOLTAGE", {}).items():
        if "Typical_Volt" in v:
            typical_v[v.get("Name", _k)] = float(v["Typical_Volt"])

    sensors: list[SensorSpec] = []
    for key, v in _power_sensors_block(board_data).items():
        rail_name = v.get("Name", key)
        sensors.append(
            SensorSpec(
                key=key,
                name=rail_name,
                part_name=v["Part_Name"],
                i2c_bus=v["I2C_Bus"],
                i2c_address=v["I2C_Address"],
                domain=_domain_for_rail(rail_name, domain_rails),
                nominal_v=typical_v.get(rail_name, 0.0),
                maximum_current=v.get("Maximum_Current"),
                shunt_resistor=v.get("Shunt_Resistor"),
                phase_multiplier=v.get("Phase_Multiplier"),
            )
        )

    if not sensors:
        raise SystemExit(f"No POWER SENSORS in {path}")

    log.info("board %s: %d sensors, domains %s", name, len(sensors), domains)
    return BoardConfig(
        board_name=name,
        json_path=path,
        features=features,
        sensors=sensors,
        domains=sorted(set(domains)),
        domain_rails=domain_rails,
    )


# Add RAFT power-management modules to sys.path for INA drivers.
def setup_import_paths() -> None:
    sys.path.insert(0, os.path.join(RAFT_DIR, "xserver/raft_services/power_management"))
    sys.path.insert(0, os.path.join(RAFT_DIR, "xserver/raft_services/power_management/devices"))
