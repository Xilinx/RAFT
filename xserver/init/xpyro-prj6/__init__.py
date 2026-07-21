#!/usr/bin/env python3
# Copyright (C) 2023-2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2026, Advanced Micro Devices, Inc."

import os
import sys
import json
import logging
import subprocess
import Pyro4
from periphery import I2C

SC_BOARD_ID = '/bin/sc-board-id'

# Ensure immediate flush for stdout
sys.stdout.reconfigure(line_buffering=True)

# Add required paths
sys.path.extend([
    '../../utils',
    '../../raft_services',
    '../../raft_services/power_management'
])

from pm import PM
from utils import get_ip_and_port

RAFT_DIR = '/usr/share/raft/'
BOARD_PATH = os.path.join(RAFT_DIR, 'xserver/raft_services/power_management/board')

# -------------------------
# Robust Logging Setup
# -------------------------
def setup_logging():
    # Remove existing handlers (e.g., Pyro4 may add its own)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create our own unbuffered stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    stdout_handler.flush = sys.stdout.flush

    logging.basicConfig(
        level=logging.INFO,
        handlers=[stdout_handler],
        force=True  # Python 3.8+: ensures config applies even if prior handlers exist
    )

setup_logging()

# -------------------------
# Utility functions
# -------------------------
def exit_program(msg="Critical Error: Unable to Run Raft-PM Server."):
    logging.error(msg)
    sys.exit(1)

def is_valid_json_file(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"Board JSON not found: {file_path}")
        return False
    try:
        with open(file_path, 'r') as file:
            json.load(file)
            return True
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON content: {file_path}")
        return False

# -------------------------
# EEPROM and Board Handling
# -------------------------
class BoardEEPROM:
    def __init__(self):
        self.Name = ""
        self.I2C_Bus = ""
        self.I2C_Addr = 0x00

onboard = BoardEEPROM()

def find_i2c_device_by_name(target_name):
    sys_i2c_path = "/sys/bus/i2c/devices/"
    for device in os.listdir(sys_i2c_path):
        name_path = os.path.join(sys_i2c_path, device, "name")
        if not os.path.isfile(name_path):
            continue
        try:
            with open(name_path, "r") as f:
                device_name = f.read().strip()
            if device_name == target_name:
                bus_number, address = device.split("-")
                bus_number = bus_number.replace("i2c", "")
                dev_path = f"/dev/i2c-{bus_number}"
                logging.debug(f"Found {target_name} at {dev_path}, address 0x{address}")
                return dev_path, int(address, 16)
        except IOError:
            continue
    return None, None

def get_eeprom_data():
    eeprom_data = bytearray(256)
    candidates = [
        ("Common", "/dev/i2c-1", 0x54),
        ("Legacy", "/dev/i2c-11", 0x54),
    ]

    for name, bus, addr in candidates:
        try:
            i2c = I2C(bus)
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(eeprom_data, read=True)]
            i2c.transfer(addr, msgs)
            i2c.close()
            onboard.Name, onboard.I2C_Bus, onboard.I2C_Addr = name, bus, addr
            logging.debug(f"EEPROM read succeeded on {name} ({bus})")
            return msgs[1].data
        except Exception:
            logging.debug(f"EEPROM read failed on {name} ({bus})")

    # Dynamic detection
    device_path, device_address = find_i2c_device_by_name("24c128")
    if device_path:
        try:
            i2c = I2C(device_path)
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(eeprom_data, read=True)]
            i2c.transfer(device_address, msgs)
            i2c.close()
            onboard.Name, onboard.I2C_Bus, onboard.I2C_Addr = "Custom", device_path, device_address
            logging.debug(f"EEPROM read succeeded on Custom device ({device_path})")
            return msgs[1].data
        except Exception:
            logging.debug("Custom EEPROM read failed.")

    exit_program("Board EEPROM Identification Failed.")
    return None

# Field index within board area in EEPROM that are represented as strings
# (from EEPROM_BOARD_FIELDS_START):
# 0: Manufacturer, 1: Product Name, 2: Serial Number, 3: Part Number,
# 4: FRU ID, 5: Revision
EEPROM_END_OF_FIELDS = 0xC1
EEPROM_BOARD_AREA = 0x08
EEPROM_BOARD_FIELDS_START = 0x0E
EEPROM_BOARD_NAME_INDEX = 1
EEPROM_BOARD_REVISION_INDEX = 5

