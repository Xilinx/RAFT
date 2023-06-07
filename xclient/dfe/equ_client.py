# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64
import json
import sys


class EQU_Client(object):
    EQU = None
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
        self.logger.info("Inside RFDC Pyro Client Constructor")
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

    @staticmethod
    def extract_b64_encoded_string(DictName):
        b64_data = DictName['data']
        b64_bytes_data = b64_data.encode('ascii')
        msg_bytes_data = base64.b64decode(b64_bytes_data)
        data = msg_bytes_data.decode('ascii')
        data = bytes(data, 'utf-8')
        return data

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform EQU Client the IP address and port number of EQU Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:EQU@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.EQU = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.EQU.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.EQU.SetServerLogLevel(PythonLogLevel)
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
        self.EQU.SetMetalLogLevel(MetalLogLevel)
        return

    # Get enum API
    def GetEnum_XDfeEqu_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeEqu_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeEqu_StateId
        """
        self.logger.debug("GetEnum_XDfeEqu_StateId()")
        XDfeEqu_StateId = self.EQU.GetEnum_XDfeEqu_StateId()
        self.logger.debug(f"XDfeEqu_StateId = {json.dumps(XDfeEqu_StateId, indent=2)}")
        return XDfeEqu_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.EQU.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    # Get structure  API
    def GetStruct_XDfeEqu_Version(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Version
        """
        self.logger.debug("GetStruct_XDfeEqu_Version()")
        XDfeEqu_Version = self.EQU.GetStruct_XDfeEqu_Version()
        return XDfeEqu_Version

    def GetStruct_XDfeEqu_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Trigger
        """
        self.logger.debug("GetStruct_XDfeEqu_Trigger()")
        XDfeEqu_Trigger = self.EQU.GetStruct_XDfeEqu_Trigger()
        return XDfeEqu_Trigger

    def GetStruct_XDfeEqu_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_TriggerCfg
        """
        self.logger.debug("GetStruct_XDfeEqu_TriggerCfg()")
        XDfeEqu_TriggerCfg = self.EQU.GetStruct_XDfeEqu_TriggerCfg()
        return XDfeEqu_TriggerCfg

    def GetStruct_XDfeEqu_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_ModelParameters
        """
        self.logger.debug("GetStruct_XDfeEqu_ModelParameters()")
        XDfeEqu_ModelParameters = self.EQU.GetStruct_XDfeEqu_ModelParameters()
        return XDfeEqu_ModelParameters

    def GetStruct_XDfeEqu_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Cfg
        """
        self.logger.debug("GetStruct_XDfeEqu_Cfg()")
        XDfeEqu_Cfg = self.EQU.GetStruct_XDfeEqu_Cfg()
        return XDfeEqu_Cfg

    def GetStruct_XDfeEqu_Coefficients(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Coefficients
        """
        self.logger.debug("GetStruct_XDfeEqu_Coefficients()")
        XDfeEqu_Coefficients = self.EQU.GetStruct_XDfeEqu_Coefficients()
        return XDfeEqu_Coefficients

    def GetStruct_XDfeEqu_EqConfig(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_EqConfig

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_EqConfig
        """
        self.logger.debug("GetStruct_XDfeEqu_EqConfig()")
        XDfeEqu_EqConfig = self.EQU.GetStruct_XDfeEqu_EqConfig()
        return XDfeEqu_EqConfig

    def GetStruct_XDfeEqu_Status(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Status
        """
        self.logger.debug("GetStruct_XDfeEqu_Status()")
        XDfeEqu_Status = self.EQU.GetStruct_XDfeEqu_Status()
        return XDfeEqu_Status

    def GetStruct_XDfeEqu_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_InterruptMask
        """
        self.logger.debug("GetStruct_XDfeEqu_InterruptMask()")
        XDfeEqu_InterruptMask = self.EQU.GetStruct_XDfeEqu_InterruptMask()
        return XDfeEqu_InterruptMask

    def GetStruct_XDfeEqu_Config(self):
        """
        Return Dictionary equivalent of structure XDfeEqu_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu_Config
        """
        self.logger.debug("GetStruct_XDfeEqu_Config()")
        XDfeEqu_Config = self.EQU.GetStruct_XDfeEqu_Config()
        return XDfeEqu_Config

    def GetStruct_XDfeEqu(self):
        """
        Return Dictionary equivalent of structure XDfeEqu

        :param : None
        :return: Dictionary equivalent of structure XDfeEqu
        """
        self.logger.debug("GetStruct_XDfeEqu()")
        XDfeEqu = self.EQU.GetStruct_XDfeEqu()
        return XDfeEqu

    # System initialization API
    def XDfeEqu_InstanceInit(self, DeviceNodeName):
        """
        API initialises one instance of an Equalizer driver.
        Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
        EQU device with the name DeviceNodeName. The first available slot in
        the instances array XDfeEqu_ChFilter[] will be taken as a DeviceNodeName
        object. On success it moves the state machine to a Ready state, while on
        failure stays in a Not Ready state.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to initialized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value

        """
        self.logger.info(f"XDfeEqu_InstanceInit({DeviceNodeName})")
        DeviceNodeName = bytes(str(DeviceNodeName), 'utf-8')
        ret, device_id, DeviceNodeName = self.EQU.XDfeEqu_InstanceInit(DeviceNodeName)
        DeviceNodeName = self.extract_b64_encoded_string(DeviceNodeName)
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeName = {DeviceNodeName}")
        return ret, device_id, DeviceNodeName

    def XDfeEqu_InstanceClose(self, device_id):
        """
        API closes the instance of an Equalizer driver.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeEqu_InstanceClose({device_id})")
        self.EQU.XDfeEqu_InstanceClose(device_id)
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
        self.EQU.XDfeEqu_WriteReg(device_id, addr_offset, data)
        return

    def XDfeEqu_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from the register using an Equalizer instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :return: Register value.
        """
        self.logger.debug(f"XDfeEqu_ReadReg({device_id}, {hex(addr_offset)})")
        regval = self.EQU.XDfeEqu_ReadReg(device_id, addr_offset)
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
        self.EQU.XDfeEqu_Reset(device_id)
        return

    def XDfeEqu_Configure(self, device_id, Cfg):
        """
        Reads configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: device config container.
        :return: Cfg: device config container.
        """
        self.logger.debug(f"XDfeEqu_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        Cfg = self.EQU.XDfeEqu_Configure(device_id, Cfg)
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeEqu_Initialize(self, device_id, EqConfig):
        """
        DFE Equalizer driver one time initialisation and moves the state machine to
        an Initialised state.

        :param device_id: id of the opened device.
        :param Config: configuration data container.
        :return: Config: configuration data container.
        """
        self.logger.debug(f"XDfeEqu_Initialize({device_id}, {json.dumps(EqConfig, indent=2)})")
        EqConfig = self.EQU.XDfeEqu_Initialize(device_id, EqConfig)
        self.logger.debug(f"Init = {json.dumps(EqConfig, indent=2)}")
        return EqConfig

    def XDfeEqu_Activate(self, device_id, EnableLowPower):
        """
        Activates channel Equalizer moves the state machine to an Activated state.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_Activate({device_id}, {EnableLowPower})")
        self.EQU.XDfeEqu_Activate(device_id, EnableLowPower)
        return

    def XDfeEqu_Deactivate(self, device_id):
        """
        Deactivates Equalizer and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeEqu_Deactivate({device_id})")
        self.EQU.XDfeEqu_Deactivate(device_id)
        return

    def XDfeEqu_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeEqu_GetStateID({device_id})")
        StateId = self.EQU.XDfeEqu_GetStateID(device_id)
        self.logger.debug(f"Return value StateId = {StateId}")
        return StateId

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
        self.logger.debug(f"XDfeEqu_Update({device_id}, {json.dumps(Config, indent=2)})")
        Config = self.EQU.XDfeEqu_Update(device_id, Config)
        self.logger.debug(f"Config = {json.dumps(Config, indent=2)}")
        return Config

    def XDfeEqu_GetTriggersCfg(self, device_id):
        """
        Returns current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeEqu_GetTriggersCfg({device_id})")
        TriggerCfg = self.EQU.XDfeEqu_GetTriggersCfg(device_id)
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeEqu_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a triger configuration container.
        :return: TriggerCfg: is a triger configuration container.
        """
        self.logger.debug(f"XDfeEqu_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        TriggerCfg = self.EQU.XDfeEqu_SetTriggersCfg(device_id, TriggerCfg)
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
        self.logger.debug(f"XDfeEqu_LoadCoefficients({device_id}, {ChannelField}, {Mode}, {Shift}, {json.dumps(EqCoeffs, indent=2)})")
        EqCoeffs = self.EQU.XDfeEqu_LoadCoefficients(
            device_id, ChannelField, Mode, Shift, EqCoeffs
        )
        self.logger.debug(f"EqCoeffs = {EqCoeffs}")
        return EqCoeffs

    def XDfeEqu_GetEventStatus(self, device_id):
        """
        Gets Equalizer event status

        :param device_id: id of the opened device.
        :return: Status: event status
        """
        self.logger.debug(f"XDfeEqu_GetEventStatus({device_id})")
        Status = self.EQU.XDfeEqu_GetEventStatus(device_id)
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
        self.logger.debug(f"XDfeEqu_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        self.EQU.XDfeEqu_ClearEventStatus(device_id, Status)
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
        self.logger.debug(f"XDfeEqu_SetInterruptMask({device_id}, {json.dumps(InterruptMask, indent=2)})")
        self.EQU.XDfeEqu_SetInterruptMask(device_id, InterruptMask)
        return

    def XDfeEqu_GetInterruptMask(self, device_id):
        """
        Gets interrupt mask.

        :param device_id: id of the opened device.
        :return: InterruptMask: Equalizer interrupt mask container.
        """
        self.logger.debug(f"XDfeEqu_GetInterruptMask({device_id})")
        InterruptMask = self.EQU.XDfeEqu_GetInterruptMask(device_id)
        self.logger.debug(f"InterruptMask = {json.dumps(InterruptMask, indent=2)}")
        return InterruptMask

    def XDfeEqu_GetActiveSets(self, device_id):
        """
        Gets used coefficients settings.

        :param device_id: id of the opened device.
        :return: RealSet: Real value
                 ImagSet: Imaginary value
        """
        self.logger.debug(f"XDfeEqu_GetActiveSets({device_id})")
        RealSet, ImagSet = self.EQU.XDfeEqu_GetActiveSets(device_id)
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
        self.EQU.XDfeEqu_SetTUserDelay(device_id, Delay)
        return

    def XDfeEqu_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfeEqu_GetTUserDelay({device_id})")
        ret = self.EQU.XDfeEqu_GetTUserDelay(device_id)
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
        ret = self.EQU.XDfeEqu_GetTDataDelay(device_id, Tap)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeEqu_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        self.logger.debug(f"XDfeEqu_GetVersions({device_id})")
        SwVersion, HwVersion = self.EQU.XDfeEqu_GetVersions(device_id)
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

equ = EQU_Client()
