# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import Pyro4
import logging
import base64
from enum import Enum
from periphery import I2C

logging.basicConfig(level=logging.ERROR)


class DeviceType(Enum):
    INA226 = 1
    INA230 = 2
    SYSMON = 99
    #Possible other Power Monitor IC definitions here.
class I2C_Client(object):

    def __init__(self, device_no, device_addr):
        logging.info("Inside I2C_Client Constructor")
        self.addr = int(device_addr, 0)
        self.device_no = device_no
        self.device = None


        logging.debug(
            "I2C_Client Initialize(" + str(self.device_no) +  ")"
        )
        try:
            self.device = I2C(self.device_no)
        except IOError:
            logging.error("I2C_Client Initialize failed.")
        

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
    
    def ReadRegister(self, reg, length):
        """
        I2C driver read a register

        :param reg: register to be read
        :param length: length to be read
        :return: ret_code, value of register
        """
        ret = False
        msgs = None
        data  = bytearray(length)
        try:
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(data, read=True)]
            self.device.transfer(self.addr, msgs)
            #logging.debug("{0}: 0x{1:02x}{2:02x}".format(self.addr, msgs[1].data[0], msgs[1].data[1]))
            ret = True
        except IOError:   
            logging.error("I2C_Client  failed.")
        return ret, msgs[1].data

    def WriteRegister(self, reg, val):
        """
        I2C driver write a register

        :param reg: register to be written
        :param val: value to be written
        :return: ret_code
        """
        ret = False
        data = None
        try:
            data = bytearray(val.to_bytes(2, "big"))
            data.insert(0, reg)
            msgs = [I2C.Message(data)]
            self.device.transfer(self.addr, msgs)
            ret = True
        except IOError:   
            logging.error("I2C_Client WriteINA226Reg failed.")
        return ret

    def Release(self):
        """
        I2C driver Release instance
        :return: none
        """
        self.device.close()

    def __del__(self):
        logging.info("Inside I2C Destructor")
