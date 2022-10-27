# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

from common_example1 import get_ip
import sys
sys.path.append('../../xclient/data_stream/data_transfer_no_dma')
import axi_memmap_client
handle = axi_memmap_client.axi_memmap
handle.SetIpAndPort(get_ip(),"9090")

# write registers
#
# Sets up loopback of downlink chain to uplink chain (from CFR output to Equalizer Input)
# See dfe_vec_mux_README.txt in Vivado Project for details of block and registers.
#
# equivalent devmem commands
#
# sudo devmem 0xa600d000 32 0x00000003

baseaddr=0xa600d000
handle.axi_write_words(baseaddr+0x00,1,[0x00000003],0)
