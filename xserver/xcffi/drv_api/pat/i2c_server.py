# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Hugh Maguire"
__copyright__ = "Copyright 2021, Xilinx"

import sys
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import Pyro4
import logging
import base64
from cffi import FFI
from utils import ffi, xhelper_handle,  open_c_library, cdata_to_py
from utils import extract_b64_encoded_string, cdata_string_to_py

i2c_handle = open_c_library(RAFT_DIR+"xserver/xcffi/drv_header/pat/xi2c_python.h", "/usr/lib/libXI2c.so")

@Pyro4.expose
class I2C(object):
    i2c_dict = {}

    def __init__(self):
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            logging.error("I2C: XHelper_MetalInit failed. ret = ", ret)
        logging.info("Inside I2C Constructor")
        pass

    # System initialization API
    def XI2c_Initialize(self, device):
        """
        API Initialise one instance of an I2c driver.

        :param device: contains the number of the i2c device
        :return: pointer to instance if successful, NULL on error.

        """
        logging.debug("XI2c_Initialize(Init)")
        Inst_ptr = ffi.new("XI2c *")
        ret = i2c_handle.XI2c_Initialize(Inst_ptr, device)
        Inst = cdata_to_py(Inst_ptr[0])
        self.i2c_dict[0] = Inst_ptr
        return ret

    def XI2c_ReadINA226Reg(self, addr, reg):
        """
        API Read a INA226 register.

        :param addr: addr of INA226 device
        :param reg:  register to be read
        :return: ret_code, pointer unsigned short

        """

        Inst_ptr = self.i2c_dict[0];
        Val_ptr = ffi.new("unsigned short *")

        ret = i2c_handle.XI2c_ReadINA226Reg(Inst_ptr, addr, reg, Val_ptr)
        return ret, Val_ptr[0]

    def XI2c_WriteINA226Reg(self, addr, reg, val):

        """
        API Write an INA266 register

        :param addr: addr of INA226 device
        :param reg:  register to be read
        :param val:  value to be written
        :return: ret_code

        """
        Inst_ptr = self.i2c_dict[0];

        ret = i2c_handle.XI2c_WriteINA226Reg(Inst_ptr, addr, reg, val)
        return ret

    # System initialization API
    def XI2c_Release(self):
        """
        API Release an Instance of I2c driver
        """
        Inst_ptr = self.i2c_dict[0]
        logging.debug("XI2c_Release()")
        i2c_handle.XI2c_Release(Inst_ptr)
        return

    def __del__(self):
        logging.info("Inside I2C Destructor")

"""
Some quick test code
"""

#if __name__ == "__main__" :
#        I2c = I2C()
#        I2c.XI2c_Initialize(2)
#        Inst_ptr = I2c.i2c_dict[0]
#        Inst = cdata_to_py(Inst_ptr[0])
#        ret, val_ptr = I2c.XI2c_ReadINA226Reg(0x43, 0x5)
#        print(hex(val_ptr[0]))
#        ret = I2c.XI2c_WriteINA226Reg(0x43, 0x5, 0x1234)
#        ret, val_ptr = I2c.XI2c_ReadINA226Reg(0x43, 0x5)
#        print(hex(val_ptr[0]))
#        pass
