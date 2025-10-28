#!/usr/bin/env python3
# Copyright (C) 2023-2025 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2025, Advanced Micro Devices, Inc."

import os
import sys
import json
import logging
import Pyro4
from periphery import I2C

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

def get_product_name():
    eeprom_data = get_eeprom_data()
    offset = 0x15
    length = int.from_bytes(eeprom_data[offset:offset+1], "big") & 0x3f
    name = eeprom_data[offset+1:(offset+1 + length)].decode("utf-8").strip('\x00')
    logging.debug(f"Product name determined: {name}")
    return name

# -------------------------
# Pyro4 Daemon
# -------------------------
def start_pyro_daemon():
    IPADDR, PORT = get_ip_and_port()
    logging.debug(f"Detected IPADDR={IPADDR}, PORT={PORT}")
    if not IPADDR:
        exit_program("No network interface found. Cannot start Pyro4 daemon.")

    json_file = os.path.join(
        RAFT_DIR, 'xserver/raft_services/power_management/board',
        f"{get_product_name()}.json"
    )
    logging.debug(f"Using board JSON file: {json_file}")
    if not is_valid_json_file(json_file):
        exit_program("Invalid or missing board configuration JSON.")

    with open(json_file, 'r') as f:
        json_data = json.load(f)
    board_name = os.path.splitext(os.path.basename(json_file))[0]

    try:
        pm_obj = PM(json_data, board_name, onboard)
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
