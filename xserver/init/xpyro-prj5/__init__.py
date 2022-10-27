# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Dragan Cvetic"
__copyright__ = "Copyright 2022, Xilinx"

import sys
sys.path.append('../../utils')
sys.path.append('../../raft_services')
import Pyro4
from console_server import CONSOLE
from utils import get_ip_and_port

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n"
          "No eth0 network interface present.\n"
          "Please pass the ipaddress to __init__.py.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit()

CONSOLE = Pyro4.expose(CONSOLE)

Pyro4.Daemon.serveSimple(
    {
        CONSOLE: "CONSOLE",
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)
