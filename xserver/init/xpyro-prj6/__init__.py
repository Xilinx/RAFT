# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import os 
import platform
import sys
import json
sys.path.append('../../utils')
sys.path.append('../../raft_services')
sys.path.append('../../raft_services/power_management')
import Pyro4
from pathlib import Path
from pm import PM
from pmic_i2c import I2C_Client
from utils import get_ip_and_port

RAFT_DIR = '/usr/share/raft/'
SYS_CTL_APP_DIR = '/usr/share/system-controller-app/'

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("RAFT ERROR: Unable to Run Pyro Server.\n"
          "No network interface present.\n"
          "Please pass the ipaddress to __init__.py and retry.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit()
else:
    print("RAFT Pyro Server run successfully\n")

def exit_program():
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n")
    sys.exit(1)

def is_valid_json_file(file_path):
    if not os.path.isfile(file_path):
        print("ERROR:root:Board Identification Json is not in Path : {file_path}")
        return False
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return True
    except json.JSONDecodeError:
        print("ERROR:root:{file} Board Identification is not a JSON")
        return False

class board_eeprom:
    Name = ""
    I2C_Bus = ""
    I2C_Addr = ""

onboard = board_eeprom()

def parse_json_file(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    return json_data

def get_eeprom_data():
    result = False
    i2c = None
    onboard.Name = "Common"
    onboard.I2C_Bus = "/dev/i2c-1"
    onboard.I2C_Addr = "0x54"
    i2c = I2C_Client(onboard.I2C_Bus, onboard.I2C_Addr) # Common_OnBoard_EEPROM
    if i2c.device is not None:
        result, eeprom_data = i2c.ReadRegister(0x00, 256)
    if result is False:
        #i2c.Release()
        onboard.Name = "Legacy"
        onboard.I2C_Bus = "/dev/i2c-11"
        onboard.I2C_Addr = "0x54"
        i2c = I2C_Client(onboard.I2C_Bus, onboard.I2C_Addr)
        if i2c.device is not None:
            result, eeprom_data = i2c.ReadRegister(0x00, 256)
        if result is False:
            print("ERROR:root:Board Identification Eeprom Failed.")
            exit_program()
        i2c.Release()
    return eeprom_data

def get_product_name():
    eeprom_data = get_eeprom_data()
    offset = 0x15
    length = int.from_bytes(eeprom_data[offset:offset+1], "big") & 0x3f
    name = eeprom_data[offset+1:(offset+1 + length)].decode("utf-8").strip('\x00')
    return name

if(len(sys.argv) > 2):

    product_name = get_product_name()
    #json_file = os.path.join(RAFT_DIR, 'xserver/raft_services/power_management/boards', '.'.join((product_name, 'json')))
    json_file = os.path.join(SYS_CTL_APP_DIR, 'board', '.'.join((product_name, 'json')))

    if is_valid_json_file(json_file):
        json_data = parse_json_file(json_file)
        board_name = os.path.splitext(os.path.basename(json_file))
    else:
        exit_program()

PM = Pyro4.expose(PM)

Pyro4.Daemon.serveSimple(
    {
        PM(json_data, board_name[0], 'INA226', onboard): "PM",
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)

