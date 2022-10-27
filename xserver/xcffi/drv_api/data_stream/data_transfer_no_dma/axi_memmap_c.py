# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
from utils import ffi, open_c_library
import logging

axi_memmap_handle = open_c_library(
    RAFT_DIR + "xserver/xcffi/drv_header/data_stream/data_transfer_no_dma/axi_memmap.h",
    "/usr/lib/libaximemmap.so.1",
)


class AXI_MEMMAP_C(object):
    def __init__(self):
        logging.info("Inside AXI_MEMMAP_C Constructor")
        pass

    def axi_read_words(self, address, num_words, network_order):
        """
        Read num_words from address.

        :param address: address to read from
        :param num_words: number of words to read
        :param network_order: Apply network byte ordering if network_order!=0
        :return: ret: whether success or failure
                 buf: the read data

        """
        buf = ffi.new("unsigned int[]", num_words)
        ret = axi_memmap_handle.axi_read_words(address, num_words, buf, network_order)
        buf = [buf[k] for k in range(num_words)]
        if ret == 0:
            logging.info("axi_read_words returned success")
        else:
            logging.info("axi_read_words returned failure ret = ", ret)
        return ret, buf

    def axi_write_words(self, address, num_words, buf, network_order):
        """
        Write num_words to address.

        :param address: address to write
        :param num_words: number of words to write
        :param buffer: data to write
        :param network_order: Apply network byte ordering if network_order!=0
        :return: ret: whether success or failure

        """
        buf_in = ffi.new("unsigned int[]", buf)
        ret = axi_memmap_handle.axi_write_words(
            address, num_words, buf_in, network_order
        )
        if ret == 0:
            logging.info("axi_write_words returned success")
        else:
            logging.info("axi_write_words returned failure ret = ", ret)
        return ret

    def __del__(self):
        logging.info("Inside AXI_MEMMAP_C Destructor")