# Read string field `index` by walking type/length fields from `start`.
def eeprom_read_field(eeprom_data, start, index, area_end):
    offset = start
    field_num = 0
    while offset < area_end and offset < len(eeprom_data):
        type_length = eeprom_data[offset]
        if type_length == EEPROM_END_OF_FIELDS:
            return ""

        # Unused/padding bytes; skip without advancing the field index.
        if type_length in (0x00, 0xFF):
            offset += 1
            continue

        field_type = type_length & 0xC0
        length = type_length & 0x3F
        if field_type == 0x80:
            logging.error("EEPROM field parsing: length in ASCII is not supported")
            return ""

        if field_num == index:
            # Board area strings are text strings (type 0xC0); length is in bytes.
            if field_type != 0xC0:
                return ""
            raw = bytes(eeprom_data[offset + 1:offset + 1 + length])
            return raw.decode("ascii", errors="ignore").replace("\x00", "").strip()

        # Advance past this field (1 type/length byte + Length data bytes) to the next field.
        offset += 1 + length
        field_num += 1
    return ""

# Run /bin/sc-board-id with a single option; return stripped stdout or None.
def run_sc_board_id(option):
    try:
        result = subprocess.run(
            [SC_BOARD_ID, option], capture_output=True, text=True, check=True, timeout=5
        )
    except (OSError, subprocess.SubprocessError) as err:
        logging.warning(f"{SC_BOARD_ID} {option} failed: {err}")
        return None

    value = result.stdout.strip()
    return value or None

def get_board_identity():
    if os.path.isfile(SC_BOARD_ID):
        product_name = run_sc_board_id('--name')
        product_revision = run_sc_board_id('--func-rev')
        if product_name and product_revision:
            product_name = product_name.upper()
            product_revision = product_revision.upper()
            logging.info(f"Board identity from {SC_BOARD_ID}")
            logging.info(f"Product name: {product_name}")
            logging.info(f"Product revision: {product_revision}")
            return product_name, product_revision

        logging.info(f"{SC_BOARD_ID} failed; using EEPROM")
    else:
        logging.info(f"{SC_BOARD_ID} not available; using EEPROM")

    eeprom_data = get_eeprom_data()
    board_area_end = EEPROM_BOARD_AREA + eeprom_data[EEPROM_BOARD_AREA + 1] * 8
    product_name = eeprom_read_field(
        eeprom_data, EEPROM_BOARD_FIELDS_START, EEPROM_BOARD_NAME_INDEX, board_area_end
    )
    product_revision = eeprom_read_field(
        eeprom_data, EEPROM_BOARD_FIELDS_START, EEPROM_BOARD_REVISION_INDEX, board_area_end
    )

    if not product_name:
        exit_program("Board EEPROM product name is missing or invalid.")
    if not product_revision:
        logging.warning(
            "Board EEPROM product revision is missing or invalid; "
            "falling back to base board JSON."
        )

    logging.info("Board identity from EEPROM")
    logging.info(f"Product name: {product_name}")
    logging.info(f"Product revision: {product_revision or '(none)'}")
    return product_name, product_revision

# -------------------------
# Pyro4 Daemon
# -------------------------
def start_pyro_daemon():
    IPADDR, PORT = get_ip_and_port()
    logging.debug(f"Detected IPADDR={IPADDR}, PORT={PORT}")
    if not IPADDR:
        exit_program("No network interface found. Cannot start Pyro4 daemon.")

    product_name, product_revision = get_board_identity()

    json_file = None
    if product_revision:
        rev_file = os.path.join(
            BOARD_PATH, f"{product_name}-{product_revision}.json"
        )
        if os.path.isfile(rev_file):
            json_file = rev_file
            logging.info(f"Board file (revision): {json_file}")
        else:
            logging.info(f"Board file (revision) not found: {rev_file}")

    if json_file is None:
        base_file = os.path.join(BOARD_PATH, f"{product_name}.json")
        if os.path.isfile(base_file):
            json_file = base_file
            logging.info(f"Board file: {json_file}")
        else:
            logging.info(f"Board file not found: {base_file}")

    if json_file is None or not is_valid_json_file(json_file):
        exit_program("Invalid or missing board configuration JSON.")

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    try:
        pm_obj = PM(json_data, product_name, onboard)
        daemon = Pyro4.Daemon(host=IPADDR, port=PORT)
        uri = daemon.register(pm_obj, objectId="PM")

        logging.info("RAFT-PM Server started successfully.")
        logging.info(f"Listening on {IPADDR}:{PORT}")

        daemon.requestLoop()
    except Exception as e:
        exit_program(f"Pyro4 Daemon startup failed: {e}")

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    start_pyro_daemon()
