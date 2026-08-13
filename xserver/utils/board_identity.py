#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Board identity via /bin/sc-board-id or FRU EEPROM (shared by raft-startup and pmcapture).

from __future__ import annotations

import logging
import os
import subprocess
from dataclasses import dataclass

from periphery import I2C

log = logging.getLogger("board_identity")

SC_BOARD_ID = "/bin/sc-board-id"

EEPROM_END_OF_FIELDS = 0xC1
EEPROM_BOARD_AREA = 0x08
EEPROM_BOARD_FIELDS_START = 0x0E
EEPROM_BOARD_NAME_INDEX = 1
EEPROM_BOARD_REVISION_INDEX = 5


class BoardIdentityError(RuntimeError):
    pass


@dataclass
class BoardEEPROM:
    Name: str = ""
    I2C_Bus: str = ""
    I2C_Addr: int = 0


_identity_cache: tuple[str, str] | None = None


# Find I2C device path and address in sysfs by driver name.
def find_i2c_device_by_name(target_name: str) -> tuple[str | None, int | None]:
    sys_i2c_path = "/sys/bus/i2c/devices/"
    if not os.path.isdir(sys_i2c_path):
        return None, None
    for device in os.listdir(sys_i2c_path):
        name_path = os.path.join(sys_i2c_path, device, "name")
        if not os.path.isfile(name_path):
            continue
        try:
            with open(name_path, "r") as f:
                device_name = f.read().strip()
            if device_name == target_name:
                bus_part, address = device.split("-", 1)
                bus_num = bus_part.replace("i2c", "")
                dev_path = f"/dev/i2c-{bus_num}"
                log.debug("Found %s at %s, address 0x%s", target_name, dev_path, address)
                return dev_path, int(address, 16)
        except OSError:
            continue
    return None, None


# Read string field `index` by walking FRU type/length fields from `start`.
def eeprom_read_field(eeprom_data, start: int, index: int, area_end: int) -> str:
    offset = start
    field_num = 0
    while offset < area_end and offset < len(eeprom_data):
        type_length = eeprom_data[offset]
        if type_length == EEPROM_END_OF_FIELDS:
            return ""

        if type_length in (0x00, 0xFF):
            offset += 1
            continue

        field_type = type_length & 0xC0
        length = type_length & 0x3F
        if field_type == 0x80:
            log.error("EEPROM field parsing: length in ASCII is not supported")
            return ""

        if field_num == index:
            if field_type != 0xC0:
                return ""
            raw = bytes(eeprom_data[offset + 1 : offset + 1 + length])
            return raw.decode("ascii", errors="ignore").replace("\x00", "").strip()

        offset += 1 + length
        field_num += 1
    return ""


# Read FRU EEPROM contents; optionally record the bus/address in *eeprom*.
def get_eeprom_data(eeprom: BoardEEPROM | None = None) -> bytes:
    eeprom_data = bytearray(256)
    candidates = [
        ("Common", "/dev/i2c-1", 0x54),
        ("Legacy", "/dev/i2c-11", 0x54),
    ]

    for name, bus, addr in candidates:
        i2c = None
        try:
            i2c = I2C(bus)
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(eeprom_data, read=True)]
            i2c.transfer(addr, msgs)
            if eeprom is not None:
                eeprom.Name, eeprom.I2C_Bus, eeprom.I2C_Addr = name, bus, addr
            log.debug("EEPROM read succeeded on %s (%s)", name, bus)
            return bytes(msgs[1].data)
        except Exception:
            log.debug("EEPROM read failed on %s (%s)", name, bus)
        finally:
            if i2c is not None:
                i2c.close()

    device_path, device_address = find_i2c_device_by_name("24c128")
    if device_path:
        i2c = None
        try:
            i2c = I2C(device_path)
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(eeprom_data, read=True)]
            i2c.transfer(device_address, msgs)
            if eeprom is not None:
                eeprom.Name, eeprom.I2C_Bus, eeprom.I2C_Addr = (
                    "Custom",
                    device_path,
                    device_address,
                )
            log.debug("EEPROM read succeeded on custom device (%s)", device_path)
            return bytes(msgs[1].data)
        except Exception:
            log.debug("Custom EEPROM read failed")
        finally:
            if i2c is not None:
                i2c.close()

    raise BoardIdentityError("Board EEPROM identification failed.")


# Run /bin/sc-board-id with a single option; return stripped stdout or None.
def run_sc_board_id(
    option: str,
    sc_board_id: str = SC_BOARD_ID,
) -> str | None:
    try:
        result = subprocess.run(
            [sc_board_id, option],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as err:
        log.warning("%s %s failed: %s", sc_board_id, option, err)
        return None

    value = result.stdout.strip()
    return value or None


# Resolve product name and revision from sc-board-id or FRU EEPROM.
def get_board_identity(
    eeprom: BoardEEPROM | None = None,
    *,
    sc_board_id: str = SC_BOARD_ID,
    use_cache: bool = True,
) -> tuple[str, str]:
    global _identity_cache
    if use_cache and _identity_cache is not None:
        return _identity_cache

    if os.path.isfile(sc_board_id):
        product_name = run_sc_board_id("--name", sc_board_id=sc_board_id)
        product_revision = run_sc_board_id("--func-rev", sc_board_id=sc_board_id)
        if product_name and product_revision:
            product_name = product_name.upper()
            product_revision = product_revision.upper()
            log.info("Board identity from %s", sc_board_id)
            log.info("Product name: %s", product_name)
            log.info("Product revision: %s", product_revision)
            identity = (product_name, product_revision)
            if use_cache:
                _identity_cache = identity
            return identity

        log.info("%s failed; using EEPROM", sc_board_id)
    else:
        log.info("%s not available; using EEPROM", sc_board_id)

    eeprom_data = get_eeprom_data(eeprom)
    board_area_end = EEPROM_BOARD_AREA + eeprom_data[EEPROM_BOARD_AREA + 1] * 8
    product_name = eeprom_read_field(
        eeprom_data,
        EEPROM_BOARD_FIELDS_START,
        EEPROM_BOARD_NAME_INDEX,
        board_area_end,
    )
    product_revision = eeprom_read_field(
        eeprom_data,
        EEPROM_BOARD_FIELDS_START,
        EEPROM_BOARD_REVISION_INDEX,
        board_area_end,
    )

    if not product_name:
        raise BoardIdentityError("Board EEPROM product name is missing or invalid.")
    if not product_revision:
        log.warning(
            "Board EEPROM product revision is missing or invalid; "
            "falling back to base board JSON."
        )

    log.info("Board identity from EEPROM")
    log.info("Product name: %s", product_name)
    log.info("Product revision: %s", product_revision or "(none)")
    identity = (product_name, product_revision)
    if use_cache:
        _identity_cache = identity
    return identity


# Pick revision-specific or base board JSON under *board_dir*.
def resolve_board_json_path(
    board_dir: str,
    product_name: str,
    product_revision: str = "",
) -> str | None:
    if product_revision:
        rev_file = os.path.join(board_dir, f"{product_name}-{product_revision}.json")
        if os.path.isfile(rev_file):
            log.info("Board file (revision): %s", rev_file)
            return rev_file
        log.info("Board file (revision) not found: %s", rev_file)

    base_file = os.path.join(board_dir, f"{product_name}.json")
    if os.path.isfile(base_file):
        log.info("Board file: %s", base_file)
        return base_file

    log.info("Board file not found: %s", base_file)
    return None
