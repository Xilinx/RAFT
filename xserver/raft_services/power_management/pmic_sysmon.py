# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import Pyro4
import logging
#import base64

logging.basicConfig(level=logging.ERROR)

class Sysmon_Client(object):
    Sysmon = None

    def __init__(self):
        logging.info("Inside Sysmon_Client Constructor")
        pass

    """
    def SetIpAndPort(self, ipaddr, port):
        API to inform Sysmon Client the IP address and port number of I2C Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        
        logging.debug("ipaddr = " + str(ipaddr))
        logging.debug("port = " + str(port))
        uri = "PYRO:SYSMON@" + str(ipaddr) + ":" + str(port)
        logging.debug("uri = " + uri)
        self.Sysmon = Pyro4.Proxy(uri)
        pass
    """      

    def XSysmon_ReadValue(self, idStr):
        """
        I2C driver read a register

        :param addr: address of INA226 device
        :param reg: register to be read
        :return: ret_code, value of register
        """
        ret, val = self.Sysmon.XSysmon_ReadValue(idStr)
        return ret, val

    def __del__(self):
        logging.info("Inside Sysmon Destructor")
