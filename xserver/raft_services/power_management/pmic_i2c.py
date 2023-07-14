# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import Pyro4
import logging
import base64
from periphery import I2C

logging.basicConfig(level=logging.ERROR)


class I2C_Client(object):

    def __init__(self, device_no, device_addr, device_type):
        logging.info("Inside I2C_Client Constructor")
        self.addr = device_addr
        self.device_no = device_no
        self.device_type = device_type

        logging.debug(
            "I2C_Client Initialize(" + str(self.device_no) +  ")"
        )
        try:
            self.device = I2C("/dev/i2c-" + str(self.device_no))
        except IOError:
            logging.error("I2C_Client Initialize failed.")
        

    """
    def SetIpAndPort(self, ipaddr, port):
        
        API to inform I2C Client the IP address and port number of I2C Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        
        logging.debug("ipaddr = " + str(ipaddr))
        logging.debug("port = " + str(port))
        uri = "PYRO:I2C@" + str(ipaddr) + ":" + str(port)
        logging.debug("uri = " + uri)
        self.I2C = Pyro4.Proxy(uri)
        pass
    """
    def Initialize(self):
        """
        I2C driver one time initialisation.

        :param device_id: id of the opened device
        :return: ret_code
        """
        ret = True
        logging.debug(
            "I2C_Client Initialize(" + str(self.device_no) +  ")"
        )
        #self.device_type = d_type
        #try:
        #    self.device = I2C("/dev/i2c-" + str(number))
        #    ret = True
        #except IOError:
        #    logging.error("I2C_Client Initialize failed.")
        return ret
    
    def ReadRegister(self, reg):
        """
        I2C driver read a register

        :param addr: address of I2C device
        :param reg: register to be read
        :return: ret_code, value of register
        """
        ret = False
        try:
            match self.device_type:
                case DeviceType.INA226:
                    msgs = [I2C.Message([reg]), I2C.Message([0x00, 0x00], read=True)]
                case _:
                    return ret, None
            self.device.transfer(self.addr, msgs)
            logging.debug("{0}: 0x{1:02x}{2:02x}".format(self.addr, msgs[1].data[0], msgs[1].data[1]))
            ret = True
        except IOError:   
            logging.error("I2C_Client ReadINA226Reg failed.")
        val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        #ret, val = self.I2C.XI2c_ReadINA226Reg(addr, reg)
        return ret, val

    def WriteRegister(self, reg, val):
        """
        I2C driver write a register

        :param addr: address of INA226 device
        :param reg: register to be written
        :param val: value to be written
        :return: ret_code
        """
        ret = False
        data = None
        try:
            match self.device_type:
                case DeviceType.INA226:
                    data = bytearray(val.to_bytes(2, "big"))
                    data.insert(0, reg)
                    msgs = [I2C.Message(data)]
                case _:
                    return ret
            self.device.transfer(self.addr, msgs)
            ret = True
        except IOError:   
            logging.error("I2C_Client WriteINA226Reg failed.")
        #val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        #ret = self.I2C.XI2c_WriteINA226Reg(addr, reg, val)
        return ret

    def Release(self):
        """
        I2C driver Release instance
        :return: none
        """
        self.device.close()

    def __del__(self):
        logging.info("Inside I2C Destructor")
