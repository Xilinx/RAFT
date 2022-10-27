# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64
import json
import sys


class CCF_Client(object):
    CCF = None
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
        self.logger.info("Inside CCF Pyro Client Constructor")
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
        API to inform CCF Client the IP address and port number of CCF Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """
        uri = f"PYRO:CCF@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.CCF = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.CCF.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.CCF.SetServerLogLevel(PythonLogLevel)
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
        self.CCF.SetMetalLogLevel(MetalLogLevel)
        return

    # Get enum API
    def GetEnum_XDfeCcf_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeCcf_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeCcf_StateId
        """
        self.logger.debug("GetEnum_XDfeCcf_StateId()")
        XDfeCcf_StateId = self.CCF.GetEnum_XDfeCcf_StateId()
        self.logger.debug(f"XDfeCcf_StateId = {json.dumps(XDfeCcf_StateId, indent=2)}")
        return XDfeCcf_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.CCF.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    # Get structure  API
    def GetStruct_XDfeCcf_Version(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Version
        """
        self.logger.debug("GetStruct_XDfeCcf_Version()")
        XDfeCcf_Version = self.CCF.GetStruct_XDfeCcf_Version()
        return XDfeCcf_Version

    def GetStruct_XDfeCcf_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Trigger
        """
        self.logger.debug("GetStruct_XDfeCcf_Trigger()")
        XDfeCcf_Trigger = self.CCF.GetStruct_XDfeCcf_Trigger()
        return XDfeCcf_Trigger

    def GetStruct_XDfeCcf_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_TriggerCfg
        """
        self.logger.debug("GetStruct_XDfeCcf_TriggerCfg()")
        XDfeCcf_TriggerCfg = self.CCF.GetStruct_XDfeCcf_TriggerCfg()
        return XDfeCcf_TriggerCfg

    def GetStruct_XDfeCcf_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CCSequence
        """
        self.logger.debug("GetStruct_XDfeCcf_CCSequence()")
        XDfeCcf_CCSequence = self.CCF.GetStruct_XDfeCcf_CCSequence()
        return XDfeCcf_CCSequence

    def GetStruct_XDfeCcf_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_ModelParameters
        """
        self.logger.debug("GetStruct_XDfeCcf_ModelParameters()")
        XDfeCcf_ModelParameters = self.CCF.GetStruct_XDfeCcf_ModelParameters()
        return XDfeCcf_ModelParameters

    def GetStruct_XDfeCcf_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Cfg
        """
        self.logger.debug("GetStruct_XDfeCcf_Cfg()")
        XDfeCcf_Cfg = self.CCF.GetStruct_XDfeCcf_Cfg()
        return XDfeCcf_Cfg

    def GetStruct_XDfeCcf_Init(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Init

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Init
        """
        self.logger.debug("GetStruct_XDfeCcf_Init()")
        XDfeCcf_Init = self.CCF.GetStruct_XDfeCcf_Init()
        return XDfeCcf_Init

    def GetStruct_XDfeCcf_Coefficients(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Coefficients

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Coefficients
        """
        self.logger.debug("GetStruct_XDfeCcf_Coefficients()")
        XDfeCcf_Coefficients = self.CCF.GetStruct_XDfeCcf_Coefficients()
        return XDfeCcf_Coefficients

    def GetStruct_XDfeCcf_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CarrierCfg
        """
        self.logger.debug("GetStruct_XDfeCcf_CarrierCfg()")
        XDfeCcf_CarrierCfg = self.CCF.GetStruct_XDfeCcf_CarrierCfg()
        return XDfeCcf_CarrierCfg

    def GetStruct_XDfeCcf_AntennaCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_AntennaCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_AntennaCfg
        """
        self.logger.debug("GetStruct_XDfeCcf_AntennaCfg()")
        XDfeCcf_AntennaCfg = self.CCF.GetStruct_XDfeCcf_AntennaCfg()
        return XDfeCcf_AntennaCfg

    def GetStruct_XDfeCcf_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_CCCfg
        """
        self.logger.debug("GetStruct_XDfeCcf_CCCfg()")
        XDfeCcf_CCCfg = self.CCF.GetStruct_XDfeCcf_CCCfg()
        return XDfeCcf_CCCfg

    def GetStruct_XDfeCcf_OverflowStatus(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_OverflowStatus

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_OverflowStatus
        """
        self.logger.debug("GetStruct_XDfeCcf_OverflowStatus()")
        XDfeCcf_OverflowStatus = self.CCF.GetStruct_XDfeCcf_OverflowStatus()
        return XDfeCcf_OverflowStatus

    def GetStruct_XDfeCcf_Status(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Status
        """
        self.logger.debug("GetStruct_XDfeCcf_Status()")
        XDfeCcf_Status = self.CCF.GetStruct_XDfeCcf_Status()
        return XDfeCcf_Status

    def GetStruct_XDfeCcf_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_InterruptMask
        """
        self.logger.debug("GetStruct_XDfeCcf_InterruptMask()")
        XDfeCcf_InterruptMask = self.CCF.GetStruct_XDfeCcf_InterruptMask()
        return XDfeCcf_InterruptMask

    def GetStruct_XDfeCcf_Config(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_Config
        """
        self.logger.debug("GetStruct_XDfeCcf_Config()")
        XDfeCcf_Config = self.CCF.GetStruct_XDfeCcf_Config()
        return XDfeCcf_Config

    def GetStruct_XDfeCcf_InternalCarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
        """
        self.logger.debug("GetStruct_XDfeCcf_InternalCarrierCfg()")
        XDfeCcf_InternalCarrierCfg = self.CCF.GetStruct_XDfeCcf_InternalCarrierCfg()
        return XDfeCcf_InternalCarrierCfg

    def GetStruct_XDfeCcf(self):
        """
        Return Dictionary equivalent of structure XDfeCcf

        :param : None
        :return: Dictionary equivalent of structure XDfeCcf
        """
        self.logger.debug("GetStruct_XDfeCcf()")
        XDfeCcf = self.CCF.GetStruct_XDfeCcf()
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
        self.logger.info(f"XDfeCcf_InstanceInit({DeviceNodeName})")
        DeviceNodeName = bytes(str(DeviceNodeName), 'utf-8')
        ret, device_id, DeviceNodeName = self.CCF.XDfeCcf_InstanceInit(DeviceNodeName)
        DeviceNodeName = self.extract_b64_encoded_string(DeviceNodeName)
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeName = {DeviceNodeName}")
        return ret, device_id, DeviceNodeName

    def XDfeCcf_InstanceClose(self, device_id):
        """
        Closes the instances of a channel filter driver and moves the state
        machine to a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeCcf_InstanceClose({device_id})")
        self.CCF.XDfeCcf_InstanceClose(device_id)
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
        self.CCF.XDfeCcf_WriteReg(device_id, addr_offset, data)
        return

    def XDfeCcf_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from register using a Ccf instance.

        :param device_id: id of the opened device.
        :param AddrOffset: address offset relative to instance base address
        :return: regval: Register value.
        """
        self.logger.debug(f"XDfeCcf_ReadReg({device_id}, {addr_offset})")
        regval = self.CCF.XDfeCcf_ReadReg(device_id, addr_offset)
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
        self.CCF.XDfeCcf_Reset(device_id)
        return

    def XDfeCcf_Configure(self, device_id, Cfg):
        """
        Read configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container
        :return: Cfg: configuration data container
        """
        self.logger.debug(f"XDfeCcf_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        Cfg = self.CCF.XDfeCcf_Configure(device_id, Cfg)
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
        self.logger.debug(f"XDfeCcf_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        Init = self.CCF.XDfeCcf_Initialize(device_id, Init)
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
        self.CCF.XDfeCcf_Activate(device_id, EnableLowPower)
        return

    def XDfeCcf_Deactivate(self, device_id):
        """
        Deactivates channel filter and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeCcf_Deactivate({device_id})")
        self.CCF.XDfeCcf_Deactivate(device_id)
        return

    def XDfeCcf_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeCcf_GetStateID({device_id})")
        StateId = self.CCF.XDfeCcf_GetStateID(device_id)
        self.logger.debug(f"Return value StateId = {StateId}")
        return StateId

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
        CurrCCCfg = self.CCF.XDfeCcf_GetCurrentCCCfg(device_id, CurrCCCfg)
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
        self.logger.debug(f"XDfeCcf_GetEmptyCCCfg({device_id})")
        CCCfg = self.CCF.XDfeCcf_GetEmptyCCCfg(device_id)
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
        CCSeqBitmap, CarrierCfg = self.CCF.XDfeCcf_GetCarrierCfg(device_id, CCCfg, CCID)
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
        CCCfg = self.CCF.XDfeCcf_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)
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
        ret, CCCfg = self.CCF.XDfeCcf_AddCCtoCCCfg(device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg)
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
        CCCfg = self.CCF.XDfeCcf_RemoveCCfromCCCfg(device_id, CCCfg, CCID)
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
        CCCfg = self.CCF.XDfeCcf_UpdateCCinCCCfg(device_id, CCCfg, CCID, CarrierCfg)
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
        ret, CCCfg = self.CCF.XDfeCcf_SetNextCCCfgAndTrigger(device_id, CCCfg)
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
        ret, CarrierCfg = self.CCF.XDfeCcf_AddCC(device_id, CCID, CCSeqBitmap, CarrierCfg)
        self.logger.debug(f"ret = {ret}, CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return ret, CarrierCfg

    def XDfeCcf_RemoveCC(self, device_id, CCID):
        """
        Removes specified CCID.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeCcf_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :return: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeCcf_RemoveCC({device_id}, {CCID})")
        ret = self.CCF.XDfeCcf_RemoveCC(device_id, CCID)
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
        self.logger.debug(f"XDfeCcf_UpdateCC({device_id}, {json.dumps(CarrierCfg, indent=2)})")
        ret, CarrierCfg = self.CCF.XDfeCcf_UpdateCC(device_id, CCID, CarrierCfg)
        self.logger.debug(f"ret = {ret}, CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return ret, CarrierCfg

    def XDfeCcf_UpdateAntenna(self, device_id, Ant, Enabled):
        """
        Updates specified antenna TDM slot enablement.
        Initiates CC update (enable CCUpdate trigger one-shot).
        Note: Clear event status with XDfeCcf_ClearEventStatus() before
        running this API.

        :param device_id: id of the opened device.
        :param Ant: is antenna ID.
        :param Enabled: flag indicating enable status of the antenna.
        :return: ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeCcf_UpdateAntenna({device_id}, {Ant}, {Enabled})")
        ret = self.CCF.XDfeCcf_UpdateAntenna(device_id, Ant, Enabled)
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
        ret = self.CCF.XDfeCcf_UpdateAntennaCfg(device_id, AntennaCfg)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeCcf_GetTriggersCfg(self, device_id):
        """
        Return current trigger configuration.

        :param device_id: id of the opened device.
	    :return: TriggerCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeCcf_GetTriggersCfg({device_id})")
        TriggerCfg = self.CCF.XDfeCcf_GetTriggersCfg(device_id)
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeCcf_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Set trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: is a trigger configuration container.
	    :return: TriggerCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeCcf_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        TriggerCfg = self.CCF.XDfeCcf_SetTriggersCfg(device_id, TriggerCfg)
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeCcf_GetCC(self, device_id, CCID):
        """
        Get specified CCID carrier configuration.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
	    :return: CarrierCfg: is a trigger configuration container.
        """
        self.logger.debug(f"XDfeCcf_GetCC({device_id}, {CCID})")
        CarrierCfg = self.CCF.XDfeCcf_GetCC(device_id, CCID)
        self.logger.debug(f"CarrierCfg = {json.dumps(CarrierCfg, indent=2)}")
        return CarrierCfg

    def XDfeCcf_GetActiveSets(self, device_id):
        """
        Return a list indicating which coefficient sets are currently in use.

        :param device_id: id of the opened device.
	    :return: IsActive: variable indicating an activation status.
        """
        self.logger.debug(f"XDfeCcf_GetActiveSets({device_id})")
        IsActive = self.CCF.XDfeCcf_GetActiveSets(device_id)
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
        self.logger.debug(f"XDfeCcf_LoadCoefficients({device_id}, {Set}, {Shift}, {json.dumps(Coeffs, indent=2)})")
        Coeffs = self.CCF.XDfeCcf_LoadCoefficients(device_id, Set, Shift, Coeffs)
        self.logger.debug(f"Coeffs = {json.dumps(Coeffs, indent=2)}")
        return Coeffs

    def XDfeCcf_GetOverflowStatus(self, device_id):
        """
        Gets overflow event status.

        :param device_id: id of the opened device.
        :return: Status: overflow event status
        """
        self.logger.debug(f"XDfeCcf_GetOverflowStatus({device_id})")
        Status = self.CCF.XDfeCcf_GetOverflowStatus(device_id)
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeCcf_GetEventStatus(self, device_id):
        """
        Get event status

        :param device_id: id of the opened device.
        :return: Status: event status
        """
        self.logger.debug(f"XDfeCcf_GetEventStatus({device_id})")
        Status = self.CCF.XDfeCcf_GetEventStatus(device_id)
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
        self.logger.debug(f"XDfeCcf_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        self.CCF.XDfeCcf_ClearEventStatus(device_id, Status)
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
        self.logger.debug(f"XDfeCcf_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        self.CCF.XDfeCcf_SetInterruptMask(device_id, Mask)
        return

    def XDfeCcf_GetInterruptMask(self, device_id):
        """
        Get Interrupt mask

        :param device_id: id of the opened device.
        :return: Mask: interrupt mask value.
        """
        self.logger.debug(f"XDfeCcf_GetInterruptMask({device_id})")
        Mask = self.CCF.XDfeCcf_GetInterruptMask(device_id)
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
        self.CCF.XDfeCcf_SetTUserDelay(device_id, Delay)
        return

    def XDfeCcf_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfeCcf_GetTUserDelay({device_id})")
        Delay = self.CCF.XDfeCcf_GetTUserDelay(device_id)
        self.logger.debug(f"Delay = {Delay}")
        return Delay

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
        ret, TDataDelay = self.CCF.XDfeCcf_GetTDataDelay(device_id, Tap, CCID, Symmetric, Num)
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
        self.logger.debug(f"XDfeCcf_GetTDataDelayFromCCCfg({device_id}, {Tap}, {CCID}, {json.dumps(CCCfg, indent=2)})")
        ret, TDataDelay = self.CCF.XDfeCcf_GetTDataDelayFromCCCfg(device_id, Tap, CCID, CCCfg, Symmetric, Num)
        self.logger.debug(f"ret = {ret}, Latency = {TDataDelay}")
        return ret, TDataDelay

    def XDfeCcf_GetVersions(self, device_id):
        """
        This API is used to get the driver version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        self.logger.debug(f"XDfeCcf_GetVersions({device_id})")
        SwVersion, HwVersion = self.CCF.XDfeCcf_GetVersions(device_id)
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

    def __del__(self):
        logging.info("Inside CCF Pyro Client Destructor")

ccf = CCF_Client()
