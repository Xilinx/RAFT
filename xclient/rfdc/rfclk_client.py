# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Gerard Thomas Colman"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import json
import sys


class RFCLK_CLIENT(object):
    RFCLK = None
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
        self.logger.info("Inside RFCLK Pyro Client Constructor")
        return

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :return: logger

        """
        log_level = logging.ERROR
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
        API to inform RFCLK Client the IP address and port number of RFCLK Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:RFCLK@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.RFCLK = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.RFCLK.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.RFCLK.SetServerLogLevel(PythonLogLevel)
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
        self.RFCLK.SetMetalLogLevel(MetalLogLevel)
        return

    def GetRfclkMacro(self):
        """
        Return Dictionary with all RFCLK macros in the rfclk header file

        :param : None
        :return: Dictionary with all RFCLK macros in the rfclk header file
        """
        self.logger.debug("GetRfclkMacro()")
        rfclk_macro = self.RFCLK.GetRfclkMacro()
        self.logger.debug(f"rfclk_macro = {json.dumps(rfclk_macro, indent=2)}")
        return rfclk_macro

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.RFCLK.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    def XRFClk_Init(self, GpioId):
        self.logger.debug(f"XRFClk_Init({GpioId})")
        ret = self.RFCLK.XRFClk_Init(GpioId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XRFClk_ResetChip(self, ChipId):
        self.logger.debug(f"XRFClk_ResetChip({ChipId})")
        ret = self.RFCLK.XRFClk_ResetChip(ChipId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XRFClk_SetConfigOnOneChipFromConfigId(self, ChipId, ConfigId):
        self.logger.debug(f"XRFClk_SetConfigOnOneChipFromConfigId({ChipId}, {ConfigId})")
        ret = self.RFCLK.XRFClk_SetConfigOnOneChipFromConfigId(ChipId, ConfigId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XRFClk_GetConfigFromOneChip(self, ChipId):
        self.logger.debug(f"XRFClk_GetConfigFromOneChip({ChipId})")
        CfgData = self.RFCLK.XRFClk_GetConfigFromOneChip(ChipId)
        self.logger.debug(f"CfgData = {CfgData}")
        return CfgData

    def XRFClk_SetConfigOnAllChipsFromConfigId(self, ConfigId_LMK, ConfigId_1, ConfigId_2):
        self.logger.debug(f"XRFClk_SetConfigOnAllChipsFromConfigId({ConfigId_LMK}, {ConfigId_1}, {ConfigId_2})")
        ret = self.RFCLK.XRFClk_SetConfigOnAllChipsFromConfigId(ConfigId_LMK, ConfigId_1, ConfigId_2)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XRFClk_WriteReg(self, ChipId, Data):
        self.logger.debug(f"XRFClk_WriteReg({ChipId}, {Data})")
        ret = self.RFCLK.XRFClk_WriteReg(ChipId, Data)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XRFClk_ReadReg(self, ChipId):
        self.logger.debug(f"XRFClk_ReadReg({ChipId})")
        DataVal = self.RFCLK.XRFClk_ReadReg(ChipId)
        self.logger.debug(f"DataVal = {DataVal}")
        return DataVal

    def __del__(self):
        self.logger.info("Inside RFCLK Destructor")

rfclk = RFCLK_CLIENT()
