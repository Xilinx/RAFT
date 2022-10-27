# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
import json
from utils import ffi, open_packed_c_library, cdata_to_py, cptr_to_pylist
from utils import cdata_to_py, get_python_log_levels
from utils import getkey_from_listbeginvalue, xhelper_handle

rfdc_handle = open_packed_c_library(RAFT_DIR + "xserver/xcffi/drv_header/rfdc/xrfdc_h_python.h", "/usr/lib/librfdc.so.1")


class RFDC(object):
    ERR_XRFDC_LOOKUPCONFIG_FAILED = 0x1
    rfdc_inst_dict = {}
    inst_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        self.logger.info("Inside RFDC Constructor")
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error(f"RFDC: XHelper_MetalInit failed. ret = {ret}")
        return

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :param : None
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

    # Log level
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

    def GetStruct_XRFdc_PLL_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_PLL_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_PLL_Settings
        """
        XRFdc_PLL_Settings_ptr = ffi.new("XRFdc_PLL_Settings *")
        XRFdc_PLL_Settings = cdata_to_py(XRFdc_PLL_Settings_ptr[0])
        return XRFdc_PLL_Settings

    def GetStruct_XRFdc_Tile_Clock_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Tile_Clock_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Tile_Clock_Settings
        """
        XRFdc_Tile_Clock_Settings_ptr = ffi.new("XRFdc_Tile_Clock_Settings *")
        XRFdc_Tile_Clock_Settings = cdata_to_py(XRFdc_Tile_Clock_Settings_ptr[0])
        return XRFdc_Tile_Clock_Settings

    def GetStruct_XRFdc_Distribution_Info(self):
        """
        Return Dictionary equivalent of structure XRFdc_Distribution_Info

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Distribution_Info
        """
        XRFdc_Distribution_Info_ptr = ffi.new("XRFdc_Distribution_Info *")
        XRFdc_Distribution_Info = cdata_to_py(XRFdc_Distribution_Info_ptr[0])
        return XRFdc_Distribution_Info

    def GetStruct_XRFdc_Distribution_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Distribution_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Distribution_Settings
        """
        XRFdc_Distribution_Settings_ptr = ffi.new("XRFdc_Distribution_Settings *")
        XRFdc_Distribution_Settings = cdata_to_py(XRFdc_Distribution_Settings_ptr[0])
        return XRFdc_Distribution_Settings

    def GetStruct_XRFdc_Distribution_System_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Distribution_System_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Distribution_System_Settings
        """
        XRFdc_Distribution_System_Settings_ptr = ffi.new("XRFdc_Distribution_System_Settings *")
        XRFdc_Distribution_System_Settings = cdata_to_py(XRFdc_Distribution_System_Settings_ptr[0])
        return XRFdc_Distribution_System_Settings


    def GetStruct_XRFdc_MTS_DTC_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_MTS_DTC_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_MTS_DTC_Settings
        """
        XRFdc_MTS_DTC_Settings_ptr = ffi.new("XRFdc_MTS_DTC_Settings *")
        XRFdc_MTS_DTC_Settings = cdata_to_py(XRFdc_MTS_DTC_Settings_ptr[0])
        return XRFdc_MTS_DTC_Settings

    def GetStruct_XRFdc_MultiConverter_Sync_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config
        """
        XRFdc_MultiConverter_Sync_Config_ptr = ffi.new("XRFdc_MultiConverter_Sync_Config *")
        XRFdc_MultiConverter_Sync_Config = cdata_to_py(XRFdc_MultiConverter_Sync_Config_ptr[0])
        return XRFdc_MultiConverter_Sync_Config

    def GetStruct_XRFdc_MTS_Marker(self):
        """
        Return Dictionary equivalent of structure XRFdc_MTS_Marker

        :param : None
        :return: Dictionary equivalent of structure XRFdc_MTS_Marker
        """
        XRFdc_MTS_Marker_ptr = ffi.new("XRFdc_MTS_Marker *")
        XRFdc_MTS_Marker = cdata_to_py(XRFdc_MTS_Marker_ptr[0])
        return XRFdc_MTS_Marker

    def GetStruct_XRFdc_Signal_Detector_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Signal_Detector_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Signal_Detector_Settings
        """
        XRFdc_Signal_Detector_Settings_ptr = ffi.new("XRFdc_Signal_Detector_Settings *")
        XRFdc_Signal_Detector_Settings = cdata_to_py(XRFdc_Signal_Detector_Settings_ptr[0])
        return XRFdc_Signal_Detector_Settings

    def GetStruct_XRFdc_QMC_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_QMC_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_QMC_Settings
        """
        XRFdc_QMC_Settings_ptr = ffi.new("XRFdc_QMC_Settings *")
        XRFdc_QMC_Settings = cdata_to_py(XRFdc_QMC_Settings_ptr[0])
        return XRFdc_QMC_Settings

    def GetStruct_XRFdc_CoarseDelay_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_CoarseDelay_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_CoarseDelay_Settings
        """
        XRFdc_CoarseDelay_Settings_ptr = ffi.new("XRFdc_CoarseDelay_Settings *")
        XRFdc_CoarseDelay_Settings = cdata_to_py(XRFdc_CoarseDelay_Settings_ptr[0])
        return XRFdc_CoarseDelay_Settings

    def GetStruct_XRFdc_Mixer_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Mixer_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Mixer_Settings
        """
        XRFdc_Mixer_Settings_ptr = ffi.new("XRFdc_Mixer_Settings *")
        XRFdc_Mixer_Settings = cdata_to_py(XRFdc_Mixer_Settings_ptr[0])
        return XRFdc_Mixer_Settings

    def GetStruct_XRFdc_Threshold_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Threshold_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Threshold_Settings
        """
        XRFdc_Threshold_Settings_ptr = ffi.new("XRFdc_Threshold_Settings *")
        XRFdc_Threshold_Settings = cdata_to_py(XRFdc_Threshold_Settings_ptr[0])
        return XRFdc_Threshold_Settings

    def GetStruct_XRFdc_Calibration_Coefficients(self):
        """
        Return Dictionary equivalent of structure XRFdc_Calibration_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Calibration_Coefficients
        """
        XRFdc_Calibration_Coefficients_ptr = ffi.new("XRFdc_Calibration_Coefficients *")
        XRFdc_Calibration_Coefficients = cdata_to_py(XRFdc_Calibration_Coefficients_ptr[0])
        return XRFdc_Calibration_Coefficients

    def GetStruct_XRFdc_Pwr_Mode_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings
        """
        XRFdc_Pwr_Mode_Settings_ptr = ffi.new("XRFdc_Pwr_Mode_Settings *")
        XRFdc_Pwr_Mode_Settings = cdata_to_py(XRFdc_Pwr_Mode_Settings_ptr[0])
        return XRFdc_Pwr_Mode_Settings

    def GetStruct_XRFdc_DSA_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_DSA_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DSA_Settings
        """
        XRFdc_DSA_Settings_ptr = ffi.new("XRFdc_DSA_Settings *")
        XRFdc_DSA_Settings = cdata_to_py(XRFdc_DSA_Settings_ptr[0])
        return XRFdc_DSA_Settings

    def GetStruct_XRFdc_Cal_Freeze_Settings(self):
        """
        Return Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings
        """
        XRFdc_Cal_Freeze_Settings_ptr = ffi.new("XRFdc_Cal_Freeze_Settings *")
        XRFdc_Cal_Freeze_Settings = cdata_to_py(XRFdc_Cal_Freeze_Settings_ptr[0])
        return XRFdc_Cal_Freeze_Settings

    def GetStruct_XRFdc_TileStatus(self):
        """
        Return Dictionary equivalent of structure XRFdc_TileStatus

        :param : None
        :return: Dictionary equivalent of structure XRFdc_TileStatus
        """
        XRFdc_TileStatus_ptr = ffi.new("XRFdc_TileStatus *")
        XRFdc_TileStatus = cdata_to_py(XRFdc_TileStatus_ptr[0])
        return XRFdc_TileStatus

    def GetStruct_XRFdc_IPStatus(self):
        """
        Return Dictionary equivalent of structure XRFdc_IPStatus

        :param : None
        :return: Dictionary equivalent of structure XRFdc_IPStatus
        """
        XRFdc_IPStatus_ptr = ffi.new("XRFdc_IPStatus *")
        XRFdc_IPStatus = cdata_to_py(XRFdc_IPStatus_ptr[0])
        return XRFdc_IPStatus

    def GetStruct_XRFdc_BlockStatus(self):
        """
        Return Dictionary equivalent of structure XRFdc_BlockStatus

        :param : None
        :return: Dictionary equivalent of structure XRFdc_BlockStatus
        """
        XRFdc_BlockStatus_ptr = ffi.new("XRFdc_BlockStatus *")
        XRFdc_BlockStatus = cdata_to_py(XRFdc_BlockStatus_ptr[0])
        return XRFdc_BlockStatus

    def GetStruct_XRFdc_DACBlock_AnalogDataPath_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config
        """
        XRFdc_DACBlock_AnalogDataPath_Config_ptr = ffi.new("XRFdc_DACBlock_AnalogDataPath_Config *")
        XRFdc_DACBlock_AnalogDataPath_Config = cdata_to_py(XRFdc_DACBlock_AnalogDataPath_Config_ptr[0])
        return XRFdc_DACBlock_AnalogDataPath_Config

    def GetStruct_XRFdc_DACBlock_DigitalDataPath_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config
        """
        XRFdc_DACBlock_DigitalDataPath_Config_ptr = ffi.new("XRFdc_DACBlock_DigitalDataPath_Config *")
        XRFdc_DACBlock_DigitalDataPath_Config = cdata_to_py(XRFdc_DACBlock_DigitalDataPath_Config_ptr[0])
        return XRFdc_DACBlock_DigitalDataPath_Config

    def GetStruct_XRFdc_ADCBlock_AnalogDataPath_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config
        """
        XRFdc_ADCBlock_AnalogDataPath_Config_ptr = ffi.new("XRFdc_ADCBlock_AnalogDataPath_Config *")
        XRFdc_ADCBlock_AnalogDataPath_Config = cdata_to_py(XRFdc_ADCBlock_AnalogDataPath_Config_ptr[0])
        return XRFdc_ADCBlock_AnalogDataPath_Config

    def GetStruct_XRFdc_ADCBlock_DigitalDataPath_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config
        """
        XRFdc_ADCBlock_DigitalDataPath_Config_ptr = ffi.new("XRFdc_ADCBlock_DigitalDataPath_Config *")
        XRFdc_ADCBlock_DigitalDataPath_Config = cdata_to_py(XRFdc_ADCBlock_DigitalDataPath_Config_ptr[0])
        return XRFdc_ADCBlock_DigitalDataPath_Config

    def GetStruct_XRFdc_DACTile_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_DACTile_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DACTile_Config
        """
        XRFdc_DACTile_Config_ptr = ffi.new("XRFdc_DACTile_Config *")
        XRFdc_DACTile_Config = cdata_to_py(XRFdc_DACTile_Config_ptr[0])
        return XRFdc_DACTile_Config

    def GetStruct_XRFdc_ADCTile_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADCTile_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADCTile_Config
        """
        XRFdc_ADCTile_Config_ptr = ffi.new("XRFdc_ADCTile_Config *")
        XRFdc_ADCTile_Config = cdata_to_py(XRFdc_ADCTile_Config_ptr[0])
        return XRFdc_ADCTile_Config

    def GetStruct_XRFdc_Config(self):
        """
        Return Dictionary equivalent of structure XRFdc_Config

        :param : None
        :return: Dictionary equivalent of structure XRFdc_Config
        """
        XRFdc_Config_ptr = ffi.new("XRFdc_Config *")
        XRFdc_Config = cdata_to_py(XRFdc_Config_ptr[0])
        return XRFdc_Config

    def GetStruct_XRFdc_DACBlock_AnalogDataPath(self):
        """
        Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath
        """
        XRFdc_DACBlock_AnalogDataPath_ptr = ffi.new("XRFdc_DACBlock_AnalogDataPath *")
        XRFdc_DACBlock_AnalogDataPath = cdata_to_py(XRFdc_DACBlock_AnalogDataPath_ptr[0])
        return XRFdc_DACBlock_AnalogDataPath

    def GetStruct_XRFdc_DACBlock_DigitalDataPath(self):
        """
        Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath
        """
        XRFdc_DACBlock_DigitalDataPath_ptr = ffi.new("XRFdc_DACBlock_DigitalDataPath *")
        XRFdc_DACBlock_DigitalDataPath = cdata_to_py(XRFdc_DACBlock_DigitalDataPath_ptr[0])
        return XRFdc_DACBlock_DigitalDataPath

    def GetStruct_XRFdc_ADCBlock_AnalogDataPath(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath
        """
        XRFdc_ADCBlock_AnalogDataPath_ptr = ffi.new("XRFdc_ADCBlock_AnalogDataPath *")
        XRFdc_ADCBlock_AnalogDataPath = cdata_to_py(XRFdc_ADCBlock_AnalogDataPath_ptr[0])
        return XRFdc_ADCBlock_AnalogDataPath

    def GetStruct_XRFdc_ADCBlock_DigitalDataPath(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath
        """
        XRFdc_ADCBlock_DigitalDataPath_ptr = ffi.new("XRFdc_ADCBlock_DigitalDataPath *")
        XRFdc_ADCBlock_DigitalDataPath = cdata_to_py(XRFdc_ADCBlock_DigitalDataPath_ptr[0])
        return XRFdc_ADCBlock_DigitalDataPath

    def GetStruct_XRFdc_DAC_Tile(self):
        """
        Return Dictionary equivalent of structure XRFdc_DAC_Tile

        :param : None
        :return: Dictionary equivalent of structure XRFdc_DAC_Tile
        """
        XRFdc_DAC_Tile_ptr = ffi.new("XRFdc_DAC_Tile *")
        XRFdc_DAC_Tile = cdata_to_py(XRFdc_DAC_Tile_ptr[0])
        return XRFdc_DAC_Tile

    def GetStruct_XRFdc_ADC_Tile(self):
        """
        Return Dictionary equivalent of structure XRFdc_ADC_Tile

        :param : None
        :return: Dictionary equivalent of structure XRFdc_ADC_Tile
        """
        XRFdc_ADC_Tile_ptr = ffi.new("XRFdc_ADC_Tile *")
        XRFdc_ADC_Tile = cdata_to_py(XRFdc_ADC_Tile_ptr[0])
        return XRFdc_ADC_Tile

    def XRFdc_LookupConfig(self, DeviceId):
        """
        Looks up the device configuration based on the unique device ID. A table
        contains the configuration info for each device in the system.

        :param : DeviceId: DeviceId contains the ID of the device to look up the configuration.
        :return: ret - XRFDC_SUCCESS on success, XRFDC_FAILURE on failure
                 Config - container with values. Will be Null on failure.
        """
        self.logger.debug(f"XRFdc_LookupConfig({DeviceId})")
        cptrXRFdc_Config = rfdc_handle.XRFdc_LookupConfig(DeviceId)
        if ffi.NULL == cptrXRFdc_Config:
            ret = 1
            Config = 0
        else:
            ret = 0
            Config = cdata_to_py(cptrXRFdc_Config[0])
        return ret, Config

    def XRFdc_RegisterMetal(self, DeviceId):
        """
        Register/open the device and map RFDC to the IO region.

        :param : DeviceId: DeviceId contains the ID of the device to register/map
        :return: ret - XRFDC_SUCCESS on success, XRFDC_FAILURE if error occurs
                 inst_id - integer handle to the initialized instance
        """
        self.logger.debug(f"XRFdc_RegisterMetal({DeviceId})")
        device = ffi.new("struct metal_device **")
        RFdcInstPtr = ffi.new("XRFdc *")
        ret = rfdc_handle.XRFdc_RegisterMetal(RFdcInstPtr, DeviceId, device)
        self.logger.debug(f"The return value ret = {ret}")
        # In rfdc_inst_dict dictionary, inst id is the key.
        # DeviceId and instance pointer are values as list
        # check if the DeviceId is already present in dictionary
        found, inst_id = getkey_from_listbeginvalue(self.rfdc_inst_dict, DeviceId)
        if 1 == found:
            # if found, update the device id key with values
            self.rfdc_inst_dict[inst_id][1] = RFdcInstPtr
        else:
            # if not found, make new inst_id from class variable
            # and increment the class variable
            inst_id = self.inst_id
            self.inst_id += 1
            # add new key and values to the dictionary
            self.rfdc_inst_dict[inst_id] = [DeviceId, RFdcInstPtr]
        return ret, inst_id

    def XRFdc_CfgInitialize(self, inst_id, Config):
        """
        Initializes a specific XRFdc instance such that the driver is ready to use.

        :param inst_id: Id of the RFDC instance
        :param Config: DeviceId contains the ID of the device to look up the configuration.
        :return: ret - XRFDC_SUCCESS if successful.
                 Config - XRFdc_Config container with values. Will be same as passed value
        """
        self.logger.debug(f"XRFdc_CfgInitialize({Config})")
        cptrConfig = ffi.new("XRFdc_Config *", Config)
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_CfgInitialize(RFdcInstPtr, cptrConfig)
        Config = cdata_to_py(cptrConfig[0])
        self.logger.debug(f"The return value ret = {ret}, Config = {Config}")
        return ret, Config

    def XRFdc_GetDeviceNameByDeviceId(self, DevId):
        """
        Traverse "/sys/bus/platform/device" directory, to find RFDC device entry,
        corresponding to provided device id. If device entry corresponding to said
        device id is found, store it in output buffer DevName.

        :param : DevId: contains the ID of the device to look up the RFDC device name
                      It is an entry in "/sys/bus/platform/device"
        :return: ret - XRFDC_SUCCESS on success, XRFDC_FAILURE if device entry not found for given device id.
                 DevName - device node name returned from driver
                                  which will be same as the passed value
        """
        self.logger.debug(f"ret = XRFdc_GetDeviceNameByDeviceId()")
        cptrDevName = ffi.new("char[100]")
        ret = rfdc_handle.XRFdc_GetDeviceNameByDeviceId(cptrDevName, DevId)
        DevName = cdata_string_to_py(cptrDevName)
        self.logger.debug(f"The return value is: {ret}, {DevName}")
        return ret, DevName

    def XRFdc_GetDriverVersion(self):
        """
        This API is used to get the driver version

        :param : None
        :return: Driver version number
        """
        self.logger.debug("version = XRFdc_GetDriverVersion()")
        version = rfdc_handle.XRFdc_GetDriverVersion()
        self.logger.debug(f"The version is: {version}")
        return version

    def XRFdc_ClrSetReg(self, inst_id, BaseAddr, RegAddr, Mask, Data):
        """
        Execute Read modify Write

        :param inst_id: Id of the RFDC instance
        :param BaseAddr: Address of a block
        :param RegAddr: Register offset value
        :param Mask: Bit mask value
        :param Data: Value to be written to register
        :return: None
        """
        self.logger.debug(f"ret = XRFdc_ClrSetReg({BaseAddr}, {RegAddr}, {Mask}, {Data})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        rfdc_handle.XRFdc_ClrSetReg(RFdcInstPtr, BaseAddr, RegAddr, Mask, Data)
        pass

    def XRFdc_ClrReg(self, inst_id, BaseAddr, RegAddr, Mask):
        """
        Execute Read and clear

        :param inst_id: Id of the RFDC instance
        :param BaseAddr: Address of a block
        :param RegAddr: Register offset value
        :param Mask: Bit mask value
        :return: None
        """
        self.logger.debug(f"ret = XRFdc_ClrReg({BaseAddr}, {RegAddr}, {Mask})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        rfdc_handle.XRFdc_ClrReg(RFdcInstPtr, BaseAddr, RegAddr, Mask)
        pass

    def XRFdc_RDReg(self, inst_id, BaseAddr, RegAddr, Mask):
        """
        Execute Read and mask with the value

        :param inst_id: Id of the RFDC instance
        :param BaseAddr: Address of a block
        :param RegAddr: Register offset value
        :param Mask: Bit mask value
        :return: None
        """
        self.logger.debug(f"ret = XRFdc_RDReg({BaseAddr}, {RegAddr}, {Mask})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_RDReg(RFdcInstPtr, BaseAddr, RegAddr, Mask)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsHighSpeedADC(self, inst_id, Tile_Id):
        """
        Get ADC type is High Speed or Medium Speed

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3
        :return: 1 if ADC type is 4GSPS, otherwise 0 if quad or invalid tile.
        """
        self.logger.debug(f"ret = XRFdc_IsHighSpeedADC({Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsHighSpeedADC(RFdcInstPtr, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsDACBlockEnabled(self, inst_id, Tile_Id, Block_Id):
        """
        Checks whether DAC block is available or not

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0 - 3
        :return: Return 1 if DAC block is available, otherwise 0
        """
        self.logger.debug(f"ret = XRFdc_IsDACBlockEnabled({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsDACBlockEnabled(RFdcInstPtr, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsADCBlockEnabled(self, inst_id, Tile_Id, Block_Id):
        """
        Checks whether ADC block is available or not

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                      Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Return 1 if ADC block is available, otherwise 0
        """
        self.logger.debug(f"ret = XRFdc_IsADCBlockEnabled( {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsADCBlockEnabled(RFdcInstPtr, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsDACDigitalPathEnabled(self, inst_id, Tile_Id, Block_Id):
        """
        Checks whether DAC Digital path is enabled or not

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                      Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: ret: Return 1 if DAC digital path is enabled, otherwise 0
        """
        self.logger.debug(f"ret = XRFdc_IsDACDigitalPathEnabled({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsDACDigitalPathEnabled(
            RFdcInstPtr, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsADCDigitalPathEnabled(self, inst_id, Tile_Id, Block_Id):
        """
        Checks whether ADC digital path is enabled or not

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                      Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Return 1 if ADC digital path is enabled, otherwise 0.
        """
        self.logger.debug(f"ret = XRFdc_IsADCDigitalPathEnabled({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsADCDigitalPathEnabled(
            RFdcInstPtr, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_CheckDigitalPathEnabled(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Checks whether ADC/DAC Digital path is enabled or not

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                      Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: - XRFDC_SUCCESS if Digital path is enabled, XRFDC_FAILURE if Digital path is not enabled.
        """
        self.logger.debug(
            f"ret = XRFdc_CheckDigitalPathEnabled({Type}, {Tile_Id}, {Block_Id})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_CheckDigitalPathEnabled(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_Get_IPBaseAddr(self, inst_id):
        """
        Get the RFDC IP Base Address

        :param inst_id: Id of the RFDC instance
        :return: Return IP BaseAddress
        """
        self.logger.debug("Inside XRFdc_Get_IPBaseAddr")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        base_address = rfdc_handle.XRFdc_Get_IPBaseAddr(RFdcInstPtr)
        self.logger.debug(f"The return value is: {base_address}")
        return base_address

    def XRFdc_Get_TileBaseAddr(self, inst_id, Type, Tile_Id):
        """
        Get Tile BaseAddress

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: Tile BaseAddress if valid, Return 0U if invalid/unavailable tile
        """
        self.logger.debug(f"ret = XRFdc_Get_TileBaseAddr({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_Get_TileBaseAddr(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_Get_BlockBaseAddr(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get Block BaseAddress

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Block BaseAddress, Return 0U if invalid/unavailable block
        """
        self.logger.debug(f"ret = XRFdc_Get_BlockBaseAddr({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_Get_BlockBaseAddr(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetNoOfDACBlock(self, inst_id, Tile_Id):
        """
        Get Number of DAC Blocks enabled

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: number of DAC blocks enabled.
        """
        self.logger.debug(f"ret = XRFdc_GetNoOfDACBlock({Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetNoOfDACBlock(RFdcInstPtr, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetNoOfADCBlocks(self, inst_id, Tile_Id):
        """
        Get Number of ADC Blocks enabled.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: number of ADC blocks enabled.
        """
        self.logger.debug(f"ret = XRFdc_GetNoOfADCBlocks({Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetNoOfADCBlocks(RFdcInstPtr, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDataType(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get Mixer Input Data Type for ADC/DAC block.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: MixerInputDataType of ADC/DAC block. 0U if converter type, tile or block number is invalid
        """
        self.logger.debug(f"ret = XRFdc_GetDataType({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDataType(RFdcInstPtr, Type, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDataWidth(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get Data Width for ADC/DAC block.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0-3.
        :return: DataWidth of ADC/DAC block.
        """
        self.logger.debug(f"ret = XRFdc_GetDataWidth({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDataWidth(RFdcInstPtr, Type, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetInverseSincFilter(self, inst_id, Tile_Id, Block_Id):
        """
        Get Inversesync filter for DAC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Inversesync filter for DAC block. Return 0 if invalid
        """
        self.logger.debug(f"ret = XRFdc_GetInverseSincFilter({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetInverseSincFilter(
            RFdcInstPtr, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetMixedMode(self, inst_id, Tile_Id, Block_Id):
        """
        Get Mixed mode for DAC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: mixed mode for DAC block
        """
        self.logger.debug(f"ret = XRFdc_GetMixedMode({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMixedMode(RFdcInstPtr, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetMasterTile(self, inst_id, Type):
        """
        Get Master Tile for ADC/DAC tiles.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :return: Master Tile for ADC/DAC tiles. Returns XRFDC_TILE_ID_INV if converter type is invalid
        """
        self.logger.debug(f"ret = XRFdc_GetMasterTile({Type})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMasterTile(RFdcInstPtr, Type)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetSysRefSource(self, inst_id, Type):
        """
        Get Sysref source for ADC/DAC tile.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :return: Sysref source for ADC/DAC tile. returns XRFDC_TILE_ID_INV if converter type is invalid
        """
        self.logger.debug(f"ret = XRFdc_GetSysRefSource({Type})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetSysRefSource(RFdcInstPtr, Type)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetFabClkFreq(self, inst_id, Type, Tile_Id):
        """
        Get Fabric Clock frequency.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3.
        :return: Fabric Clock frequency for ADC/DAC tile
        """
        self.logger.debug(f"ret = XRFdc_GetFabClkFreq({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabClkFreq(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IsFifoEnabled(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get whether FIFO is enabled or not.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Return 1 if FIFO is enabled, otherwise 0.
        """
        self.logger.debug(f"ret = XRFdc_IsFifoEnabled({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IsFifoEnabled(RFdcInstPtr, Type, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetConnectedIData(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get Data Converter connected for digital data path I

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)
        """
        self.logger.debug(f"ret = XRFdc_GetConnectedIData({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetConnectedIData(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetConnectedQData(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get Data Converter connected for digital data path Q

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)
        """
        self.logger.debug(f"ret = XRFdc_GetConnectedQData({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetConnectedQData(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetConnectedIQData(
        self, inst_id, Type, Tile_Id, Block_Id, ConnectedIData, ConnectedQData
    ):
        """
        Set Data Converter connected for digital data path I and Q

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: #TODO
        :param ConnectedIData: ConnectedIData is Converter Id to which DigitalPathI connected.
        :param ConnectedQData: ConnectedQData is Converter Id to which DigitalPathQ connected.
        :return: None
        """
        self.logger.debug(
            f"ret = XRFdc_SetConnectedIQData({Type}, {Tile_Id}, {Block_Id}, "
            f"{ConnectedIData}, {ConnectedQData})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetConnectedIQData(
            RFdcInstPtr, Type, Tile_Id, Block_Id, ConnectedIData, ConnectedQData
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetMultibandConfig(self, inst_id, Type, Tile_Id):
        """
        Get Multiband Config data

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: Multiband Configuration. Return 0 if invalid.
        """
        self.logger.debug(f"ret = XRFdc_GetMultibandConfig({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMultibandConfig(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_CheckBlockEnabled(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Checks whether ADC/DAC block is enabled or not.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: XRFDC_SUCCESS if block enabled, XRFDC_FAILURE if block is not enabled
        """
        self.logger.debug(f"ret = XRFdc_CheckBlockEnabled({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_CheckBlockEnabled(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_CheckTileEnabled(self, inst_id, Type, Tile_Id):
        """
        Checks whether ADC/DAC tile is enabled or not.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: XRFDC_SUCCESS if tile enabled, XRFDC_FAILURE if tile not enabled
        """
        self.logger.debug(f"ret = XRFdc_CheckTileEnabled({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_CheckTileEnabled(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetMaxSampleRate(self, inst_id, Type, Tile_Id):
        """
        Gets ADC/DAC tile maximum sampling rate.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
        :param Tile_Id: Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if found sampling rate, XRFDC_FAILURE if could not find sampling rate.
                 MaxSampleRate: maximum sample rate
        """
        self.logger.debug(
            f"ret = XRFdc_GetMaxSampleRate({Type}, {Tile_Id}, MaxSampleRatePtr)"
        )
        MaxSampleRatePtr = ffi.new("double *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMaxSampleRate(
            RFdcInstPtr, Type, Tile_Id, MaxSampleRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        MaxSampleRate = MaxSampleRatePtr[0]
        return ret, MaxSampleRate

    def XRFdc_GetMinSampleRate(self, inst_id, Type, Tile_Id):
        """
        Gets ADC/DAC tile minimum sampling rate.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if found sampling rate XRFDC_FAILURE if could not find sampling rate.
                 MinSampleRate: minimum sample rate
        """
        self.logger.debug(
            f"ret = XRFdc_GetMinSampleRate({Type}, {Tile_Id}, MinSampleRatePtr)"
        )
        MinSampleRatePtr = ffi.new("double *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMinSampleRate(
            RFdcInstPtr, Type, Tile_Id, MinSampleRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        MinSampleRate = MinSampleRatePtr[0]
        return ret, MinSampleRate

    def XRFdc_StartUp(self, inst_id, Type, Tile_Id):
        """
        The API Restarts the requested tile. It can restart a single tile and
        alternatively can restart all the tiles. Existing register settings are not
        lost or altered in the process. It just starts the requested tile(s).

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3 and -1
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_StartUp({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_StartUp(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_Shutdown(self, inst_id, Type, Tile_Id):
        """
        The API stops the tile as requested. It can also stop all the tiles if
        asked for. It does not clear any of the existing register settings. It just
        stops the requested tile(s).

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3, and -1
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_Shutdown({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_Shutdown(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_Reset(self, inst_id, Type, Tile_Id):
        """
        The API resets the requested tile. It can reset all the tiles as well. In
        the process, all existing register settings are cleared and are replaced
        with the settings initially configured (through the GUI).

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3, and -1.
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_Reset({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_Reset(RFdcInstPtr, Type, Tile_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_CustomStartUp(self, inst_id, Type, Tile_Id, StartState, EndState):
        """
        The API starts the requested tile from a provided state and runs to the given
        end state. It can restart a single tile and alternatively can restart all the
        tiles. If starting from/ending at XRFDC_START_STATE_OFF/XRFDC_END_STATE_OFF,
        register settings will be wiped.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3, and -1.
        :param StartState: StartState Valid values are XRFDC_START_STATE_*.
        :param EndState: EndState Valid values are XRFDC_END_STATE_*.
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_CustomStartUp({Type}, {Tile_Id}, {StartState}, {EndState})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_CustomStartUp(RFdcInstPtr, Type, Tile_Id, StartState, EndState)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_WaitForState(self, inst_id, Type, Tile_Id, State):
        """
        This function is used to wait for a tile to reach a given state.

        :param inst_id: Id of the RFDC instance
        :param Type: represents ADC or DAC.
        :param Tile_Id: Valid values are 0-3.
        :param State: represents the state which the tile must reach.
        :return: XRFDC_SUCCESS if valid, XRFDC_FAILURE if not valid.
        """
        self.logger.debug(f"ret = XRFdc_WaitForState({Type}, {Tile_Id}, {State})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_WaitForState(RFdcInstPtr, Type, Tile_Id, State)
        self.logger.debug(f"The return value is: {ret}")
        return ret


    def XRFdc_GetIPStatus(self, inst_id):
        """
        The API returns the IP status.

        :param inst_id: Id of the RFDC instance
        :return: ret: XRFDC_SUCCESS if successful
                 IPStatus: Dictionary equivalent to XRFdc_IPStatus structure
        """
        IPStatusPtr = ffi.new("XRFdc_IPStatus *")
        self.logger.debug(f"ret = XRFdc_GetIPStatus(IPStatusPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetIPStatus(RFdcInstPtr, IPStatusPtr)
        self.logger.debug(f"The return value is: {ret}")
        IPStatus = cdata_to_py(IPStatusPtr[0])
        return ret, IPStatus

    def XRFdc_GetBlockStatus(self, inst_id, Type, Tile_Id, Block_Id):
        """
        The API returns the requested block status.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled.
                 BlockStatus: Dictionary equivalent of XRFdc_BlockStatus structure
                 through which the ADC/DAC block status is returned.
        """
        BlockStatusPtr = ffi.new("XRFdc_BlockStatus *")
        self.logger.debug(
            f"ret = XRFdc_GetBlockStatus({Type}, {Tile_Id}, {Block_Id}, BlockStatusPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetBlockStatus(
            RFdcInstPtr, Type, Tile_Id, Block_Id, BlockStatusPtr
        )
        BlockStatus = cdata_to_py(BlockStatusPtr[0])
        self.logger.debug(f"The return value is: {ret}, {BlockStatus}")
        return ret, BlockStatus

    def XRFdc_SetMixerSettings(self, inst_id, Type, Tile_Id, Block_Id, MixerSettings):
        """
        The API is used to update various mixer settings, fine, coarse, NCO etc.
        Mixer/NCO settings passed are used to update the corresponding
        block level registers. Driver structure is updated with the new values.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param MixerSettings: Dictionary in which the Mixer/NCO settings are passed
               FineMixerScale in Mixer_Settings dictionary can have 3 values.
               XRFDC_MIXER_SCALE_* represents the valid values.
               XRFDC_MIXER_SCALE_AUTO - If mixer mode is R2C, Mixer Scale is
               set to 1 and for other modes mixer scale is set to 0.7
               XRFDC_MIXER_SCALE_1P0 - To set fine mixer scale to 1.
               XRFDC_MIXER_SCALE_0P7 - To set fine mixer scale to 0.7.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 MixerSettings: Dictionary in which the Mixer/NCO settings are passed
        """
        MixerSettingsPtr = ffi.new("XRFdc_Mixer_Settings *", MixerSettings)
        self.logger.debug(
            f"ret = XRFdc_SetMixerSettings({Type}, {Tile_Id}, {Block_Id}, MixerSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetMixerSettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, MixerSettingsPtr
        )
        MixerSettings = cdata_to_py(MixerSettingsPtr[0])
        self.logger.debug(f"The return value is: {ret}, {MixerSettings}")
        return ret, MixerSettings

    def XRFdc_GetMixerSettings(self, inst_id, Type, Tile_Id, Block_Id):
        """
        The API returns back Mixer/NCO settings to the caller.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 MixerSettings: Dictionary in which the Mixer/NCO settings are passed
                 FineMixerScale in Mixer_Settings dictionary can have 3 values.
                 XRFDC_MIXER_SCALE_* represents the valid values.
                 XRFDC_MIXER_SCALE_AUTO - If mixer mode is R2C, Mixer Scale is
                 set to 1 and for other modes mixer scale is set to 0.7
                 XRFDC_MIXER_SCALE_1P0 - To set fine mixer scale to 1.
                 XRFDC_MIXER_SCALE_0P7 - To set fine mixer scale to 0.7.
        """
        MixerSettingsPtr = ffi.new("XRFdc_Mixer_Settings *")
        self.logger.debug(
            f"ret = XRFdc_GetMixerSettings({Type}, {Tile_Id}, {Block_Id}, MixerSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMixerSettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, MixerSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        MixerSettings = cdata_to_py(MixerSettingsPtr[0])
        self.logger.debug(MixerSettings)
        return ret, MixerSettings

    def XRFdc_SetQMCSettings(self, inst_id, Type, Tile_Id, Block_Id, QMCSettings):
        """
        This API is used to update various QMC settings, eg gain, phase, offset etc.
        QMC settings passed are used to update the corresponding
        block level registers. Driver structure is updated with the new values.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param QMCSettings: Dictionary equivalent of XRFdc_QMC_Settings structure
                             in which the QMC settings are passed.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        QMCSettingsPtr = ffi.new("XRFdc_QMC_Settings *", QMCSettings)
        self.logger.debug(
            f"ret = XRFdc_SetQMCSettings({Type}, {Tile_Id}, {Block_Id}, QMCSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetQMCSettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, QMCSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        QMCSettings = cdata_to_py(QMCSettingsPtr[0])
        self.logger.debug(QMCSettings)
        return ret, QMCSettings

    def XRFdc_GetQMCSettings(self, inst_id, Type, Tile_Id, Block_Id):
        """
        QMC settings are returned back to the caller through this API.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 QMC_Settings: Dictionary equivalent of XRFdc_QMC_Settings structure
                               in which the QMC settings are passed.
        """
        QMCSettingsPtr = ffi.new("XRFdc_QMC_Settings *")
        self.logger.debug(
            f"ret = XRFdc_GetQMCSettings({Type}, {Tile_Id}, {Block_Id}, QMCSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetQMCSettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, QMCSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        QMCSettings = cdata_to_py(QMCSettingsPtr[0])
        self.logger.debug(QMCSettings)
        return ret, QMCSettings

    def XRFdc_SetCoarseDelaySettings(
        self, inst_id, Type, Tile_Id, Block_Id, CoarseDelaySettings
    ):
        """
        Coarse delay settings passed are used to update the corresponding
        block level registers. Driver structure is updated with the new values.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
                                    structure in which the CoarseDelay settings are passed.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        CoarseDelaySettingsPtr = ffi.new(
            "XRFdc_CoarseDelay_Settings *", CoarseDelaySettings
        )
        self.logger.debug(
            f"ret = XRFdc_SetCoarseDelaySettings({Type}, {Tile_Id}, {Block_Id}, CoarseDelaySettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetCoarseDelaySettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, CoarseDelaySettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        CoarseDelaySettings = cdata_to_py(CoarseDelaySettingsPtr[0])
        self.logger.debug(CoarseDelaySettings)
        return ret, CoarseDelaySettings

    def XRFdc_GetCoarseDelaySettings(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Coarse delay settings are returned back to the caller.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
                                    structure in which the CoarseDelay settings are passed.
        """
        CoarseDelaySettingsPtr = ffi.new("XRFdc_CoarseDelay_Settings *")
        self.logger.debug(
            f"ret = XRFdc_GetCoarseDelaySettings({Type}, {Tile_Id}, {Block_Id}, CoarseDelaySettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetCoarseDelaySettings(
            RFdcInstPtr, Type, Tile_Id, Block_Id, CoarseDelaySettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        CoarseDelaySettings = cdata_to_py(CoarseDelaySettingsPtr[0])
        self.logger.debug(CoarseDelaySettings)
        return ret, CoarseDelaySettings

    def XRFdc_GetInterpolationFactor(self, inst_id, Tile_Id, Block_Id):
        """
        Interpolation factor are returned back to the caller.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 InterpolationFactor: the interpolation factor for DAC blocks.
        """
        self.logger.debug(
            f"ret = XRFdc_GetInterpolationFactor({Tile_Id}, {Block_Id}, InterpolationFactorPtr)"
        )
        InterpolationFactorPtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetInterpolationFactor(
            RFdcInstPtr, Tile_Id, Block_Id, InterpolationFactorPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        InterpolationFactor = InterpolationFactorPtr[0]
        return ret, InterpolationFactor

    def XRFdc_GetDecimationFactor(self, inst_id, Tile_Id, Block_Id):
        """
        Decimation factor are returned back to the caller for both actual and
        observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 DecimationFactor: the decimation factor for DAC blocks.
        """
        self.logger.debug(
            f"ret = XRFdc_GetDecimationFactor({Tile_Id}, {Block_Id}, DecimationFactor)"
        )
        DecimationFactorPtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDecimationFactor(
            RFdcInstPtr, Tile_Id, Block_Id, DecimationFactorPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        DecimationFactor = DecimationFactorPtr[0]
        return ret, DecimationFactor

    def XRFdc_GetDecimationFactorObs(self, inst_id, Tile_Id, Block_Id):
        """
        Decimation factor are returned back to the caller for both actual and
        observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 DecimationFactor: the decimation factor for DAC blocks.
        """
        self.logger.debug(
            f"ret = XRFdc_GetDecimationFactorObs({Tile_Id}, {Block_Id}, DecimationFactor)"
        )
        DecimationFactorPtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDecimationFactor(
            RFdcInstPtr, Tile_Id, Block_Id, DecimationFactorPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        DecimationFactor = DecimationFactorPtr[0]
        return ret, DecimationFactor

    def XRFdc_GetFabWrVldWords(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This function returns the the number of fabric write valid words requested
        for the block. For ADCs this is for both the actual and observation FIFO.
        ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 FabricDataRate: Fabric data rate for DAC block
        """
        self.logger.debug(f"ret = XRFdc_GetFabWrVldWords({Type}, {Tile_Id}, {Block_Id})")
        FabricDataRatePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabWrVldWords(
            RFdcInstPtr, Type, Tile_Id, Block_Id, FabricDataRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        FabricDataRate = FabricDataRatePtr[0]
        return ret, FabricDataRate

    def XRFdc_GetFabWrVldWordsObs(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This API returns the number of fabric write valid words requested
        for the block. This is for the observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 FabricDataRate:  fabric data rate for DAC block
        """
        self.logger.debug(f"ret = XRFdc_GetFabWrVldWordsObs({Type}, {Tile_Id}, {Block_Id})")
        FabricDataRatePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabWrVldWordsObs(
            RFdcInstPtr, Type, Tile_Id, Block_Id, FabricDataRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        FabricDataRate = FabricDataRatePtr[0]
        return ret, FabricDataRate

    def XRFdc_GetFabRdVldWords(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This function returns the number of fabric read valid words requested
        for the block. For ADCs this is for both the actual and observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 FabricDataRate: Fabric data rate for ADC/DAC block
        """
        self.logger.debug(f"ret = XRFdc_GetFabRdVldWords({Type}, {Tile_Id}, {Block_Id})")
        FabricDataRatePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabRdVldWords(
            RFdcInstPtr, Type, Tile_Id, Block_Id, FabricDataRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        FabricDataRate = FabricDataRatePtr[0]
        return ret, FabricDataRate

    def XRFdc_GetFabRdVldWordsObs(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This function returns the number of fabric read valid words requested
        for the block. This is for the observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 FabricDataRate: Fabric data rate for ADC/DAC block
        """
        self.logger.debug(f"ret = XRFdc_GetFabRdVldWordsObs({Type}, {Tile_Id}, {Block_Id})")
        FabricDataRatePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabRdVldWordsObs(
            RFdcInstPtr, Type, Tile_Id, Block_Id, FabricDataRatePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        FabricDataRate = FabricDataRatePtr[0]
        return ret, FabricDataRate

    def XRFdc_SetFabRdVldWords(self, inst_id, Tile_Id, Block_Id, FabricRdVldWords):
        """
        Fabric data rate for the requested ADC block is set by writing to the
        corresponding register. The function writes the number of valid read words
        for the requested ADC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param FabricRdVldWords: Read fabric rate to be set for ADC block.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetFabRdVldWords({Tile_Id}, {Block_Id}, {FabricRdVldWords})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetFabRdVldWords(
            RFdcInstPtr, Tile_Id, Block_Id, FabricRdVldWords
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetFabRdVldWordsObs(self, inst_id, Tile_Id, Block_Id, FabricRdVldWords):
        """
        Fabric data rate for the requested ADC block is set by writing to the
        corresponding register. The function writes the number of valid read words
        for the requested ADC block. This is for the observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param FabricRdVldWords: Read fabric rate to be set for ADC block.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetFabRdVldWordsObs({Tile_Id}, {Block_Id}, {FabricRdVldWords})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetFabRdVldWordsObs(
            RFdcInstPtr, Tile_Id, Block_Id, FabricRdVldWords
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetFabWrVldWords(self, inst_id, Tile_Id, Block_Id, FabricWrVldWords):
        """
        Fabric data rate for the requested DAC block is set by writing to the
        corresponding register. The function writes the number of valid write words
        for the requested DAC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param FabricWrVldWords: write fabric rate to be set for DAC block
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetFabWrVldWords({Tile_Id}, {Block_Id}, {FabricWrVldWords})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetFabWrVldWords(
            RFdcInstPtr, Tile_Id, Block_Id, FabricWrVldWords
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetThresholdSettings(self, inst_id, Tile_Id, Block_Id):
        """
        Threshold settings are read from the corresponding registers and are passed
        back to the caller. There can be two threshold settings:
        threshold0 and threshold1. Both of them are independent of each other.
        The function returns the requested threshold (which can be threshold0,
        threshold1, or both.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 ThresholdSettings:  the register settings for thresholds are passed back
        """
        ThresholdSettingsPtr = ffi.new("XRFdc_Threshold_Settings *")
        self.logger.debug(
            f"ret = XRFdc_GetThresholdSettings({Tile_Id}, {Block_Id}, ThresholdSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetThresholdSettings(
            RFdcInstPtr, Tile_Id, Block_Id, ThresholdSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        ThresholdSettings = cdata_to_py(ThresholdSettingsPtr[0])
        self.logger.debug(ThresholdSettings)
        return ret, ThresholdSettings

    def XRFdc_SetThresholdSettings(self, inst_id, Tile_Id, Block_Id, ThresholdSettings):
        """
        Threshold settings are updated into the relevant registers. Driver structure
        is updated with the new values. There can be two threshold settings:
        threshold0 and threshold1. Both of them are independent of each other.
        The function returns the requested threshold (which can be threshold0,
        threshold1, or both.
        Only ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param ThresholdSettings: the register settings
                                  for thresholds are passed to the API
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 ThresholdSettings: the register settings for thresholds are passed back
        """
        ThresholdSettingsPtr = ffi.new("XRFdc_Threshold_Settings *", ThresholdSettings)
        self.logger.debug(
            f"ret = XRFdc_SetThresholdSettings({Tile_Id}, {Block_Id}, ThresholdSettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetThresholdSettings(
            RFdcInstPtr, Tile_Id, Block_Id, ThresholdSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        ThresholdSettings = cdata_to_py(ThresholdSettingsPtr[0])
        self.logger.debug(ThresholdSettings)
        return ret, ThresholdSettings

    def XRFdc_SetDecoderMode(self, inst_id, Tile_Id, Block_Id, DecoderMode):
        """
        Decoder mode is updated into the relevant registers. Driver structure is
        updated with the new values.
        Only DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param DecoderMode: DecoderMode Valid values are 1 (Maximum SNR, for non-
               randomized decoder), 2 (Maximum Linearity, for randomized decoder)
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetDecoderMode({Tile_Id}, {Block_Id}, {DecoderMode})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDecoderMode(
            RFdcInstPtr, Tile_Id, Block_Id, DecoderMode
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_UpdateEvent(self, inst_id, Type, Tile_Id, Block_Id, Event):
        """
        This function will trigger the update event for an event.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Event: Event is for which dynamic update event will trigger.
                      XRFDC_EVENT_* defines the different events.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_UpdateEvent({Type}, {Tile_Id}, {Block_Id}, {Event})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_UpdateEvent(
            RFdcInstPtr, Type, Tile_Id, Block_Id, Event
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDecoderMode(self, inst_id, Tile_Id, Block_Id):
        """
        Decoder mode is read and returned back.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 DecoderMode: Valid values are 1 (Maximum SNR, for non-randomized
*           decoder), 2 (Maximum Linearity, for randomized decoder)
        """
        DecoderModePtr = ffi.new("u32 *")
        self.logger.debug(
            f"ret = XRFdc_GetDecoderMode({Tile_Id}, {Block_Id}, DecoderModePtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDecoderMode(
            RFdcInstPtr, Tile_Id, Block_Id, DecoderModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        DecoderMode = DecoderModePtr[0]
        return ret, DecoderMode

    def XRFdc_ResetNCOPhase(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Resets the NCO phase of the current block phase accumulator.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_ResetNCOPhase({Type}, {Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_ResetNCOPhase(RFdcInstPtr, Type, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_DumpRegs(self, inst_id, Type, Tile_Id):
        """
        This Prints the offset of the register along with the content. This API is
        meant to be used for debug purposes. It prints to the console the contents
        of registers for the passed Tile_Id. If -1 is passed, it prints the contents
        of the registers for all the tiles for the respective ADC or DAC

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: None
        """
        self.logger.debug(f"XRFdc_DumpRegs({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        rfdc_handle.XRFdc_DumpRegs(RFdcInstPtr, Type, Tile_Id)
        pass

    def XRFdc_MultiBand(
        self, inst_id, Type, Tile_Id, DigitalDataPathMask, MixerInOutDataType, DataConverterMask
    ):
        """
        User-level API to setup multiband configuration.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param DigitalDataPathMask: DigitalDataPathMask is the DataPath mask. First 4 bits represent
               4 data paths, 1 means enabled and 0 means disabled.
        :param MixerInOutDataType: MixerInOutDataType is mixer data type, valid values are XRFDC_MB_DATATYPE_*
        :param DataConverterMask: DataConverterMask is block enabled mask (input/output driving
              blocks). 1 means enabled and 0 means disabled.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_MultiBand({Type}, {Tile_Id}, {DigitalDataPathMask}, {MixerInOutDataType}, {DataConverterMask} )"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_MultiBand(
            RFdcInstPtr,
            Type,
            Tile_Id,
            DigitalDataPathMask,
            MixerInOutDataType,
            DataConverterMask,
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IntrHandler(self, inst_id, Vector):
        """
        This function is the interrupt handler for the driver.
        It must be connected to an interrupt system by the application such that it
        can be called when an interrupt occurs.

        :param inst_id: Id of the RFDC instance
        :param Vector: Vector is interrupt vector number. Libmetal status handler
            expects two parameters in the handler prototype, hence
            kept this parameter. This is not used inside
            the interrupt handler API.
        :return:
        """
        XRFdcPtr = ffi.new("void *")
        self.logger.debug(f"ret = XRFdc_IntrHandler({Vector}, XRFdcPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IntrHandler(RFdcInstPtr, Vector, XRFdcPtr)
        self.logger.debug(f"The return value is: {ret}")
        return ret, XRFdcPtr

    def XRFdc_IntrClr(self, inst_id, Type, Tile_Id, Block_Id, IntrMask):
        """
        This function clear the interrupts.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param IntrMask: IntrMask contains the interrupts to be cleared.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
        """
        self.logger.debug(f"ret = XRFdc_IntrClr({Type}, {Tile_Id}, {Block_Id}, {IntrMask})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IntrClr(
            RFdcInstPtr, Type, Tile_Id, Block_Id, IntrMask
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetIntrStatus(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This function returns the interrupt status read from Interrupt Status
        Register(ISR).

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
                 IntrSts: the contents of the Interrupt Status Registers (FIFO interface,
                 Decoder interface, Data Path Interface).
        """
        self.logger.debug(
            f"ret = XRFdc_GetIntrStatus({Type}, {Tile_Id}, {Block_Id}, IntrStsPtr)"
        )
        IntrStsPtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetIntrStatus(
            RFdcInstPtr, Type, Tile_Id, Block_Id, IntrStsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        IntrSts = IntrStsPtr[0]
        return ret, IntrSts

    def XRFdc_IntrDisable(self, inst_id, Type, Tile_Id, Block_Id, IntrMask):
        """
        This function clears the interrupt mask.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param IntrMask: IntrMask contains the interrupts to be disabled.
                         '1' disables an interrupt, and '0' remains no change.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
        """
        self.logger.debug(
            f"ret = XRFdc_IntrDisable({Type}, {Tile_Id}, {Block_Id}, {IntrMask})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IntrDisable(
            RFdcInstPtr, Type, Tile_Id, Block_Id, IntrMask
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_IntrEnable(self, inst_id, Type, Tile_Id, Block_Id, IntrMask):
        """
        This function sets the interrupt mask.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param IntrMask: IntrMask contains the interrupts to be enabled.
            '1' enables an interrupt, and '0' disables.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
        """
        self.logger.debug(
            f"ret = XRFdc_IntrEnable({Type}, {Tile_Id}, {Block_Id}, {IntrMask})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_IntrEnable(
            RFdcInstPtr, Type, Tile_Id, Block_Id, IntrMask
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetEnabledInterrupts(self, inst_id, Type, Tile_Id, Block_Id):
        """
        This function gets a mask of enabled interrupts.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
                 IntrMask: mask of enabled interrupts.
           *              '1' denotes an enabled interrupt, and '0' denotes a disabled interrupt
        """
        self.logger.debug(
            f"ret = XRFdc_GetEnabledInterrupts({Type}, {Tile_Id}, {Block_Id}, IntrMask)"
        )
        IntrMask = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetEnabledInterrupts(
            RFdcInstPtr, Type, Tile_Id, Block_Id, IntrMask
        )
        self.logger.debug(f"The return value is: {ret}")
        IntrMask = IntrMask[0]
        return ret, IntrMask

    def XRFdc_SetThresholdClrMode(self, inst_id, Tile_Id, Block_Id, ThresholdToUpdate, ClrMode):
        """
        This API sets the threshold clear mode. The clear mode can be through
        explicit DRP access (manual) or auto clear (QMC gain update event).
        Only ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param ThresholdToUpdate: Select which Threshold (Threshold0 or
                                  Threshold1 or both) to update.
        :param ClrMode: ClrMode can be DRP access (manual) or auto clear (QMC gain
                       update event).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetThresholdClrMode({Tile_Id}, {Block_Id}, {ThresholdToUpdate}, {ClrMode} )"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetThresholdClrMode(
            RFdcInstPtr, Tile_Id, Block_Id, ThresholdToUpdate, ClrMode
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_ThresholdStickyClear(self, inst_id, Tile_Id, Block_Id, ThresholdToUpdate):
        """
        This API is to clear the Sticky bit in threshold config registers.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param ThresholdToUpdate: Select which Threshold (Threshold0 or
                                  Threshold1 or both) to update.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_ThresholdStickyClear({Tile_Id}, {Block_Id}, {ThresholdToUpdate})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_ThresholdStickyClear(
            RFdcInstPtr, Tile_Id, Block_Id, ThresholdToUpdate
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    # TODO
    def XRFdc_SetStatusHandler(self):
        pass

    def XRFdc_SetupFIFO(self, inst_id, Type, Tile_Id, Enable):
        """
        Enable and Disable the ADC/DAC FIFO. For ADCs this is for the actual and
        observation FIFO.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Enable: Enable valid values are 1 (FIFO enable) and 0 (FIFO Disable)
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_SetupFIFO({Type}, {Tile_Id}, {Enable})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetupFIFO(RFdcInstPtr, Type, Tile_Id, Enable)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetupFIFOObs(self, inst_id, Type, Tile_Id, Enable):
        """
        Enable and Disable the ADC/DAC FIFO. 
        For ADCs this is for the observtion FIFO.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_SetupFIFOObs({Type}, {Tile_Id}, {Enable})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetupFIFOObs(RFdcInstPtr, Type, Tile_Id, Enable)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetupFIFOBoth(self, inst_id, Type, Tile_Id, Enable):
        """
        Enable and Disable the ADC/DAC FIFO.
        For ADCs this is for the observtion FIFO.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_SetupFIFOBoth({Type}, {Tile_Id}, {Enable})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetupFIFOBoth(RFdcInstPtr, Type, Tile_Id, Enable)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetFIFOStatus(self, inst_id, Type, Tile_Id):
        """
        Current status of ADC/DAC FIFO. For ADCs this is for both the actual and
        observations FIFOs.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
        """
        self.logger.debug(f"ret = XRFdc_GetFIFOStatus({Type}, {Tile_Id}, EnablePtr)")
        EnablePtr = ffi.new("u8 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFIFOStatus(
            RFdcInstPtr, Type, Tile_Id, EnablePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Enable = EnablePtr[0]
        return ret, Enable

    def XRFdc_GetFIFOStatusObs(self, inst_id, Type, Tile_Id):
        """
        Current status of ADC/DAC FIFO. This is for both the actual and
        observations FIFOs. ADC blocks only

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
        """
        self.logger.debug(f"ret = XRFdc_GetFIFOStatusObs({Type}, {Tile_Id}, EnablePtr)")
        EnablePtr = ffi.new("u8 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFIFOStatusObs(
            RFdcInstPtr, Type, Tile_Id, EnablePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Enable = EnablePtr[0]
        return ret, Enable

    def XRFdc_SetNyquistZone(self, inst_id, Type, Tile_Id, Block_Id, NyquistZone):
        """
        Set the Nyquist zone.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param NyquistZone: valid values are 1 (Odd),2 (Even).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetNyquistZone({Type}, {Tile_Id}, {Block_Id}, {NyquistZone})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetNyquistZone(
            RFdcInstPtr, Type, Tile_Id, Block_Id, NyquistZone
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetNyquistZone(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Get the Nyquist zone.
        Common API for ADC/DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 NyquistZone: returned Nyquist zone
        """
        NyquistZonePtr = ffi.new("u32 *")
        self.logger.debug(
            f"ret = XRFdc_GetNyquistZone({Type}, {Tile_Id}, {Block_Id}, NyquistZonePtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetNyquistZone(
            RFdcInstPtr, Type, Tile_Id, Block_Id, NyquistZonePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        NyquistZone = NyquistZonePtr[0]
        return ret, NyquistZone

    def XRFdc_GetOutputCurr(self, inst_id, Tile_Id, Block_Id):
        """
        Get Output Current for DAC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
                 OutputCurr: Return Output Current for DAC block
        """
        OutputCurrPtr = ffi.new("u32 *")
        self.logger.debug(
            f"ret = XRFdc_GetOutputCurr({Tile_Id}, {Block_Id}, OutputCurrPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetOutputCurr(
            RFdcInstPtr, Tile_Id, Block_Id, OutputCurrPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        OutputCurr = OutputCurrPtr[0]
        return ret, OutputCurr

    def XRFdc_SetDecimationFactor(self, inst_id, Tile_Id, Block_Id, DecimationFactor):
        """
        This API is to set the decimation factor and also update the FIFO write
        words w.r.t to decimation factor.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param DecimationFactor: DecimationFactor to be set for DAC block.
                                 XRFDC_INTERP_DECIM_* defines the valid values.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetDecimationFactor({Tile_Id}, {Block_Id}, {DecimationFactor})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDecimationFactor(
            RFdcInstPtr, Tile_Id, Block_Id, DecimationFactor
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetDecimationFactorObs(self, inst_id, Tile_Id, Block_Id, DecimationFactor):
        """
        This API is to set the decimation factor and also update the FIFO write
        words w.r.t to decimation factor for the observation FIFO.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param DecimationFactor: DecimationFactor to be set for DAC block.
                                 XRFDC_INTERP_DECIM_* defines the valid values.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetDecimationFactorObs({Tile_Id}, {Block_Id}, {DecimationFactor})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDecimationFactorObs(
            RFdcInstPtr, Tile_Id, Block_Id, DecimationFactor
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetInterpolationFactor(self, inst_id, Tile_Id, Block_Id, InterpolationFactor):
        """
        This API is to set the interpolation factor and also update the FIFO read
        words w.r.t to interpolation factor.
        Only DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param InterpolationFactor: InterpolationFactor to be set for DAC block.
                                    XRFDC_INTERP_DECIM_* defines the valid values.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetInterpolationFactor({Tile_Id}, {Block_Id}, {InterpolationFactor})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetInterpolationFactor(
            RFdcInstPtr, Tile_Id, Block_Id, InterpolationFactor
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetFabClkOutDiv(self, inst_id, Type, Tile_Id, FabClkDiv):
        """
        This API is to set the divider for clock fabric out.
        ADC and DAC Tiles

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param FabClkDiv: FabClkDiv to be set for a tile.
                          XRFDC_FAB_CLK_* defines the valid divider values.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_SetFabClkOutDiv({Type}, {Tile_Id}, {FabClkDiv})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetFabClkOutDiv(
            RFdcInstPtr, Type, Tile_Id, FabClkDiv
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetCalibrationMode(self, inst_id, Tile_Id, Block_Id, CalibrationMode):
        """
        This API is to set the Calibration mode.
        Only for ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CalibrationMode: valid values are 1 and 2.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(
            f"ret = XRFdc_SetCalibrationMode({Tile_Id}, {Block_Id}, {CalibrationMode})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetCalibrationMode(
            RFdcInstPtr, Tile_Id, Block_Id, CalibrationMode
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetCalibrationMode(self, inst_id, Tile_Id, Block_Id):
        """
        This API is to get the Calibration mode.
        Only for ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                CalibrationMode: calibration mode
        """
        CalibrationModePtr = ffi.new("u8 *")
        self.logger.debug(
            f"ret = XRFdc_GetCalibrationMode({Tile_Id}, {Block_Id}, CalibrationModePtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetCalibrationMode(
            RFdcInstPtr, Tile_Id, Block_Id, CalibrationModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        CalibrationMode = CalibrationModePtr[0]
        return ret, CalibrationMode

    def XRFdc_GetClockSource(self, inst_id, Type, Tile_Id):
        """
        This function gets Clock source

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                ClockSource:  return the clock source
        """
        self.logger.debug(f"ret = XRFdc_GetClockSource({Type}, {Tile_Id}, ClockSourcePtr)")
        ClockSourcePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetClockSource(
            RFdcInstPtr, Type, Tile_Id, ClockSourcePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        ClockSource = ClockSourcePtr[0]
        return ret, ClockSource

    def XRFdc_GetPLLLockStatus(self, inst_id, Type, Tile_Id):
        """
        This function gets PLL lock status

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                LockStatus:  return the PLL lock status
        """
        self.logger.debug(f"ret = XRFdc_GetPLLLockStatus({Type}, {Tile_Id}, LockStatusPtr)")
        LockStatusPtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetPLLLockStatus(
            RFdcInstPtr, Type, Tile_Id, LockStatusPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        LockStatus = LockStatusPtr[0]
        return ret, LockStatus

    def XRFdc_GetPLLConfig(self, inst_id, Type, Tile_Id):
        """
        This API is used to get the PLL Configurations.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 PLLSettings: dictionary equivalent of XRFdc_PLL_Settings structure to get
                              the PLL configurations
        """
        PLLSettings = ffi.new("XRFdc_PLL_Settings *")
        self.logger.debug(f"ret = XRFdc_GetPLLConfig({Type}, {Tile_Id}, PLLSettings)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetPLLConfig(
            RFdcInstPtr, Type, Tile_Id, PLLSettings
        )
        self.logger.debug(f"The return value is: {ret}")
        PLLSettings = cdata_to_py(PLLSettings[0])
        self.logger.debug(PLLSettings)
        return ret, PLLSettings

    def XRFdc_DynamicPLLConfig(self, inst_id, Type, Tile_Id, Source, RefClkFreq, SamplingRate):
        """
        This function used for dynamically switch between internal PLL and
        external clcok source and configuring the internal PLL
        This API enables automatic selection of the VCO which will work in
        IP version 2.0.1 and above. Using older version of IP this API is
        not likely to work.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Source: Clock source internal PLL or external clock source
        :param RefClkFreq: Reference Clock Frequency in MHz(102.40625MHz - 1.2GHz)
        :param SamplingRate: Sampling Rate in MHz(0.1- 6.554GHz for DAC and
                             0.5/1.0 - 2.058/4.116GHz for ADC based on the device package).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(
            f"ret = XRFdc_DynamicPLLConfig({Type}, {Tile_Id}, {Source}, {RefClkFreq}, {SamplingRate} )"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_DynamicPLLConfig(
            RFdcInstPtr, Type, Tile_Id, Source, RefClkFreq, SamplingRate
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetInvSincFIR(self, inst_id, Tile_Id, Block_Id, Mode):
        """
        This API is used to set the mode for the Inverse-Sinc filter.
        Only DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Mode: Mode valid values are 0(disable),  1(1st Nyquist zone)
                     and 2(2nd Nyquist zone).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled/invalid mode.
        """
        self.logger.debug(f"ret = XRFdc_SetInvSincFIR({Tile_Id}, {Block_Id}, {Mode})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetInvSincFIR(RFdcInstPtr, Tile_Id, Block_Id, Mode)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetInvSincFIR(self, inst_id, Tile_Id, Block_Id):
        """
        This API is used to get the Inverse-Sinc filter mode.
        Only DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Mode: return the inv-sinc status. valid values
                       are 0(disable),  1(1st Nyquist zone) and 2(2nd Nyquist zone).
        """
        ModePtr = ffi.new("u16 *")
        self.logger.debug(f"ret = XRFdc_GetInvSincFIR({Tile_Id}, {Block_Id}, ModePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetInvSincFIR(
            RFdcInstPtr, Tile_Id, Block_Id, ModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Mode = ModePtr[0]
        return ret, Mode

    def XRFdc_GetLinkCoupling(self, inst_id, Tile_Id, Block_Id):
        """
        This function is used to get the Link Coupling mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Mode: return the link coupling mode
        """
        ModePtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetLinkCoupling({Tile_Id}, {Block_Id}, ModePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetLinkCoupling(
            RFdcInstPtr, Tile_Id, Block_Id, ModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Mode = ModePtr[0]
        return ret, Mode

    def XRFdc_GetFabClkOutDiv(self, inst_id, Type, Tile_Id):
        """
        This API is to get the divider for clock fabric out.
        API is applicable for both ADC and DAC Tiles

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 FabClkDiv: fabric clock for a tile. XRFDC_FAB_CLK_* defines the valid divider values.
        """
        self.logger.debug(f"ret = XRFdc_GetFabClkOutDiv({Type}, {Tile_Id}, FabClkDivPtr)")
        FabClkDivPtr = ffi.new("u16 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetFabClkOutDiv(
            RFdcInstPtr, Type, Tile_Id, FabClkDivPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        FabClkDiv = FabClkDivPtr[0]
        return ret, FabClkDiv

    def XRFdc_SetDither(self, inst_id, Tile_Id, Block_Id, Mode):
        """
        This function is used to set the IM3 Dither mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Mode: set the link coupling mode
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(f"ret = XRFdc_SetDither({Tile_Id}, {Block_Id}, {Mode})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDither(RFdcInstPtr, Tile_Id, Block_Id, Mode)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDither(self, inst_id, Tile_Id, Block_Id):
        """
        This function is used to get the IM3 Dither mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                Mode: get link coupling mode
        """
        ModePtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetDither({Tile_Id}, {Block_Id}, ModePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDither(RFdcInstPtr, Tile_Id, Block_Id, ModePtr)
        self.logger.debug(f"The return value is: {ret}")
        Mode = ModePtr[0]
        return ret, Mode

    def XRFdc_SetClkDistribution(self, inst_id, DistributionSettings):
        """
        This function is used to set the clock distribution

        :param inst_id: Id of the RFDC instance
        :param DistributionSettings: distribution settings dictionary
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if could not set distribution
                 DistributionSettings: Dictionary equivalent of XRFdc_Distribution_Settings
        """
        DistributionSettingsPtr = ffi.new(
            "XRFdc_Distribution_Settings *", DistributionSettings
        )
        self.logger.debug(f"ret = XRFdc_SetClkDistribution(DistributionSettingsPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetClkDistribution(
            RFdcInstPtr, DistributionSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        DistributionSettings = cdata_to_py(DistributionSettingsPtr[0])
        self.logger.debug(DistributionSettings)
        return ret, DistributionSettings

    def XRFdc_GetClkDistribution(self, inst_id):
        """
        This function is used to get the clock distribution

        :param inst_id: Id of the RFDC instance
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if no valid distribution found.
                 DistributionSystemSettings: Dictionary equivalent of XRFdc_Distribution_Settings
        """
        DistributionSystemSettingsPtr = ffi.new("XRFdc_Distribution_System_Settings *")
        self.logger.debug(f"ret = XRFdc_GetClkDistribution(XRFdc_Distribution_System_Settings)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetClkDistribution(
            RFdcInstPtr, DistributionSystemSettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        DistributionSystemSettings = cdata_to_py(DistributionSystemSettingsPtr[0])
        self.logger.debug(f"DistributionSystemSettings = {json.dumps(DistributionSystemSettings, indent=2)}")
        return ret, DistributionSystemSettings

    def XRFdc_SetDataPathMode(self, inst_id, Tile_Id, Block_Id, Mode):
        """
        This API is to set the DAC Datapath mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Mode: Mode valid values are 0-3.
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / out of range.
        """
        self.logger.debug(f"ret = XRFdc_SetDataPathMode({Tile_Id}, {Block_Id}, {Mode})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDataPathMode(
            RFdcInstPtr, Tile_Id, Block_Id, Mode
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDataPathMode(self, inst_id, Tile_Id, Block_Id):
        """
        This API is to get the DAC Datapath mode.
        This is only for DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Mode: valid values are 0-3
        """
        ModePtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetDataPathMode({Tile_Id}, {Block_Id}, ModePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDataPathMode(
            RFdcInstPtr, Tile_Id, Block_Id, ModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Mode = ModePtr[0]
        return ret, Mode

    def XRFdc_SetIMRPassMode(self, inst_id, Tile_Id, Block_Id, Mode):
        """
        This API is to set the DAC Image Reject Filter Pass mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Mode: valid values are 0 (for low pass) 1 (for high pass).
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / bad parameter passed
        """
        self.logger.debug(f"ret = XRFdc_SetIMRPassMode({Tile_Id}, {Block_Id}, {Mode})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetIMRPassMode(
            RFdcInstPtr, Tile_Id, Block_Id, Mode
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetIMRPassMode(self, inst_id, Tile_Id, Block_Id):
        """
        This API is to get the DAC Image Reject Filter Pass mode.
        This is only for DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Mode: 0 (for low pass) 1 (for high pass)
        """
        ModePtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetIMRPassMode({Tile_Id}, {Block_Id}, ModePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetIMRPassMode(
            RFdcInstPtr, Tile_Id, Block_Id, ModePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Mode = ModePtr[0]
        return ret, Mode

    def XRFdc_SetSignalDetector(self, inst_id, Tile_Id, Block_Id, Settings):
        """
        This function is used to set the ADC Signal Detector Settings.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Settings: signal detector configurations dictionary
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled, or invalid values.
                 Settings: dictionary equivalent of XRFdc_Signal_Detector_Settings structure
        """
        SettingsPtr = ffi.new("XRFdc_Signal_Detector_Settings *", Settings)
        self.logger.debug(
            f"ret = XRFdc_SetSignalDetector({Tile_Id}, {Block_Id}, SettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetSignalDetector(
            RFdcInstPtr, Tile_Id, Block_Id, SettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_GetSignalDetector(self, inst_id, Tile_Id, Block_Id):
        """
        This function is used to get the ADC Signal Detector Settings.
        This is only for DAC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Settings: dictionary equivalent of XRFdc_Signal_Detector_Settings structure
        """
        SettingsPtr = ffi.new("XRFdc_Signal_Detector_Settings *")
        self.logger.debug(
            f"ret = XRFdc_GetSignalDetector({Tile_Id}, {Block_Id}, SettingsPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetSignalDetector(
            RFdcInstPtr, Tile_Id, Block_Id, SettingsPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_DisableCoefficientsOverride(self, inst_id, Tile_Id, Block_Id, CalibrationBlock):
        """
        This function is used to disable Calibration Coefficients override.
        Only for ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CalibrationBlock: indicates the calibration block
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(
            f"ret = XRFdc_DisableCoefficientsOverride({Tile_Id}, {Block_Id}, {CalibrationBlock})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_DisableCoefficientsOverride(
            RFdcInstPtr, Tile_Id, Block_Id, CalibrationBlock
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetCalCoefficients(self, inst_id, Tile_Id, Block_Id, CalibrationBlock, Coeff):
        """
        This function is used to set the ADC Calibration Coefficients.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CalibrationBlock: indicates the block to be written to
        :param Coeff: dictionary to the XRFdc_Calibration_Coefficients structure to set the calibration coefficients
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients
        """
        CoeffPtr = ffi.new("XRFdc_Calibration_Coefficients *", Coeff)
        self.logger.debug(
            f"ret = XRFdc_SetCalCoefficients({Tile_Id}, {Block_Id}, {CalibrationBlock}, CoeffPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetCalCoefficients(
            RFdcInstPtr, Tile_Id, Block_Id, CalibrationBlock, CoeffPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Coeff = cdata_to_py(CoeffPtr[0])
        self.logger.debug(Coeff)
        return ret, Coeff

    def XRFdc_GetCalCoefficients(self, inst_id, Tile_Id, Block_Id, CalibrationBlock):
        """
        This function is used to get the ADC Calibration Coefficients.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CalibrationBlock: indicates the block to be read from
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients
        """
        CoeffPtr = ffi.new("XRFdc_Calibration_Coefficients *")
        self.logger.debug(
            f"ret = XRFdc_GetCalCoefficients({Tile_Id}, {Block_Id}, {CalibrationBlock}, CoeffPtr)"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetCalCoefficients(
            RFdcInstPtr, Tile_Id, Block_Id, CalibrationBlock, CoeffPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Coeff = cdata_to_py(CoeffPtr[0])
        self.logger.debug(Coeff)
        return ret, Coeff

    def XRFdc_SetCalFreeze(self, inst_id, Tile_Id, Block_Id, CalFreeze):
        """
        This function is used to set calibration freeze settings.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure
        """
        CalFreezePtr = ffi.new("XRFdc_Cal_Freeze_Settings *", CalFreeze)
        self.logger.debug(f"ret = XRFdc_SetCalFreeze({Tile_Id}, {Block_Id}, CalFreezePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetCalFreeze(
            RFdcInstPtr, Tile_Id, Block_Id, CalFreezePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        CalFreeze = cdata_to_py(CalFreezePtr[0])
        self.logger.debug(CalFreeze)
        return ret, CalFreeze

    def XRFdc_GetCalFreeze(self, inst_id, Tile_Id, Block_Id):
        """
        This function is used to get calibration freeze settings and status.
        Only for ADC blocks

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure
        """
        CalFreezePtr = ffi.new("XRFdc_Cal_Freeze_Settings *")
        self.logger.debug(f"ret = XRFdc_GetCalFreeze({Tile_Id}, {Block_Id}, CalFreezePtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetCalFreeze(
            RFdcInstPtr, Tile_Id, Block_Id, CalFreezePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        CalFreeze = cdata_to_py(CalFreezePtr[0])
        self.logger.debug(CalFreeze)
        return ret, CalFreeze

    def XRFdc_SetDACVOP(self, inst_id, Tile_Id, Block_Id, uACurrent):
        """
        Set Output Current for DAC block.
        Range 6425 - 32000 uA with 25 uA resolution.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param uACurrent: the current in uA.
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(f"ret = XRFdc_SetDACVOP({Tile_Id}, {Block_Id}, {uACurrent})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDACVOP(
            RFdcInstPtr, Tile_Id, Block_Id, uACurrent
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_SetDACCompMode(self, inst_id, Tile_Id, Block_Id, Enable):
        """
        Gets VOP compatibility mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Enable:  filled with whether the mode is enabled (1) or disabled(0).
        :return: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(f"ret = XRFdc_SetDACCompMode({Tile_Id}, {Block_Id}, {Enable})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDACCompMode(
            RFdcInstPtr, Tile_Id, Block_Id, Enable
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDACCompMode(self, inst_id, Tile_Id, Block_Id):
        """
        Gets VOP compatibility mode.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Enabled: filled with whether the mode is enabled (1) or disabled(0).
        """
        EnabledPtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetDACCompMode({Tile_Id}, {Block_Id}, EnabledPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDACCompMode(
            RFdcInstPtr, Tile_Id, Block_Id, EnabledPtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Enabled = EnabledPtr[0]
        return ret, Enabled

    def XRFdc_SetDSA(self, inst_id, Tile_Id, Block_Id, Settings):
        """
        Set DSA for ADC block.
        Range 0 - 11 dB with 0.5 dB resolution ES1 Si.
        Range 0 - 27 dB with 1 dB resolution for Production Si.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Settings:
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Settings: Dictionary equivalent of XRFdc_DSA_Settings
        """
        SettingsPtr = ffi.new("XRFdc_DSA_Settings *", Settings)
        self.logger.debug(f"ret = XRFdc_SetDSA({Tile_Id}, {Block_Id}, SettingsPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDSA(RFdcInstPtr, Tile_Id, Block_Id, SettingsPtr)
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_GetDSA(self, inst_id, Tile_Id, Block_Id):
        """
        Get DSA for ADC block.

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Settings: Dictionary equivalent of XRFdc_DSA_Settings
        """
        SettingsPtr = ffi.new("XRFdc_DSA_Settings *")
        self.logger.debug(f"ret = XRFdc_GetDSA({Tile_Id}, {Block_Id}, SettingsPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDSA(RFdcInstPtr, Tile_Id, Block_Id, SettingsPtr)
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_SetPwrMode(self, inst_id, Type, Tile_Id, Block_Id, Settings):
        """
        Set The Power up/down mode of a given converter.

        :param inst_id: Id of the RFDC instance
        :param Type: ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Settings: Dictionary equivalent of XRFdc_DSA_Settings
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Settings: Dictionary equivalent of XRFdc_DSA_Settings
        """
        SettingsPtr = ffi.new("XRFdc_Pwr_Mode_Settings *")
        self.logger.debug(f"ret = XRFdc_SetPwrMode({Type}, {Tile_Id}, {Block_Id}, SettingsPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetPwrMode(RFdcInstPtr, Type, Tile_Id, Block_Id, SettingsPtr)
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_GetPwrMode(self, inst_id, Type, Tile_Id, Block_Id, Settings):
        """
        Get The Power up/down mode of a given converter.

        :param inst_id: Id of the RFDC instance
        :param Type: ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3.
        :param Settings: Dictionary equivalent of XRFdc_Pwr_Mode_Settings
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Settings: Dictionary equivalent of XRFdc_Pwr_Mode_Settings
        """
        SettingsPtr = ffi.new("XRFdc_Pwr_Mode_Settings *")
        self.logger.debug(f"ret = XRFdc_GetPwrMode({Type}, {Tile_Id}, {Block_Id}, SettingsPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetPwrMode(RFdcInstPtr, Type, Tile_Id, Block_Id, SettingsPtr)
        self.logger.debug(f"The return value is: {ret}")
        Settings = cdata_to_py(SettingsPtr[0])
        self.logger.debug(Settings)
        return ret, Settings

    def XRFdc_ResetInternalFIFOWidth(self, inst_id, Type, Tile_Id, Block_Id):
        """
        Set the correct FIFO width for current mixer & rate change settings.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Tile_Id Valid values are 0-3
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                      Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(
            f"ret = XRFdc_ResetInternalFIFOWidth({Type}, {Tile_Id}, {Block_Id})"
        )
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_ResetInternalFIFOWidth(
            RFdcInstPtr, Type, Tile_Id, Block_Id
        )
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_ResetInternalFIFOWidthObs(self, inst_id, Tile_Id, Block_Id):
        """
        Set the correct Observation FIFO width for current mixer & rate change settings.
        ADC blocks only

        :param inst_id: Id of the RFDC instance
        :param Tile_Id: Tile_Id Valid values are 0-3.
        :param Block_Id: Block_Id is ADC/DAC block number inside the tile.
                         Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
        """
        self.logger.debug(f"ret = XRFdc_ResetInternalFIFOWidthObs({Tile_Id}, {Block_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_ResetInternalFIFOWidthObs(RFdcInstPtr, Tile_Id, Block_Id)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_MultiConverter_Sync(self, inst_id, Type, Config):
        """
        This is the top level API which will be used for Multi-tile
        Synchronization.

        :param inst_id: Id of the RFDC instance
        :param Type: ADC or DAC. 0 for ADC and 1 for DAC
        :param Config: Multi-tile sync config.
        :return: ret - XRFDC_MTS_OK if successful.
                     - XRFDC_MTS_TIMEOUT if timeout occurs.
                     - XRFDC_MTS_MARKER_RUN
                     - XRFDC_MTS_MARKER_MISM
                     - XRFDC_MTS_NOT_SUPPORTED if MTS is not supported.
                Config: Multi-tile sync config.
        """
        ConfigPtr = ffi.new("XRFdc_MultiConverter_Sync_Config *", Config)
        self.logger.debug(f"ret, Config = XRFdc_MultiConverter_Sync({Type}, ConfigPtr)")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_MultiConverter_Sync(RFdcInstPtr, Type, ConfigPtr)
        self.logger.debug(f"The return value ret is: {ret}")
        Config = cdata_to_py(ConfigPtr[0])
        self.logger.debug(f"The return value Config is: {Config}")
        return ret, Config

    def XRFdc_MultiConverter_Init(self, Config, PLL_Codes, T1_Codes, RefTile):
        """
        This API Initializes the multi-tile sync config structures.
        Optionally allows target codes to be provided for the Pll/T1
        analog sysref capture

        :param Config: Multi-tile sync config
        :param PLL_Codes: PLL analog sysref capture.
        :param T1_Codes: T1 analog sysref capture.
        :param RefTile: tile ID of the reference tile.
        :return: Config: Multi-tile sync config
                 PLL_Codes: PLL analog sysref capture.
                 T1_Codes: T1 analog sysref capture.
        """
        ConfigPtr = ffi.new("XRFdc_MultiConverter_Sync_Config *", Config)
        if None == PLL_Codes:
            PLL_CodesPtr = ffi.NULL
        else:
            PLL_CodesPtr = ffi.new("int [4]", PLL_Codes)
        if None == T1_Codes:
            T1_CodesPtr = ffi.NULL
        else:
            T1_CodesPtr = ffi.new("int [4]", T1_Codes)
        self.logger.debug(
            f"ret = XRFdc_MultiConverter_Init(Config,{ PLL_Codes}, {T1_Codes},{RefTile})"
        )
        self.logger.debug(f"The input value Config is: {Config}")
        rfdc_handle.XRFdc_MultiConverter_Init(ConfigPtr, PLL_CodesPtr, T1_CodesPtr, RefTile)
        Config = cdata_to_py(ConfigPtr[0])
        self.logger.debug(f"The return value Config is: {Config}")
        if None != PLL_Codes:
            PLL_Codes = cptr_to_pylist(PLL_CodesPtr, 4)
        if None != T1_Codes:
            T1_Codes = cptr_to_pylist(T1_CodesPtr, 4)
        self.logger.debug(f"The return value PLL_Codes is: {PLL_Codes}")
        self.logger.debug(f"The return value T1_Codes is: {T1_Codes}")
        return Config, PLL_Codes, T1_Codes

    def XRFdc_MTS_Sysref_Config(self, inst_id, DACSyncConfig, ADCSyncConfig, SysRefEnable):
        """
        This API is used to enable/disable the sysref.

        :param inst_id: Id of the RFDC instance
        :param DACSyncConfig - DAC Multi-Tile Sync config.
        :param ADCSyncConfig - ADC Multi-Tile Sync config structure
        :param SysRefEnable - valid values are 0(disable) and 1(enable)
        :return: ret: XRFDC_MTS_OK if successful.
        """
        DACSyncConfigPtr = ffi.new("XRFdc_MultiConverter_Sync_Config *", DACSyncConfig)
        ADCSyncConfigPtr = ffi.new("XRFdc_MultiConverter_Sync_Config *", ADCSyncConfig)
        self.logger.debug(
            f"ret = XRFdc_MTS_Sysref_Config(DACSyncConfigPtr, ADCSyncConfigPtr, {SysRefEnable})"
        )
        self.logger.debug(f"The input value DACSyncConfig is: {DACSyncConfig}")
        self.logger.debug(f"The input value ADCSyncConfig is: {ADCSyncConfig}")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_MTS_Sysref_Config(
            RFdcInstPtr, DACSyncConfigPtr, ADCSyncConfigPtr, SysRefEnable
        )
        DACSyncConfig = cdata_to_py(DACSyncConfigPtr[0])
        ADCSyncConfig = cdata_to_py(ADCSyncConfigPtr[0])
        self.logger.debug(f"The return value DACSyncConfig is: {DACSyncConfig}")
        self.logger.debug(f"The return value ADCSyncConfig is: {ADCSyncConfig}")
        return ret, DACSyncConfig, ADCSyncConfig

    def XRFdc_GetMTSEnable(self, inst_id, Type, Tile_Id):
        """
        This API is used to enable/disable the sysref.

        :param inst_id: Id of the RFDC instance
        :param Type - ADC or DAC. 0 for ADC and 1 for DAC.
        :param Tile_Id - indicates Tile number (0-3).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_SUCCESS if error occurs.
                 Enable: valid values are 1 (enable) and 0 (disable).
        """
        EnablePtr = ffi.new("u32 *")
        self.logger.debug(f"ret = XRFdc_GetMTSEnable({Type}, {Tile_Id})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetMTSEnable(RFdcInstPtr, Type, Tile_Id, EnablePtr)
        self.logger.debug(f"The return value ret is: {ret}")
        Enable = EnablePtr[0]
        self.logger.debug(f"The return value ret is: {ret}")
        self.logger.debug(f"The return value Enable is: {Enable}")
        return ret, Enable

    def XRFdc_SetDACDataScaler(self, inst_id, Type, Tile_Id, Enable):
        """
        Set data scaler for DAC block.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :param Enable: valid values are 1 (enable) and 0 (disable).
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
        """
        self.logger.debug(f"ret = XRFdc_SetDACDataScaler({Type}, {Tile_Id}, {Enable})")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_SetDACDataScaler(RFdcInstPtr, Type, Tile_Id, Enable)
        self.logger.debug(f"The return value is: {ret}")
        return ret

    def XRFdc_GetDACDataScaler(self, inst_id, Type, Tile_Id):
        """
        Get data scaler for DAC block.

        :param inst_id: Id of the RFDC instance
        :param Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
        :param Tile_Id: Valid values are 0-3
        :return: ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
                 Enable:  valid values are 1 (enable) and 0 (disable).
        """
        self.logger.debug(f"ret = XRFdc_GetDACDataScaler({Type}, {Tile_Id}, EnablePtr)")
        EnablePtr = ffi.new("u32 *")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        ret = rfdc_handle.XRFdc_GetDACDataScaler(
            RFdcInstPtr, Type, Tile_Id, EnablePtr
        )
        self.logger.debug(f"The return value is: {ret}")
        Enable = EnablePtr[0]
        return ret, Enable

    def XRFdc_GetTileLayout(self, inst_id):
        """
        Gets whether the device is a DFE variant or not

        :param inst_id - integer handle to the initialized instance
        :return: tile_layout - XRFDC_3ADC_2DAC_TILES if DFE variant.
                             - XRFDC_4ADC_4DAC_TILES if regular Gen 1/2/3.
        """
        self.logger.debug(f"tile_layout = XRFdc_GetTileLayout()")
        RFdcInstPtr = self.rfdc_inst_dict[inst_id][1]
        tile_layout = rfdc_handle.XRFdc_GetTileLayout(RFdcInstPtr)
        self.logger.debug(f"The return value tile_layout is: {tile_layout}")
        return tile_layout

    def __del__(self):
        self.logger.info("Inside RFDC Destructor")
