# Copyright (C) 2023-2025 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2025, Advanced Micro Devices, Inc."

import os
import sys
import json
import logging
sys.path.append('../../utils')
sys.path.append('../../raft_services')
sys.path.append('../../raft_services/power_management')
import Pyro4
from periphery import I2C
from pm import PM
from utils import get_ip_and_port

RAFT_DIR = '/usr/share/raft/'

logging.basicConfig(level=logging.ERROR)

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n"
          "No eth0 network interface present.\n"
          "Please pass the ipaddress to __init__.py and retry.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit(1)
else:
    print("RAFT Pyro Server run successfully\n")

def exit_program():
    logging.error("CRITICAL ERROR: Unable to Run Raft-PM Server.")
    sys.exit(1)

def is_valid_json_file(file_path):
    if not os.path.isfile(file_path):
        logging.error("ERROR:root:Board Identification Json is not in Path : {file_path}")
        return False
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return True
    except json.JSONDecodeError:
        logging.error("ERROR:root:{file} Board Identification is not a JSON")
        return False

class board_eeprom:
    Name = ""
    I2C_Bus = ""
    I2C_Addr = ""

onboard = board_eeprom()

def parse_json_file(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
        #print(json.dumps(json_data, indent=2))
    return json_data

def find_i2c_device_by_name(target_name):
    sys_i2c_path = "/sys/bus/i2c/devices/"

    for device in os.listdir(sys_i2c_path):
        name_path = os.path.join(sys_i2c_path, device, "name")

        if os.path.isfile(name_path):
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

    logging.debug(f"Device {target_name} not found")
    return None, None

def get_eeprom_data():
    result = False
    i2c = None
    onboard.Name = "Common"
    onboard.I2C_Bus = "/dev/i2c-1"
    onboard.I2C_Addr = 0x54
    data  = bytearray(256)
    try:
        i2c = I2C(onboard.I2C_Bus)
        msgs = [I2C.Message([0x0, 0x0]), I2C.Message(data, read=True)]
        i2c.transfer(onboard.I2C_Addr, msgs)
        eeprom_data = msgs[1].data
        result = True
        i2c.close()
    except:
        logging.debug(f"Onboard {onboard.Name} Eeprom read failed!")

    if result is False:
        onboard.Name = "Legacy"
        onboard.I2C_Bus = "/dev/i2c-11"
        onboard.I2C_Addr = 0x54
        data  = bytearray(256)
        try:
            i2c = I2C(onboard.I2C_Bus)
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(data, read=True)]
            i2c.transfer(onboard.I2C_Addr, msgs)
            eeprom_data = msgs[1].data
            result = True
            i2c.close()
        except:
            logging.debug(f"Onboard {onboard.Name} Eeprom read failed!")

    if result is False:
        device_path, device_address = find_i2c_device_by_name("24c128")
        if device_path is not None:
            onboard.Name = "Custom"
            onboard.I2C_Bus = device_path
            onboard.I2C_Addr = device_address
            data  = bytearray(256)
            try:
                i2c = I2C(onboard.I2C_Bus)
                msgs = [I2C.Message([0x0, 0x0]), I2C.Message(data, read=True)]
                i2c.transfer(onboard.I2C_Addr, msgs)
                eeprom_data = msgs[1].data
                result = True
                i2c.close()
            except:
                logging.debug(f"Onboard {onboard.Name} Eeprom read failed!")

    if result is False:
        logging.error("Board Eeprom Identification Failed.")
        exit_program()

    return eeprom_data

def get_product_name():
    eeprom_data = get_eeprom_data()
    offset = 0x15
    length = int.from_bytes(eeprom_data[offset:offset+1], "big") & 0x3f
    name = eeprom_data[offset+1:(offset+1 + length)].decode("utf-8").strip('\x00')
    return name

json_file = os.path.join(RAFT_DIR, 'xserver/raft_services/power_management/board', '.'.join((get_product_name(), 'json')))

if is_valid_json_file(json_file):
    json_data = parse_json_file(json_file)
    board_name = os.path.splitext(os.path.basename(json_file))
else:
    exit_program()

PM = Pyro4.expose(PM)

Pyro4.Daemon.serveSimple(
    {
        PM(json_data, board_name[0], onboard): "PM",
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)
