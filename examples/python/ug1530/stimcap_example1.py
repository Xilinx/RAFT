#   Copyright (c) 2022, Xilinx, Inc.
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
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
# Sets up playback of pre-loaded stimulus.
# See vec_mem_stimcap_README.txt in Vivado Project for details of block and registers.
#
# equivalent devmem commands
#
#sudo devmem 0xad0e0000 32 0x00100001
#sudo devmem 0xad0e0000 32 0x00100000
#sudo devmem 0xad0e0008 32 0x000140FF
#sudo devmem 0xad0e000c 32 0x0
#sudo devmem 0xad0e0010 32 0x0
#sudo devmem 0xad0e0014 32 0x00003FFF

baseaddr=0xad0e0000
# reset
handle.axi_write_words(baseaddr+0x00,1,[0x00100001],0)
handle.axi_write_words(baseaddr+0x00,1,[0x00100000],0)
# write trigger
wdata=[0x000140FF,0,0,0x3FFF]
handle.axi_write_words(baseaddr+0x08,4,wdata,0)
