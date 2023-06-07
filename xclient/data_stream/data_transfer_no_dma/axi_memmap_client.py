# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import serpent
import logging

def convert_to_bytearray(data):
    b = bytearray()
    for i in range(len(data)):
        c = data[i].to_bytes(4, byteorder='little', signed=False)
        b.extend(c)
    return b

def convert_to_list(data):
    k = []
    for i in range(int(len(data)/4)):
        k.append(int.from_bytes(data[(i*4):(((i+1)*4))], byteorder='little'))
    return k


class AXI_MEMMAP_Client(object):
    AXI_MEMMAP = None

    def __init__(self):
        logging.info("Inside AXI_MEMMAP Pyro Client Constructor")
        pass

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform AXI_MEMMAP Client the IP address and port number of AXI_MEMMAP Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:AXI_MEMMAP@{ipaddr}:{port}"
        logging.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.AXI_MEMMAP = Pyro4.Proxy(uri)
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
        logging.debug("axi_read_words({address}, {num_words}, {network_order})")
        ret, buf = self.AXI_MEMMAP.axi_read_words(address, num_words, network_order)
        logging.debug(f"ret = {ret}")
        buf = serpent.tobytes(buf)
        buf = convert_to_list(buf)
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
        buf = convert_to_bytearray(buf)
        logging.debug("axi_write_words({address}, {num_words}, {network_order})")
        ret = self.AXI_MEMMAP.axi_write_words(address, num_words, buf, network_order)
        logging.debug(f"ret = {ret}")
        return ret

axi_memmap = AXI_MEMMAP_Client()
