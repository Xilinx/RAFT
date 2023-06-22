# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
import json
from utils import ffi, open_c_library, cdata_to_py
from utils import extract_b64_encoded_string, cdata_string_to_py, xhelper_handle
from utils import get_python_log_levels, getkey_from_listbeginvalue


ofdm_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/dfe/xdfeofdm_python.h", "/usr/lib/libdfeofdm.so.1")


class OFDM(object):
    ofdm_dict = {}
    device_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error("OFDM: XHelper_MetalInit failed. ret = ", ret)
        self.logger.info("Inside OFDM Constructor")
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
        self.logger.debug(f"MetalLogLevel = {MetalLogLevel}")
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

    # Get enum API
    def GetEnum_XDfeOfdm_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeOfdm_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeOfdm_StateId
        """
        XDfeOfdm_StateId = ffi.typeof("enum XDfeOfdm_StateId").relements
        self.logger.debug(f"XDfeOfdm_StateId = {json.dumps(XDfeOfdm_StateId, indent=2)}")
        return XDfeOfdm_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        metal_log_level = ffi.typeof("enum metal_log_level").relements
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    # Get structure  API
    def GetStruct_XDfeOfdm_Version(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Version
        """
        XDfeOfdm_Version_ptr = ffi.new("XDfeOfdm_Version *")
        XDfeOfdm_Version = cdata_to_py(XDfeOfdm_Version_ptr[0])
        return XDfeOfdm_Version

    def GetStruct_XDfeOfdm_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Trigger
        """
        XDfeOfdm_Trigger_ptr = ffi.new("XDfeOfdm_Trigger *")
        XDfeOfdm_Trigger = cdata_to_py(XDfeOfdm_Trigger_ptr[0])
        return XDfeOfdm_Trigger

    def GetStruct_XDfeOfdm_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_TriggerCfg
        """
        XDfeOfdm_TriggerCfg_ptr = ffi.new("XDfeOfdm_TriggerCfg *")
        XDfeOfdm_TriggerCfg = cdata_to_py(XDfeOfdm_TriggerCfg_ptr[0])
        return XDfeOfdm_TriggerCfg

    def GetStruct_XDfeOfdm_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CCSequence
        """
        XDfeOfdm_CCSequence_ptr = ffi.new("XDfeOfdm_CCSequence *")
        XDfeOfdm_CCSequence = cdata_to_py(XDfeOfdm_CCSequence_ptr[0])
        return XDfeOfdm_CCSequence

    def GetStruct_XDfeOfdm_FTSequence(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_FTSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_FTSequence
        """
        XDfeOfdm_FTSequence_ptr = ffi.new("XDfeOfdm_FTSequence *")
        XDfeOfdm_FTSequence = cdata_to_py(XDfeOfdm_FTSequence_ptr[0])
        return XDfeOfdm_FTSequence

    def GetStruct_XDfeOfdm_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_ModelParameters
        """
        XDfeOfdm_ModelParameters_ptr = ffi.new("XDfeOfdm_ModelParameters *")
        XDfeOfdm_ModelParameters = cdata_to_py(XDfeOfdm_ModelParameters_ptr[0])
        return XDfeOfdm_ModelParameters

    def GetStruct_XDfeOfdm_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Cfg
        """
        XDfeOfdm_Cfg_ptr = ffi.new("XDfeOfdm_Cfg *")
        XDfeOfdm_Cfg = cdata_to_py(XDfeOfdm_Cfg_ptr[0])
        return XDfeOfdm_Cfg

    def GetStruct_XDfeOfdm_Init(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Init

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Init
        """
        XDfeOfdm_Init_ptr = ffi.new("XDfeOfdm_Init *")
        XDfeOfdm_Init = cdata_to_py(XDfeOfdm_Init_ptr[0])
        return XDfeOfdm_Init

    def GetStruct_XDfeOfdm_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CarrierCfg
        """
        XDfeOfdm_CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *")
        XDfeOfdm_CarrierCfg = cdata_to_py(XDfeOfdm_CarrierCfg_ptr[0])
        return XDfeOfdm_CarrierCfg

    def GetStruct_XDfeOfdm_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_AntennaCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_AntennaCfg
        """
        XDfeOfdm_AntennaCfg_ptr = ffi.new("XDfeOfdm_AntennaCfg *")
        XDfeOfdm_AntennaCfg = cdata_to_py(XDfeOfdm_AntennaCfg_ptr[0])
        return XDfeOfdm_AntennaCfg

    def GetStruct_XDfeOfdm_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CCCfg
        """
        XDfeOfdm_CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *")
        XDfeOfdm_CCCfg = cdata_to_py(XDfeOfdm_CCCfg_ptr[0])
        return XDfeOfdm_CCCfg

    def GetStruct_XDfeOfdm_Status(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Status
        """
        XDfeOfdm_Status_ptr = ffi.new("XDfeOfdm_Status *")
        XDfeOfdm_Status = cdata_to_py(XDfeOfdm_Status_ptr[0])
        return XDfeOfdm_Status

    def GetStruct_XDfeOfdm_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_InterruptMask
        """
        XDfeOfdm_InterruptMask_ptr = ffi.new("XDfeOfdm_InterruptMask *")
        XDfeOfdm_InterruptMask = cdata_to_py(XDfeOfdm_InterruptMask_ptr[0])
        return XDfeOfdm_InterruptMask

    def GetStruct_XDfeOfdm_Config(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Config
        """
        XDfeOfdm_Config_ptr = ffi.new("XDfeOfdm_Config *")
        XDfeOfdm_Config = cdata_to_py(XDfeOfdm_Config_ptr[0])
        return XDfeOfdm_Config

    def GetStruct_XDfeOfdm_InternalCarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_InternalCarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_InternalCarrierCfg
        """
        XDfeOfdm_InternalCarrierCfg_ptr = ffi.new("XDfeOfdm_InternalCarrierCfg *")
        XDfeOfdm_InternalCarrierCfg = cdata_to_py(XDfeOfdm_InternalCarrierCfg_ptr[0])
        return XDfeOfdm_InternalCarrierCfg

    def GetStruct_XDfeOfdm(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm
        """
        XDfeOfdm_ptr = ffi.new("XDfeOfdm *")
        XDfeOfdm = cdata_to_py(XDfeOfdm_ptr[0])
        return XDfeOfdm

    # System initialization API
    def XDfeOfdm_InstanceInit(self, DeviceNodeName):
        """
        API initialises one instance of a channel filter driver.
        Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
        OFDM device with the name DeviceNodeName. The first available slot in
        the instances array XDfeOfdm_ChFilter[] will be taken as a DeviceNodeName
        object.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to the initialized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value

        """
        DeviceNodeName = extract_b64_encoded_string(DeviceNodeName)
        cptrDeviceNodeName = ffi.new("char[128]", DeviceNodeName)
        self.logger.info(f"XDfeOfdm_InstanceInit({DeviceNodeName})")
        # Pass the device node name to the driver
        xofdm = ofdm_handle.XDfeOfdm_InstanceInit(cptrDeviceNodeName)
        DeviceNodeNameRet = cdata_string_to_py(cptrDeviceNodeName);
        if xofdm == ffi.NULL:
            # if driver returns NULL, pass it as error to user
            ret = 1
            self.logger.error(f"The pointer returned for {DeviceNodeName} is NULL")
            device_id = 0xFFFFFFFF
        else:
            # otherwise treat as success
            ret = 0
            # In ofdm_dict dictionary, device id is the key.
            # device node name and instance pointer from driver are values as list
            # check if the device node name is already present in dictionary
            found, device_id = getkey_from_listbeginvalue(self.ofdm_dict, DeviceNodeName)
            if 1 == found:
                # if found, update the device id key with values
                self.ofdm_dict[device_id][0] = DeviceNodeNameRet
                self.ofdm_dict[device_id][1] = xofdm
            else:
                # if not found, make new device_id from class variable
                # and increment the class variable
                device_id = self.device_id
                self.device_id += 1
                # add new key and values to the dictionary
                self.ofdm_dict[device_id] = [DeviceNodeNameRet, xofdm]
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeNameRet = {DeviceNodeNameRet}")
        return ret, device_id, DeviceNodeNameRet

    def XDfeOfdm_InstanceClose(self, device_id):
        """
        API closes the instances of a Ofdm driver.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeOfdm_InstanceClose({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_InstanceClose(xofdm)
        if device_id in self.ofdm_dict:
            del self.ofdm_dict[device_id]
        return

    # Register access API
    def XDfeOfdm_WriteReg(self, device_id, addr_offset, data):
        """
        Writes value to register in a Ofdm instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address.
        :param Data: value to be written.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_WriteReg({device_id}, {addr_offset}, {data})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_WriteReg(xofdm, addr_offset, data)
        return

    def XDfeOfdm_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from register using a Ofdm instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address
        :return: regval: Register value.
        """
        self.logger.debug(f"XDfeOfdm_ReadReg({device_id}, {addr_offset})")
        xofdm = self.ofdm_dict[device_id][1]
        regval = ofdm_handle.XDfeOfdm_ReadReg(xofdm, addr_offset)
        self.logger.debug(f"regval = {regval}")
        return regval

    # DFE ChFilter component initialization API
    def XDfeOfdm_Reset(self, device_id):
        """
        The function puts block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_Reset({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_Reset(xofdm)
        return

    def XDfeOfdm_Configure(self, device_id, Cfg):
        """
        Read configuration from device tree/xparameters.h and IP registers.
        S/W reset removed.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container
        :return: Cfg: configuration data container
        """
        Cfg_ptr = ffi.new("XDfeOfdm_Cfg *", Cfg)
        self.logger.debug(f"XDfeOfdm_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_Configure(xofdm, Cfg_ptr)
        Cfg = cdata_to_py(Cfg_ptr[0])
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeOfdm_Initialize(self, device_id, Init):
        """
        DFE Ofdm driver one time initialisation.

        :param device_id: id of the opened device.
        :param Init: initialisation data container
        :return: Init: initialisation data container
        """
        Init_ptr = ffi.new("XDfeOfdm_Init *", Init)
        self.logger.debug(f"XDfeOfdm_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_Initialize(xofdm, Init_ptr)
        Init = cdata_to_py(Init_ptr[0])
        self.logger.debug(f"Init = {json.dumps(Init, indent=2)}")
        return Init

    def XDfeOfdm_Activate(self, device_id, EnableLowPower):
        """
        Activates channel filter.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_Activate({device_id}, {EnableLowPower})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_Activate(xofdm, EnableLowPower)
        return

    def XDfeOfdm_Deactivate(self, device_id):
        """
        DeActivate ofdm.
        Note: Writting to ACTIVATE reg.toggles between "initialized" and "operational".

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_Deactivate({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_Deactivate(xofdm)
        return

    def XDfeOfdm_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeOfdm_GetStateID({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        StateId = ofdm_handle.XDfeOfdm_GetStateID(xofdm)
        StateId_edict = ffi.typeof("XDfeOfdm_StateId").elements
        self.logger.debug(f"Return value = {json.dumps(StateId, indent=2)}")
        return StateId_edict[StateId]

    def XDfeOfdm_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeOfdm_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CurrCCCfg)
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetCurrentCCCfg(xofdm, CurrCCCfg_ptr)
        CurrCCCfg = cdata_to_py(CurrCCCfg_ptr[0])
        self.logger.debug(f"CurrCCCfg = {json.dumps(CurrCCCfg, indent=2)}")
        return CurrCCCfg

    def XDfeOfdm_GetEmptyCCCfg(self, device_id):
        """
        Returns the empty CC configuration.

        :param device_id: id of the opened device.
        :return: CCCfg: CC configuration container
        """
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *")
        self.logger.debug(f"XDfeOfdm_GetEmptyCCCfg({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetEmptyCCCfg(xofdm, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeOfdm_GetCarrierCfg(self, device_id, CCCfg, CCID):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: CC ID.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
        """
        self.logger.debug(f"XDfeOfdm_GetCarrierCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        CCSeqBitmap_ptr = ffi.new("u32 *")
        CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *")
        ofdm_handle.XDfeOfdm_GetCarrierCfg(xofdm, CCCfg_ptr, CCID, CCSeqBitmap_ptr, CarrierCfg_ptr)
        CCSeqBitmap = CCSeqBitmap_ptr[0]
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}")
        return CCSeqBitmap, CarrierCfg

    def XDfeOfdm_AddCCtoCCCfg(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: CC ID.
        :param CCSeqBitmap: CC slot position container.
        :param CarrierCfg: CC configuration container.
        :param FTSeq: FTSeq container.
        :return: ret: 0 if successful, 1 on error.
                 CCCfg: component carrier (CC) configuration container.
                 FTSeq: FTSeq container.
        """
        self.logger.debug(f"XDfeOfdm_AddCCtoCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {CCSeqBitmap}, {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *", CarrierCfg)
        FTSeq_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        ret = ofdm_handle.XDfeOfdm_AddCCtoCCCfg(xofdm, CCCfg_ptr, CCID, CCSeqBitmap,
                                                CarrierCfg_ptr, FTSeq_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        FTSeq = cdata_to_py(FTSeq_ptr[0])
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)}")
        return ret, CCCfg, FTSeq

    def XDfeOfdm_RemoveCCfromCCCfg(self, device_id, CCCfg, CCID, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: CC ID.
        :param FTSeq: FTSeq container.
        :return: ret: 0 on success and 1 on failure
                 CCCfg: component carrier (CC) configuration container.
                 FTSeq: FTSeq container.
        """
        self.logger.debug(f"XDfeOfdm_RemoveCCfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {CCID}), "
                          f"{json.dumps(FTSeq, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        FTSeq_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        ret = ofdm_handle.XDfeOfdm_RemoveCCfromCCCfg(xofdm, CCCfg_ptr, CCID, FTSeq_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        FTSeq = cdata_to_py(FTSeq_ptr[0])
        self.logger.debug(f"ret = {ret}, Return value = {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)}")
        return ret, CCCfg, FTSeq

    def XDfeOfdm_UpdateCCinCCCfg(self, device_id, CCCfg, CCID, CarrierCfg, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: CC ID.
        :param CarrierCfg: CC configuration container.
        :param FTSeq: FTSeq container.
        :return: ret: 0 on success and 1 on failure
                 CCCfg: component carrier (CC) configuration container.
                 FTSeq: FTSeq container.
        """
        self.logger.debug(f"XDfeOfdm_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {json.dumps(CarrierCfg, indent=2)}), "
                          f"{json.dumps(FTSeq, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *", CarrierCfg)
        FTSeq_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        ret = ofdm_handle.XDfeOfdm_UpdateCCinCCCfg(xofdm, CCCfg_ptr, CCID, CarrierCfg_ptr, FTSeq_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        FTSeq = cdata_to_py(FTSeq_ptr[0])
        self.logger.debug(f"ret = {ret}, Return value = {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)}")
        return ret, CCCfg, FTSeq

    def XDfeOfdm_SetNextCCCfg(self, device_id, CCCfg):
        """
        Sets the next CC configuration.

        :param device_id: id of the opened device.
        :return: ret: 0 if successful, 1 on error.
                 NextCCCfg: Next CC configuration container.
        """
        self.logger.debug(f"XDfeOfdm_SetNextCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        ofdm_handle.XDfeOfdm_SetNextCCCfg(xofdm, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeOfdm_EnableCCUpdateTrigger(self, device_id):
        """
        Reads the Triggers and sets enable bit of update trigger. If
        Mode = IMMEDIATE, then trigger will be applied immediately.

        :param device_id: id of the opened device.
        :return: ret: 0 if successful, 1 on error.
        """
        self.logger.debug(f"XDfeOfdm_EnableCCUpdateTrigger({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ret = ofdm_handle.XDfeOfdm_EnableCCUpdateTrigger(xofdm)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeOfdm_SetNextCCCfgAndTrigger(self, device_id, CCCfg):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :return: ret: 0 if successful, 1 on error.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeOfdm_SetNextCCCfgAndTrigger({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeOfdm_CCCfg *", CCCfg)
        ret = ofdm_handle.XDfeOfdm_SetNextCCCfgAndTrigger(xofdm, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CCCfg = {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeOfdm_AddCC(self, device_id, CCID, CCSeqBitmap, CarrierCfg, FTSeq):
        """
        Adds specified CCID, with specified configuration.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCID: CC ID.
        :param CCSeqBitmap: up to 16 defined slots into which a CC can be
               allocated. The number of slots can be from 1 to 16 depending on
               system initialization. The number of slots is defined by the
               "sequence length" parameter which is provided during initialization.
               The Bit offset within the CCSeqBitmap indicates the equivalent
               Slot number to allocate. e.g. 0x0003  means the caller wants the
               passed component carrier (CC) to be allocated to slots 0 and 1.
        :param CarrierCfg: is a CC configuration container.
        :param FTSeq: FTSeq container.
        :return: ret: 0 if successful, 1 on error.
        """
        self.logger.debug(f"XDfeOfdm_AddCC({device_id}, {CCID}, {CCSeqBitmap}, "
                          f"{json.dumps(CarrierCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)})")
        CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *", CarrierCfg)
        FTSequence_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        xofdm = self.ofdm_dict[device_id][1]
        ret = ofdm_handle.XDfeOfdm_AddCC(xofdm, CCID, CCSeqBitmap, CarrierCfg_ptr, FTSequence_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeOfdm_RemoveCC(self, device_id, CCID, FTSeq):
        """
        Removes specified CCID.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param FTSeq: FTSeq container.
        :return: ret: 0 on success and 1 on failure
        """
        self.logger.debug(f"XDfeOfdm_RemoveCC({device_id}, {CCID}, "
                          f"{json.dumps(FTSeq, indent=2)})")
        FTSequence_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        xofdm = self.ofdm_dict[device_id][1]
        ret = ofdm_handle.XDfeOfdm_RemoveCC(xofdm, CCID, FTSequence_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeOfdm_UpdateCC(self, device_id, CCID, CarrierCfg, FTSeq):
        """
        Updates specified CCID carrier configuration; change gain or filter
        coefficients set.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param CarrierCfg: is a CC configuration container.
        :param FTSeq: FTSeq container.
        :return: ret - 0 on success and 1 on failure
        """
        self.logger.debug(f"XDfeOfdm_UpdateCC({device_id}, {CCID}, "
                          f"{json.dumps(CarrierCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)})")
        CarrierCfg_ptr = ffi.new("XDfeOfdm_CarrierCfg *", CarrierCfg)
        FTSequence_ptr = ffi.new("XDfeOfdm_FTSequence *", FTSeq)
        xofdm = self.ofdm_dict[device_id][1]
        ret = ofdm_handle.XDfeOfdm_UpdateCC(xofdm, CCID, CarrierCfg_ptr, FTSequence_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeOfdm_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: is a trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeOfdm_TriggerCfg *")
        self.logger.debug(f"XDfeOfdm_GetTriggersCfg({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetTriggersCfg(xofdm, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeOfdm_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a trigger configuration container.
        :return: TriggerCfg: is a trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeOfdm_TriggerCfg *", TriggerCfg)
        self.logger.debug(f"XDfeOfdm_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_SetTriggersCfg(xofdm, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeOfdm_SetTuserOutFrameLocation(self, device_id, TuserOutFrameLocation):
        """
        Sets TUSER Framing bit Location register where bit location indicates which
        bit to be used for sending framing information on DL_DOUT IF and
        M_AXIS_TBASE IF.
        TUSER bit width is fixed to its default value of 8. Therefore, legal values
        of FRAME_BIT are 0 to 7.

        :param device_id: id of the opened device.
        :param TuserOutFrameLocation: TUSER OutFrame Location
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_SetTuserOutFrameLocation({device_id}, {TuserOutFrameLocation})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_SetTuserOutFrameLocation(xofdm, TuserOutFrameLocation)
        return

    def XDfeOfdm_GetTuserOutFrameLocation(self, device_id):
        """
        Gets TUSER Framing bit Location register where bit location indicates which
        bit to be used for sending framing information on DL_DOUT IF and
        M_AXIS_TBASE IF.
        TUSER bit width is fixed to its default value of 8. Therefore, legal values
        of FRAME_BIT are 0 to 7.

        :param device_id: id of the opened device.
        :return: TuserOutFrameLocation: TUSER OutFrame Location
        """
        self.logger.debug(f"XDfeOfdm_GetTuserOutFrameLocation({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        TuserOutFrameLocation = ofdm_handle.XDfeOfdm_GetTuserOutFrameLocation(xofdm)
        self.logger.debug(f"Return value = {TuserOutFrameLocation}")
        return TuserOutFrameLocation

    def XDfeOfdm_GetEventStatus(self, device_id):
        """
        Get event status

        :param device_id: id of the opened device.
        :return: Status: event status
        """
        Status_ptr = ffi.new("XDfeOfdm_Status *")
        self.logger.debug(f"XDfeOfdm_GetEventStatus({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetEventStatus(xofdm, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeOfdm_ClearEventStatus(self, device_id, Status):
        """
        Clears all event statuses.

        :param device_id: id of the opened device.
        :param Status: event status.
        :return: None
        """
        Status_ptr = ffi.new("XDfeOfdm_Status *", Status)
        self.logger.debug(f"XDfeOfdm_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_ClearEventStatus(xofdm, Status_ptr)
        return

    def XDfeOfdm_SetInterruptMask(self, device_id, Mask):
        """
        Sets interrupt masks.

        :param device_id: id of the opened device.
        :param Mask: interrupt mask value
        :return: None
        """
        Mask_ptr = ffi.new("XDfeOfdm_InterruptMask *", Mask)
        self.logger.debug(f"XDfeOfdm_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_SetInterruptMask(xofdm, Mask_ptr)
        return

    def XDfeOfdm_GetInterruptMask(self, device_id):
        """
        Get Interrupt mask value

        :param device_id: id of the opened device.
        :return: Mask: interrupt mask value.
        """
        Mask_ptr = ffi.new("XDfeOfdm_InterruptMask *")
        self.logger.debug(f"XDfeOfdm_GetInterruptMask({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetInterruptMask(xofdm, Mask_ptr)
        Mask = cdata_to_py(Mask_ptr[0])
        self.logger.debug(f"Mask = {json.dumps(Mask, indent=2)}")
        return Mask

    def XDfeOfdm_SetTUserDelay(self, device_id, TUserDelay):
        """
        Sets the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :param TUserDelay: Requested delay variable.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_SetTUserDelay({device_id}, {TUserDelay})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_SetTUserDelay(xofdm, TUserDelay)
        return

    def XDfeOfdm_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: TUserDelay: Delay value.
        """
        self.logger.debug(f"XDfeOfdm_GetTUserDelay({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        TUserDelay = ofdm_handle.XDfeOfdm_GetTUserDelay(xofdm)
        self.logger.debug(f"Return value = {TUserDelay}")
        return TUserDelay

    def XDfeOfdm_GetDataLatency(self, device_id):
        """
        Returns data latency.

        :param device_id: id of the opened device.
        :return: Returned Data latency.
        """
        self.logger.debug(f"XDfeOfdm_GetDataLatency({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        TDataLatency = ofdm_handle.XDfeOfdm_GetDataLatency(xofdm)
        self.logger.debug(f"Return value = {TDataLatency}")
        return TDataLatency

    def XDfeOfdm_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        SwVersion_ptr = ffi.new("XDfeOfdm_Version *")
        HwVersion_ptr = ffi.new("XDfeOfdm_Version *")
        self.logger.debug(f"XDfeOfdm_GetVersions({device_id})")
        xofdm = self.ofdm_dict[device_id][1]
        ofdm_handle.XDfeOfdm_GetVersions(xofdm, SwVersion_ptr, HwVersion_ptr)
        SwVersion = cdata_to_py(SwVersion_ptr[0])
        HwVersion = cdata_to_py(HwVersion_ptr[0])
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        self.logger.info("Inside OFDM Destructor")
