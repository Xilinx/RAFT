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
# Sets up CC Sequence on TID signal matching default vectors.
# See dfe_vec_ccseq_README.txt in Vivado Project for details of block and registers.
#
# equivalent devmem commands
#
#sudo devmem 0xad0b1010 32 0x00000701
#sudo devmem 0xad0b1014 32 0xF0F0F0F0
#sudo devmem 0xad0b1018 32 0x0
#sudo devmem 0xad0b101C 32 0x1

baseaddr=0xad0b1000
wdata=[0x00000701,0xf0f0f0f0,0,1]
handle.axi_write_words(baseaddr+0x10,4,wdata,0)
