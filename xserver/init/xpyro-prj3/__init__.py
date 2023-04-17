# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Hugh Maguire"
__copyright__ = "Copyright 2021, Xilinx"

import sys
sys.path.append('../../utils')
sys.path.append('../../xcffi/drv_api/rfdc')
import Pyro4
from rfdc_server import RFDC
from utils import get_ip_and_port

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n"
          "No eth0 network interface present.\n"
          "Please pass the ipaddress to __init__.py.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit()

RFDC = Pyro4.expose(RFDC)

Pyro4.Daemon.serveSimple(
    {
        RFDC: "RFDC"
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)
