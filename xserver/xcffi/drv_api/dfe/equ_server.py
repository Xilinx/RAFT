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

equ_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/dfe/xdfeequ_python.h", "/usr/lib/libdfeequ.so.1")


class EQU(object):
    equ_dict = {}
    device_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error(f"EQU: XHelper_MetalInit failed. ret = {ret}")
        self.logger.info("Inside EQU Constructor")
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

    # Get enum API
    def GetEnum_XDfeEqu_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeEqu_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeEqu_StateId
        """
        XDfeEqu_StateId = ffi.typeof("enum XDfeEqu_StateId").relements
        self.logger.debug(f"XDfeEqu_StateId = {json.dumps(XDfeEqu_StateId, indent=2)}")
        return XDfeEqu_StateId

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
    def GetStruct_XDfeEqu_Version(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Version
        """
        XDfeEqu_Version_ptr = ffi.new("XDfeEqu_Version *")
        XDfeEqu_Version = cdata_to_py(XDfeEqu_Version_ptr[0])
        return XDfeEqu_Version

    def GetStruct_XDfeEqu_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Trigger
        """
        XDfeEqu_Trigger_ptr = ffi.new("XDfeEqu_Trigger *")
        XDfeEqu_Trigger = cdata_to_py(XDfeEqu_Trigger_ptr[0])
        return XDfeEqu_Trigger

    def GetStruct_XDfeEqu_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_TriggerCfg
        """
        XDfeEqu_TriggerCfg_ptr = ffi.new("XDfeEqu_TriggerCfg *")
        XDfeEqu_TriggerCfg = cdata_to_py(XDfeEqu_TriggerCfg_ptr[0])
        return XDfeEqu_TriggerCfg

    def GetStruct_XDfeEqu_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_ModelParameters
        """
        XDfeEqu_ModelParameters_ptr = ffi.new("XDfeEqu_ModelParameters *")
        XDfeEqu_ModelParameters = cdata_to_py(XDfeEqu_ModelParameters_ptr[0])
        return XDfeEqu_ModelParameters

    def GetStruct_XDfeEqu_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Cfg
        """
        XDfeEqu_Cfg_ptr = ffi.new("XDfeEqu_Cfg *")
        XDfeEqu_Cfg = cdata_to_py(XDfeEqu_Cfg_ptr[0])
        return XDfeEqu_Cfg

    def GetStruct_XDfeEqu_Coefficients(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Coefficients
        """
        XDfeEqu_Coefficients_ptr = ffi.new("XDfeEqu_Coefficients *")
        XDfeEqu_Coefficients = cdata_to_py(XDfeEqu_Coefficients_ptr[0])
        return XDfeEqu_Coefficients

    def GetStruct_XDfeEqu_EqConfig(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_EqConfig

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_EqConfig
        """
        XDfeEqu_EqConfig_ptr = ffi.new("XDfeEqu_EqConfig *")
        XDfeEqu_EqConfig = cdata_to_py(XDfeEqu_EqConfig_ptr[0])
        return XDfeEqu_EqConfig

    def GetStruct_XDfeEqu_Status(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Status
        """
        XDfeEqu_Status_ptr = ffi.new("XDfeEqu_Status *")
        XDfeEqu_Status = cdata_to_py(XDfeEqu_Status_ptr[0])
        return XDfeEqu_Status

    def GetStruct_XDfeEqu_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_InterruptMask
        """
        XDfeEqu_InterruptMask_ptr = ffi.new("XDfeEqu_InterruptMask *")
        XDfeEqu_InterruptMask = cdata_to_py(XDfeEqu_InterruptMask_ptr[0])
        return XDfeEqu_InterruptMask

    def GetStruct_XDfeEqu_Config(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Config
        """
        XDfeEqu_Config_ptr = ffi.new("XDfeEqu_Config *")
        XDfeEqu_Config = cdata_to_py(XDfeEqu_Config_ptr[0])
        return XDfeEqu_Config

    def GetStruct_XDfeEqu(self):
        """
        Return Dictionary equivalent of structure XDfeEqu

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu
        """
        XDfeEqu_ptr = ffi.new("XDfeEqu *")
        XDfeEqu = cdata_to_py(XDfeEqu_ptr[0])
        return XDfeEqu

    # System initialization API
    def XDfeEqu_InstanceInit(self, DeviceNodeName):
        """
        API initialises one instance of an Equalizer driver.
        Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
        EQU device with the name DeviceNodeName. The first available slot in
        the instances array XDfeEqu_ChFilter[] will be taken as a DeviceNodeName
        object.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to initialized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value

        """
        DeviceNodeName = extract_b64_encoded_string(DeviceNodeName)
        cptrDeviceNodeName = ffi.new("char[128]", DeviceNodeName)
        self.logger.info(f"XDfeEqu_InstanceInit DeviceNodeName = {DeviceNodeName}")
        # Pass the device node name to the driver
        xequ = equ_handle.XDfeEqu_InstanceInit(cptrDeviceNodeName)
        self.logger.info(f"The initalized pointer value = {xequ}")
        DeviceNodeNameRet = cdata_string_to_py(cptrDeviceNodeName);
        if xequ == ffi.NULL:
            # if driver returns NULL, pass it as error to user
            ret = 1        
            self.logger.error(f"The pointer returned for {DeviceNodeName} is NULL")
            device_id = 0xFFFFFFFF
        else:
            # otherwise treat as success
            ret = 0        
            # In equ_dict dictionary, device id is the key.
            # device node name and instance pointer from driver are values as list
            # check if the device node name is already present in dictionary
            found, device_id = getkey_from_listbeginvalue(self.equ_dict, DeviceNodeName)
            if 1 == found:
                # if found, update the device id key with values
                self.equ_dict[device_id][0] = DeviceNodeNameRet 
                self.equ_dict[device_id][1] = xequ                            
            else:
                # if not found, make new device_id from class variable
                # and increment the class variable
                device_id = self.device_id
                self.device_id += 1
                # add new key and values to the dictionary
                self.equ_dict[device_id] = [DeviceNodeNameRet, xequ]            
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeNameRet = {DeviceNodeNameRet}")
        return ret, device_id, DeviceNodeNameRet

    def XDfeEqu_InstanceClose(self, device_id):
        """
        API closes the instance of an Equalizer driver and moves the state machine
        to a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeEqu_InstanceClose({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_InstanceClose(xequ)
        if device_id in self.equ_dict:
            del self.equ_dict[device_id]        
        return

    # Register access API
    def XDfeEqu_WriteReg(self, device_id, addr_offset, data):
        """
        Writes value to register in an Equalizer instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :param Data: is value to be written.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_WriteReg({device_id}, {hex(addr_offset)}, {hex(data)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_WriteReg(xequ, addr_offset, data)
        return

    def XDfeEqu_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from the register using an Equalizer instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :return: Register value.
        """
        self.logger.debug(f"ret = XDfeEqu_ReadReg({device_id}, {hex(addr_offset)})")
        xequ = self.equ_dict[device_id][1]
        regval = equ_handle.XDfeEqu_ReadReg(xequ, addr_offset)
        self.logger.debug(f"regval = {regval}")
        return regval

    # DFE Equalizer component initialization API
    def XDfeEqu_Reset(self, device_id):
        """
        Resets Equalizer and puts block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_Reset({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Reset(xequ)
        return

    def XDfeEqu_Configure(self, device_id, Cfg):
        """
        Reads configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: device config container.
        :return: Cfg: device config container.
        """
        Cfg_ptr = ffi.new("XDfeEqu_Cfg *", Cfg)
        self.logger.debug(f"XDfeEqu_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Configure(xequ, Cfg_ptr)
        Cfg = cdata_to_py(Cfg_ptr[0])
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeEqu_Initialize(self, device_id, Config):
        """
        DFE Equalizer driver one time initialisation and moves the state machine to
        an Initialised state.

        :param device_id: id of the opened device.
        :param Config: configuration data container.
        :return: Config: configuration data container.
        """
        Config_ptr = ffi.new("XDfeEqu_EqConfig *", Config)
        self.logger.debug(f"XDfeEqu_Initialize({device_id}, {json.dumps(Config, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Initialize(xequ, Config_ptr)
        Config = cdata_to_py(Config_ptr[0])
        self.logger.debug(f"Init = {json.dumps(Config, indent=2)}")
        return Config

    def XDfeEqu_Activate(self, device_id, EnableLowPower):
        """
        Activates channel Equalizer moves the state machine to an Activated state.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_Activate({device_id}, {EnableLowPower})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Activate(xequ, EnableLowPower)
        return

    def XDfeEqu_Deactivate(self, device_id):
        """
        Deactivates Equalizer and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_Deactivate({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Deactivate(xequ)
        return

    def XDfeEqu_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeEqu_GetStateID({device_id})")
        xequ = self.equ_dict[device_id][1]
        StateId = equ_handle.XDfeEqu_GetStateID(xequ)
        StateId_edict = ffi.typeof("XDfeEqu_StateId").elements
        self.logger.debug(f"Return value = {json.dumps(StateId, indent=2)}")
        return StateId_edict[StateId]

    # User APIs
    def XDfeEqu_Update(self, device_id, Config):
        """
        The software first sets bits 7:4 of the Next Control register (0x24) with
        the values in Config.Real_Datapath_Set, Config.Im_Datapath_Set.
        In real mode bits, 5:4 are set to the value held in
        Config.Real_Datapath_Set.
        Bits 7:6 are set to the value held in Config.Real_Datapath_Set.
        In complex mode bits, 5:4 are set to the value held in value
        Config.Real_Datapath_Set. Bits 7:6 are set to the value held in
        Config.Real_Datapath_Set plus 1.
        In matrix mode bits 5:4 are set to the value held in
        Config.Real_Datapath_Set. Bits 7:6 are set to the value held in
        Config.Im_Datapath_Set.
        The software sets bit 1 depending on Config.Flush.
        The software then sets the _Enable bit in the Next Control Trigger
        Source register (0x28) high.

        :param device_id: id of the opened device.
        :param Config: configuration container
        :return: Config: configuration container
        """
        Config_ptr = ffi.new("XDfeEqu_EqConfig *", Config)
        self.logger.debug(f"XDfeEqu_Update({device_id}, {json.dumps(Config, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_Update(xequ, Config_ptr)
        Config = cdata_to_py(Config_ptr[0])
        self.logger.debug(f"Config = {json.dumps(Config, indent=2)}")
        return Config

    def XDfeEqu_GetTriggersCfg(self, device_id):
        """
        Returns current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: is a trigger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeEqu_TriggerCfg *")
        self.logger.debug(f"XDfeEqu_GetTriggersCfg({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_GetTriggersCfg(xequ, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeEqu_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a triger configuration container.
        :return: TriggerCfg: is a triger configuration container.
        """
        TriggerCfg_ptr = ffi.new("XDfeEqu_TriggerCfg *", TriggerCfg)
        self.logger.debug(f"XDfeEqu_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_SetTriggersCfg(xequ, TriggerCfg_ptr)
        TriggerCfg = cdata_to_py(TriggerCfg_ptr[0])
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeEqu_LoadCoefficients(self, device_id, ChannelField, Mode, Shift, EqCoeffs):
        """
        Sets Equalizer filter coefficients in Real, Complex or Matrix mode.

        :param device_id: id of the opened device.
        :param ChannelField: is a flag in which bits indicate the channel is enabled.
        :param Mode: is an equalizer mode.
        :param Shift: is a coefficient shift value.
        :param EqCoeffs: is equalizer coefficients container.
        :return: EqCoeffs: is equalizer coefficients container.
        """
        EqCoeffs_ptr = ffi.new("XDfeEqu_Coefficients *", EqCoeffs)
        self.logger.debug(f"XDfeEqu_LoadCoefficients({device_id}, {ChannelField}, {Mode}, {Shift}, {json.dumps(EqCoeffs, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_LoadCoefficients(xequ, ChannelField, Mode, Shift, EqCoeffs_ptr)
        EqCoeffs = cdata_to_py(EqCoeffs_ptr[0])
        self.logger.debug(f"EqCoeffs = {EqCoeffs}")
        return EqCoeffs

    def XDfeEqu_GetEventStatus(self, device_id):
        """
        Gets Equalizer event status

        :param device_id: id of the opened device.
	    :return: Status: event status
        """
        Status_ptr = ffi.new("XDfeEqu_Status *")
        self.logger.debug(f"XDfeEqu_GetEventStatus({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_GetEventStatus(xequ, Status_ptr)
        Status = cdata_to_py(Status_ptr[0])
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeEqu_ClearEventStatus(self, device_id, Status):
        """
        Clears Equalizer status. The channel status will be cleared for any IStatus
        or QStatus not equal 0.
        Note: The Status registers are only present for a given channel when it
              is present in the configured IP. The number of channels present is
              given by CONFIG.NUM_CHANNELS.        

        :param device_id: id of the opened device.
        :param Status: event status.
        :return: None
        """
        Status_ptr = ffi.new("XDfeEqu_Status *", Status)
        self.logger.debug(f"XDfeEqu_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_ClearEventStatus(xequ, Status_ptr)
        return

    def XDfeEqu_SetInterruptMask(self, device_id, InterruptMask):
        """
        Enables an Equalizer status for channel ID.
        Note: The Status Mask registers are only present for a given channel when
               it is present in the configured IP. The number of channels present
               is given by CONFIG.NUM_CHANNELS.
               
        :param device_id: id of the opened device.
        :param InterruptMask: interrupt mask value
        :return: None
        """
        InterruptMask_ptr = ffi.new("XDfeEqu_InterruptMask *", InterruptMask)
        self.logger.debug(f"XDfeEqu_SetInterruptMask({device_id}, {json.dumps(InterruptMask, indent=2)})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_SetInterruptMask(xequ, InterruptMask_ptr)
        return

    def XDfeEqu_GetInterruptMask(self, device_id):
        """
        Gets interrupt mask.

        :param device_id: id of the opened device.
        :return: InterruptMask: Equalizer interrupt mask container.
        """
        InterruptMask_ptr = ffi.new("XDfeEqu_InterruptMask *")
        self.logger.debug(f"XDfeEqu_GetInterruptMask({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_GetInterruptMask(xequ, InterruptMask_ptr)
        InterruptMask = cdata_to_py(InterruptMask_ptr[0])
        self.logger.debug(f"InterruptMask = {json.dumps(InterruptMask, indent=2)}")
        return InterruptMask

    def XDfeEqu_GetActiveSets(self, device_id):
        """
        Gets used coefficients settings.

        :param device_id: id of the opened device.
        :return: RealSet: Real value
                 ImagSet: Imaginary value
        """
        RealSet_ptr = ffi.new("u32 *")
        ImagSet_ptr = ffi.new("u32 *")
        self.logger.debug(f"XDfeEqu_GetActiveSets({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_GetActiveSets(xequ, RealSet_ptr, ImagSet_ptr)
        RealSet = RealSet_ptr[0]
        ImagSet = ImagSet_ptr[0]
        self.logger.debug(f"RealSet = {json.dumps(RealSet, indent=2)}, ImagSet = {json.dumps(ImagSet, indent=2)}")
        return RealSet, ImagSet

    def XDfeEqu_SetTUserDelay(self, device_id, Delay):
        """
        Sets the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :param Delay: requested delay variable.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_SetTUserDelay({device_id}, {Delay})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_SetTUserDelay(xequ, Delay)
        return

    def XDfeEqu_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfeEqu_GetTUserDelay({device_id})")
        xequ = self.equ_dict[device_id][1]
        ret = equ_handle.XDfeEqu_GetTUserDelay(xequ)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeEqu_GetTDataDelay(self, device_id, Tap):
        """
        Returns CONFIG.DATA_LATENCY.VALUE + tap, where the tap is between 0
        and 23 in real mode and between 0 and 11 in complex/matrix mode.

        :param device_id: id of the opened device.
        :param Tap: is a tap variable.
        :return: ret: data latency value.
        """
        self.logger.debug(f"XDfeEqu_GetTDataDelay({device_id}, {Tap})")
        xequ = self.equ_dict[device_id][1]
        ret = equ_handle.XDfeEqu_GetTDataDelay(xequ, Tap)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeEqu_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        SwVersion_ptr = ffi.new("XDfeEqu_Version *")
        HwVersion_ptr = ffi.new("XDfeEqu_Version *")
        self.logger.debug(f"XDfeEqu_GetVersions({device_id})")
        xequ = self.equ_dict[device_id][1]
        equ_handle.XDfeEqu_GetVersions(xequ, SwVersion_ptr, HwVersion_ptr)
        SwVersion = cdata_to_py(SwVersion_ptr[0])
        HwVersion = cdata_to_py(HwVersion_ptr[0])
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        self.logger.info("Inside EQU Destructor")
