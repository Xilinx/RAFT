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

prach_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/dfe/xdfeprach_python.h", "/usr/lib/libdfeprach.so.1")


class PRACH(object):
    prach_dict = {}
    device_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error(f"PRACH: XHelper_MetalInit failed. ret = {ret}")
        self.logger.info("Inside PRACH Constructor")
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

    def GetEnum_XDfePrach_StateId(self):
        """
        Return Dictionary equivalent of enum XDfePrach_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfePrach_StateId
        """
        XDfePrach_StateId = ffi.typeof("enum XDfePrach_StateId").relements
        self.logger.debug(f"XDfePrach_StateId = {json.dumps(XDfePrach_StateId, indent=2)}")
        return XDfePrach_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        metal_log_level = ffi.typeof("enum metal_log_level").relements
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    def GetStruct_XDfePrach_Version(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Version

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Version
        """
        XDfePrach_Version_ptr = ffi.new("XDfePrach_Version *")
        XDfePrach_Version = cdata_to_py(XDfePrach_Version_ptr[0])
        return XDfePrach_Version

    def GetStruct_XDfePrach_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Trigger
        """
        XDfePrach_Trigger_ptr = ffi.new("XDfePrach_Trigger *")
        XDfePrach_Trigger = cdata_to_py(XDfePrach_Trigger_ptr[0])
        return XDfePrach_Trigger

    def GetStruct_XDfePrach_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_TriggerCfg
        """
        XDfePrach_TriggerCfg_ptr = ffi.new("XDfePrach_TriggerCfg *")
        XDfePrach_TriggerCfg = cdata_to_py(XDfePrach_TriggerCfg_ptr[0])
        return XDfePrach_TriggerCfg

    def GetStruct_XDfePrach_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CCSequence
        """
        XDfePrach_CCSequence_ptr = ffi.new("XDfePrach_CCSequence *")
        XDfePrach_CCSequence = cdata_to_py(XDfePrach_CCSequence_ptr[0])
        return XDfePrach_CCSequence

    def GetStruct_XDfePrach_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfePrach_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_ModelParameters
        """
        XDfePrach_ModelParameters_ptr = ffi.new("XDfePrach_ModelParameters *")
        XDfePrach_ModelParameters = cdata_to_py(XDfePrach_ModelParameters_ptr[0])
        return XDfePrach_ModelParameters

    def GetStruct_XDfePrach_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Cfg
        """
        XDfePrach_Cfg_ptr = ffi.new("XDfePrach_Cfg *")
        XDfePrach_Cfg = cdata_to_py(XDfePrach_Cfg_ptr[0])
        return XDfePrach_Cfg

    def GetStruct_XDfePrach_Init(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Init

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Init
        """
        XDfePrach_Init_ptr = ffi.new("XDfePrach_Init *")
        XDfePrach_Init = cdata_to_py(XDfePrach_Init_ptr[0])
        return XDfePrach_Init

    def GetStruct_XDfePrach_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CarrierCfg
        """
        XDfePrach_CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *")
        XDfePrach_CarrierCfg = cdata_to_py(XDfePrach_CarrierCfg_ptr[0])
        return XDfePrach_CarrierCfg

    def GetStruct_XDfePrach_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CCCfg
        """
        XDfePrach_CCCfg_ptr = ffi.new("XDfePrach_CCCfg *")
        XDfePrach_CCCfg = cdata_to_py(XDfePrach_CCCfg_ptr[0])
        return XDfePrach_CCCfg

    def GetStruct_XDfePrach_NCO(self):
        """
        Return Dictionary equivalent of structure XDfePrach_NCO

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_NCO
        """
        XDfePrach_NCO_ptr = ffi.new("XDfePrach_NCO *")
        XDfePrach_NCO = cdata_to_py(XDfePrach_NCO_ptr[0])
        return XDfePrach_NCO

    def GetStruct_XDfePrach_DDCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DDCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DDCCfg
        """
        XDfePrach_DDCCfg_ptr = ffi.new("XDfePrach_DDCCfg *")
        XDfePrach_DDCCfg = cdata_to_py(XDfePrach_DDCCfg_ptr[0])
        return XDfePrach_DDCCfg

    def GetStruct_XDfePrach_Schedule(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Schedule

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Schedule
        """
        XDfePrach_Schedule_ptr = ffi.new("XDfePrach_Schedule *")
        XDfePrach_Schedule = cdata_to_py(XDfePrach_Schedule_ptr[0])
        return XDfePrach_Schedule

    def GetStruct_XDfePrach_InternalChannelCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_InternalChannelCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_InternalChannelCfg
        """
        XDfePrach_InternalChannelCfg_ptr = ffi.new("XDfePrach_InternalChannelCfg *")
        XDfePrach_InternalChannelCfg = cdata_to_py(XDfePrach_InternalChannelCfg_ptr[0])
        return XDfePrach_InternalChannelCfg

    def GetStruct_XDfePrach_ChannelCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_ChannelCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_ChannelCfg
        """
        XDfePrach_ChannelCfg_ptr = ffi.new("XDfePrach_ChannelCfg *")
        XDfePrach_ChannelCfg = cdata_to_py(XDfePrach_ChannelCfg_ptr[0])
        return XDfePrach_ChannelCfg

    def GetStruct_XDfePrach_RCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_RCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_RCCfg
        """
        XDfePrach_RCCfg_ptr = ffi.new("XDfePrach_RCCfg *")
        XDfePrach_RCCfg = cdata_to_py(XDfePrach_RCCfg_ptr[0])
        return XDfePrach_RCCfg

    def GetStruct_XDfePrach_MixerStatusOverflow(self):
        """
        Return Dictionary equivalent of structure XDfePrach_MixerStatusOverflow

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_MixerStatusOverflow
        """
        XDfePrach_MixerStatusOverflow_ptr = ffi.new("XDfePrach_MixerStatusOverflow *")
        XDfePrach_MixerStatusOverflow = cdata_to_py(
            XDfePrach_MixerStatusOverflow_ptr[0]
        )
        return XDfePrach_MixerStatusOverflow

    def GetStruct_XDfePrach_DecimatorStatusOverflow(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DecimatorStatusOverflow

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DecimatorStatusOverflow
        """
        XDfePrach_DecimatorStatusOverflow_ptr = ffi.new(
            "XDfePrach_DecimatorStatusOverflow *"
        )
        XDfePrach_DecimatorStatusOverflow = cdata_to_py(
            XDfePrach_DecimatorStatusOverflow_ptr[0]
        )
        return XDfePrach_DecimatorStatusOverflow

    def GetStruct_XDfePrach_MixerStatusOverrun(self):
        """
        Return Dictionary equivalent of structure XDfePrach_MixerStatusOverrun

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_MixerStatusOverrun
        """
        XDfePrach_MixerStatusOverrun_ptr = ffi.new("XDfePrach_MixerStatusOverrun *")
        XDfePrach_MixerStatusOverrun = cdata_to_py(XDfePrach_MixerStatusOverrun_ptr[0])
        return XDfePrach_MixerStatusOverrun

    def GetStruct_XDfePrach_DecimatorStatusOverrun(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DecimatorStatusOverrun

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DecimatorStatusOverrun
        """
        XDfePrach_DecimatorStatusOverrun_ptr = ffi.new(
            "XDfePrach_DecimatorStatusOverrun *"
        )
        XDfePrach_DecimatorStatusOverrun = cdata_to_py(
            XDfePrach_DecimatorStatusOverrun_ptr[0]
        )
        return XDfePrach_DecimatorStatusOverrun

    def GetStruct_XDfePrach_Status(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Status

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Status
        """
        XDfePrach_Status_ptr = ffi.new("XDfePrach_Status *")
        XDfePrach_Status = cdata_to_py(XDfePrach_Status_ptr[0])
        return XDfePrach_Status

    def GetStruct_XDfePrach_StatusMask(self):
        """
        Return Dictionary equivalent of structure XDfePrach_StatusMask

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_StatusMask
        """
        XDfePrach_StatusMask_ptr = ffi.new("XDfePrach_StatusMask *")
        XDfePrach_StatusMask = cdata_to_py(XDfePrach_StatusMask_ptr[0])
        return XDfePrach_StatusMask

    def GetStruct_XDfePrach_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfePrach_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_InterruptMask
        """
        XDfePrach_InterruptMask_ptr = ffi.new("XDfePrach_InterruptMask *")
        XDfePrach_InterruptMask = cdata_to_py(XDfePrach_InterruptMask_ptr[0])
        return XDfePrach_InterruptMask

    def GetStruct_XDfePrach_Config(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Config

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Config
        """
        XDfePrach_Config_ptr = ffi.new("XDfePrach_Config *")
        XDfePrach_Config = cdata_to_py(XDfePrach_Config_ptr[0])
        return XDfePrach_Config

    def GetStruct_XDfePrach(self):
        """
        Return Dictionary equivalent of structure XDfePrach

        :param : None
        :return: Dictionary equivalent of structure XDfePrach
        """
        XDfePrach_ptr = ffi.new("XDfePrach *")
        XDfePrach = cdata_to_py(XDfePrach_ptr[0])
        return XDfePrach

    def XDfePrach_InstanceInit(self, DeviceNodeName):
        """
        API initialise an instance of the driver.
        Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
        PRACH device with the name DeviceNodeName. The first available slot in
        the instance array XDfePrach_Prach[] will be taken as a DeviceNodeName
        object. On success it moves the state machine to a Ready state, while on
        failure stays in a Not Ready state.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to initalized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value
        """
        DeviceNodeName = extract_b64_encoded_string(DeviceNodeName)
        cptrDeviceNodeName = ffi.new("char[128]", DeviceNodeName)
        self.logger.info(f"XDfePrach_InstanceInit DeviceNodeName = {DeviceNodeName}")
        # Pass the device node name to the driver
        xprach = prach_handle.XDfePrach_InstanceInit(cptrDeviceNodeName)
        self.logger.info(f"The initalized pointer value = {xprach}")
        DeviceNodeNameRet = cdata_string_to_py(cptrDeviceNodeName);
        if xprach == ffi.NULL:
            # if driver returns NULL, pass it as error to user
            ret = 1        
            self.logger.error(f"The pointer returned for {DeviceNodeName} is NULL")
            device_id = 0xFFFFFFFF
        else:
            # otherwise treat as success
            ret = 0        
            # In prach_dict dictionary, device id is the key.
            # device node name and instance pointer from driver are values as list
            # check if the device node name is already present in dictionary
            found, device_id = getkey_from_listbeginvalue(self.prach_dict, DeviceNodeName)
            if 1 == found:
                # if found, update the device id key with values
                self.prach_dict[device_id][0] = DeviceNodeNameRet 
                self.prach_dict[device_id][1] = xprach                            
            else:
                # if not found, make new device_id from class variable
                # and increment the class variable
                device_id = self.device_id
                self.device_id += 1
                # add new key and values to the dictionary
                self.prach_dict[device_id] = [DeviceNodeNameRet, xprach]
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeNameRet = {DeviceNodeNameRet}")
        return ret, device_id, DeviceNodeNameRet

    def XDfePrach_InstanceClose(self, device_id):
        """
        API closes the instances of a PRACH driver and moves the state machine to
        a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfePrach_InstanceClose({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_InstanceClose(xprach)
        if device_id in self.prach_dict:
            del self.prach_dict[device_id]
        return

    # Register access API
    def XDfePrach_WriteReg(self, device_id, addr_offset, data):
        """
        Writes a value to register in a PRACH instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :param Data: is value to be written.
        :return: None
        """
        self.logger.debug(f"XDfePrach_WriteReg({device_id}, {addr_offset}, {data})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_WriteReg(xprach, addr_offset, data)
        return

    def XDfePrach_ReadReg(self, device_id, addr_offset):
        """
        Reads a value the register in a PRACH instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :return: ret: Register value.
        """
        self.logger.debug(f"XDfePrach_ReadReg({device_id}, {addr_offset})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_ReadReg(xprach, addr_offset)
        self.logger.debug(f"The return value ret = {ret}")
        return ret

    # DFE PRACH component initialization API
    def XDfePrach_Reset(self, device_id):
        """
        Resets PRACH and puts block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_Reset({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_Reset(xprach)
        return

    def XDfePrach_Configure(self, device_id, Cfg):
        """
        Reads configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container.
        :return: Cfg: configuration data container.
        """
        Cfg_ptr = ffi.new("XDfePrach_Cfg *", Cfg)
        self.logger.debug(f"XDfePrach_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_Configure(xprach, Cfg_ptr)
        Cfg = cdata_to_py(Cfg_ptr[0])
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfePrach_Initialize(self, device_id, Init):
        """
        DFE PRACH driver one time initialisation also moves the state machine to
        an Initialised state.

        :param device_id: id of the opened device.
        :param Init: initialisation data container.
        :return: Init: initialisation data container.
        """
        Init_ptr = ffi.new("XDfePrach_Init *", Init)
        self.logger.debug(f"XDfePrach_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_Initialize(xprach, Init_ptr)
        Init = cdata_to_py(Init_ptr[0])
        self.logger.debug(f"Init = {json.dumps(Init, indent=2)}")
        return Init

    def XDfePrach_Activate(self, device_id, EnableLowPower):
        """
        Activates PRACH and moves the state machine to an Activated state.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power.
        :return: None
        """
        self.logger.debug(f"XDfePrach_Activate({device_id}, {EnableLowPower})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_Activate(xprach, EnableLowPower)
        return

    def XDfePrach_Deactivate(self, device_id):
        """
        Deactivates PRACH and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_Deactivate({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_Deactivate(xprach)
        return

    def XDfePrach_GetStateID(self, device_id):
        """
        Gets a state machine state id.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfePrach_GetStateID({device_id})")
        xprach = self.prach_dict[device_id][1]
        StateId = prach_handle.XDfePrach_GetStateID(xprach)
        StateId_edict = ffi.typeof("XDfePrach_StateId").elements
        self.logger.debug(f"Return value = {json.dumps(StateId, indent=2)}")
        return StateId_edict[StateId]

    def XDfePrach_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfePrach_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CurrCCCfg)
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetCurrentCCCfg(xprach, CurrCCCfg_ptr)
        CurrCCCfg = cdata_to_py(CurrCCCfg_ptr[0])
        self.logger.debug(f"CurrCCCfg = {json.dumps(CurrCCCfg, indent=2)}")
        return CurrCCCfg

    def XDfePrach_GetEmptyCCCfg(self, device_id):
        """
        Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
        in XDfePrach_Configure(), array CCCfg->Sequence.CCID[] members are set to not
        used value (-1) and the other CCCfg members are set to 0.

        :param device_id: id of the opened device.
        :return: CCCfg: CC configuration container
        """
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *")
        self.logger.debug(f"XDfePrach_GetEmptyCCCfg({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetEmptyCCCfg(xprach, CCCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_GetCarrierCfgMB(self, device_id, CCCfg, CCID, BandId):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param BandId: Band Id.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
        """
        self.logger.debug(f"XDfePrach_GetCarrierCfgMB({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CCSeqBitmap_ptr = ffi.new("u32 *")
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *")
        prach_handle.XDfePrach_GetCarrierCfgMB(xprach, CCCfg_ptr, CCID, CCSeqBitmap_ptr, CarrierCfg_ptr, BandId)
        CCSeqBitmap = CCSeqBitmap_ptr[0]
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}")
        return CCSeqBitmap, CarrierCfg

    def XDfePrach_GetCarrierCfg(self, device_id, CCCfg, CCID):
        """
        Returns the current CCID carrier configuration on Band which Id = 0.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
        """
        self.logger.debug(f"XDfePrach_GetCarrierCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CCSeqBitmap_ptr = ffi.new("u32 *")
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *")
        prach_handle.XDfePrach_GetCarrierCfg(xprach, CCCfg_ptr, CCID, CCSeqBitmap_ptr, CarrierCfg_ptr)
        CCSeqBitmap = CCSeqBitmap_ptr[0]
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}")
        return CCSeqBitmap, CarrierCfg

    def XDfePrach_SetAntennaCfgInCCCfg(self, device_id, CCCfg, AntennaCfg):
        """
        Set antenna configuration in CC configuration container.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param AntennaCfg: Array of all antenna configurations.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_SetAntennaCfgInCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {json.dumps(AntennaCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        AntennaCfg_ptr = ffi.new("u32[]", AntennaCfg)
        prach_handle.XDfePrach_SetAntennaCfgInCCCfg(xprach, CCCfg_ptr, AntennaCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_AddCCtoCCCfgMB(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg, BandId):
        """
        Adds specified CCID, with specified configuration, to a local CC
        configuration structure for the chosen Band.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CCSeqBitmap: CC slot position container.
        :param CarrierCfg: CC configuration container.
        :param BandId: Band Id.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_AddCCtoCCCfgMB({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        ret = prach_handle.XDfePrach_AddCCtoCCCfgMB(xprach, CCCfg_ptr, CCID, CCSeqBitmap,
                                              CarrierCfg_ptr, BandId)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfePrach_AddCCtoCCCfg(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg):
        """
        Adds specified CCID, with specified configuration, to a local CC
        configuration structure on Band which Id = 0.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CCSeqBitmap: CC slot position container.
        :param CarrierCfg: CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_AddCCtoCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        ret = prach_handle.XDfePrach_AddCCtoCCCfg(xprach, CCCfg_ptr, CCID, CCSeqBitmap,
                                              CarrierCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfePrach_RemoveCCfromCCCfgMB(self, device_id, CCCfg, CCID, BandId):
        """
        Removes specified CCID from a local CC configuration structure for
        selected band.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param BandId: Band Id.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_RemoveCCfromCCCfgMB({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        prach_handle.XDfePrach_RemoveCCfromCCCfgMB(xprach, CCCfg_ptr, CCID, BandId)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_RemoveCCfromCCCfg(self, device_id, CCCfg, CCID):
        """
        Removes specified CCID from a local CC configuration structure on Band
        which Id = 0.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_RemoveCCfromCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        prach_handle.XDfePrach_RemoveCCfromCCCfg(xprach, CCCfg_ptr, CCID)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_UpdateCCinCCCfgMB(self, device_id, CCCfg, CCID, CarrierCfg, BandId):
        """
        Updates specified CCID, with specified configuration to a local CC
        configuration structure for selected band.
        If there is insufficient capacity for the new CC the function will return
        an error.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CarrierCfg: CC configuration container.
        :param BandId: Band Id.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_UpdateCCinCCCfgMB({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {json.dumps(CarrierCfg, indent=2)}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        prach_handle.XDfePrach_UpdateCCinCCCfgMB(xprach, CCCfg_ptr, CCID, CarrierCfg_ptr, BandId)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_UpdateCCinCCCfg(self, device_id, CCCfg, CCID, CarrierCfg):
        """
        Updates specified CCID, with specified configuration to a local CC
        configuration structure on Band which Id = 0.
        If there is insufficient capacity for the new CC the function will return
        an error.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CarrierCfg: CC configuration container.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfePrach_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID}, {json.dumps(CarrierCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        CCCfg_ptr = ffi.new("XDfePrach_CCCfg *", CCCfg)
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        prach_handle.XDfePrach_UpdateCCinCCCfg(xprach, CCCfg_ptr, CCID, CarrierCfg_ptr)
        CCCfg = cdata_to_py(CCCfg_ptr[0])
        self.logger.debug(f"Return value CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfePrach_AddCC(self, device_id, CCID, BitSequence, CarrierCfg):
        """
        Add specified CCID, with specified configuration.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param BitSequence: up to 16 defined slots into which a CC can be
                            allocated. The number of slots can be from 1 to 16 depending on
                            system initialization. The number of slots is defined by the
                            "sequence length" parameter which is provided during initialization.
                            The Bit offset within the CCSeqBitmap indicates the equivalent
                            Slot number to allocate. e.g. 0x0003  means the caller wants the
                            passed component carrier (CC) to be allocated to slots 0 and 1.
        :param CarrierCfg: is a CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CarrierCfg: is a CC configuration container.
        """
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        self.logger.debug(f"XDfePrach_AddCC({device_id}, {CCID}, {BitSequence}, {json.dumps(CarrierCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddCC(xprach, CCID, BitSequence, CarrierCfg_ptr)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return ret, CarrierCfg

    def XDfePrach_RemoveCC(self, device_id, CCID):
        """
        Remove a CCID from sequence.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfePrach_RemoveCC({device_id}, {CCID})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_RemoveCC(xprach, CCID)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_UpdateCC(self, device_id, CCID, CarrierCfg):
        """
        Updates a CCID sequence.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param CarrierCfg: is carrier data container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *", CarrierCfg)
        self.logger.debug(f"XDfePrach_UpdateCC({device_id}, {CCID}, {json.dumps(CarrierCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_UpdateCC(xprach, CCID, CarrierCfg_ptr)
        self.logger.debug(f"The return value ret = {ret}")
        return ret

    def XDfePrach_GetCurrentRCCfg(self, device_id):
        """
        Reads all of the RC configuration back.

        :param device_id: id of the opened device.
        :return: RCCfg: RC configuration container.
        """
        self.logger.debug(f"XDfePrach_GetCurrentRCCfg({device_id})")
        RCCfg_ptr = ffi.new("XDfePrach_RCCfg *")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetCurrentRCCfg(xprach, RCCfg_ptr)
        RCCfg = cdata_to_py(RCCfg_ptr[0])
        self.logger.debug(f"RCCfg = {json.dumps(RCCfg, indent=2)}")
        return RCCfg

    def XDfePrach_GetEmptyRCCfg(self, device_id):
        """
        Returns the empty CC configuration.

        :param device_id: id of the opened device.
        :return: RCCfg: RC configuration container.
        """
        RCCfg_ptr = ffi.new("XDfePrach_RCCfg *")
        self.logger.debug(f"XDfePrach_GetEmptyRCCfg({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetEmptyRCCfg(xprach, RCCfg_ptr)
        RCCfg = cdata_to_py(RCCfg_ptr[0])
        return RCCfg

    def XDfePrach_GetChannelCfg(self, device_id, RCCfg, RCId):
        """
        Gets RACH channel configuration.

        :param device_id: id of the opened device.
        :param RCCfg: RC configuration container.
        :param RCId: Chosen RACH channel Id.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                ChannelCfg: RACH channel container.
        """
        RCCfg_ptr = ffi.new("XDfePrach_RCCfg *", RCCfg)
        ChannelCfg_ptr = ffi.new("XDfePrach_ChannelCfg *")
        self.logger.debug(f"XDfePrach_GetChannelCfg({device_id}, {RCId})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetChannelCfg(xprach, RCCfg_ptr, RCId, ChannelCfg_ptr)
        ChannelCfg = cdata_to_py(ChannelCfg_ptr[0])
        self.logger.debug(f"ret = ChannelCfg_ptr = {json.dumps(ChannelCfg, indent=2)}")
        return ChannelCfg

    def XDfePrach_AddRCtoRCCfgMB(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg, BandId):
        """
        Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param Schedule: is Schedule data container.
        :param NextCCCfg: CC configuration container.
        :param BandId: Band id.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_AddRCtoRCCfgMB({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddRCtoRCCfgMB(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr,
                                                  NextCCCfg_ptr, BandId)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return ret, CurrentRCCfg

    def XDfePrach_AddRCtoRCCfgMBDynamic(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, NextCCCfg, BandId):
        """
        Adds a new RC entry to the RC_CONFIGURATION in dynamic mode. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param NextCCCfg: CC configuration container.
        :param BandId: Band id.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_AddRCtoRCCfgMBDynamic({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(NextCCCfg, indent=2)}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddRCtoRCCfgMBDynamic(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, NextCCCfg_ptr, BandId)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return ret, CurrentRCCfg

    def XDfePrach_AddRCtoRCCfg(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg):
        """
        Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param Schedule: is Schedule data container.
        :param NextCCCfg: CC configuration container.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_AddRCtoRCCfg({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddRCtoRCCfg(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr,
                                                  NextCCCfg_ptr)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return ret, CurrentRCCfg

    def XDfePrach_AddRCtoRCCfgDynamic(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, NextCCCfg):
        """
        Adds a new RC entry to the RC_CONFIGURATION in dynamic mode. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param NextCCCfg: CC configuration container.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_AddRCtoRCCfgDynamic({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(NextCCCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddRCtoRCCfgDynamic(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, NextCCCfg_ptr)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return ret, CurrentRCCfg

    def XDfePrach_RemoveRCfromRCCfg(self, device_id, CurrentRCCfg, RCId):
        """
        Removes an RC configuration entry from the RC_CONFIGURATION. RCId must be
        same as the physical channel RachChan.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param RCId: is RC Id.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
                CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        self.logger.debug(f"XDfePrach_RemoveRCfromRCCfg({device_id}, {json.dumps(CurrentRCCfg, indent=2)}, {RCId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_RemoveRCfromRCCfg(xprach, CurrentRCCfg_ptr, RCId)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"ret = {ret}, CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return ret, CurrentRCCfg

    def XDfePrach_UpdateRCinRCCfgMB(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg, BandId):
        """
        Updates an RC entry to the RC_CONFIGURATION.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param Schedule: is Schedule data container.
        :param NextCCCfg: CC configuration container.
        :param BandId: Band id.
        :return: CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_UpdateRCinRCCfgMB({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_UpdateRCinRCCfgMB(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr,
                                                  NextCCCfg_ptr, BandId)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return CurrentRCCfg

    def XDfePrach_UpdateRCinRCCfg(self, device_id, CurrentRCCfg, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg):
        """
        Updates an RC entry to the RC_CONFIGURATION.

        :param device_id: id of the opened device.
        :param CurrentRCCfg: current PRACH configuration container
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param Schedule: is Schedule data container.
        :param NextCCCfg: CC configuration container.
        :return: CurrentRCCfg: current PRACH configuration container
        """
        CurrentRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", CurrentRCCfg)
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        self.logger.debug(f"XDfePrach_UpdateRCinRCCfg({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_UpdateRCinRCCfg(xprach, CurrentRCCfg_ptr, CCID, RCId,
                                                  RachChan, DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr,
                                                  NextCCCfg_ptr)
        CurrentRCCfg = cdata_to_py(CurrentRCCfg_ptr[0])
        self.logger.debug(f"CurrentRCCfg = {json.dumps(CurrentRCCfg, indent=2)}")
        return CurrentRCCfg

    def XDfePrach_SetNextCfg(self, device_id, NextCCCfg, NextRCCfg):
        """
        Writes local CC configuration to the shadow (NEXT) registers and triggers
        copying from shadow to operational registers.

        :param device_id: id of the opened device.
        :param NextCCCfg: a CC configuration container.
        :param NextRCCfg: a RC configuration container.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
        """
        NextCCCfg_ptr = ffi.new("XDfePrach_CCCfg *", NextCCCfg)
        NextRCCfg_ptr = ffi.new("XDfePrach_RCCfg *", NextRCCfg)
        self.logger.debug(f"XDfePrach_SetNextRCCfg({device_id}, {json.dumps(NextCCCfg, indent=2)}), {json.dumps(NextRCCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_SetNextCfg(xprach, NextCCCfg_ptr, NextRCCfg_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_UpdateRCCfg(self, device_id, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule):
        """
        Updates an RC entry to the RC_CONFIGURATION. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is PRACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param Schedule: is Schedule data container.
        :return: ret: XST_SUCCESS on success, XST_FAILURE on failure
        """
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        self.logger.debug(f"XDfePrach_UpdateRCCfg({device_id}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_UpdateRCCfg(xprach, CCID, RCId, RachChan,
                                                 DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_AddRCCfg(self, device_id, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule):
        """
        Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
        physical channel RachChan.

        :param device_id: id of the opened device.
        :param CCID: is CC Id.
        :param RCId: is RC Id.
        :param RachChan: is RACH channel.
        :param DdcCfg: is DDC data container.
        :param NcoCfg: is NCO data container.
        :param StaticSchedule: is Schedule data container.
        :return: ret: XST_SUCCESS on succes, XST_FAILURE on failure
                DdcCfg: is DDC data container.
                NcoCfg: is NCO data container.
                Schedule: is Schedule data container.        
        """
        DdcCfg_ptr = ffi.new("XDfePrach_DDCCfg *", DdcCfg)
        NcoCfg_ptr = ffi.new("XDfePrach_NCO *", NcoCfg)
        StaticSchedule_ptr = ffi.new("XDfePrach_Schedule *", StaticSchedule)
        self.logger.debug(f"XDfePrach_AddRCCfg({device_id}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_AddRCCfg(
            xprach, CCID, RCId, RachChan, DdcCfg_ptr, NcoCfg_ptr, StaticSchedule_ptr
        )
        DdcCfg = cdata_to_py(DdcCfg_ptr[0])
        NcoCfg = cdata_to_py(NcoCfg_ptr[0])
        StaticSchedule = cdata_to_py(StaticSchedule_ptr[0])
        self.logger.debug(f"ret = {ret}, DdcCfg = {json.dumps(DdcCfg, indent=2)}, NcoCfg = {json.dumps(NcoCfg, indent=2)}, StaticSchedule = {json.dumps(StaticSchedule, indent=2)}")
        return ret, DdcCfg, NcoCfg, StaticSchedule

    def XDfePrach_RemoveRC(self, device_id, RCId):
        """
        Removes an RC configuration entry from the RC_CONFIGURATION.

        :param device_id: id of the opened device.
        :param RCId: is RC Id.
        :return: ret: XST_SUCCESS on succes, XST_FAILURE on failure
        """
        self.logger.debug(f"XDfePrach_RemoveRC({device_id}, {RCId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_RemoveRC(xprach, RCId)
        self.logger.debug(f"The return value ret = {ret}")
        return ret

    def XDfePrach_MoveRC(self, device_id, RCId, ToChannel):
        """
        Move specified RCID from one NCO & Decimation Channel to another NCO &&
        Decimation Channel.

        :param device_id: id of the opened device.
        :param RCId: is RC Id.
        :param ToChannel: is destination channel Id.
        :return: ret: XST_SUCCESS on succes, XST_FAILURE on failure
        """
        self.logger.debug(f"XDfePrach_MoveRC({device_id}, {RCId}, {ToChannel})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_MoveRC(xprach, RCId, ToChannel)
        self.logger.debug(f"The return value ret = {ret}")
        return ret

    def XDfePrach_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: Trigger configuration container
        """
        TriggerCfg_ptr = ffi.new("XDfePrach_TriggerCfg *")
        self.logger.debug(f"XDfePrach_GetTriggersCfg({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetTriggersCfg(xprach, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"The return value TriggerCfg = {TriggerCfg}")
        return TriggerCfg

    def XDfePrach_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: Trigger configuration container.
        :return: TriggerCfg: Trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfePrach_TriggerCfg *", TriggerCfg)
        self.logger.debug(f"XDfePrach_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_SetTriggersCfg(xprach, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfePrach_GetCC(self, device_id, Next, CCID):
        """
        Get specified CCID carrier configuration from either Current or Next
        for band id 0.

        :param device_id: id of the opened device.
        :param Next: is next or current data flag.
        :param CCID: is component carrier id number.
        :return: CarrierCfg: Carrier config container.
        """
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *")
        self.logger.debug(f"XDfePrach_GetCC({device_id}, {Next}, {CCID})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetCC(xprach, Next, CCID, CarrierCfg_ptr)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return CarrierCfg

    def XDfePrach_GetCCMB(self, device_id, Next, CCID, BandId):
        """
        Get specified CCID carrier configuration from either Current or Next
        for selected band in multi-band mode.

        :param device_id: id of the opened device.
        :param Next: is next or current data flag.
        :param CCID: is component carrier id number.
        :param BandId: is Band Id.
        :return: CarrierCfg: Carrier config container.
        """
        CarrierCfg_ptr = ffi.new("XDfePrach_CarrierCfg *")
        self.logger.debug(f"XDfePrach_GetCC({device_id}, {Next}, {CCID}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetCCMB(xprach, Next, CCID, CarrierCfg_ptr, BandId)
        CarrierCfg = cdata_to_py(CarrierCfg_ptr[0])
        self.logger.debug(f"CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return CarrierCfg

    def XDfePrach_GetStatus(self, device_id):
        """
        Get PRACH Status.

        :param device_id: id of the opened device.
        :return: Status: Status data container.
        """
        Status_ptr = ffi.new("XDfePrach_Status *")
        self.logger.debug(f"XDfePrach_GetStatus({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetStatus(xprach, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfePrach_ClearStatus(self, device_id):
        """
        Clear the PRACH status registers.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_ClearStatus({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_ClearStatus(xprach)
        return

    def XDfePrach_CapturePhase(self, device_id):
        """
        Captures phase for all phase accumulators in associated AXI-lite registers.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_CapturePhase({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_CapturePhase(xprach)
        return

    def XDfePrach_GetCapturePhase(self, device_id, RachChan):
        """
        Reads the captured phase for a given Rach Channel.

        :param device_id: id of the opened device.
        :param RachChan: is RACH channel Id.
        :return: NCO data container.
        """
        CapturedPhase_ptr = ffi.new("XDfePrach_NCO *")
        self.logger.debug(f"XDfePrach_GetCapturePhase({device_id}, {RachChan})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetCapturePhase(xprach, RachChan, CapturedPhase_ptr)
        CapturedPhase = cdata_to_py(CapturedPhase_ptr[0])
        self.logger.debug(f"CapturedPhase = {json.dumps(CapturedPhase, indent=2)}")
        return CapturedPhase

    def XDfePrach_GetInterruptMask(self, device_id):
        """
        Gets interrupt mask status.

        :param device_id: id of the opened device.
        :return: Mask: interrupt masks container.
        """
        Mask_ptr = ffi.new("XDfePrach_InterruptMask *")
        self.logger.debug(f"XDfePrach_GetInterruptMask({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetInterruptMask(xprach, Mask_ptr)
        Mask = cdata_to_py(Mask_ptr[0])
        self.logger.debug(f"Mask = {json.dumps(Mask, indent=2)}")
        return Mask

    def XDfePrach_SetInterruptMask(self, device_id, Mask):
        """
        Sets interrupt mask.

        :param device_id: id of the opened device.
        :param Mask: interrupt masks container.
                     0 - does not mask coresponding interrupt
                     1 - masks coresponding interrupt
        :return: None
        """
        Mask_ptr = ffi.new("XDfePrach_InterruptMask *", Mask)
        self.logger.debug(f"XDfePrach_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_SetInterruptMask(xprach, Mask_ptr)
        return

    def XDfePrach_GetEventStatus(self, device_id):
        """
        Gets event status.

        :param device_id: id of the opened device.
        :return: Status: event status container.
        """
        Status_ptr = ffi.new("XDfePrach_StatusMask *")
        self.logger.debug(f"XDfePrach_GetEventStatus({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetEventStatus(xprach, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfePrach_ClearEventStatus(self, device_id, Status):
        """
        Clears event status.

        :param device_id: id of the opened device.
        :param Status: Clear event status container.
                       0 - does not clear coresponding event status
                       1 - clear coresponding event status
        :return: None
        """
        Status_ptr = ffi.new("XDfePrach_StatusMask *", Status)
        self.logger.debug(f"XDfePrach_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_ClearEventStatus(xprach, Status_ptr)
        return

    def XDfePrach_SetTUserDelay(self, device_id, Delay):
        """
        Sets the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :param Delay: requested delay variable.
        :return: None
        """
        self.logger.debug(f"XDfePrach_SetTUserDelay({device_id}, {Delay})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_SetTUserDelay(xprach, Delay)
        return

    def XDfePrach_SetTUserDelayMB(self, device_id, Delay, BandId):
        """
        Sets the delay of specified band in multiband mode, which will be added
        to TUSER and TLAST (delay matched through the IP).

        :param device_id: id of the opened device.
        :param Delay: requested delay variable.
        :param BandId: is Band Id.
        :return: None
        """
        self.logger.debug(f"XDfePrach_SetTUserDelayMB({device_id}, {Delay}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_SetTUserDelayMB(xprach, Delay, BandId)
        return

    def XDfePrach_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfePrach_GetTUserDelay({device_id})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_GetTUserDelay(xprach)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetTUserDelayMB(self, device_id, BandId):
        """
        Reads the delay of specified band in multiband mode, which will be
        added to TUSER and TLAST (delay matched through the IP).

        :param device_id: id of the opened device.
        :param BandId: is Band Id.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfePrach_GetTUserDelayMB({device_id}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_GetTUserDelayMB(xprach, BandId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetTDataDelay(self, device_id):
        """
        Returns data latency.

        :param device_id: id of the opened device.
        :return: ret: data latency value.
        """
        self.logger.debug(f"XDfePrach_GetTDataDelay({device_id})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_GetTDataDelay(xprach)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetTDataDelayMB(self, device_id, BandId):
        """
        Returns data latency of specified band in multiband mode.

        :param device_id: id of the opened device.
        :param BandId: is Band Id.
        :return: ret: data latency value.
        """
        self.logger.debug(f"XDfePrach_GetTDataDelayMB({device_id}, {BandId})")
        xprach = self.prach_dict[device_id][1]
        ret = prach_handle.XDfePrach_GetTDataDelayMB(xprach, BandId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetVersions(self, device_id):
        """
        This API gets the driver and HW design version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        SwVersion_ptr = ffi.new("XDfePrach_Version *")
        HwVersion_ptr = ffi.new("XDfePrach_Version *")
        self.logger.debug(f"XDfePrach_GetVersions({device_id})")
        xprach = self.prach_dict[device_id][1]
        prach_handle.XDfePrach_GetVersions(xprach, SwVersion_ptr, HwVersion_ptr)
        SwVersion = cdata_to_py(SwVersion_ptr[0])
        HwVersion = cdata_to_py(HwVersion_ptr[0])
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        self.logger.info("Inside PRACH Destructor")
