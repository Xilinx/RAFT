# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import os
import sys
import json
sys.path.append('../../utils')
sys.path.append('../../raft_services')
sys.path.append('../../raft_services/power_management')
import Pyro4
from pm import PM
from utils import get_ip_and_port

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n"
          "No eth0 network interface present.\n"
          "Please pass the ipaddress to __init__.py.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit()


def is_valid_json_file(file_path):
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, 'r') as file:
            json.load(file)
        return True
    except (ValueError, OSError):
        return False

def parse_json_file(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    return json_data

if(len(sys.argv) > 3):
    json_file = sys.argv[3]
    if is_valid_json_file(json_file):
        print("The file is a valid JSON file.")
        json_data = parse_json_file(json_file)
    else:
        print("The file is NOT a valid JSON file")
        sys.exit()

PM = Pyro4.expose(PM)

Pyro4.Daemon.serveSimple(
    {
        PM(json_data): "PM",
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)
