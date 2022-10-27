# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
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


ccf_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/dfe/xdfeccf_python.h", "/usr/lib/libdfeccf.so.1")


class CCF(object):
    ccf_dict = {}
    device_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error("CCF: XHelper_MetalInit failed. ret = ", ret)
        self.logger.info("Inside CCF Constructor")
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
    def GetEnum_XDfeCcf_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeCcf_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeCcf_StateId
        """
        XDfeCcf_StateId = ffi.typeof("enum XDfeCcf_StateId").relements
        self.logger.debug(f"XDfeCcf_StateId = {json.dumps(XDfeCcf_StateId, indent=2)}")
        return XDfeCcf_StateId

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
    def GetStruct_XDfeCcf_Version(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Version
        """
        XDfeCcf_Version_ptr = ffi.new("XDfeCcf_Version *")
        XDfeCcf_Version = cdata_to_py(XDfeCcf_Version_ptr[0])
        return XDfeCcf_Version

    def GetStruct_XDfeCcf_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Trigger
        """
        XDfeCcf_Trigger_ptr = ffi.new("XDfeCcf_Trigger *")
        XDfeCcf_Trigger = cdata_to_py(XDfeCcf_Trigger_ptr[0])
        return XDfeCcf_Trigger

    def GetStruct_XDfeCcf_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_TriggerCfg
        """
        XDfeCcf_TriggerCfg_ptr = ffi.new("XDfeCcf_TriggerCfg *")
        XDfeCcf_TriggerCfg = cdata_to_py(XDfeCcf_TriggerCfg_ptr[0])
        return XDfeCcf_TriggerCfg

    def GetStruct_XDfeCcf_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CCSequence
        """
        XDfeCcf_CCSequence_ptr = ffi.new("XDfeCcf_CCSequence *")
        XDfeCcf_CCSequence = cdata_to_py(XDfeCcf_CCSequence_ptr[0])
        return XDfeCcf_CCSequence

    def GetStruct_XDfeCcf_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_ModelParameters
        """
        XDfeCcf_ModelParameters_ptr = ffi.new("XDfeCcf_ModelParameters *")
        XDfeCcf_ModelParameters = cdata_to_py(XDfeCcf_ModelParameters_ptr[0])
        return XDfeCcf_ModelParameters

    def GetStruct_XDfeCcf_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Cfg
        """
        XDfeCcf_Cfg_ptr = ffi.new("XDfeCcf_Cfg *")
        XDfeCcf_Cfg = cdata_to_py(XDfeCcf_Cfg_ptr[0])
        return XDfeCcf_Cfg

    def GetStruct_XDfeCcf_Init(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Init

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Init
        """
        XDfeCcf_Init_ptr = ffi.new("XDfeCcf_Init *")
        XDfeCcf_Init = cdata_to_py(XDfeCcf_Init_ptr[0])
        return XDfeCcf_Init

    def GetStruct_XDfeCcf_Coefficients(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Coefficients
        """
        XDfeCcf_Coefficients_ptr = ffi.new("XDfeCcf_Coefficients *")
        XDfeCcf_Coefficients = cdata_to_py(XDfeCcf_Coefficients_ptr[0])
        return XDfeCcf_Coefficients

    def GetStruct_XDfeCcf_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CarrierCfg
        """
        XDfeCcf_CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *")
        XDfeCcf_CarrierCfg = cdata_to_py(XDfeCcf_CarrierCfg_ptr[0])
        return XDfeCcf_CarrierCfg

    def GetStruct_XDfeCcf_AntennaCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_AntennaCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_AntennaCfg
        """
        XDfeCcf_AntennaCfg_ptr = ffi.new("XDfeCcf_AntennaCfg *")
        XDfeCcf_AntennaCfg = cdata_to_py(XDfeCcf_AntennaCfg_ptr[0])
        return XDfeCcf_AntennaCfg

    def GetStruct_XDfeCcf_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CCCfg
        """
        XDfeCcf_CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *")
        XDfeCcf_CCCfg = cdata_to_py(XDfeCcf_CCCfg_ptr[0])
        return XDfeCcf_CCCfg

    def GetStruct_XDfeCcf_OverflowStatus(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_OverflowStatus

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_OverflowStatus
        """
        XDfeCcf_OverflowStatus_ptr = ffi.new("XDfeCcf_OverflowStatus *")
        XDfeCcf_OverflowStatus = cdata_to_py(XDfeCcf_OverflowStatus_ptr[0])
        return XDfeCcf_OverflowStatus

    def GetStruct_XDfeCcf_Status(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Status
        """
        XDfeCcf_Status_ptr = ffi.new("XDfeCcf_Status *")
        XDfeCcf_Status = cdata_to_py(XDfeCcf_Status_ptr[0])
        return XDfeCcf_Status

    def GetStruct_XDfeCcf_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_InterruptMask
        """
        XDfeCcf_InterruptMask_ptr = ffi.new("XDfeCcf_InterruptMask *")
        XDfeCcf_InterruptMask = cdata_to_py(XDfeCcf_InterruptMask_ptr[0])
        return XDfeCcf_InterruptMask

    def GetStruct_XDfeCcf_Config(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Config
        """
        XDfeCcf_Config_ptr = ffi.new("XDfeCcf_Config *")
        XDfeCcf_Config = cdata_to_py(XDfeCcf_Config_ptr[0])
        return XDfeCcf_Config

    def GetStruct_XDfeCcf_InternalCarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
        """
        XDfeCcf_InternalCarrierCfg_ptr = ffi.new("XDfeCcf_InternalCarrierCfg *")
        XDfeCcf_InternalCarrierCfg = cdata_to_py(XDfeCcf_InternalCarrierCfg_ptr[0])
        return XDfeCcf_InternalCarrierCfg

    def GetStruct_XDfeCcf(self):
        """
        Return Dictionary equivalent of structure XDfeCcf

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf
        """
        XDfeCcf_ptr = ffi.new("XDfeCcf *")
        XDfeCcf = cdata_to_py(XDfeCcf_ptr[0])
        return XDfeCcf

    # System initialization API
    def XDfeCcf_InstanceInit(self, DeviceNodeName):
        """
        Initialises one instance of a channel filter driver.
        Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
        CCF device with the name DeviceNodeName. The first available slot in
        the instances array XDfeCcf_ChFilter[] will be taken as a DeviceNodeName 
        object. On success it moves the state machine to a Ready state, while on
        failure stays in a Not Ready state.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to the initialized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value
        """
        DeviceNodeName = extract_b64_encoded_string(DeviceNodeName)
        cptrDeviceNodeName = ffi.new("char[128]", DeviceNodeName)
        self.logger.info(f"XDfeCcf_InstanceInit({DeviceNodeName})")
        # Pass the device node name to the driver
        xccf = ccf_handle.XDfeCcf_InstanceInit(cptrDeviceNodeName)
        DeviceNodeNameRet = cdata_string_to_py(cptrDeviceNodeName);
        if xccf == ffi.NULL:
            # if driver returns NULL, pass it as error to user
            ret = 1
            self.logger.error(f"The pointer returned for {DeviceNodeName} is NULL")
            device_id = 0xFFFFFFFF
        else:
            # otherwise treat as success
            ret = 0
            # In ccf_dict dictionary, device id is the key.
            # device node name and instance pointer from driver are values as list
            # check if the device node name is already present in dictionary
            found, device_id = getkey_from_listbeginvalue(self.ccf_dict, DeviceNodeName)
            if 1 == found:
                # if found, update the device id key with values
                self.ccf_dict[device_id][0] = DeviceNodeNameRet
                self.ccf_dict[device_id][1] = xccf
            else:
                # if not found, make new device_id from class variable
                # and increment the class variable
                device_id = self.device_id
                self.device_id += 1
                # add new key and values to the dictionary
                self.ccf_dict[device_id] = [DeviceNodeNameRet, xccf]
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeNameRet = {DeviceNodeNameRet}")
        return ret, device_id, DeviceNodeNameRet

    def XDfeCcf_InstanceClose(self, device_id):
        """
        Closes the instances of a channel filter driver and moves the state
        machine to a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeCcf_InstanceClose({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_InstanceClose(xccf)
        if device_id in self.ccf_dict:
            del self.ccf_dict[device_id]
        return

    # Register access API
    def XDfeCcf_WriteReg(self, device_id, addr_offset, data):
        """
        Writes value to register in a Ccf instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address.
        :param Data: value to be written.
        :return: None
        """
        self.logger.debug(f"XDfeCcf_WriteReg({device_id}, {addr_offset}, {data})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_WriteReg(xccf, addr_offset, data)
        return

    def XDfeCcf_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from register using a Ccf instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address
        :return: regval: Register value.
        """
        self.logger.debug(f"XDfeCcf_ReadReg({device_id}, {addr_offset})")
        xccf = self.ccf_dict[device_id][1]
        regval = ccf_handle.XDfeCcf_ReadReg(xccf, addr_offset)
        self.logger.debug(f"regval = {regval}")
        return regval

    # DFE ChFilter component initialization API
    def XDfeCcf_Reset(self, device_id):
        """
        Resets channel filter and puts block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeCcf_Reset({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_Reset(xccf)
        return

    def XDfeCcf_Configure(self, device_id, Cfg):
        """
        Read configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container
        :return: Cfg: configuration data container
        """
        Cfg_ptr = ffi.new("XDfeCcf_Cfg *", Cfg)
        self.logger.debug(f"XDfeCcf_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_Configure(xccf, Cfg_ptr)
        Cfg = cdata_to_py(Cfg_ptr[0])
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeCcf_Initialize(self, device_id, Init):
        """
        DFE Ccf driver one time initialisation, also moves the state machine to
        an Initialised state.

        :param device_id: id of the opened device.
        :param Init: initialisation data container
        :return: Init: initialisation data container
        """
        Init_ptr = ffi.new("XDfeCcf_Init *", Init)
        self.logger.debug(f"XDfeCcf_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_Initialize(xccf, Init_ptr)
        Init = cdata_to_py(Init_ptr[0])
        self.logger.debug(f"Init = {json.dumps(Init, indent=2)}")
        return Init

    def XDfeCcf_Activate(self, device_id, EnableLowPower):
        """
        Activates channel filter and moves the state machine to an Activated state.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power
        :return: None
        """
        self.logger.debug(f"XDfeCcf_Activate({device_id}, {EnableLowPower})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_Activate(xccf, EnableLowPower)
        return

    def XDfeCcf_Deactivate(self, device_id):
        """
        Deactivates channel filter and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeCcf_Deactivate({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_Deactivate(xccf)
        return

    def XDfeCcf_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeCcf_GetStateID({device_id})")
        xccf = self.ccf_dict[device_id][1]
        StateId = ccf_handle.XDfeCcf_GetStateID(xccf)
        StateId_edict = ffi.typeof("XDfeCcf_StateId").elements
        self.logger.debug(f"Return value = {json.dumps(StateId, indent=2)}")
        return StateId_edict[StateId]

    def XDfeCcf_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration. Not used slot ID in a sequence
        (Sequence.CCID[Index]) are represented as (-1), not the value in registers.
        Note: For a sequence conversion see XDfeCcf_AddCCtoCCCfg() comment.

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeCcf_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CurrCCCfg)
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetCurrentCCCfg(xccf, CurrCCCfg_ptr)
        CurrCCCfg = cdata_to_py(CurrCCCfg_ptr[0])
        self.logger.debug(f"CurrCCCfg = {json.dumps(CurrCCCfg, indent=2)}")
        return CurrCCCfg

    def XDfeCcf_GetEmptyCCCfg(self, device_id):
        """
        Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
        in XDfeCcf_Configure(), array CCCfg->Sequence.CCID[] members are set to not
        used value (-1) and the other CCCfg members are set to 0.

        :param device_id: id of the opened device.
        :return: CCCfg: CC configuration container
        """
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *")
        self.logger.debug(f"XDfeCcf_GetEmptyCCCfg({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetEmptyCCCfg(xccf, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeCcf_GetCarrierCfg(self, device_id, CCCfg, CCID):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
        """
        self.logger.debug(f"XDfeCcf_GetCarrierCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        CCSeqBitmap_ptr = ffi.new("u32 *")
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *")
        ccf_handle.XDfeCcf_GetCarrierCfg(xccf, CCCfg_ptr, CCID, CCSeqBitmap_ptr, CarrierCfg_ptr)
        CCSeqBitmap = CCSeqBitmap_ptr[0]
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}")
        return CCSeqBitmap, CarrierCfg

    def XDfeCcf_SetAntennaCfgInCCCfg(self, device_id, CCCfg, AntennaCfg):
        """
        Set antenna configuration in CC configuration container.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param AntennaCfg: Array of all antenna configurations.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeCcf_SetAntennaCfgInCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {json.dumps(AntennaCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        AntennaCfg_ptr = ffi.new("XDfeCcf_AntennaCfg *", AntennaCfg)
        ccf_handle.XDfeCcf_SetAntennaCfgInCCCfg(xccf, CCCfg_ptr, AntennaCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeCcf_AddCCtoCCCfg(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg):
        """
        Adds specified CCID, with specified configuration, to a local CC
        configuration structure.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        The returned CCCfg.Sequence is transleted as there is no explicite indication that
        SEQUENCE[i] is not used - 0 can define the slot as either used or not used.
        Sequence data that is returned in the CCIDSequence is not the same as what is
        written in the registers. The translation is:
            - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
            - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
            - a returned CCIDSequence->Length = length in register + 1

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CCSeqBitmap: CC slot position container.
        :param CarrierCfg: CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeCcf_AddCCtoCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {CCSeqBitmap}, {json.dumps(CCCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *", CarrierCfg)
        ret = ccf_handle.XDfeCcf_AddCCtoCCCfg(xccf, CCCfg_ptr, CCID, CCSeqBitmap, CarrierCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeCcf_RemoveCCfromCCCfg(self, device_id, CCCfg, CCID):
        """
        Removes specified CCID from a local CC configuration structure.
        Note: For a sequence conversion see XDfeCcf_AddCCtoCCCfg comment.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeCcf_RemoveCCfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {CCID})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        ccf_handle.XDfeCcf_RemoveCCfromCCCfg(xccf, CCCfg_ptr, CCID)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeCcf_UpdateCCinCCCfg(self, device_id, CCCfg, CCID, CarrierCfg):
        """
        Updates specified CCID, with specified configuration to a local CC
        configuration structure.
        If there is insufficient capacity for the new CC the function will return
        an error.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CarrierCfg: CC configuration container.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeCcf_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {json.dumps(CarrierCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *", CarrierCfg)
        ccf_handle.XDfeCcf_UpdateCCinCCCfg(xccf, CCCfg_ptr, CCID, CarrierCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeCcf_SetNextCCCfgAndTrigger(self, device_id, CCCfg):
        """
        Writes local CC configuration to the shadow (NEXT) registers and triggers
        copying from shadow to operational registers.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeCcf_SetNextCCCfgAndTrigger({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        ret = ccf_handle.XDfeCcf_SetNextCCCfgAndTrigger(xccf, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CCCfg = {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeCcf_AddCC(self, device_id, CCID, CCSeqBitmap, CarrierCfg):
        """
        Adds specified CCID, with specified configuration.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCID: Channel ID.
        :param CCSeqBitmap: up to 16 defined slots into which a CC can be
               allocated. The number of slots can be from 1 to 16 depending on
               system initialization. The number of slots is defined by the
               "sequence length" parameter which is provided during initialization.
               The Bit offset within the CCSeqBitmap indicates the equivalent
               Slot number to allocate. e.g. 0x0003  means the caller wants the
               passed component carrier (CC) to be allocated to slots 0 and 1.
        :param CarrierCfg: is a CC configuration container.
        :return: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CarrierCfg: is a CC configuration container.
        """
        self.logger.debug(f"XDfeCcf_AddCC({device_id}, {CCID}, {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)})")
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *", CarrierCfg)
        xccf = self.ccf_dict[device_id][1]
        ret = ccf_handle.XDfeCcf_AddCC(xccf, CCID, CCSeqBitmap, CarrierCfg_ptr)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return ret, CarrierCfg

    def XDfeCcf_RemoveCC(self, device_id, CCID):
        """
        Removes specified CCID.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeCcf_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :return: ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeCcf_RemoveCC({device_id}, {CCID})")
        xccf = self.ccf_dict[device_id][1]
        ret = ccf_handle.XDfeCcf_RemoveCC(xccf, CCID)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeCcf_UpdateCC(self, device_id, CCID, CarrierCfg):
        """
        Updates specified CCID carrier configuration; change gain or filter
        coefficients set.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeCcf_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param CarrierCfg: is a CC configuration container.
        :return: ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
             CarrierCfg - CC configuration container
        """
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *", CarrierCfg)
        self.logger.debug(f"XDfeCcf_UpdateCC({device_id}, {json.dumps(CarrierCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ret = ccf_handle.XDfeCcf_UpdateCC(xccf, CCID, CarrierCfg_ptr)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return ret, CarrierCfg

    def XDfeCcf_UpdateAntenna(self, device_id, Ant, Enabled):
        """
        Updates specified antenna TDM slot enablement.
        Initiates CC update (enable CCUpdate trigger one-shot).
        Note: Clear event status with XDfeCcf_ClearEventStatus()
        before running this API.        

        :param device_id: id of the opened device.
        :param Ant: is antenna ID.
        :param Enabled: flag indicating enable status of the antenna.
        :return: ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeCcf_UpdateAntenna({device_id}, {Ant}, {Enabled})")
        xccf = self.ccf_dict[device_id][1]
        ret = ccf_handle.XDfeCcf_UpdateAntenna(xccf, Ant, Enabled)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeCcf_UpdateAntennaCfg(self, device_id, AntennaCfg):
        """
        Updates antenna configuration to all antennas.
        Note: Clear event status with XDfeCcf_ClearEventStatus() before
        running this API.

        :param device_id: id of the opened device.
        :param AntennaCfg: Array of all antenna configurations.
        :return: ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeCcf_UpdateAntennaCfg({device_id}, {json.dumps(AntennaCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        AntennaCfg_ptr = ffi.new("XDfeCcf_AntennaCfg *", AntennaCfg)
        ret = ccf_handle.XDfeCcf_UpdateAntennaCfg(xccf, AntennaCfg_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeCcf_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: is a trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeCcf_TriggerCfg *")
        self.logger.debug(f"XDfeCcf_GetTriggersCfg({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetTriggersCfg(xccf, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeCcf_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a trigger configuration container.
        :return: TriggerCfg: is a trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeCcf_TriggerCfg *", TriggerCfg)
        self.logger.debug(f"XDfeCcf_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_SetTriggersCfg(xccf, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeCcf_GetCC(self, device_id, CCID):
        """
        Get specified CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :return: CarrierCfg: is a trigger configuration container.
        """
        CarrierCfg_ptr = ffi.new("XDfeCcf_CarrierCfg *")
        self.logger.debug(f"XDfeCcf_GetCC({device_id}, {CCID})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetCC(xccf, CCID, CarrierCfg_ptr)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return CarrierCfg

    def XDfeCcf_GetActiveSets(self, device_id):
        """
        Return a list indicating which coefficient sets are currently in use.

        :param device_id: id of the opened device.
        :return: IsActive: variable indicating an activation status.
        """
        IsActive_ptr = ffi.new("u32[8]")
        self.logger.debug(f"XDfeCcf_GetActiveSets({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetActiveSets(xccf, IsActive_ptr)
        IsActive = cdata_to_py(IsActive_ptr)
        self.logger.debug(f"IsActive = {IsActive}")
        return IsActive

    def XDfeCcf_LoadCoefficients(self, device_id, Set, Shift, Coeffs):
        """
        Writes the coefficient set defined into the register map and commit them
        to the hard block's internal coefficient memory for the specified Set.

        :param device_id: id of the opened device.
        :param Set: coefficient set Id
        :param Shift: is a coefficient shift value.
        :param Coeffs: an array of filter coefficients
        :return: Coeffs: an array of filter coefficients
        """
        Coeffs_ptr = ffi.new("XDfeCcf_Coefficients *", Coeffs)
        self.logger.debug(f"XDfeCcf_LoadCoefficients({device_id}, {Set}, {Shift}, {json.dumps(Coeffs, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_LoadCoefficients(xccf, Set, Shift, Coeffs_ptr)
        Coeffs = cdata_to_py(Coeffs_ptr[0])
        self.logger.debug(f"Coeffs = {json.dumps(Coeffs, indent=2)}")
        return Coeffs

    def XDfeCcf_GetOverflowStatus(self, device_id):
        """
        Gets overflow event status.

        :param device_id: id of the opened device.
        :return: Status: overflow event status
        """
        Status_ptr = ffi.new("XDfeCcf_OverflowStatus *")
        self.logger.debug(f"XDfeCcf_GetOverflowStatus({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetOverflowStatus(xccf, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeCcf_GetEventStatus(self, device_id):
        """
        Get event status

        :param device_id: id of the opened device.
        :return: Status: event status
        """
        Status_ptr = ffi.new("XDfeCcf_Status *")
        self.logger.debug(f"XDfeCcf_GetEventStatus({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetEventStatus(xccf, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeCcf_ClearEventStatus(self, device_id, Status):
        """
        Clears event status.

        :param device_id: id of the opened device.
        :param Status: event status.
                       0 - does not clear corresponding event status
                       1 - clears corresponding event status
        :return: None
        """
        Status_ptr = ffi.new("XDfeCcf_Status *", Status)
        self.logger.debug(f"XDfeCcf_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_ClearEventStatus(xccf, Status_ptr)
        return

    def XDfeCcf_SetInterruptMask(self, device_id, Mask):
        """
        Sets interrupt masks.

        :param device_id: id of the opened device.
        :param Mask: interrupt mask value
                     0 - does not mask corresponding interrupt
                     1 - masks corresponding interrupt

        :return: None
        """
        Mask_ptr = ffi.new("XDfeCcf_InterruptMask *", Mask)
        self.logger.debug(f"XDfeCcf_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_SetInterruptMask(xccf, Mask_ptr)
        return

    def XDfeCcf_GetInterruptMask(self, device_id):
        """
        Get Interrupt mask value

        :param device_id: id of the opened device.
        :return: Mask: interrupt mask value.
        """
        Mask_ptr = ffi.new("XDfeCcf_InterruptMask *")
        self.logger.debug(f"XDfeCcf_GetInterruptMask({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetInterruptMask(xccf, Mask_ptr)
        Mask = cdata_to_py(Mask_ptr[0])
        self.logger.debug(f"Mask = {json.dumps(Mask, indent=2)}")
        return Mask

    def XDfeCcf_SetTUserDelay(self, device_id, Delay):
        """
        Sets the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :param Delay: requested delay variable.
        :return: None
        """
        self.logger.debug(f"XDfeCcf_SetTUserDelay({device_id}, {Delay})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_SetTUserDelay(xccf, Delay)
        return

    def XDfeCcf_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfeCcf_GetTUserDelay({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ret = ccf_handle.XDfeCcf_GetTUserDelay(xccf)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeCcf_GetTDataDelay(self, device_id, Tap, CCID, Symmetric, Num):
        """
        Gets calculated TDataDelay value for CCID from current CC configuration.

        :param device_id: id of the opened device.
        :param Tap: is a tap variable.
        :param CCID: CC ID.
        :param Symmetric: Select symetric (1) or non-symetric (0) filter.
        :param Num: Number of coefficients values.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 TDataDelay: Delay value container.
        """
        self.logger.debug(f"XDfeCcf_GetTDataDelay({device_id}, {Tap}, {CCID}, {Symmetric}, {Num})")
        xccf = self.ccf_dict[device_id][1]
        TDataDelay_ptr = ffi.new("u32 *")
        ret = ccf_handle.XDfeCcf_GetTDataDelay(xccf, Tap, CCID, Symmetric, Num, TDataDelay_ptr)
        TDataDelay = TDataDelay_ptr[0]
        self.logger.debug(f"ret = {ret}, Latency = {TDataDelay}")
        return ret, TDataDelay

    def XDfeCcf_GetTDataDelayFromCCCfg(self, device_id, Tap, CCID, CCCfg, Symmetric, Num):
        """
        Gets calculated TDataDelay value for CCID.

        :param device_id: id of the opened device.
        :param Tap: is a tap variable.
        :param CCID: CC ID.
        :param CCCfg: Component carrier (CC) configuration container.
        :param Symmetric: Select symetric (1) or non-symetric (0) filter.
        :param Num: Number of coefficients values.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 TDataDelay: Delay value container.
        """
        self.logger.debug(f"XDfeCcf_GetTDataDelayFromCCCfg({device_id}, {Tap}, {CCID}, {json.dumps(CCCfg, indent=2)}, {Symmetric}, {Num})")
        xccf = self.ccf_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfeCcf_CCCfg *", CCCfg)
        TDataDelay_ptr = ffi.new("u32 *")
        ret = ccf_handle.XDfeCcf_GetTDataDelayFromCCCfg(xccf, Tap, CCID, CCCfg_ptr, Symmetric, Num, TDataDelay_ptr)
        TDataDelay = TDataDelay_ptr[0]
        self.logger.debug(f"ret = {ret}, Latency = {TDataDelay}")
        return ret, TDataDelay

    def XDfeCcf_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        SwVersion_ptr = ffi.new("XDfeCcf_Version *")
        HwVersion_ptr = ffi.new("XDfeCcf_Version *")
        self.logger.debug(f"XDfeCcf_GetVersions({device_id})")
        xccf = self.ccf_dict[device_id][1]
        ccf_handle.XDfeCcf_GetVersions(xccf, SwVersion_ptr, HwVersion_ptr)
        SwVersion = cdata_to_py(SwVersion_ptr[0])
        HwVersion = cdata_to_py(HwVersion_ptr[0])
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        self.logger.info("Inside CCF Destructor")
