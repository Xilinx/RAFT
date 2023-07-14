# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Hugh Maguire"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64

logging.basicConfig(level=logging.ERROR)

class I2C_Client(object):
    I2C = None

    def __init__(self):
        logging.info("Inside CCF_Client Constructor")
        pass

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform I2C Client the IP address and port number of I2C Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        logging.debug("ipaddr = " + str(ipaddr))
        logging.debug("port = " + str(port))
        uri = "PYRO:I2C@" + str(ipaddr) + ":" + str(port)
        logging.debug("uri = " + uri)
        self.I2C = Pyro4.Proxy(uri)
        pass

    def XI2c_Initialize(self, device):
        """
        I2C driver one time initialisation.

        :param device_id: id of the opened device
        :return: ret_code
        """
        logging.debug(
            "XDfeCcf_Initialize(" + str(device) +  ")"
        )
        ret = self.I2C.XI2c_Initialize(device)
        logging.debug("The return value Init = " + str(ret))
        return ret

    def XI2c_ReadINA226Reg(self, addr, reg):
        """
        I2C driver read a register

        :param addr: address of INA226 device
        :param reg: register to be read
        :return: ret_code, value of register
        """
        ret, val = self.I2C.XI2c_ReadINA226Reg(addr, reg)
        return ret, val

    def XI2c_WriteINA226Reg(self, addr, reg, val):
        """
        I2C driver write a register

        :param addr: address of INA226 device
        :param reg: register to be written
        :param val: value to be written
        :return: ret_code
        """
        ret = self.I2C.XI2c_WriteINA226Reg(addr, reg, val)
        return ret

    def XI2c_Release(self):
        """
        I2C driver Release instance
        :return: none
        """
        self.I2C.XI2c_Release()

    def __del__(self):
        logging.info("Inside I2C Destructor")

i2c = I2C_Client()
