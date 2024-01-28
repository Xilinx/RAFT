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
from utils import ffi, xhelper_handle, open_c_library, cdata_to_py
from utils import extract_b64_encoded_string, cdata_string_to_py

sysmon_handle = open_c_library(RAFT_DIR+"xserver/xcffi/drv_header/pat/xsysmon_python.h", "/usr/lib/libXSysmon.so.1")

@Pyro4.expose
class SYSMON(object):

    def __init__(self):
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            logging.error("SYSMON: XHelper_MetalInit failed. ret = ", ret)
        logging.info("Inside Sysmon Constructor")
        pass

    def XSysmon_ReadValue(self, idStr):
        """
        API Read a INA226 register.

        :param addr: addr of INA226 device
        :param reg:  register to be read
        :return: ret_code, pointer unsigned short

        """
        logging.info("Inside XSysmon_ReadValue")
        idStr = idStr.encode('ascii')

        Val_ptr = ffi.new("float *")

        ret = sysmon_handle.XSysmon_ReadValue(idStr, Val_ptr)
        return ret, Val_ptr[0]



    def __del__(self):
        logging.info("Inside Sysmon Destructor")

#if __name__ == "__main__" :
#        Sysmon = SYSMON()
#        ret, val = Sysmon.XSysmon_ReadValue("in_temp0_ps_temp")
