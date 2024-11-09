# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import Pyro4
import logging
import base64
import json
import sys


class MIX_Client(object):
    MIX = None
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
        self.logger.info("Inside Mixer Pyro Client Constructor")
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
        API to inform MIXER Client the IP address and port number of MIXER Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None

        """    
        uri = f"PYRO:MIX@{ipaddr}:{port}"
        logging.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")   
        self.MIX = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.MIX.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.MIX.SetServerLogLevel(PythonLogLevel)
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
        self.MIX.SetMetalLogLevel(MetalLogLevel)
        return

    def GetMixMacro(self):
        """
        Return Dictionary with all MIX macros in the mix header file

        :param : None
        :return: Dictionary with all MIX macros in the mix header file
        """
        self.logger.debug("GetMixMacro()")
        mix_macro = self.MIX.GetMixMacro()
        self.logger.debug(f"mix_macro = {json.dumps(mix_macro, indent=2)}")
        return mix_macro

    # Get enum API
    def GetEnum_XDfeMix_StateId(self):
        """
        Return Dictionary equivalent of enum XDfeMix_StateId

        :param : None
        :return: Dictionary equivalent of enum XDfeMix_StateId
        """
        self.logger.debug("GetEnum_XDfeMix_StateId()")
        XDfeMix_StateId = self.MIX.GetEnum_XDfeMix_StateId()
        self.logger.debug(f"XDfeMix_StateId = {json.dumps(XDfeMix_StateId, indent=2)}")
        return XDfeMix_StateId

    def GetEnum_metal_log_level(self):
        """
        Return Dictionary equivalent of enum metal_log_level

        :param : None
        :return: Dictionary equivalent of enum metal_log_level
        """
        self.logger.debug("GetEnum_metal_log_level()")
        metal_log_level = self.MIX.GetEnum_metal_log_level()
        self.logger.debug(f"metal_log_level = {json.dumps(metal_log_level, indent=2)}")
        return metal_log_level

    # Get structure  API
    def GetStruct_XDfeMix_Version(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Version

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Version
        """
        self.logger.debug("GetStruct_XDfeMix_Version()")
        XDfeMix_Version = self.MIX.GetStruct_XDfeMix_Version()
        return XDfeMix_Version

    def GetStruct_XDfeMix_Trigger(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Trigger

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Trigger
        """
        self.logger.debug("GetStruct_XDfeMix_Trigger()")
        XDfeMix_Trigger = self.MIX.GetStruct_XDfeMix_Trigger()
        return XDfeMix_Trigger

    def GetStruct_XDfeMix_TriggerCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_TriggerCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_TriggerCfg
        """
        self.logger.debug("GetStruct_XDfeMix_TriggerCfg()")
        XDfeMix_TriggerCfg = self.MIX.GetStruct_XDfeMix_TriggerCfg()
        return XDfeMix_TriggerCfg

    def GetStruct_XDfeMix_CCSequence(self):
        """
        Return Dictionary equivalent of structure XDfeMix_CCSequence

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_CCSequence
        """
        self.logger.debug("GetStruct_XDfeMix_CCSequence()")
        XDfeMix_CCSequence = self.MIX.GetStruct_XDfeMix_CCSequence()
        return XDfeMix_CCSequence

    def GetStruct_XDfeMix_ModelParameters(self):
        """
        Return Dictionary equivalent of structure XDfeMix_ModelParameters

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_ModelParameters
        """
        self.logger.debug("GetStruct_XDfeMix_ModelParameters()")
        XDfeMix_ModelParameters = self.MIX.GetStruct_XDfeMix_ModelParameters()
        return XDfeMix_ModelParameters

    def GetStruct_XDfeMix_Cfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Cfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Cfg
        """
        self.logger.debug("GetStruct_XDfeMix_Cfg()")
        XDfeMix_Cfg = self.MIX.GetStruct_XDfeMix_Cfg()
        return XDfeMix_Cfg

    def GetStruct_XDfeMix_Init(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Init

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Init
        """
        self.logger.debug("GetStruct_XDfeMix_Init()")
        XDfeMix_Init = self.MIX.GetStruct_XDfeMix_Init()
        return XDfeMix_Init

    def GetStruct_XDfeMix_PhaseOffset(self):
        """
        Return Dictionary equivalent of structure XDfeMix_PhaseOffset

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_PhaseOffset
        """
        self.logger.debug("GetStruct_XDfeMix_PhaseOffset()")
        XDfeMix_PhaseOffset = self.MIX.GetStruct_XDfeMix_PhaseOffset()
        return XDfeMix_PhaseOffset

    def GetStruct_XDfeMix_Frequency(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Frequency

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Frequency
        """
        self.logger.debug("GetStruct_XDfeMix_Frequency()")
        XDfeMix_Frequency = self.MIX.GetStruct_XDfeMix_Frequency()
        return XDfeMix_Frequency

    def GetStruct_XDfeMix_Phase(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Phase

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Phase
        """
        self.logger.debug("GetStruct_XDfeMix_Phase()")
        XDfeMix_Phase = self.MIX.GetStruct_XDfeMix_Phase()
        return XDfeMix_Phase

    def GetStruct_XDfeMix_NCO(self):
        """
        Return Dictionary equivalent of structure XDfeMix_NCO

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_NCO
        """
        self.logger.debug("GetStruct_XDfeMix_NCO()")
        XDfeMix_NCO = self.MIX.GetStruct_XDfeMix_NCO()
        return XDfeMix_NCO

    def GetStruct_XDfeMix_InternalDUCDDCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_InternalDUCDDCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_InternalDUCDDCCfg
        """
        self.logger.debug("GetStruct_XDfeMix_InternalDUCDDCCfg()")
        XDfeMix_InternalDUCDDCCfg = self.MIX.GetStruct_XDfeMix_InternalDUCDDCCfg()
        return XDfeMix_InternalDUCDDCCfg

    def GetStruct_XDfeMix_DUCDDCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_DUCDDCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_DUCDDCCfg
        """
        self.logger.debug("GetStruct_XDfeMix_DUCDDCCfg()")
        XDfeMix_DUCDDCCfg = self.MIX.GetStruct_XDfeMix_DUCDDCCfg()
        return XDfeMix_DUCDDCCfg

    def GetStruct_XDfeMix_AuxiliaryCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_AuxiliaryCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_AuxiliaryCfg
        """
        self.logger.debug("GetStruct_XDfeMix_AuxiliaryCfg()")
        XDfeMix_AuxiliaryCfg = self.MIX.GetStruct_XDfeMix_AuxiliaryCfg()
        return XDfeMix_AuxiliaryCfg

    def GetStruct_XDfeMix_CarrierCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_CarrierCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_CarrierCfg
        """
        self.logger.debug("GetStruct_XDfeMix_CarrierCfg()")
        XDfeMix_CarrierCfg = self.MIX.GetStruct_XDfeMix_CarrierCfg()
        return XDfeMix_CarrierCfg

    def GetStruct_XDfeMix_AntennaCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_AntennaCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_AntennaCfg
        """
        self.logger.debug("GetStruct_XDfeMix_AntennaCfg()")
        XDfeMix_AntennaCfg = self.MIX.GetStruct_XDfeMix_AntennaCfg()
        return XDfeMix_AntennaCfg

    def GetStruct_XDfeMix_CCCfg(self):
        """
        Return Dictionary equivalent of structure XDfeMix_CCCfg

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_CCCfg
        """
        self.logger.debug("GetStruct_XDfeMix_CCCfg()")
        XDfeMix_CCCfg = self.MIX.GetStruct_XDfeMix_CCCfg()
        return XDfeMix_CCCfg

    def GetStruct_XDfeMix_DUCDDCStatus(self):
        """
        Return Dictionary equivalent of structure XDfeMix_DUCDDCStatus

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_DUCDDCStatus
        """
        self.logger.debug("GetStruct_XDfeMix_DUCDDCStatus()")
        XDfeMix_DUCDDCStatus = self.MIX.GetStruct_XDfeMix_DUCDDCStatus()
        return XDfeMix_DUCDDCStatus

    def GetStruct_XDfeMix_MixerStatus(self):
        """
        Return Dictionary equivalent of structure XDfeMix_MixerStatus

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_MixerStatus
        """
        self.logger.debug("GetStruct_XDfeMix_MixerStatus()")
        XDfeMix_MixerStatus = self.MIX.GetStruct_XDfeMix_MixerStatus()
        return XDfeMix_MixerStatus

    def GetStruct_XDfeMix_Status(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Status

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Status
        """
        self.logger.debug("GetStruct_XDfeMix_Status()")
        XDfeMix_Status = self.MIX.GetStruct_XDfeMix_Status()
        return XDfeMix_Status

    def GetStruct_XDfeMix_InterruptMask(self):
        """
        Return Dictionary equivalent of structure XDfeMix_InterruptMask

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_InterruptMask
        """
        self.logger.debug("GetStruct_XDfeMix_InterruptMask()")
        XDfeMix_InterruptMask = self.MIX.GetStruct_XDfeMix_InterruptMask()
        return XDfeMix_InterruptMask

    def GetStruct_XDfeMix_Config(self):
        """
        Return Dictionary equivalent of structure XDfeMix_Config

        :param : None
        :return: Dictionary equivalent of structure XDfeMix_Config
        """
        self.logger.debug("GetStruct_XDfeMix_Config()")
        XDfeMix_Config = self.MIX.GetStruct_XDfeMix_Config()
        return XDfeMix_Config

    def GetStruct_XDfeMix(self):
        """
        Return Dictionary equivalent of structure XDfeMix

        :param : None
        :return: Dictionary equivalent of structure XDfeMix
        """
        self.logger.debug("GetStruct_XDfeMix()")
        XDfeMix = self.MIX.GetStruct_XDfeMix()
        return XDfeMix

    # System initialization API
    def XDfeMix_InstanceInit(self, DeviceNodeName):
        """
        API initialises one instance of a Mixer driver.
        Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
        XDfeMix device with the name DeviceNodeName. The first available slot in
        the instances array XDfeMix_Mixer[] will be taken as a DeviceNodeName
        object. On success it moves the state machine to a Ready state, while on
        failure stays in a Not Ready state.

        :param DeviceNodeName: device node name.
        :return: ret - 0 on success, 1 on failure
                 device_id - integer handle to initialized instance
                 DeviceNodeNameRet - device node name returned from driver
                                     which will be same as the passed value

        """
        self.logger.info(f"XDfeMix_InstanceInit({DeviceNodeName})")
        DeviceNodeName = bytes(str(DeviceNodeName), 'utf-8')
        ret, device_id, DeviceNodeName = self.MIX.XDfeMix_InstanceInit(DeviceNodeName)
        DeviceNodeName = self.extract_b64_encoded_string(DeviceNodeName)
        self.logger.info(f"ret = {ret}, device_id = {device_id}, DeviceNodeName = {DeviceNodeName}")
        return ret, device_id, DeviceNodeName

    def XDfeMix_InstanceClose(self, device_id):
        """
        API closes the instances of a Mixer driver and moves the state machine to
        a Not Ready state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.info(f"XDfeMix_InstanceClose({device_id})")
        self.MIX.XDfeMix_InstanceClose(device_id)
        return

    # Register access API
    def XDfeMix_WriteReg(self, device_id, addr_offset, data):
        """
        Writes a value to register in a Mixer instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :param Data: is value to be written.
        :return: None
        """
        self.logger.debug(f"XDfeMix_WriteReg({device_id}, {hex(addr_offset)}, {hex(data)})")
        self.MIX.XDfeMix_WriteReg(device_id, addr_offset, data)
        return

    def XDfeMix_ReadReg(self, device_id, addr_offset):
        """
        Reads a value from the register from a Mixer instance.

        :param device_id: id of the opened device.
        :param AddrOffset: is address offset relative to instance base address.
        :return: regval: Register value.
        """
        self.logger.debug(f"XDfeMix_ReadReg({device_id}, {hex(addr_offset)})")
        regval = self.MIX.XDfeMix_ReadReg(device_id, addr_offset)
        self.logger.debug(f"regval = {regval}")
        return regval

    # DFE Mixer component initialization API
    def XDfeMix_Reset(self, device_id):
        """
        Resets and put block into a reset state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeMix_Reset({device_id})")
        self.MIX.XDfeMix_Reset(device_id)
        return

    def XDfeMix_Configure(self, device_id, Cfg):
        """
        Reads configuration from device tree/xparameters.h and IP registers.
        Removes S/W reset and moves the state machine to a Configured state.

        :param device_id: id of the opened device.
        :param Cfg: configuration data container.
        :return: Cfg: configuration data container.
        """
        self.logger.debug(f"XDfeMix_Configure({device_id}, {json.dumps(Cfg, indent=2)})")
        Cfg = self.MIX.XDfeMix_Configure(device_id, Cfg)
        self.logger.debug(f"Cfg = {json.dumps(Cfg, indent=2)}")
        return Cfg

    def XDfeMix_Initialize(self, device_id, Init):
        """
        DFE Mixer driver one time initialisation and moves the state machine to
        an Initialised state.

        :param device_id: id of the opened device.
        :param Init: initialisation data container.
        :return: Init: initialisation data container.
        """
        self.logger.debug(f"XDfeMix_Initialize({device_id}, {json.dumps(Init, indent=2)})")
        Init = self.MIX.XDfeMix_Initialize(device_id, Init)
        self.logger.debug(f"Init = {json.dumps(Init, indent=2)}")
        return Init

    def XDfeMix_Activate(self, device_id, EnableLowPower):
        """
        Activates Mixer and moves the state machine to an Activated state.

        :param device_id: id of the opened device.
        :param EnableLowPower: flag indicating low power.
        :return: None
        """
        self.logger.debug(f"XDfeMix_Activate({device_id}, {EnableLowPower})")
        self.MIX.XDfeMix_Activate(device_id, EnableLowPower)
        return

    def XDfeMix_Deactivate(self, device_id):
        """
        Deactivates Mixer and moves the state machine to Initialised state.

        :param device_id: id of the opened device.
        :return: None
        """
        self.logger.debug(f"XDfeMix_Deactivate({device_id})")
        self.MIX.XDfeMix_Deactivate(device_id)
        return

    def XDfeMix_GetStateID(self, device_id):
        """
        Gets a state machine state id. The state id is returned as a string.
        The enum is mapped to a dictionary in python.

        :param device_id: id of the opened device.
        :return: StateId: State machine StateID as a string
        """
        self.logger.debug(f"XDfeMix_GetStateID({device_id})")
        StateId = self.MIX.XDfeMix_GetStateID(device_id)
        self.logger.debug(f"Return value StateId = {StateId}")
        return StateId

    def XDfeMix_GetCurrentCCCfg(self, device_id, CurrCCCfg):
        """
        Returns the current CC configuration. Not used slot ID in a sequence
        (Sequence.CCID[Index]) are represented as (-1), not the value in registers.

        :param device_id: id of the opened device.
        :param CurrCCCfg: CC configuration container.
        :return: CurrCCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeMix_GetCurrentCCCfg({device_id}, {json.dumps(CurrCCCfg, indent=2)})")
        CurrCCCfg = self.MIX.XDfeMix_GetCurrentCCCfg(device_id, CurrCCCfg)
        self.logger.debug(f"CurrCCCfg = {json.dumps(CurrCCCfg, indent=2)}")
        return CurrCCCfg

    def XDfeMix_GetCurrentCCCfgSwitchable(self, device_id, CCCfgDownlink, CCCfgUplink):
        """
		Returns the current CC configuration for DL and UL in switchable mode.
		Not used slot ID in a sequence (Sequence.CCID[Index]) are represented
		as (-1), not the value in registers.

        :param device_id: id of the opened device.
		:param CCCfgDownlink: Downlink CC configuration container.
		:param CCCfgUplink: Uplink CC configuration container.
        :return: CCCfgDownlink, CCCfgUplink: CC configuration containers
        """
        self.logger.debug(f"XDfeMix_GetCurrentCCCfgSwitchable({device_id}, "
						  f"{json.dumps(CCCfgDownlink, indent=2)}, "
						  f"{json.dumps(CCCfgUplink, indent=2)})")
        CCCfgDownlink, CCCfgUplink = self.MIX.XDfeMix_GetCurrentCCCfgSwitchable(device_id, CCCfgDownlink, CCCfgUplink)
        self.logger.debug(f"CCCfgDownlink = {json.dumps(CCCfgDownlink, indent=2)}")
        self.logger.debug(f"CCCfgUplink = {json.dumps(CCCfgUplink, indent=2)}")
        return CCCfgDownlink, CCCfgUplink

    def XDfeMix_GetEmptyCCCfg(self, device_id):
        """
        Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
        in XDfeMix_Configure(), array CCCfg->Sequence.CCID[] members are set to not
        used value (-1) and the other CCCfg members are set to 0.

        :param device_id: id of the opened device.
        :return: CCCfg: CC configuration container
        """
        self.logger.debug(f"XDfeMix_GetEmptyCCCfg({device_id})")
        CCCfg = self.MIX.XDfeMix_GetEmptyCCCfg(device_id)
        self.logger.debug(f"CCCfg = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeMix_GetCarrierCfgAndNCO(self, device_id, CCCfg, CCID):
        """
        Returns the current CC sequence bitmap, CCID carrier configuration and
        NCO configuration.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCSeqBitmap: CC slot position container.
                 CarrierCfg: CC configuration container.
                 NCO: NCO configuration container.
        """
        self.logger.debug(f"XDfeMix_GetCarrierCfgAndNCO({device_id}, {json.dumps(CCCfg, indent=2)}, {CCID})")
        CCSeqBitmap, CarrierCfg, NCO = self.MIX.XDfeMix_GetCarrierCfgAndNCO(device_id, CCCfg, CCID)
        self.logger.debug(f"Return value = {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)},"
                          f" {json.dumps(NCO, indent=2)}")
        return CCSeqBitmap, CarrierCfg, NCO

    def XDfeMix_SetAntennaCfgInCCCfg(self, device_id, CCCfg, AntennaCfg):
        """
        Set antenna configuration in CC configuration container.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param AntennaCfg: Array of all antenna configurations.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_SetAntennaCfgInCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, {json.dumps(AntennaCfg, indent=2)})")
        CCCfg = self.MIX.XDfeMix_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeMix_AddCCtoCCCfg(self, device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg, NCO):
        """
        Adds specified CCID, with specified configuration, to a local CC
        configuration structure.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).

        The returned CCCfg.Sequence is transleted as there is no explicit indication
        that SEQUENCE[i] is not used - 0 can define the slot as either used or
        not used. Sequence data that is returned in the CCIDSequence is not the same
        as what is written in the registers. The translation is:
            - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
            - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
            - a returned CCIDSequence->Length = length in register + 1

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CCSeqBitmap: CC slot position container.
        :param CarrierCfg: CC configuration container.
        :param NCO: NCO configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_AddCCtoCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {CCSeqBitmap}, {json.dumps(CarrierCfg, indent=2)}, "
                          f"{json.dumps(NCO, indent=2)})")
        ret, CCCfg = self.MIX.XDfeMix_AddCCtoCCCfg(device_id, CCCfg, CCID, CCSeqBitmap,
                                                   CarrierCfg, NCO)
        self.logger.debug(f"Return value = {ret}, {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeMix_RemoveCCfromCCCfg(self, device_id, CCCfg, CCID):
        """
        Removes specified CCID from a local CC configuration structure.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_RemoveCCfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {CCID})")
        CCCfg = self.MIX.XDfeMix_RemoveCCfromCCCfg(device_id, CCCfg, CCID)
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeMix_AddAuxNCOtoCCCfg(self, device_id, CCCfg, AuxId, NCO, AuxCfg):
        """
		Adds specified auxiliary NCO, with specified configuration, to a local CCCfg.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param AuxId: Channel ID.
        :param NCO: Auxiliary NCO configuration container.
        :param AuxCfg: Auxiliary NCO configuration container.
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_AddAuxNCOtoCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{AuxId}, {json.dumps(AuxCfg, indent=2)})")
        CCCfg = self.MIX.XDfeMix_AddAuxNCOtoCCCfg(device_id, CCCfg, AuxId, NCO, AuxCfg)
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeMix_RemoveAuxNCOfromCCCfg(self, device_id, CCCfg, AuxId):
        """
		Disables specified auxiliary NCO configuration structure.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param AuxId: Auxiliary NCO ID to be disabled, range [0-3].
        :return: CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_RemoveAuxNCOfromCCCfg({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)}, {AuxId})")
        CCCfg = self.MIX.XDfeMix_RemoveAuxNCOfromCCCfg(device_id, CCCfg, AuxId)
        self.logger.debug(f"Return value = {json.dumps(CCCfg, indent=2)}")
        return CCCfg

    def XDfeMix_UpdateCCinCCCfg(self, device_id, CCCfg, CCID, CarrierCfg):
        """
        Updates specified CCID, with specified configuration to a local CC
        configuration structure.
        If there is insufficient capacity for the new CC the function will return
        an error.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :param CCID: Channel ID.
        :param CarrierCfg: CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CarrierCfg: is a CC configuration container.
        """
        self.logger.debug(f"XDfeMix_UpdateCCinCCCfg({device_id}, {json.dumps(CCCfg, indent=2)}, "
                          f"{CCID}, {json.dumps(CarrierCfg, indent=2)}")
        ret, CCCfg = self.MIX.XDfeMix_UpdateCCinCCCfg(device_id, CCCfg, CCID, CarrierCfg)
        self.logger.debug(f"Return value CCCfg = {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeMix_SetNextCCCfgAndTrigger(self, device_id, CCCfg):
        """
        Writes local CC configuration to the shadow (NEXT) registers and triggers
        copying from shadow to operational registers.

        :param device_id: id of the opened device.
        :param CCCfg: component carrier (CC) configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfg: component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_SetNextCCCfgAndTrigger({device_id}, "
                          f"{json.dumps(CCCfg, indent=2)})")
        ret, CCCfg = self.MIX.XDfeMix_SetNextCCCfgAndTrigger(device_id, CCCfg)
        self.logger.debug(f"ret = {ret}, CCCfg = {json.dumps(CCCfg, indent=2)}")
        return ret, CCCfg

    def XDfeMix_SetNextCCCfgAndTriggerSwitchable(self, device_id, CCCfgDownlink, CCCfgUplink):
        """
		Writes local CC configuration to the shadow (NEXT) registers and triggers
		copying from shadow to operational (CURRENT) registers.

        :param device_id: id of the opened device.
        :param CCCfgDownlink: Downlink CC configuration container.
        :param CCCfgUplink Uplink CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CCCfgDownlink: Downlink component carrier (CC) configuration container.
                 CCCfgUplink: Uplink component carrier (CC) configuration container.
        """
        self.logger.debug(f"XDfeMix_SetNextCCCfgAndTriggerSwitchable({device_id}, "
                          f"{json.dumps(CCCfgDownlink, indent=2)}, "
                          f"{json.dumps(CCCfgDownlink, indent=2)})")
        ret, CCCfgDownlink, CCCfgUplink = self.MIX.XDfeMix_SetNextCCCfgAndTriggerSwitchable(device_id, CCCfgDownlink, CCCfgUplink)
        self.logger.debug(f"ret = {ret}, CCCfgDownlink = {json.dumps(CCCfgDownlink, indent=2)}, , CCCfgUplink = {json.dumps(CCCfgUplink, indent=2)}")
        return ret, CCCfgDownlink, CCCfgUplink

    def XDfeMix_AddCC(self, device_id, CCID, BitSequence, CarrierCfg, NCO):
        """
        Adds specified CCID, with specified configuration.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

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
        :param NCO: NCO configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CarrierCfg: is a CC configuration container.
        """
        self.logger.debug(f"XDfeMix_AddCC({device_id}, {CCID}, {BitSequence}, "
                          f"{json.dumps(CarrierCfg, indent=2)}, "
                          f"{json.dumps(NCO, indent=2)})")
        ret, CarrierCfg = self.MIX.XDfeMix_AddCC(device_id, CCID, BitSequence, CarrierCfg, NCO)
        self.logger.debug(f"ret = {ret}, CarrerCfg = {json.dumps(CarrierCfg, indent=2)})")
        return ret, CarrierCfg

    def XDfeMix_RemoveCC(self, device_id, CCID):
        """
        Removes specified CCID.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeMix_RemoveCC({device_id}, {CCID})")
        ret = self.MIX.XDfeMix_RemoveCC(device_id, CCID)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_MoveCC(self, device_id, CCID, Rate, FromNCO, ToNCO):
        """
        Moves specified CCID from one NCO to another aligning phase to make it
        transparent.
        Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param Rate: is a NCO rate value.
        :param FromNCO: is a NCO value moving from.
        :param ToNCO: is a NCO value moving to.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeMix_MoveCC({device_id}, {CCID}, {Rate}, {FromNCO}, {ToNCO})")
        ret = self.MIX.XDfeMix_MoveCC(device_id, CCID, Rate, FromNCO, ToNCO)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_UpdateCC(self, device_id, CCID, CarrierCfg):
        """
        Updates specified CCID, with a configuration defined in CarrierCfg
        structure.
        If there is insufficient capacity for the new CC the function will return
        an error.
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param CCID: is a Channel ID.
        :param CarrierCfg: is a CC configuration container.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeMix_UpdateCC({device_id}, {CCID}, "
                          f"{json.dumps(CarrierCfg, indent=2)})")
        ret = self.MIX.XDfeMix_UpdateCC(device_id, CCID, CarrierCfg)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_SetAntennaGain(self, device_id, AntennaId, AntennaGain):
        """
        Sets antenna gain. Initiate CC update (enable CCUpdate trigger TUSER
        Single Shot).
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param AntennaId: is an antenna ID.
        :param AntennaGain: is an antenna gain.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeMix_SetAntennaGain({device_id}, {AntennaId}, {AntennaGain})")
        ret = self.MIX.XDfeMix_SetAntennaGain(device_id, AntennaId, AntennaGain)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_UpdateAntennaCfg(self, device_id, AntennaCfg):
        """
        Updates antenna configuration to all antennas.
        Note: Clear event status with XDfeMix_ClearEventStatus() before running this API.

        :param device_id: id of the opened device.
        :param AntennaCfg: Array of all antenna configurations.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
        """
        self.logger.debug(f"XDfeMix_UpdateAntennaCfg({device_id}, {json.dumps(AntennaCfg, indent=2)})")
        ret = self.MIX.XDfeMix_UpdateAntennaCfg(device_id, AntennaCfg)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_GetTriggersCfg(self, device_id):
        """
        Returns current trigger configuration.

        :param device_id: id of the opened device.
        :return: TriggerCfg: trigger configuration container
        """
        self.logger.debug(f"XDfeMix_GetTriggersCfg({device_id})")
        TriggerCfg = self.MIX.XDfeMix_GetTriggersCfg(device_id)
        self.logger.debug(f"TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeMix_SetTriggersCfg(self, device_id, TriggerCfg):
        """
        Sets trigger configuration.

        :param device_id: id of the opened device.
        :param TriggerCfg: trigger configuration container.
        :return: TriggerCfg: trigger configuration container.
        """
        self.logger.debug(f"XDfeMix_SetTriggersCfg({device_id}, {json.dumps(TriggerCfg, indent=2)})")
        TriggerCfg = self.MIX.XDfeMix_SetTriggersCfg(device_id, TriggerCfg)
        self.logger.debug(f"The return value TriggerCfg = {json.dumps(TriggerCfg, indent=2)}")
        return TriggerCfg

    def XDfeMix_GetDUCDDCStatus(self, device_id):
        """
        Gets DUC/DDC overflow status.

        :param device_id: id of the opened device.
        :return: DUCDDCStatus: DUC/DDC status container.
        """
        self.logger.debug(f"XDfeMix_GetDUCDDCStatus({device_id})")
        DUCDDCStatus = self.MIX.XDfeMix_GetDUCDDCStatus(device_id)
        self.logger.debug(f"The return value DUCDDCStatus = {json.dumps(DUCDDCStatus, indent=2)}")
        return DUCDDCStatus

    def XDfeMix_GetMixerStatus(self, device_id):
        """
        Gets Mixer overflow status.

        :param device_id: id of the opened device.
        :return: DUCDDCStatus: DUC/DDC status container.
        """
        self.logger.debug(f"XDfeMix_GetMixerStatus({device_id})")
        MixerStatus = self.MIX.XDfeMix_GetMixerStatus(device_id)
        self.logger.debug(f"MixerStatus = {json.dumps(MixerStatus, indent=2)}")
        return MixerStatus

    def XDfeMix_GetInterruptMask(self, device_id):
        """
        Gets interrupt mask status.

        :param device_id: id of the opened device.
        :return: Mask: interrupt masks container.
        """
        self.logger.debug(f"XDfeMix_GetInterruptMask({device_id})")
        Mask = self.MIX.XDfeMix_GetInterruptMask(device_id)
        self.logger.debug(f"Mask = {json.dumps(Mask, indent=2)}")
        return Mask

    def XDfeMix_SetInterruptMask(self, device_id, Mask):
        """
        Sets interrupt mask.

        :param device_id: id of the opened device.
        :param Mask: interrupt masks flags container.
                     0 - does not mask coresponding interrupt
                     1 - masks coresponding interrupt
        :return: None
        """
        self.logger.debug(f"XDfeMix_SetInterruptMask({device_id}, {json.dumps(Mask, indent=2)})")
        self.MIX.XDfeMix_SetInterruptMask(device_id, Mask)
        return

    def XDfeMix_GetEventStatus(self, device_id):
        """
        Gets event status.

        :param device_id: id of the opened device.
        :return: Status: event status container.
        """
        self.logger.debug(f"XDfeMix_GetEventStatus({device_id})")
        Status = self.MIX.XDfeMix_GetEventStatus(device_id)
        self.logger.debug(f"Status = {json.dumps(Status, indent=2)}")
        return Status

    def XDfeMix_ClearEventStatus(self, device_id, Status):
        """
        Clears event status.

        :param device_id: id of the opened device.
        :param Status: Clear event status container.
                       0 - does not clear coresponding event status
                       1 - clear coresponding event status
        :return: None
        """
        self.logger.debug(f"XDfeMix_ClearEventStatus({device_id}, {json.dumps(Status, indent=2)})")
        self.MIX.XDfeMix_ClearEventStatus(device_id, Status)
        return

    def XDfeMix_SetTUserDelay(self, device_id, Delay):
        """
        Sets the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :param Delay: requested delay variable.
        :return: None
        """
        self.logger.debug(f"XDfeMix_SetTUserDelay({device_id}, {Delay})")
        self.MIX.XDfeMix_SetTUserDelay(device_id, Delay)
        return

    def XDfeMix_GetTUserDelay(self, device_id):
        """
        Reads the delay, which will be added to TUSER and TLAST (delay matched
        through the IP).

        :param device_id: id of the opened device.
        :return: ret: Delay value
        """
        self.logger.debug(f"XDfeMix_GetTUserDelay({device_id})")
        ret = self.MIX.XDfeMix_GetTUserDelay(device_id)
        self.logger.debug(f"ret = {ret}")
        return ret

    def XDfeMix_GetTDataDelay(self, device_id, Tap):
        """
        Returns data latency + tap.

        :param device_id: id of the opened device.
        :param Tap: Tap value.
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 TDataDelay: Returned Data latency value.
        """
        self.logger.debug(f"XDfeMix_GetTDataDelay({device_id}, {Tap})")
        ret, TDataDelay = self.MIX.XDfeMix_GetTDataDelay(device_id, Tap)
        self.logger.debug(f"TDataDelay = {json.dumps(TDataDelay, indent=2)}")
        self.logger.debug(f"ret = {ret}")
        return ret, TDataDelay

    def XDfeMix_GetCenterTap(self, device_id, Rate):
        """
        Returns predefined Central Tap value for chosen RATE.

        :param device_id: id of the opened device.
        :param Rate: Interpolation/decimation rate index value [1-5].
        :return: ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
                 CenterTap: Returned Central Tap value.
        """
        self.logger.debug(f"XDfeMix_GetCenterTap({device_id}, {Rate})")
        ret, CenterTap = self.MIX.XDfeMix_GetCenterTap(device_id, Rate)
        self.logger.debug(f"CenterTap = {json.dumps(CenterTap, indent=2)}")
        self.logger.debug(f"ret = {ret}")
        return ret, CenterTap

    def XDfeMix_SetRegBank(self, device_id, RegBank):
        """
        Sets uplink/downlink register bank.

        :param device_id: id of the opened device.
        :param RegBank: Register bank value to be set.
        :return: None
        """
        self.logger.debug(f"XDfeMix_SetRegBank({device_id}, {RegBank})")
        self.MIX.XDfeMix_SetRegBank(device_id, RegBank)
        return

    def XDfeMix_GetVersions(self, device_id):
        """
        This API gets the driver and HW design version.

        :param device_id: id of the opened device.
        :return: SwVersion: driver version numbers.
                 HwVersion: HW version numbers.
        """
        self.logger.debug(f"XDfeMix_GetVersions({device_id})")
        SwVersion, HwVersion = self.MIX.XDfeMix_GetVersions(device_id)
        self.logger.debug(f"SwVersion = {json.dumps(SwVersion, indent=2)}")
        self.logger.debug(f"HwVersion = {json.dumps(HwVersion, indent=2)}")
        return SwVersion, HwVersion

mix = MIX_Client()
