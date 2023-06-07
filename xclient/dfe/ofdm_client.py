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


class OFDM_Client(object):
    OFDM = None
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
        self.logger.info("Inside OFDM Pyro Client Constructor")
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
        API to inform OFDM Client the IP address and port number of OFDM Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:OFDM@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.OFDM = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.OFDM.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.OFDM.SetServerLogLevel(PythonLogLevel)
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
        self.OFDM.SetMetalLogLevel(MetalLogLevel)
        return

    # Get enum API
    def GetEnum_XDfeOfdm_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeOfdm_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeOfdm_StateId
        """
        self.logger.debug("GetEnum_XDfeOfdm_StateId()")
        XDfeOfdm_StateId = self.OFDM.GetEnum_XDfeOfdm_StateId()
        self.logger.debug(f"XDfeOfdm_StateId = {json.dumps(XDfeOfdm_StateId, indent=2)}")
        return XDfeOfdm_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.OFDM.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    # Get structure  API
    def GetStruct_XDfeOfdm_Version(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Version
        """
        self.logger.debug("GetStruct_XDfeOfdm_Version()")
        XDfeOfdm_Version = self.OFDM.GetStruct_XDfeOfdm_Version()
        return XDfeOfdm_Version

    def GetStruct_XDfeOfdm_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Trigger
        """
        self.logger.debug("GetStruct_XDfeOfdm_Trigger()")
        XDfeOfdm_Trigger = self.OFDM.GetStruct_XDfeOfdm_Trigger()
        return XDfeOfdm_Trigger

    def GetStruct_XDfeOfdm_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_TriggerCfg
        """
        self.logger.debug("GetStruct_XDfeOfdm_TriggerCfg()")
        XDfeOfdm_TriggerCfg = self.OFDM.GetStruct_XDfeOfdm_TriggerCfg()
        return XDfeOfdm_TriggerCfg

    def GetStruct_XDfeOfdm_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CCSequence
        """
        self.logger.debug("GetStruct_XDfeOfdm_CCSequence()")
        XDfeOfdm_CCSequence = self.OFDM.GetStruct_XDfeOfdm_CCSequence()
        return XDfeOfdm_CCSequence

    def GetStruct_XDfeOfdm_FTSequence(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_FTSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_FTSequence
        """
        self.logger.debug("GetStruct_XDfeOfdm_FTSequence()")
        XDfeOfdm_FTSequence = self.OFDM.GetStruct_XDfeOfdm_FTSequence()
        return XDfeOfdm_FTSequence

    def GetStruct_XDfeOfdm_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_ModelParameters
        """
        self.logger.debug("GetStruct_XDfeOfdm_ModelParameters()")
        XDfeOfdm_ModelParameters = self.OFDM.GetStruct_XDfeOfdm_ModelParameters()
        return XDfeOfdm_ModelParameters

    def GetStruct_XDfeOfdm_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Cfg
        """
        self.logger.debug("GetStruct_XDfeOfdm_Cfg()")
        XDfeOfdm_Cfg = self.OFDM.GetStruct_XDfeOfdm_Cfg()
        return XDfeOfdm_Cfg

    def GetStruct_XDfeOfdm_Init(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Init

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Init
        """
        self.logger.debug("GetStruct_XDfeOfdm_Init()")
        XDfeOfdm_Init = self.OFDM.GetStruct_XDfeOfdm_Init()
        return XDfeOfdm_Init

    def GetStruct_XDfeOfdm_Coefficients(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Coefficients
        """
        self.logger.debug("GetStruct_XDfeOfdm_Coefficients()")
        XDfeOfdm_Coefficients = self.OFDM.GetStruct_XDfeOfdm_Coefficients()
        return XDfeOfdm_Coefficients

    def GetStruct_XDfeOfdm_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CarrierCfg
        """
        self.logger.debug("GetStruct_XDfeOfdm_CarrierCfg()")
        XDfeOfdm_CarrierCfg = self.OFDM.GetStruct_XDfeOfdm_CarrierCfg()
        return XDfeOfdm_CarrierCfg

    def GetStruct_XDfeOfdm_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_CCCfg
        """
        self.logger.debug("GetStruct_XDfeOfdm_CCCfg()")
        XDfeOfdm_CCCfg = self.OFDM.GetStruct_XDfeOfdm_CCCfg()
        return XDfeOfdm_CCCfg

    def GetStruct_XDfeOfdm_Status(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Status
        """
        self.logger.debug("GetStruct_XDfeOfdm_Status()")
        XDfeOfdm_Status = self.OFDM.GetStruct_XDfeOfdm_Status()
        return XDfeOfdm_Status

    def GetStruct_XDfeOfdm_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_InterruptMask
        """
        self.logger.debug("GetStruct_XDfeOfdm_InterruptMask()")
        XDfeOfdm_InterruptMask = self.OFDM.GetStruct_XDfeOfdm_InterruptMask()
        return XDfeOfdm_InterruptMask

    def GetStruct_XDfeOfdm_Config(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_Config
        """
        self.logger.debug("GetStruct_XDfeOfdm_Config()")
        XDfeOfdm_Config = self.OFDM.GetStruct_XDfeOfdm_Config()
        return XDfeOfdm_Config

    def GetStruct_XDfeOfdm_InternalCarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm_InternalCarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm_InternalCarrierCfg
        """
        self.logger.debug("GetStruct_XDfeOfdm_InternalCarrierCfg()")
        XDfeOfdm_InternalCarrierCfg = self.OFDM.GetStruct_XDfeOfdm_InternalCarrierCfg()
        return XDfeOfdm_InternalCarrierCfg

    def GetStruct_XDfeOfdm(self):
        """
        Return Dictionary equivalent of structure XDfeOfdm

        :param : None
        :return: Dictionary equivalent of structure XDfeOfdm
        """
        self.logger.debug("GetStruct_XDfeOfdm()")
        XDfeOfdm = self.OFDM.GetStruct_XDfeOfdm()
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
        self.logger.info(f"XDfeOfdm_InstanceInit({DeviceNodeName})")
        DeviceNodeName = bytes(str(DeviceNodeName), 'utf-8')
        ret, device_id, DeviceNodeName = self.OFDM.XDfeOfdm_InstanceInit(DeviceNodeName)
        DeviceNodeName = self.extract_b64_encoded_string(DeviceNodeName)
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeName = {DeviceNodeName}")
        return ret, device_id, DeviceNodeName

    def XDfeOfdm_InstanceClose(self, device_id):
        """
        API closes the instances of a Ofdm driver.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeOfdm_InstanceClose({device_id})")
        self.OFDM.XDfeOfdm_InstanceClose(device_id)
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
        self.OFDM.XDfeOfdm_WriteReg(device_id, addr_offset, data)
        return

    def XDfeOfdm_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from register using a Ofdm instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address
        :return: regval: Register value.
        """
        self.logger.debug(f"XDfeOfdm_ReadReg({device_id}, {addr_offset})")
        regval = self.OFDM.XDfeOfdm_ReadReg(device_id, addr_offset)
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
        self.OFDM.XDfeOfdm_Reset(device_id)
        return

    def XDfeOfdm_Configure(self, device_id, Cfg):
        """
        Read configuration from device tree/xparameters.h and IP registers.
        S/W reset removed.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container
        :return: Cfg: configuration data container
        """
        self.logger.debug(f"XDfeOfdm_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        Cfg = self.OFDM.XDfeOfdm_Configure(device_id, Cfg)
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeOfdm_Initialize(self, device_id, Init):
        """
        DFE Ofdm driver one time initialisation.

        :param device_id: id of the opened device.
        :param Init: initialisation data container
        :return: Init: initialisation data container
        """
        self.logger.debug(f"XDfeOfdm_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        Init = self.OFDM.XDfeOfdm_Initialize(device_id, Init)
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
        self.OFDM.XDfeOfdm_Activate(device_id, EnableLowPower)
        return

    def XDfeOfdm_Deactivate(self, device_id):
        """
        DeActivate ofdm.
        Note: Writing to ACTIVATE register toggles between "initialized" and "operational".

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_Deactivate({device_id})")
        self.OFDM.XDfeOfdm_Deactivate(device_id)
        return

    def XDfeOfdm_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeOfdm_GetStateID({device_id})")
        StateId = self.OFDM.XDfeOfdm_GetStateID(device_id)
        self.logger.debug(f"Return value StateId = {StateId}")
        return StateId

    def XDfeOfdm_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeOfdm_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg = self.OFDM.XDfeOfdm_GetCurrentCCCfg(device_id, CurrCCCfg)
        self.logger.debug(f"CurrCCCfg = {json.dumps(CurrCCCfg, indent=2)}")
        return CurrCCCfg

    def XDfeOfdm_GetEmptyCCCfg(self, device_id):
        """
        Returns the empty CC configuration.

        :param device_id: id of the opened device.
        :return: CCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeOfdm_GetEmptyCCCfg({device_id})")
        CCCfg = self.OFDM.XDfeOfdm_GetEmptyCCCfg(device_id)
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeOfdm_GetCarrierCfg(self, device_id, CCCfg, CCID):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
        """
        self.logger.debug(f"XDfeOfdm_GetCarrierCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        CCSeqBitmap, CarrierCfg = self.OFDM.XDfeOfdm_GetCarrierCfg(device_id, CCCfg, CCID)
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}")
        return CCSeqBitmap, CarrierCfg

    def XDfeOfdm_AddCCtoCCCfg(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
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
        ret, CCCfg, FTSeq = self.OFDM.XDfeOfdm_AddCCtoCCCfg(device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg, FTSeq)
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)}")
        return ret, CCCfg, FTSeq

    def XDfeOfdm_RemoveCCfromCCCfg(self, device_id, CCCfg, CCID, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param FTSeq: FTSeq container.
        :return: ret: 0 on success and 1 on failure
                 CCCfg: component carrier (CC) configuration container.
                 FTSeq: FTSeq container.
        """
        self.logger.debug(f"XDfeOfdm_RemoveCCfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {CCID}), "
                          f"{json.dumps(FTSeq, indent=2)})")
        ret, CCCfg, FTSeq = self.OFDM.XDfeOfdm_RemoveCCfromCCCfg(device_id, CCCfg, CCID, FTSeq)
        self.logger.debug(f"ret = {ret}, Return value = {json.dumps(CCCfg, indent=2)}, "
                          f"{json.dumps(FTSeq, indent=2)}")
        return ret, CCCfg, FTSeq

    def XDfeOfdm_UpdateCCinCCCfg(self, device_id, CCCfg, CCID, CarrierCfg, FTSeq):
        """
        Returns the current CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CarrierCfg: CC configuration container.
        :param FTSeq: FTSeq container.
        :return: ret: 0 on success and 1 on failure
                 CCCfg: component carrier (CC) configuration container.
                 FTSeq: FTSeq container.
        """
        self.logger.debug(f"XDfeOfdm_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {json.dumps(CarrierCfg, indent=2)}), "
                          f"{json.dumps(FTSeq, indent=2)})")
        ret, CCCfg, FTSeq = self.OFDM.XDfeOfdm_UpdateCCinCCCfg(device_id, CCCfg, CCID, CarrierCfg, FTSeq)
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
        CCCfg = self.OFDM.XDfeOfdm_SetNextCCCfg(device_id, CCCfg)
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
        ret = self.OFDM.XDfeOfdm_EnableCCUpdateTrigger(device_id)
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
        ret, CCCfg = self.OFDM.XDfeOfdm_SetNextCCCfgAndTrigger(device_id, CCCfg)
        self.logger.debug(f"ret = {ret}, CCCfg = {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeOfdm_AddCC(self, device_id, CCID, CCSeqBitmap, CarrierCfg, FTSeq):
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
        :param FTSeq: FTSeq container.
        :return: ret: 0 if successful, 1 on error.
        """
        self.logger.debug(f"XDfeOfdm_AddCC({device_id}, {CCID}, {CCSeqBitmap}, "
                          f"{json.dumps(CarrierCfg, indent=2)}, {json.dumps(FTSeq, indent=2)})")
        ret = self.OFDM.XDfeOfdm_AddCC(device_id, CCID, CCSeqBitmap, CarrierCfg, FTSeq)
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
        ret = self.OFDM.XDfeOfdm_RemoveCC(device_id, CCID, FTSeq)
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
        ret = self.OFDM.XDfeOfdm_UpdateCC(device_id, CCID, CarrierCfg, FTSeq)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeOfdm_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
	    :return: TriggerCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeOfdm_GetTriggersCfg({device_id})")
        TriggerCfg = self.OFDM.XDfeOfdm_GetTriggersCfg(device_id)
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeOfdm_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a trigger configuration container.
	    :return: TriggerCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeOfdm_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        TriggerCfg = self.OFDM.XDfeOfdm_SetTriggersCfg(device_id, TriggerCfg)
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeOfdm_GetEventStatus(self, device_id):
        """
        Get event status

        :param device_id: id of the opened device.
        :return: Status: event status
        """
        self.logger.debug(f"XDfeOfdm_GetEventStatus({device_id})")
        Status = self.OFDM.XDfeOfdm_GetEventStatus(device_id)
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeOfdm_ClearEventStatus(self, device_id, Status):
        """
        Clears all event statuses.

        :param device_id: id of the opened device.
        :param Status: event status.
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        self.OFDM.XDfeOfdm_ClearEventStatus(device_id, Status)
        return

    def XDfeOfdm_SetInterruptMask(self, device_id, Mask):
        """
        Sets interrupt masks.

        :param device_id: id of the opened device.
        :param Mask: interrupt mask value
        :return: None
        """
        self.logger.debug(f"XDfeOfdm_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        self.OFDM.XDfeOfdm_SetInterruptMask(device_id, Mask)
        return

    def XDfeOfdm_GetInterruptMask(self, device_id):
        """
        Get Interrupt mask value

        :param device_id: id of the opened device.
        :return: Mask: interrupt mask value.
        """
        self.logger.debug(f"XDfeOfdm_GetInterruptMask({device_id})")
        Mask = self.OFDM.XDfeOfdm_GetInterruptMask(device_id)
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
        self.OFDM.XDfeOfdm_SetTUserDelay(device_id, TUserDelay)
        return

    def XDfeOfdm_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: TUserDelay: Delay value.
        """
        self.logger.debug(f"XDfeOfdm_GetTUserDelay({device_id})")
        TUserDelay = self.OFDM.XDfeOfdm_GetTUserDelay(device_id)
        self.logger.debug(f"Return value = {TUserDelay}")
        return TUserDelay

    def XDfeOfdm_GetDataLatency(self, device_id):
        """
        Returns data latency.

        :param device_id: id of the opened device.
        :return: Returned Data latency.
        """
        self.logger.debug(f"XDfeOfdm_GetDataLatency({device_id})")
        TDataLatency = self.OFDM.XDfeOfdm_GetDataLatency(device_id)
        self.logger.debug(f"Return value = {TDataLatency}")
        return TDataLatency

    def XDfeOfdm_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        self.logger.debug(f"XDfeOfdm_GetVersions({device_id})")
        SwVersion, HwVersion = self.OFDM.XDfeOfdm_GetVersions(device_id)
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

ofdm = OFDM_Client()
