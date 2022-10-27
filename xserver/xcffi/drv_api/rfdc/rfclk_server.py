# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
import json
from utils import ffi, open_c_library, cdata_to_py, xhelper_handle
from utils import get_python_log_levels

rfclk_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/rfdc/xrfclk_h_python.h", "/usr/lib/librfclk.so.1")


class RFCLK(object):
    MAX_DATA_SIZE_LMK = 128
    MAX_DATA_SIZE_LMX = 116
    RFCLK_LMX2594_1 = 0
    RFCLK_LMX2594_2 = 1
    RFCLK_LMK = 2
    max_size = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error("RFCLK: XHelper_MetalInit failed. ret = ", ret)
        self.logger.info(f"Inside RFCLK Constructor")
        pass

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
            logger.handler_set = True
            logger.disabled = False
        return logger

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        return get_python_log_levels()

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"PythonLogLevel = {PythonLogLevel}")
        LogLevelsDict = get_python_log_levels()
        if PythonLogLevel == LogLevelsDict["DEBUG"]:
            self.logger.setLevel(logging.DEBUG)
        elif PythonLogLevel == LogLevelsDict["INFO"]:
            self.logger.setLevel(logging.INFO)
        elif PythonLogLevel == LogLevelsDict["WARNING"]:
            self.logger.setLevel(logging.WARNING)
        elif PythonLogLevel == LogLevelsDict["ERROR"]:
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
        metal_log_level = ffi.typeof("enum metal_log_level").relements
        if MetalLogLevel == metal_log_level["METAL_LOG_DEBUG"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_DEBUG)
        elif MetalLogLevel == metal_log_level["METAL_LOG_INFO"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_INFO)
        elif MetalLogLevel == metal_log_level["METAL_LOG_NOTICE"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_NOTICE)
        elif MetalLogLevel == metal_log_level["METAL_LOG_WARNING"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_WARNING)
        elif MetalLogLevel == metal_log_level["METAL_LOG_ERROR"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_ERROR)
        elif MetalLogLevel == metal_log_level["METAL_LOG_CRITICAL"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_CRITICAL)
        elif MetalLogLevel == metal_log_level["METAL_LOG_ALERT"]:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_ALERT)
        else:
            xhelper_handle.XHelper_MetalSetLogLevel(xhelper_handle.METAL_LOG_EMERGENCY)
        return

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        metal_log_level = ffi.typeof("enum metal_log_level").relements
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    def XRFClk_Init(self, GpioId):
        ret = rfclk_handle.XRFClk_Init(GpioId)
        self.logger.debug(f"\nret = XRFClk_Init({GpioId})")
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFClk_ResetChip(self, ChipId):
        self.logger.debug(f"\nret = XRFClk_ResetChip({ChipId})")
        ret = rfclk_handle.XRFClk_ResetChip(ChipId)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFClk_SetConfigOnOneChipFromConfigId(self, ChipId, ConfigId):
        self.logger.debug(
            f"\nret = XRFClk_SetConfigOnOneChipFromConfigId({ChipId}, {ConfigId})"
        )
        ret = rfclk_handle.XRFClk_SetConfigOnOneChipFromConfigId(ChipId, ConfigId)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFClk_GetConfigFromOneChip(self, ChipId):
        if ChipId == self.RFCLK_LMK:
            self.max_size = self.MAX_DATA_SIZE_LMK
        else:
            self.max_size = self.MAX_DATA_SIZE_LMX
        CfgData = ffi.new("unsigned int a[]", self.max_size)
        self.logger.debug(f"\nret = XRFClk_GetConfigFromOneChip({ChipId}, {CfgData})")
        ret = rfclk_handle.XRFClk_GetConfigFromOneChip(ChipId, CfgData)
        self.logger.debug(f"The return value is {ret}")
        self.logger.debug(f"The Configuration data is the following:")
        print("[{}]".format(", ".join(hex(x) for x in CfgData)))
        return list(CfgData)

    def XRFClk_SetConfigOnAllChipsFromConfigId(
        self, ConfigId_LMK, ConfigId_1, ConfigId_2
    ):
        self.logger.debug(
            f"\nret = XRFClk_SetConfigOnAllChipsFromConfigId({ConfigId_LMK}, {ConfigId_1}, {ConfigId_2}"
        )
        ret = rfclk_handle.XRFClk_SetConfigOnAllChipsFromConfigId(
            ConfigId_LMK, ConfigId_1, ConfigId_2
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFClk_WriteReg(self, ChipId, Data):
        self.logger.debug(f"\nret = XRFClk_WriteReg({ChipId}, {hex(Data)})")
        ret = rfclk_handle.XRFClk_WriteReg(ChipId, Data)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFClk_ReadReg(self, ChipId):
        self.logger.debug(f"\nret = XRFClk_ReadReg({ChipId})")
        DataPtr = ffi.new("u32 *")
        ret = rfclk_handle.XRFClk_ReadReg(ChipId, DataPtr)
        Data = DataPtr[0]
        self.logger.debug(f"The return value is {ret} and Data is {Data}")
        return Data

    def __del__(self):
        self.logger.info("Inside RFCLK Destructor")
