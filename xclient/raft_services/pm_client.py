# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import Pyro4
import Pyro4.utils
import logging
import base64
import json
import sys

sys.excepthook = Pyro4.util.excepthook

class PM_Client(object):
    PM = None
    logger = None
    LogLevelsDict = {
        "DEBUG": 4,
        "INFO": 3,
        "WARNING": 2,
        "ERROR": 1,
        "CRITICAL": 0
    }

    def __init__(self):
        self.logger = self.GetLogger()
        self.logger.info("Inside PM Pyro Client Constructor")
        self.SetIpAndPort("127.0.0.1", "9090")
        return

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :return: logger

        """
        log_level = logging.DEBUG
        logging.basicConfig(format="%(levelname)s:%(message)s")
        logger = logging.getLogger(__name__)
        try:
            handler_set_check = getattr(logger, 'handler_set')
        except AttributeError:
            handler_set_check = False
        if not handler_set_check:
            logger.setLevel(log_level)
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.handler_set = True
            logger.disabled = False
        return logger

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform PM Client the IP address and port number of PM Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:PM@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.PM = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.PM.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.PM.SetServerLogLevel(PythonLogLevel)
        return

    def SetClientLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """

        if PythonLogLevel == self.LogLevelsDict["DEBUG"]:
            self.logger.setLevel(logging.DEBUG)
        elif PythonLogLevel == self.LogLevelsDict["INFO"]:
            self.logger.setLevel(logging.INFO)
        elif PythonLogLevel == self.LogLevelsDict["WARNING"]:
            self.logger.setLevel(logging.WARNING)
        elif PythonLogLevel == self.LogLevelsDict["ERROR"]:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.CRITICAL)
        return

    def SetMetalLogLevel(self, MetalLogLevel):
        """
        Set the metal log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetMetalLogLevel({MetalLogLevel})")
        self.PM.SetMetalLogLevel(MetalLogLevel)
        return

    def GetBoardInfo(self):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        #self.logger.debug(f"execute: " + strCmd)
        status = self.PM.GetBoardInfo()
        #self.logger.debug(f"return: ststus: {status}, command output: {strCmdRet}")
        return status

    def GetPowerDomains(self):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        #self.logger.debug(f"execute: " + strCmd)
        #my_dict["power-domains"]
        my_list = []
        my_list = self.PM.GetPowerDomains()
        for d in my_list:
            print(d)
        #self.logger.debug(f"return: ststus: {status}, command output: {strCmdRet}")
        return True

    def GetSuppliesOfDomain(self, tag):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        #self.logger.debug(f"execute: " + strCmd)
        list_s = self.PM.GetSuppliesOfDomain(tag)
        print(list_s)
        #self.logger.debug(f"return: ststus: {status}, command output: {strCmdRet}")
        return True

    def GetSupplyDetails(self, supplyname):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        #self.logger.debug(f"execute: " + strCmd)
        supply = self.PM.GetSupplyDetails(supplyname)
        print(supply)
        return True

    def ReadValues(self):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        #self.logger.debug(f"execute: " + strCmd)
        status = self.PM.GetValues()
        #self.logger.debug(f"return: ststus: {status}, command output: {strCmdRet}")
        return status

    def RaftConsole(self, strCmd):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        self.logger.debug(f"execute: " + strCmd)
        status, strCmdRet = self.PM.RaftConsole(strCmd)
        self.logger.debug(f"return: ststus: {status}, command output: {strCmdRet}")
        return status, strCmdRet

pm_c = PM_Client()
pm_c.GetBoardInfo()
pm_c.GetPowerDomains()
pm_c.GetSuppliesOfDomain("FPD")
pm_c.GetSupplyDetails("VCCINT")
#client.GetSu("saasa")
##client.ReadValues()
