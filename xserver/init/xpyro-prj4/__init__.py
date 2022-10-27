# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
sys.path.append('../../utils')
sys.path.append('../../xcffi/drv_api/dfe')
sys.path.append('../../xcffi/drv_api/rfdc')
sys.path.append('../../xcffi/drv_api/data_stream/data_transfer_no_dma')
sys.path.append('../../xpyro/data_stream/data_transfer_no_dma')
import Pyro4
from rfdc_server import RFDC
from rfclk_server import RFCLK
from mix_server import MIX
from ccf_server import CCF
from equ_server import EQU
from prach_server import PRACH
from ofdm_server import OFDM
from axi_memmap import AXI_MEMMAP
from utils import get_ip_and_port

IPADDR, PORT = get_ip_and_port()
if len(IPADDR) == 0:
    print("CRITITCAL ERROR: Unable to Run Pyro Server.\n"
          "No eth0 network interface present.\n"
          "Please pass the ipaddress to __init__.py.\n"
          "Usage:python3 __init__.py <ipaddress> <port>\n")
    sys.exit()

RFDC = Pyro4.expose(RFDC)
RFCLK = Pyro4.expose(RFCLK)
MIX = Pyro4.expose(MIX)
CCF = Pyro4.expose(CCF)
EQU = Pyro4.expose(EQU)
PRACH = Pyro4.expose(PRACH)
OFDM = Pyro4.expose(OFDM)
AXI_MEMMAP = Pyro4.expose(AXI_MEMMAP)

Pyro4.Daemon.serveSimple(
    {
        RFDC: "RFDC",
        RFCLK: "RFCLK",
        MIX: "MIX",
        CCF: "CCF",
        EQU: "EQU",
        PRACH: "PRACH",
        OFDM: "OFDM",
        AXI_MEMMAP: "AXI_MEMMAP",
    },
    host=IPADDR,
    port=PORT,
    ns=False,
    verbose=True,
)
