# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64
import json
import sys


class PRACH_Client(object):
    PRACH = None
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
        self.logger.info("Inside Prach Pyro Client Constructor")
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
        API to inform PRACH Client the IP address and port number of PRACH Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """    
        uri = f"PYRO:PRACH@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.PRACH = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.PRACH.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.PRACH.SetServerLogLevel(PythonLogLevel)
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
        self.PRACH.SetMetalLogLevel(MetalLogLevel)
        return

    def GetEnum_XDfePrach_StateId(self):
        """
        Return Dictionary equivalent of enum XDfePrach_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfePrach_StateId
        """
        self.logger.debug("GetEnum_XDfePrach_StateId()")
        XDfePrach_StateId = self.PRACH.GetEnum_XDfePrach_StateId()
        self.logger.debug(f"XDfePrach_StateId = {json.dumps(XDfePrach_StateId, indent=2)}")
        return XDfePrach_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.PRACH.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    def GetStruct_XDfePrach_Version(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Version

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Version
        """
        self.logger.debug("GetStruct_XDfePrach_Version()")
        XDfePrach_Version = self.PRACH.GetStruct_XDfePrach_Version()
        return XDfePrach_Version

    def GetStruct_XDfePrach_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Trigger
        """
        self.logger.debug("GetStruct_XDfePrach_Trigger()")
        XDfePrach_Trigger = self.PRACH.GetStruct_XDfePrach_Trigger()
        return XDfePrach_Trigger

    def GetStruct_XDfePrach_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_TriggerCfg
        """
        self.logger.debug("GetStruct_XDfePrach_TriggerCfg()")
        XDfePrach_TriggerCfg = self.PRACH.GetStruct_XDfePrach_TriggerCfg()
        return XDfePrach_TriggerCfg

    def GetStruct_XDfePrach_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CCSequence
        """
        self.logger.debug("GetStruct_XDfePrach_CCSequence()")
        XDfePrach_CCSequence = self.PRACH.GetStruct_XDfePrach_CCSequence()
        return XDfePrach_CCSequence

    def GetStruct_XDfePrach_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfePrach_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_ModelParameters
        """
        self.logger.debug("GetStruct_XDfePrach_ModelParameters()")
        XDfePrach_ModelParameters = self.PRACH.GetStruct_XDfePrach_ModelParameters()
        return XDfePrach_ModelParameters

    def GetStruct_XDfePrach_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Cfg
        """
        self.logger.debug("GetStruct_XDfePrach_Cfg()")
        XDfePrach_Cfg = self.PRACH.GetStruct_XDfePrach_Cfg()
        return XDfePrach_Cfg

    def GetStruct_XDfePrach_Init(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Init

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Init
        """
        self.logger.debug("GetStruct_XDfePrach_Init()")
        XDfePrach_Init = self.PRACH.GetStruct_XDfePrach_Init()
        return XDfePrach_Init

    def GetStruct_XDfePrach_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CarrierCfg
        """
        self.logger.debug("GetStruct_XDfePrach_CarrierCfg()")
        XDfePrach_CarrierCfg = self.PRACH.GetStruct_XDfePrach_CarrierCfg()
        return XDfePrach_CarrierCfg

    def GetStruct_XDfePrach_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_CCCfg
        """
        self.logger.debug("GetStruct_XDfePrach_CCCfg()")
        XDfePrach_CCCfg = self.PRACH.GetStruct_XDfePrach_CCCfg()
        return XDfePrach_CCCfg

    def GetStruct_XDfePrach_NCO(self):
        """
        Return Dictionary equivalent of structure XDfePrach_NCO

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_NCO
        """
        self.logger.debug("GetStruct_XDfePrach_NCO()")
        XDfePrach_NCO = self.PRACH.GetStruct_XDfePrach_NCO()
        return XDfePrach_NCO

    def GetStruct_XDfePrach_DDCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DDCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DDCCfg
        """
        self.logger.debug("GetStruct_XDfePrach_DDCCfg()")
        XDfePrach_DDCCfg = self.PRACH.GetStruct_XDfePrach_DDCCfg()
        return XDfePrach_DDCCfg

    def GetStruct_XDfePrach_Schedule(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Schedule

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Schedule
        """
        self.logger.debug("GetStruct_XDfePrach_Schedule()")
        XDfePrach_Schedule = self.PRACH.GetStruct_XDfePrach_Schedule()
        return XDfePrach_Schedule

    def GetStruct_XDfePrach_InternalChannelCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_InternalChannelCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_InternalChannelCfg
        """
        self.logger.debug("GetStruct_XDfePrach_InternalChannelCfg()")
        XDfePrach_InternalChannelCfg = self.PRACH.GetStruct_XDfePrach_InternalChannelCfg()
        return XDfePrach_InternalChannelCfg

    def GetStruct_XDfePrach_ChannelCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_ChannelCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_ChannelCfg
        """
        self.logger.debug("GetStruct_XDfePrach_ChannelCfg()")
        XDfePrach_ChannelCfg = self.PRACH.GetStruct_XDfePrach_ChannelCfg()
        return XDfePrach_ChannelCfg

    def GetStruct_XDfePrach_RCCfg(self):
        """
        Return Dictionary equivalent of structure XDfePrach_RCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_RCCfg
        """
        self.logger.debug("GetStruct_XDfePrach_RCCfg()")
        XDfePrach_RCCfg = self.PRACH.GetStruct_XDfePrach_RCCfg()
        return XDfePrach_RCCfg

    def GetStruct_XDfePrach_MixerStatusOverflow(self):
        """
        Return Dictionary equivalent of structure XDfePrach_MixerStatusOverflow

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_MixerStatusOverflow
        """
        self.logger.debug("GetStruct_XDfePrach_MixerStatusOverflow()")
        XDfePrach_MixerStatusOverflow = self.PRACH.GetStruct_XDfePrach_MixerStatusOverflow()
        return XDfePrach_MixerStatusOverflow

    def GetStruct_XDfePrach_DecimatorStatusOverflow(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DecimatorStatusOverflow

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DecimatorStatusOverflow
        """
        self.logger.debug("GetStruct_XDfePrach_DecimatorStatusOverflow()")
        XDfePrach_DecimatorStatusOverflow = self.PRACH.GetStruct_XDfePrach_DecimatorStatusOverflow()
        return XDfePrach_DecimatorStatusOverflow

    def GetStruct_XDfePrach_MixerStatusOverrun(self):
        """
        Return Dictionary equivalent of structure XDfePrach_MixerStatusOverrun

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_MixerStatusOverrun
        """
        self.logger.debug("GetStruct_XDfePrach_MixerStatusOverrun()")
        XDfePrach_MixerStatusOverrun = self.PRACH.GetStruct_XDfePrach_MixerStatusOverrun()
        return XDfePrach_MixerStatusOverrun

    def GetStruct_XDfePrach_DecimatorStatusOverrun(self):
        """
        Return Dictionary equivalent of structure XDfePrach_DecimatorStatusOverrun

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_DecimatorStatusOverrun
        """
        self.logger.debug("GetStruct_XDfePrach_DecimatorStatusOverrun()")
        XDfePrach_DecimatorStatusOverrun = self.PRACH.GetStruct_XDfePrach_DecimatorStatusOverrun()
        return XDfePrach_DecimatorStatusOverrun

    def GetStruct_XDfePrach_Status(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Status

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Status
        """
        self.logger.debug("GetStruct_XDfePrach_Status()")
        XDfePrach_Status = self.PRACH.GetStruct_XDfePrach_Status()
        return XDfePrach_Status

    def GetStruct_XDfePrach_StatusMask(self):
        """
        Return Dictionary equivalent of structure XDfePrach_StatusMask

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_StatusMask
        """
        self.logger.debug("GetStruct_XDfePrach_StatusMask()")
        XDfePrach_StatusMask = self.PRACH.GetStruct_XDfePrach_StatusMask()
        return XDfePrach_StatusMask

    def GetStruct_XDfePrach_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfePrach_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_InterruptMask
        """
        self.logger.debug("GetStruct_XDfePrach_InterruptMask()")
        XDfePrach_InterruptMask = self.PRACH.GetStruct_XDfePrach_InterruptMask()
        return XDfePrach_InterruptMask

    def GetStruct_XDfePrach_Config(self):
        """
        Return Dictionary equivalent of structure XDfePrach_Config

        :param : None
        :return: Dictionary equivalent of structure XDfePrach_Config
        """
        self.logger.debug("GetStruct_XDfePrach_Config()")
        XDfePrach_Config = self.PRACH.GetStruct_XDfePrach_Config()
        return XDfePrach_Config

    def GetStruct_XDfePrach(self):
        """
        Return Dictionary equivalent of structure XDfePrach

        :param : None
        :return: Dictionary equivalent of structure XDfePrach
        """
        self.logger.debug("GetStruct_XDfePrach()")
        XDfePrach = self.PRACH.GetStruct_XDfePrach()
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
        self.logger.info(f"XDfePrach_InstanceInit({DeviceNodeName})")
        DeviceNodeName = bytes(str(DeviceNodeName), 'utf-8')
        ret, device_id, DeviceNodeName = self.PRACH.XDfePrach_InstanceInit(DeviceNodeName)
        DeviceNodeName = self.extract_b64_encoded_string(DeviceNodeName)
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeName = {DeviceNodeName}")
        return ret, device_id, DeviceNodeName

    def XDfePrach_InstanceClose(self, device_id):
        """
        API closes the instances of a PRACH driver and moves the state machine to
        a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfePrach_InstanceClose({device_id})")
        self.PRACH.XDfePrach_InstanceClose(device_id)
        return

    def XDfePrach_WriteReg(self, device_id, addr_offset, data):
        """
        Writes a value to register in a PRACH instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :param Data: is value to be written.
        :return: None
        """
        self.logger.debug(f"XDfePrach_WriteReg({device_id}, {addr_offset}, {data})")
        self.PRACH.XDfePrach_WriteReg(device_id, addr_offset, data)
        return

    def XDfePrach_ReadReg(self, device_id, addr_offset):
        """
        Reads a value the register in a PRACH instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :return: ret: Register value.
        """
        self.logger.debug(f"XDfePrach_ReadReg({device_id}, {addr_offset})")
        regval = self.PRACH.XDfePrach_ReadReg(device_id, addr_offset)
        self.logger.debug(f"regval = {regval}")
        return regval

    # DFE PRACH component initialization API
    def XDfePrach_Reset(self, device_id):
        """
        Resets PRACH and puts block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_Reset({device_id})")
        self.PRACH.XDfePrach_Reset(device_id)
        return

    def XDfePrach_Configure(self, device_id, Cfg):
        """
        Reads configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container.
        :return: Cfg: configuration data container.
        """
        self.logger.debug(f"XDfePrach_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        Cfg = self.PRACH.XDfePrach_Configure(device_id, Cfg)
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
        self.logger.debug(f"XDfePrach_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        Init = self.PRACH.XDfePrach_Initialize(device_id, Init)
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
        self.PRACH.XDfePrach_Activate(device_id, EnableLowPower)
        return

    def XDfePrach_Deactivate(self, device_id):
        """
        Deactivates PRACH and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_Deactivate({device_id})")
        self.PRACH.XDfePrach_Deactivate(device_id)
        return

    def XDfePrach_GetStateID(self, device_id):
        """
        Gets a state machine state id.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfePrach_GetStateID({device_id})")
        StateId = self.PRACH.XDfePrach_GetStateID(device_id)
        self.logger.debug(f"Return value StateId = {StateId}")
        return StateId

    def XDfePrach_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfePrach_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg = self.PRACH.XDfePrach_GetCurrentCCCfg(device_id, CurrCCCfg)
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
        self.logger.debug(f"XDfePrach_GetEmptyCCCfg({device_id})")
        CCCfg = self.PRACH.XDfePrach_GetEmptyCCCfg(device_id)
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
        CCSeqBitmap, CarrierCfg = self.PRACH.XDfePrach_GetCarrierCfgMB(device_id, CCCfg, CCID, BandId)
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
        CCSeqBitmap, CarrierCfg = self.PRACH.XDfePrach_GetCarrierCfg(device_id, CCCfg, CCID)
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
        CCCfg = self.PRACH.XDfePrach_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)
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
        ret, CCCfg = self.PRACH.XDfePrach_AddCCtoCCCfgMB(device_id, CCCfg, CCID, CCSeqBitmap,
                                                   CarrierCfg, BandId)
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
        ret, CCCfg = self.PRACH.XDfePrach_AddCCtoCCCfg(device_id, CCCfg, CCID, CCSeqBitmap,
                                                   CarrierCfg)
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
        CCCfg = self.PRACH.XDfePrach_RemoveCCfromCCCfgMB(device_id, CCCfg, CCID, BandId)
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
        self.logger.debug(f"XDfePrach_RemoveCCfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {CCID})")
        CCCfg = self.PRACH.XDfePrach_RemoveCCfromCCCfg(device_id, CCCfg, CCID)
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
        CCCfg = self.PRACH.XDfePrach_UpdateCCinCCCfgMB(device_id, CCCfg, CCID, CarrierCfg, BandId)
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
        self.logger.debug(f"XDfePrach_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {json.dumps(CarrierCfg, indent=2)})")
        CCCfg = self.PRACH.XDfePrach_UpdateCCinCCCfg(device_id, CCCfg, CCID, CarrierCfg)
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
        self.logger.debug(f"XDfePrach_AddCC({device_id}, {CCID}, {BitSequence}, {json.dumps(CarrierCfg, indent=2)})")
        ret, CarrierCfg = self.PRACH.XDfePrach_AddCC(device_id, CCID, BitSequence, CarrierCfg)
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
        ret = self.PRACH.XDfePrach_RemoveCC(device_id, CCID)
        self.logger.debug(f"ret = {ret}")
        return

    def XDfePrach_UpdateCC(self, device_id, CCID, CarrierCfg):
        """
        Updates a CCID sequence.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param CarrierCfg: is carrier data container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfePrach_UpdateCC({device_id}, {CCID}, "
                          f"{json.dumps(CarrierCfg, indent=2)})")
        ret = self.PRACH.XDfePrach_UpdateCC(device_id, CCID, CarrierCfg)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetCurrentRCCfg(self, device_id):
        """
        Reads all of the RC configuration back.

        :param device_id: id of the opened device.
        :return: RCCfg: RC configuration container.
        """
        self.logger.debug(f"XDfePrach_GetCurrentRCCfg({device_id})")
        RCCfg = self.PRACH.XDfePrach_GetCurrentRCCfg(device_id)
        self.logger.debug(f"RCCfg = {json.dumps(RCCfg, indent=2)}")
        return RCCfg

    def XDfePrach_GetEmptyRCCfg(self, device_id):
        """
        Returns the empty CC configuration.

        :param device_id: id of the opened device.
        :return: RCCfg: RC configuration container.
        """
        self.logger.debug(f"XDfePrach_GetEmptyRCCfg({device_id})")
        RCCfg = self.PRACH.XDfePrach_GetEmptyRCCfg(device_id)
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
        self.logger.debug(f"XDfePrach_GetChannelCfg({device_id}, {RCId}")
        ChannelCfg = self.PRACH.XDfePrach_GetChannelCfg(device_id, RCCfg, RCId)
        self.logger.debug(f"ret = ChannelCfg = {json.dumps(ChannelCfg, indent=2)}")
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
        self.logger.debug(f"XDfePrach_AddRCtoRCCfgMB({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)}, {BandId})")
        ret, CurrentRCCfg = self.PRACH.XDfePrach_AddRCtoRCCfgMB(device_id, CurrentRCCfg, CCID, RCId,
                                                RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg, BandId)
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
        self.logger.debug(f"XDfePrach_AddRCtoRCCfg({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, "
                          f"{json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, "
                          f"{json.dumps(StaticSchedule, indent=2)}, "
                          f"{json.dumps(NextCCCfg, indent=2)})")
        ret, CurrentRCCfg = self.PRACH.XDfePrach_AddRCtoRCCfg(device_id, CurrentRCCfg, CCID, RCId,
                                                RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg)
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
        self.logger.debug(f"XDfePrach_RemoveRCfromRCCfg({device_id}, "
                          f"{json.dumps(CurrentRCCfg, indent=2)}, {RCId})")
        ret, CurrentRCCfg = self.PRACH.XDfePrach_RemoveRCfromRCCfg(device_id, CurrentRCCfg, RCId)
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
        self.logger.debug(f"XDfePrach_UpdateRCinRCCfgMB({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)}, {BandId})")
        CurrentRCCfg = self.PRACH.XDfePrach_UpdateRCinRCCfgMB(device_id, CurrentRCCfg, CCID, RCId,
                                                  RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg, BandId)
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
        self.logger.debug(f"XDfePrach_UpdateRCinRCCfg({device_id}, {CurrentRCCfg}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)}, {json.dumps(NextCCCfg, indent=2)})")
        CurrentRCCfg = self.PRACH.XDfePrach_UpdateRCinRCCfg(device_id, CurrentRCCfg, CCID, RCId,
                                                  RachChan, DdcCfg, NcoCfg, StaticSchedule, NextCCCfg)
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
        self.logger.debug(f"XDfePrach_SetNextRCCfg({device_id}, {json.dumps(NextCCCfg, indent=2)}), {json.dumps(NextRCCfg, indent=2)})")
        ret = self.PRACH.XDfePrach_SetNextCfg(device_id, NextCCCfg, NextRCCfg)
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
        self.logger.debug(f"XDfePrach_UpdateRCCfg({device_id}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)})")
        ret = self.PRACH.XDfePrach_UpdateRCCfg(device_id, CCID, RCId, RachChan,
                                               DdcCfg, NcoCfg, StaticSchedule)
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
        self.logger.debug(f"XDfePrach_AddRCCfg({device_id}, {CCID}, {RCId}, {RachChan}, {json.dumps(DdcCfg, indent=2)}, {json.dumps(NcoCfg, indent=2)}, {json.dumps(StaticSchedule, indent=2)})")
        ret, DdcCfg, NcoCfg, StaticSchedule = self.PRACH.XDfePrach_AddRCCfg(device_id, CCID, RCId, RachChan, DdcCfg, NcoCfg, StaticSchedule)
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
        ret = self.PRACH.XDfePrach_RemoveRC(device_id, RCId)
        self.logger.debug(f"ret = {ret}")
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
        ret = self.PRACH.XDfePrach_MoveRC(device_id, RCId, ToChannel)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: Trigger configuration container
        """
        self.logger.debug(f"XDfePrach_GetTriggersCfg({device_id})")
        TriggerCfg = self.PRACH.XDfePrach_GetTriggersCfg(device_id)
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfePrach_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: Trigger configuration container.
        :return: TriggerCfg: Trigger configuration container.
        """
        self.logger.debug(f"XDfePrach_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        TriggerCfg = self.PRACH.XDfePrach_SetTriggersCfg(device_id, TriggerCfg)
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
        self.logger.debug(f"XDfePrach_GetCC({device_id}, {Next}, {CCID})")
        CarrierCfg = self.PRACH.XDfePrach_GetCC(device_id, Next, CCID)
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
        self.logger.debug(f"XDfePrach_GetCC({device_id}, {Next}, {CCID}, {BandId})")
        CarrierCfg = self.PRACH.XDfePrach_GetCCMB(device_id, Next, CCID, BandId)
        self.logger.debug(f"CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return CarrierCfg

    def XDfePrach_GetStatus(self, device_id):
        """
        Get PRACH Status.

        :param device_id: id of the opened device.
        :return: Status: Status data container.
        """
        self.logger.debug(f"XDfePrach_GetStatus({device_id})")
        Status = self.PRACH.XDfePrach_GetStatus(device_id)
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfePrach_ClearStatus(self, device_id):
        """
        Clear the PRACH status registers.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_ClearStatus({device_id})")
        self.PRACH.XDfePrach_ClearStatus(device_id)
        return

    def XDfePrach_CapturePhase(self, device_id):
        """
        Captures phase for all phase accumulators in associated AXI-lite registers.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfePrach_CapturePhase({device_id})")
        self.PRACH.XDfePrach_CapturePhase(device_id)
        return

    def XDfePrach_GetCapturePhase(self, device_id, RachChan):
        """
        Reads the captured phase for a given Rach Channel.

        :param device_id: id of the opened device.
        :param RachChan: is RACH channel Id.
        :return: NCO data container.
        """
        self.logger.debug(f"XDfePrach_GetCapturePhase({device_id}, {RachChan})")
        CapturedPhase = self.PRACH.XDfePrach_GetCapturePhase(device_id, RachChan)
        self.logger.debug(f"CapturedPhase = {json.dumps(CapturedPhase, indent=2)}")
        return CapturedPhase

    def XDfePrach_GetInterruptMask(self, device_id):
        """
        Gets interrupt mask status.

        :param device_id: id of the opened device.
        :return: Mask: interrupt masks container.
        """
        self.logger.debug(f"XDfePrach_GetInterruptMask({device_id})")
        Mask = self.PRACH.XDfePrach_GetInterruptMask(device_id)
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
        self.logger.debug(f"XDfePrach_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        self.PRACH.XDfePrach_SetInterruptMask(device_id, Mask)
        return

    def XDfePrach_GetEventStatus(self, device_id):
        """
        Gets event status.

        :param device_id: id of the opened device.
        :return: Status: event status container.
        """
        self.logger.debug(f"XDfePrach_GetEventStatus({device_id})")
        Status = self.PRACH.XDfePrach_GetEventStatus(device_id)
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
        self.logger.debug(f"XDfePrach_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        self.PRACH.XDfePrach_ClearEventStatus(device_id, Status)
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
        self.PRACH.XDfePrach_SetTUserDelay(device_id, Delay)
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
        self.PRACH.XDfePrach_SetTUserDelayMB(device_id, Delay, BandId)
        return

    def XDfePrach_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfePrach_GetTUserDelay({device_id})")
        ret = self.PRACH.XDfePrach_GetTUserDelay(device_id)
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
        ret = self.PRACH.XDfePrach_GetTUserDelayMB(device_id, BandId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetTDataDelay(self, device_id):
        """
        Returns data latency.

        :param device_id: id of the opened device.
        :return: ret: data latency value.
        """
        self.logger.debug(f"XDfePrach_GetTDataDelay({device_id})")
        ret = self.PRACH.XDfePrach_GetTDataDelay(device_id)
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
        ret = self.PRACH.XDfePrach_GetTDataDelayMB(device_id, BandId)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfePrach_GetVersions(self, device_id):
        """
        This API gets the driver and HW design version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        self.logger.debug(f"XDfePrach_GetVersions({device_id})")
        SwVersion, HwVersion = self.PRACH.XDfePrach_GetVersions(device_id)
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        self.logger.info("Inside PRACH Destructor")


prach = PRACH_Client()
