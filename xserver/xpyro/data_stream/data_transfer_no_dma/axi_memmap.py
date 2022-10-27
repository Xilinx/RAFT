# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64
from utils import convert_to_bytearray, convert_to_list
import serpent
from axi_memmap_c import AXI_MEMMAP_C


class AXI_MEMMAP(object):
    memmap_c = None
    def __init__(self):
        self.memmap_c = AXI_MEMMAP_C()
        logging.info("Inside AXI MEMMAP Constructor")
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
        ret, buf = self.memmap_c.axi_read_words(address, num_words, network_order)
        buf = convert_to_bytearray(buf)
        if ret == 0:
            logging.info("axi_memmap_c.axi_read_words returned success")
        else:
            logging.info("axi_memmap_c.axi_read_words returned failure ret = ", ret)
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
        if Pyro4.config.SERIALIZER == "serpent" and type(buf) is dict:
            buf = serpent.tobytes(buf)  # in case of serpent encoded bytes
        buf = convert_to_list(buf[0:num_words*4])
        ret = self.memmap_c.axi_write_words(address, num_words, buf,  network_order)
        if ret == 0:
            logging.info("axi_memmap_c.axi_write_words returned success")
        else:
            logging.info("axi_memmap_c.axi_write_words returned failure ret = ", ret)
        return ret

    def __del__(self):
        logging.info("Inside AXI MEMMAP Destructor")

