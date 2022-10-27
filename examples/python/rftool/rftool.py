# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
sys.path.append('../../../xclient/rfdc')
sys.path.append('../../../xclient/data_stream/data_transfer_no_dma')
sys.path.append('/usr/share/raft/xclient/rfdc')
sys.path.append('/usr/share/raft/xclient/data_stream/data_transfer_no_dma')
from rfdc_client import RFDC_Client
from rfclk_client import RFCLK_CLIENT
from axi_memmap_client import AXI_MEMMAP_Client
import logging
import time
import numpy as np


class Rftool(RFDC_Client, RFCLK_CLIENT, AXI_MEMMAP_Client):
    logger = None

    # Function return values
    SUCCESS = 0
    FAIL = 1
    ERROR_EXECUTE = 3
    WARN_EXECUTE = 4

    # RFCLK Values
    RFCLK_LMX2594_1 = 0
    RFCLK_LMX2594_2 = 1
    RFCLK_LMK = 2
    DEFAULT_RFCLK_LMK_CONFIG = 0
    MAX_DATA_SIZE_LMK = 128
    MAX_DATA_SIZE_LMX = 116

    # ADC and DAC - Tile and Block Values
    XRFDC_ADC_TILE = 0
    XRFDC_DAC_TILE = 1
    MAX_DAC_TILE = 4
    MAX_ADC_TILE = 4
    ADC = 0
    DAC = 1
    MAX_DAC = 16
    MAX_BLOCK_ID = 2
    AdcMemMap = [0] * 16
    DacMemMap = [0] * 16
    AdcMap = [{} for _ in range(16)]
    DacMap = [{} for _ in range(16)]

    # Mixer Mode
    XRFDC_MIXER_MODE_OFF = 0
    XRFDC_MIXER_MODE_C2C = 1
    XRFDC_MIXER_MODE_C2R = 2
    XRFDC_MIXER_MODE_R2C = 3
    XRFDC_MIXER_MODE_R2R = 4
    XRFDC_MIXER_TYPE_COARSE = 1
    XRFDC_MIXER_TYPE_FINE = 2
    XRFDC_COARSE_MIX_BYPASS = 0x10
    DEFAULT_DECIMATION_FACTOR = 1
    XRFDC_EVENT_MIXER = 1
    XRFDC_INTERP_DECIM_OFF = 0
    DEFAULT_INTERPOLATION_FACTOR = 1
    XRFDC_EVNT_SRC_TILE = 2
    DEFAULT_DATA_PATH_MODE = 4

    # MMCM variable
    MMCMFin = [0] * 8

    # Local Memory variables
    LMEM_INFO = 0
    LMEM_TRIGGER = 0x04
    LMEM_ENABLE = 0x08
    LMEM_ENABLE_TILE = 0x0C
    LMEM0_ENDADDR = 0x10

    # Base Address and size
    DAC_SOURCE_I_BASEADDR = 0xB0000000
    ADC_SINK_I_BASEADDR = 0xB0400000
    FIFO_SIZE = 16 * 1024 * 2

    # Board name
    BOARD = "zcu208"

    info = {
        "paddr_dac": 0xB0000000,
        "paddr_adc": 0xB0400000,
        "clk_wiz_dac0": 0xB4C00000,
        "clk_wiz_dac1": 0xB4C10000,
        "clk_wiz_dac2": 0xB4C20000,
        "clk_wiz_dac3": 0xB4C30000,
        "clk_wiz_adc0": 0xB4C40000,
        "clk_wiz_adc1": 0xB4C50000,
        "clk_wiz_adc2": 0xB4C60000,
        "clk_wiz_adc3": 0xB4C70000,
        "mts_enable_dac_mask": 0,
        "mts_enable_adc_mask": 0
    }

    LogLevelsDict = {
        "DEBUG": 4,
        "INFO": 3,
        "WARNING": 2,
        "ERROR": 1,
        "CRITICAL": 0
    }

    def __init__(self):
        self.logger = self.GetLogger()
        self.logger.info("Inside RFtool Constructor")
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

    def SetLogLevel(self, PythonLogLevel):
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

    def SetBoardName(self, board_name):
        """
        API to inform the Rftool class the board under use.
        zcu208 and zcu216 are the currently supported boards

        :param board_name: name of the board in use. "zcu208" or "zcu216"
        :return: None
        """
        self.BOARD = board_name
        return

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform the Rftool class the IP address and port number
        of the board to communicate.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None
        """
        RFDC_Client.SetIpAndPort(self, ipaddr, port)
        RFCLK_CLIENT.SetIpAndPort(self, ipaddr, port)
        AXI_MEMMAP_Client.SetIpAndPort(self, ipaddr, port)
        return

    def Initialize(self):
        """
        Initialization of the Rftool functionalities

        :param None
        :return: ret: 0 on Success else failure
                 inst_id: RFDC instance id
        """
        def RFClk_Initialize():
            if self.BOARD == "zcu208":
                ret_rfclk_init = self.XRFClk_Init(493)
            else:
                ret_rfclk_init = self.XRFClk_Init(485)
            if ret_rfclk_init == self.SUCCESS:
                ret_rfclk_config = self.XRFClk_SetConfigOnOneChipFromConfigId(self.RFCLK_LMK, self.DEFAULT_RFCLK_LMK_CONFIG)
                if ret_rfclk_config == self.SUCCESS:
                    ret_rfclk_write = self.XRFClk_WriteReg(self.RFCLK_LMX2594_1, 0x1)
                    if ret_rfclk_write == self.SUCCESS:
                        ret_rfclk_write = self.XRFClk_WriteReg(self.RFCLK_LMX2594_2, 0x1)
                        if ret_rfclk_write != self.SUCCESS:
                            logging.warning("RFCLK: XRFClk_WriteReg RFCLK_LMX2594_2 failed")
                    else:
                        logging.warning("RFCLK: XRFClk_WriteReg RFCLK_LMX2594_1 failed")
                else:
                    logging.warning("RFCLK: XRFClk_SetConfigOnOneChipFromConfigId failed.")
            else:
                logging.warning("RFCLK: XRFClk_Init failed.")
            return

        def RFDC_Initalize():
            inst_id = 0
            ret, Config = self.XRFdc_LookupConfig(0)
            if ret == self.SUCCESS:
                ret, inst_id = self.XRFdc_RegisterMetal(0)
                if ret == self.SUCCESS:
                    ret, Config = self.XRFdc_CfgInitialize(inst_id, Config)
                    if ret != self.SUCCESS:
                        logging.error("RFDC: XRFdc_CfgInitialize failed.")
                else:
                    logging.error("RFDC: XRFdc_RegisterMetal failed.")
            else:
                logging.error("RFDC: XRFdc_LookupConfig failed.")
            return ret, inst_id

        def RFInitBuildMemoryMap(inst_id):
            mem_info = self.lmem_rd32(self.info["paddr_adc"])
            mem_size = mem_info & 0x00FFFFFF
            num_mem = (mem_info >> 24) & 0x0000007f
            mem_size = int(2 * mem_size / (num_mem + 1) / 16)
            CurAddr = self.info["paddr_adc"] + mem_size
            channel = 0
            i = 0
            for Tile_Id in range(4):
                high_speed_adc = self.XRFdc_IsHighSpeedADC(inst_id, Tile_Id)
                if 1 == high_speed_adc:
                    numblockpertile = 1
                else:
                    numblockpertile = 4
                for Block_Id in range(numblockpertile):
                    i += 1
                    enable = self.XRFdc_IsADCDigitalPathEnabled(inst_id, Tile_Id, Block_Id)
                    if enable != 0:
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_I"] = CurAddr
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_I"] = channel
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["channel"] = Tile_Id * numblockpertile + Block_Id
                        self.AdcMemMap[channel] = Tile_Id * numblockpertile + Block_Id
                        CurAddr += mem_size
                        channel += 1
                        high_speed_adc = self.XRFdc_IsHighSpeedADC(inst_id, Tile_Id)
                        if 1 == high_speed_adc:
                            ADC4GSPS = 1
                        else:
                            ADC4GSPS = 0
                        data_type = self.XRFdc_GetDataType(inst_id, self.ADC, Tile_Id, Block_Id << ADC4GSPS)
                        if (high_speed_adc and data_type) != 0:
                            self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_Q"] = CurAddr
                            self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_Q"] = channel
                            self.AdcMemMap[channel] = Tile_Id * numblockpertile + Block_Id
                            CurAddr += mem_size
                            channel += 1
                        else:
                            self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_Q"] = \
                                self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_I"]
                            self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_Q"] = \
                                self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_I"]
                    else:
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_I"] = 0xffffffff
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["addr_Q"] = 0xffffffff
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_I"] = 0xffffffff
                        self.AdcMap[Tile_Id * numblockpertile + Block_Id]["Channel_Q"] = 0xffffffff
            for i in range(i, 16):
                self.AdcMap[i]["addr_I"] = 0xffffffff
                self.AdcMap[i]["addr_Q"] = 0xffffffff
                self.AdcMap[i]["Channel_I"] = 0xffffffff
                self.AdcMap[i]["Channel_Q"] = 0xffffffff
            channel = 0
            i = 0
            mem_info = self.lmem_rd32(self.info["paddr_dac"])
            mem_size = mem_info & 0x00FFFFFF
            num_mem = (mem_info >> 24) & 0x0000007f
            mem_size = int(2 * mem_size / (num_mem + 1) / 16)
            CurAddr = self.info["paddr_dac"] + mem_size
            for Tile_Id in range(4):
                for Block_Id in range(4):
                    i += 1
                    enable = self.XRFdc_IsDACDigitalPathEnabled(inst_id, Tile_Id, Block_Id)
                    if enable != 0:
                        self.DacMap[Tile_Id * 4 + Block_Id]["addr_I"] = CurAddr
                        self.DacMap[Tile_Id * 4 + Block_Id]["addr_Q"] = CurAddr
                        self.DacMap[Tile_Id * 4 + Block_Id]["Channel_I"] = channel
                        self.DacMap[Tile_Id * 4 + Block_Id]["Channel_Q"] = channel
                        self.DacMemMap[channel] = Tile_Id * 4 + Block_Id
                        CurAddr += mem_size
                        channel += 1
                    else:
                        self.DacMap[Tile_Id * 4 + Block_Id]["addr_I"] = 0xffffffff
                        self.DacMap[Tile_Id * 4 + Block_Id]["addr_Q"] = 0xffffffff
                        self.DacMap[Tile_Id * 4 + Block_Id]["Channel_I"] = 0xffffffff
                        self.DacMap[Tile_Id * 4 + Block_Id]["Channel_Q"] = 0xffffffff
            for i in range(i, 16):
                self.DacMap[i]["addr_I"] = 0xffffffff
                self.DacMap[i]["addr_Q"] = 0xffffffff
                self.DacMap[i]["Channel_I"] = 0xffffffff
                self.DacMap[i]["Channel_Q"] = 0xffffffff

        def InitMMCM_ADC(inst_id):
            MTSenable = 0
            ClkWiz_Id = 0
            status = 0
            for Tile_Id in range(4):
                tile_enable = self.XRFdc_CheckTileEnabled(inst_id, self.XRFDC_ADC_TILE, Tile_Id)
                if tile_enable == self.SUCCESS:
                    if (Tile_Id & (not MTSenable)) == 0:
                        ClkBaseAddr = self.info["clk_wiz_adc0"]
                    elif (Tile_Id & (not MTSenable)) == 1:
                        ClkBaseAddr = self.info["clk_wiz_adc1"]
                    elif (Tile_Id & (not MTSenable)) == 2:
                        ClkBaseAddr = self.info["clk_wiz_adc2"]
                    elif (Tile_Id & (not MTSenable)) == 3:
                        ClkBaseAddr = self.info["clk_wiz_adc3"]
                    else:
                        ClkBaseAddr = 0
                    if ClkBaseAddr != 0:
                        ClkConfigReg = self.lmem_rd32(ClkBaseAddr + 0x200)
                        mult = (ClkConfigReg & 0x0000ff00) >> 8
                        div = ClkConfigReg & 0x000000ff
                        fracmult = (ClkConfigReg & 0x03ff0000) >> 16
                        mult = (1000 * mult) + fracmult
                        ClkConfigReg = self.lmem_rd32(ClkBaseAddr + 0x208)
                        clkoutdiv = ClkConfigReg & 0x000000ff
                        clkoutfrac = (ClkConfigReg & 0x0003ff00) >> 8
                        clkoutdiv = (1000 * clkoutdiv) + clkoutfrac
                        status, PLLSettings = self.XRFdc_GetPLLConfig(inst_id, self.XRFDC_ADC_TILE, Tile_Id)
                        SampleRate = int(1000000 * PLLSettings["SampleRate"]) & 0xffffffff
                        Block_Id = 0
                        for Block_Id in range(4):
                            enable = self.XRFdc_CheckDigitalPathEnabled(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id)
                            if enable != self.SUCCESS:
                                Block_Id += 1
                            else:
                                break
                        ret, FabricDataRate = self.XRFdc_GetFabRdVldWords(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id)
                        status |= ret
                        ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id)
                        status |= ret
                        high_speed_adc = self.XRFdc_IsHighSpeedADC(inst_id, Tile_Id)
                        if (Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2R) or \
                                high_speed_adc or (Mixer_Settings["MixerType"] == self.XRFDC_MIXER_TYPE_COARSE and
                                                   Mixer_Settings["CoarseMixFreq"] == self.XRFDC_COARSE_MIX_BYPASS):
                            DataIQ = 1
                        else:
                            DataIQ = 2

                        ret, DecimationFactor = self.XRFdc_GetDecimationFactor(inst_id, Tile_Id, Block_Id)
                        status |= ret
                        MmcmFout = int(SampleRate * DataIQ / (DecimationFactor * FabricDataRate)) & 0xffffffff
                        self.MMCMFin[ClkWiz_Id] = int(MmcmFout * div * clkoutdiv) & 0xffffffff
                        self.MMCMFin[ClkWiz_Id] = int(self.MMCMFin[ClkWiz_Id] / mult) & 0xffffffff
                    else:
                        self.MMCMFin[ClkWiz_Id] = 0
                    ClkWiz_Id += 1
            return status

        def InitMMCM_DAC(inst_id):
            MTSenable = 0
            ClkWiz_Id = 4
            status = 0
            InterDecim = 1
            for Tile_Id in range(4):
                enable = self.XRFdc_CheckTileEnabled(inst_id, self.XRFDC_DAC_TILE, Tile_Id)
                if enable == self.SUCCESS:
                    if Tile_Id & (not MTSenable) == 0:
                        ClkBaseAddr = self.info["clk_wiz_dac0"]
                    elif Tile_Id & (not MTSenable) == 1:
                        ClkBaseAddr = self.info["clk_wiz_dac1"]
                    elif (Tile_Id & (not MTSenable)) == 2:
                        ClkBaseAddr = self.info["clk_wiz_dac2"]
                    elif (Tile_Id & (not MTSenable)) == 3:
                        ClkBaseAddr = self.info["clk_wiz_dac3"]
                    else:
                        ClkBaseAddr = 0
                    if ClkBaseAddr != 0:
                        ClkConfigReg = self.lmem_rd32(ClkBaseAddr + 0x200)
                        mult = (ClkConfigReg & 0x0000ff00) >> 8
                        div = ClkConfigReg & 0x000000ff
                        fracmult = (ClkConfigReg & 0x03ff0000) >> 16
                        mult = (1000 * mult) + fracmult
                        ClkConfigReg = self.lmem_rd32(ClkBaseAddr + 0x208)
                        clkoutdiv = ClkConfigReg & 0x000000ff
                        clkoutfrac = (ClkConfigReg & 0x0003ff00) >> 8
                        clkoutdiv = (1000 * clkoutdiv) + clkoutfrac
                        status, PLLSettings = self.XRFdc_GetPLLConfig(inst_id, self.XRFDC_DAC_TILE, Tile_Id)
                        SampleRate = int(1000000 * PLLSettings["SampleRate"]) & 0xffffffff
                        Block_Id = 0
                        for Block_Id in range(4):
                            enable = self.XRFdc_CheckDigitalPathEnabled(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id)
                            if enable != self.SUCCESS:
                                Block_Id += 1
                            else:
                                break
                        ret, FabricDataRate = self.XRFdc_GetFabRdVldWords(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id)
                        status |= ret
                        ret, DataPathMode = self.XRFdc_GetDataPathMode(inst_id, Tile_Id, Block_Id)
                        status |= ret
                        if DataPathMode != 4:
                            ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id)
                            status |= ret
                            ret, InterDecim = self.XRFdc_GetInterpolationFactor(inst_id, Tile_Id, Block_Id)
                            status |= ret
                        if DataPathMode == 2 or DataPathMode == 3:
                            InterDecim = 2 * InterDecim

                        if DataPathMode == 4 or (Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2R) or \
                                Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2C or \
                                (Mixer_Settings["MixerType"] == self.XRFDC_MIXER_TYPE_COARSE and
                                 Mixer_Settings["CoarseMixFreq"] == self.XRFDC_COARSE_MIX_BYPASS):
                            DataIQ = 1
                        else:
                            DataIQ = 2
                        MmcmFout = int(SampleRate * DataIQ / (InterDecim * FabricDataRate)) & 0xffffffff
                        self.MMCMFin[ClkWiz_Id] = int(MmcmFout * div * clkoutdiv / mult) & 0xffffffff
                    else:
                        self.MMCMFin[ClkWiz_Id] = 0
                    ClkWiz_Id += 1
            return status

        def EnableAllInterrupts(inst_id):
            for Tile_Id in range(4):
                self.XRFdc_SetupFIFO(inst_id, self.XRFDC_DAC_TILE, Tile_Id, 0)
                for Block_Id in range(self.MAX_BLOCK_ID):
                    dac_block_enable = self.XRFdc_IsDACBlockEnabled(inst_id, Tile_Id, Block_Id)
                    if dac_block_enable != 0:
                        self.XRFdc_IntrDisable(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id, 0xffffffff)
                        self.XRFdc_IntrEnable(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id, 0xffffffff)
                        self.XRFdc_IntrClr(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id, 0xffffffff)
                self.XRFdc_SetupFIFO(inst_id, self.XRFDC_DAC_TILE, Tile_Id, 1)
                self.XRFdc_SetupFIFO(inst_id, self.XRFDC_ADC_TILE, Tile_Id, 0)
                for Block_Id in range(self.MAX_BLOCK_ID):
                    adc_block_enable = self.XRFdc_IsADCBlockEnabled(inst_id, Tile_Id, Block_Id)
                    if adc_block_enable != 0:
                        self.XRFdc_IntrDisable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                        self.XRFdc_IntrEnable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                        self.XRFdc_IntrClr(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                self.XRFdc_SetupFIFO(inst_id, self.XRFDC_ADC_TILE, Tile_Id, 1)

        def StartUpConfig(inst_id):
            adc_blocks = 4
            status = 0
            for Tile_Id in range(adc_blocks):
                for Block_Id in range(self.MAX_BLOCK_ID):
                    ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id)
                    status |= self.WARN_EXECUTE
                    if self.FAIL == ret:
                        logging.warning(f"XRFdc_GetMixerSettings failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id} ===")
                    Mixer_Settings["MixerType"] = self.XRFDC_MIXER_TYPE_COARSE
                    Mixer_Settings["CoarseMixFreq"] = self.XRFDC_COARSE_MIX_BYPASS
                    Mixer_Settings["MixerMode"] = self.XRFDC_MIXER_MODE_R2R
                    Mixer_Settings["EventSource"] = self.XRFDC_EVNT_SRC_TILE
                    ret, Mixer_Settings = self.XRFdc_SetMixerSettings(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, Mixer_Settings)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_SetMixerSettings failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    ret = self.XRFdc_SetDecimationFactor(inst_id, Tile_Id, Block_Id, self.DEFAULT_DECIMATION_FACTOR)
                    status |= ret
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_SetDecimationFactor failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    self.SetMMCM(inst_id, self.ADC, Tile_Id)

            for Tile_Id in range(4):
                if 2 == self.MAX_BLOCK_ID:
                    ret = self.XRFdc_MultiBand(inst_id, self.XRFDC_DAC_TILE, Tile_Id, 0x1, 0x4, 0x1)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_MultiBand failed for Tile_Id = {Tile_Id}")
                    ret = self.XRFdc_MultiBand(inst_id, self.XRFDC_DAC_TILE, Tile_Id, 0x4, 0x4, 0x4)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_MultiBand failed for Tile_Id = {Tile_Id}")
                for Block_Id in range(4):
                    ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_GetMixerSettings failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    Mixer_Settings["MixerType"] = self.XRFDC_MIXER_TYPE_COARSE
                    Mixer_Settings["CoarseMixFreq"] = self.XRFDC_COARSE_MIX_BYPASS
                    Mixer_Settings["MixerMode"] = self.XRFDC_MIXER_MODE_R2R
                    Mixer_Settings["EventSource"] = self.XRFDC_EVNT_SRC_TILE
                    ret, Mixer_Settings = self.XRFdc_SetMixerSettings(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id, Mixer_Settings)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_SetMixerSettings failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    ret = self.XRFdc_ResetNCOPhase(inst_id, self.XRFDC_DAC_TILE, Tile_Id, Block_Id)
                    if self.FAIL == ret:
                        status |= self.WARN_EXECUTE
                        logging.warning(f"XRFdc_ResetNCOPhase failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    ret = self.XRFdc_UpdateEvent(inst_id, self.XRFDC_DAC_TILE, Tile_Id,
                                                                Block_Id, self.XRFDC_EVENT_MIXER)
                    if self.FAIL == ret:
                        logging.warning(f"XRFdc_UpdateEvent failed for Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    if 2 == self.MAX_BLOCK_ID:
                        if Block_Id == 1 or Block_Id == 3:
                            ret = self.XRFdc_SetInterpolationFactor(inst_id, Tile_Id, Block_Id,
                                                                    self.XRFDC_INTERP_DECIM_OFF)
                            if self.FAIL == ret:
                                status |= self.WARN_EXECUTE
                                logging.warning(f"XRFdc_SetInterpolationFactor failed for "
                                                f"Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                        else:
                            ret = self.XRFdc_SetInterpolationFactor(inst_id, Tile_Id, Block_Id,
                                                                    self.DEFAULT_INTERPOLATION_FACTOR)
                            if self.FAIL == ret:
                                status |= self.WARN_EXECUTE
                                logging.warning(f"XRFdc_SetInterpolationFactor failed for "
                                                f"Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    else:
                        ret = self.XRFdc_SetInterpolationFactor(inst_id, Tile_Id, Block_Id,
                                                                self.DEFAULT_INTERPOLATION_FACTOR)
                        if self.FAIL == ret:
                            status |= self.WARN_EXECUTE
                            logging.warning(f"XRFdc_SetInterpolationFactor failed for "
                                            f"Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    if 2 == self.MAX_BLOCK_ID:
                        if Block_Id == 0 or Block_Id == 2:
                            ret = self.XRFdc_SetDataPathMode(inst_id, Tile_Id, Block_Id,
                                                                    self.DEFAULT_DATA_PATH_MODE)
                            if self.FAIL == ret:
                                status |= self.WARN_EXECUTE
                                logging.warning(f"XRFdc_SetDataPathMode failed for "
                                                f"Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    else:
                        ret = self.XRFdc_SetDataPathMode(inst_id, Tile_Id, Block_Id,
                                                         self.DEFAULT_DATA_PATH_MODE)
                        if self.FAIL == ret:
                            status |= self.WARN_EXECUTE
                            logging.warning(f"XRFdc_SetDataPathMode failed for "
                                            f"Tile_Id = {Tile_Id} Block_Id = {Block_Id}")
                    self.SetMMCM(inst_id, self.DAC, Tile_Id)
                for Tile_Id in range(4):
                    for Block_Id in range(self.MAX_BLOCK_ID):
                        adc_block_enable = self.XRFdc_IsADCBlockEnabled(inst_id, Tile_Id, Block_Id)
                        if 1 == adc_block_enable:
                            self.XRFdc_IntrDisable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                            self.XRFdc_IntrEnable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                            self.XRFdc_IntrClr(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)

                    for Block_Id in range(4):
                        dac_block_enable = self.XRFdc_IsDACBlockEnabled(inst_id, Tile_Id, Block_Id)
                        if 1 == dac_block_enable:
                            self.XRFdc_IntrDisable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                            self.XRFdc_IntrEnable(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)
                            self.XRFdc_IntrClr(inst_id, self.XRFDC_ADC_TILE, Tile_Id, Block_Id, 0xffffffff)

        RFClk_Initialize()
        ret_val, inst_id = RFDC_Initalize()
        RFInitBuildMemoryMap(inst_id)
        ret_val |= InitMMCM_ADC(inst_id)
        ret_val |= InitMMCM_DAC(inst_id)
        EnableAllInterrupts(inst_id)
        StartUpConfig(inst_id)
        return ret_val, inst_id

    def lmem_wr32(self, addr, value):
        """
        Write a 32 bit register

        :param addr: address to write
               value: value to write
        :return: None
        """
        self.axi_write_words(addr, 1, [value & 0xffffffff], 0)
        return

    def lmem_rd32(self, addr):
        """
        Read a 32 bit register

        :param addr: address to read
        :return: ret: Read value
        """
        ret, value = self.axi_read_words(addr, 1, 0)
        return value[0] & 0xffffffff

    def MMCM_Reprog_HW(self, Type, Tile_Id, Mult, Mult_frac, Div, clkout0_div, clkout0_frac):
        if Type == self.ADC:
            if self.info["mts_enable_adc_mask"] & (0x1 << Tile_Id):
                Tile_Id = 0
            logging.debug(f'info.mts_enable_adc_mask = {self.info["mts_enable_adc_mask"]} Tile_Id = {Tile_Id}')
            if 0 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc0"]
            elif 1 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc1"]
            elif 2 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc2"]
            elif 3 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc3"]
            else:
                logging.error(f"MMCM associated with ADC Tile_Id {Tile_Id} does not exist")
                return self.ERROR_EXECUTE
        else:
            if 0 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac0"]
            elif 1 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac1"]
            elif 2 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac2"]
            elif 3 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac3"]
            else:
                logging.error(f"MMCM associated with DAC Tile_Id {Tile_Id} does not exist")
                return self.ERROR_EXECUTE

        time.sleep(100 / 1000000.0)
        self.lmem_wr32(BaseAddr + 0x200, (Mult_frac << 16) | (Mult << 8) | Div)
        time.sleep(100 / 1000000.0)
        # MMCM CLKOUT DIV value
        self.lmem_wr32(BaseAddr + 0x208, (clkout0_frac << 8) | clkout0_div)
        self.lmem_wr32(BaseAddr + 0x214, clkout0_div << 1)  # clkoutdiv1 always half clkoutdiv0
        time.sleep(100 / 1000000.0)
        self.lmem_wr32(BaseAddr + 0x25C, 0x03)
        time.sleep(100 / 1000000.0)
        MMCM_Lock = self.lmem_rd32(BaseAddr + 0x04)
        MMCM_Lock &= 0x00000001
        time.sleep(100 / 1000000.0)
        return MMCM_Lock

    def MMCM_Rst_HW(self, Type, Tile_Id):
        if Type == self.ADC:
            if self.info["mts_enable_adc_mask"] & (0x1 << Tile_Id):
                Tile_Id = 0
            logging.debug(f'info.mts_enable_adc_mask = {self.info["mts_enable_adc_mask"]} Tile_Id = {Tile_Id}')
            if 0 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc0"]
            elif 1 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc1"]
            elif 2 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc2"]
            elif 3 == Tile_Id:
                BaseAddr = self.info["clk_wiz_adc3"]
            else:
                logging.error(f"MMCM associated with ADC Tile_Id {Tile_Id} does not exist")
                return self.ERROR_EXECUTE
        else:
            if 0 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac0"]
            elif 1 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac1"]
            elif 2 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac2"]
            elif 3 == Tile_Id:
                BaseAddr = self.info["clk_wiz_dac3"]
            else:
                logging.error(f"MMCM associated with DAC Tile_Id {Tile_Id} does not exist")
                return self.ERROR_EXECUTE
        # Read the reg of interest so that we can reprogram them after reset
        Clk_conf0 = self.lmem_rd32(BaseAddr + 0x200)
        Clkoutdiv0 = self.lmem_rd32(BaseAddr + 0x208)
        # Reset
        self.lmem_wr32(BaseAddr + 0x00, 0x0A)

        time.sleep(100 / 1000000.0)
        # Reprogram the reg of interests so that they are in sync
        self.lmem_wr32(BaseAddr + 0x200, Clk_conf0)
        self.lmem_wr32(BaseAddr + 0x208, Clkoutdiv0)

        # read the lock
        MMCM_Lock = self.lmem_rd32(BaseAddr + 0x04) & 0x00000001
        return MMCM_Lock

    def GetMemInfoHw(self, inst_id, type, mem):
        data = self.lmem_rd32(mem + self.LMEM_INFO)
        DcChEnabled = 0
        status = 0
        if self.ADC == type:
            MemChMap = self.AdcMemMap.copy()
            ret, FabWords = self.XRFdc_GetFabRdVldWords(inst_id, self.ADC, 0, 0)
        else:
            MemChMap = self.DacMemMap.copy()
            ret, FabWords = self.XRFdc_GetFabRdVldWords(inst_id, self.DAC, 0, 0)
        status |= ret
        num_mem = (data >> 24) & 0x7F
        mem_size = data & 0x00FFFFFF
        mem_size = int(mem_size/(num_mem + 1)/16) & 0xffffffff
        data = self.lmem_rd32(mem + self.LMEM_ENABLE)
        for i in range(16):
            if(data >> i) & 0x1:
                DcChEnabled |= 0x01 << MemChMap[i]
        return status, num_mem, mem_size, FabWords, DcChEnabled

    def SetMMCM(self, inst_id, Type, Tile_Id):
        """
        Setup the MMCM

        :param inst_id: rfdc instance id
               Type: DAC 1 ADC 0
               Tile_Id: tile id
        :return: status: 0 on SUCCESS else 1
        """
        Mult = 1
        Clk0DivFrac = 0
        clkout0_div = 1
        found_ratio = 0
        Fpdmax = 450
        Fpdmin = 70
        FvcoMax = 1500
        FvcoMin = 800
        FoutMin = 6250
        Block_Id = 0
        MMCMFin = [0] * 8
        InterDecim = 1
        high_speed_adc = self.XRFdc_IsHighSpeedADC(inst_id, Tile_Id)
        if Type == self.XRFDC_DAC_TILE or (Type == self.XRFDC_ADC_TILE and high_speed_adc):
            ConstDivider = 8
        else:
            ConstDivider = 4
        ret, PLLSettings = self.XRFdc_GetPLLConfig(inst_id, Type, Tile_Id)
        status = ret
        ret, FabClkDiv = self.XRFdc_GetFabClkOutDiv(inst_id, Type, Tile_Id)
        status |= ret
        ret, RdWidth = self.XRFdc_GetFabRdVldWords(inst_id, Type, Tile_Id, Block_Id)
        status |= ret
        ret, WrWidth = self.XRFdc_GetFabWrVldWords(inst_id, Type, Tile_Id, Block_Id)
        status |= ret
        if Type == self.XRFDC_DAC_TILE:
            Wpl = WrWidth
            ret, DataPathMode = self.XRFdc_GetDataPathMode(inst_id, Tile_Id, Block_Id)
            status |= ret
            if DataPathMode != 4:
                ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, Type, Tile_Id, Block_Id)
                status |= ret
                ret, InterDecim  = self.XRFdc_GetInterpolationFactor(inst_id, Tile_Id, Block_Id)
                status |= ret
            if DataPathMode == 2 or DataPathMode == 3:
                InterDecim = 2 * InterDecim
            if ((DataPathMode == 4) or
                    (Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2R) or
                    (Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2C) or
                    (Mixer_Settings["MixerType"] == self.XRFDC_MIXER_TYPE_COARSE and
                     Mixer_Settings["CoarseMixFreq"] == self.XRFDC_COARSE_MIX_BYPASS)):
                DataIQ = 1
            else:
                DataIQ = 2
        else:
            Wpl = RdWidth
            ret, Mixer_Settings = self.XRFdc_GetMixerSettings(inst_id, Type, Tile_Id, Block_Id)
            status |= ret
            ret, InterDecim = self.XRFdc_GetDecimationFactor(inst_id, Tile_Id, Block_Id)
            status |= ret
            high_speed_adc = self.XRFdc_IsHighSpeedADC(inst_id, Tile_Id)
            if ((Mixer_Settings["MixerMode"] == self.XRFDC_MIXER_MODE_R2R) or
                    high_speed_adc or
                    (Mixer_Settings["MixerType"] == self.XRFDC_MIXER_TYPE_COARSE and
                     Mixer_Settings["CoarseMixFreq"] == self.XRFDC_COARSE_MIX_BYPASS)):
                DataIQ = 1
            else:
                DataIQ = 2

        SampleRate = 1000 * PLLSettings["SampleRate"]
        FDCout = SampleRate / float(ConstDivider * (1 << (FabClkDiv - 1)))
        Fplin = FDCout
        MMCMFin[(4 * Type) + Tile_Id] = int(1000 * FDCout) & 0xffffffff
        if Fplin > Fpdmax:
            Div_Min = 2
        else:
            Div_Min = 1
        Div_Max = int(int(Fplin) / Fpdmin) & 0xffffffff
        if Div_Max == 0:
            Fpdmin = 10
            Div_Max = int(Fplin / Fpdmin) & 0xffffffff
            status |= self.FAIL
            logging.error(f"MMCM specification violation, Fin={Fplin} is below {Fpdmin}")
        Fratio_N = int(DataIQ * ConstDivider * (1 << (FabClkDiv - 1))) & 0xffffffff
        Fratio_D = InterDecim * Wpl
        FRatio = Fratio_N / float(Fratio_D)
        terminate_loop = 0
        for Div in range(Div_Min, Div_Max + 1):
            if ((int(FvcoMin * Div / Fplin) & 0xffffffff) ==
                    (int(FvcoMin * Div / Fplin) & 0xffffffff)):
                Mult_Min = int(FvcoMin * Div / Fplin) & 0xffffffff
            else:
                Mult_Min = int(1 + FvcoMin * Div / Fplin) & 0xffffffff
            Mult_Max = int(FvcoMax * Div / Fplin) & 0xffffffff
            for Mult in range(Mult_Max, Mult_Min - 1, -1):
                for i in range(1, 129):
                    if (int(Div * Fratio_N * i) & 0xffffffff ==
                            int(Mult * Fratio_D) & 0xffffffff):
                        clkout0_div = i
                        found_ratio = 1
                        terminate_loop = 1
                        break
                if 1 == terminate_loop:
                    break
            if 1 == terminate_loop:
                break
        if Type == self.XRFDC_ADC_TILE:
            Type_str = "ADC"
        else:
            Type_str = "DAC"
        if Mult < 2 or Mult > 128:
            logging.error(f"MMCM specification violation {Type_str} Tile {Tile_Id}: "
                          f"Mult = {Mult} is outside range 2 to 128")
            status |= self.FAIL

        if found_ratio == 0:
            logging.error(f"Could not find MMCM/PLL ratio for {Type_str} Tile {Tile_Id} "
                          f"Fin {Fplin} Fout {FRatio * Fplin}")
            status |= self.FAIL
        if Fplin < 10:
            logging.error(f"MMCM {Type_str} Tile {Tile_Id} specification violation: Fin={FDCout} "
                         f"Fin<10, M={Mult}, Div={Div}, clkout0div={clkout0_div}")
            status |= self.FAIL
        if (FvcoMin * Div > (Fplin * Mult)) or (Div * FvcoMax < (Fplin * Mult)):
            logging.error(f"MMCM {Type_str} Tile {Tile_Id} specification violation: "
                          f"VCO={FDCout * Mult / float(Div)} 800<VCO<{FvcoMax}, M={Mult}, "
                          f"Div={Div}, clkout0div={clkout0_div}")
            status |= self.FAIL
        if (Fpdmin > Fplin / float(Div)) or (Fpdmax < Fplin / float(Div)):
            logging.error(f"MMCM {Type_str} Tile {Tile_Id} specification violation: Fph is "
                          f"outside range {Fpdmin} < {Fplin / float(Div)} < {Fpdmax}, "
                          f"M={Mult}, Div={Div}, clkout0div={clkout0_div}")
            status |= self.FAIL
        if 1000 * Fplin * Mult / (Div * clkout0_div) < FoutMin:
            logging.error(f"MMCM {Type_str} Tile {Tile_Id} specification violation: "
                          f"Fout={1000 * Fplin * Mult / (Div * clkout0_div)}kHz<{FoutMin}kHz, "
                          f"M={Mult}, Div={Div}, clkout0div={clkout0_div}")
            status |= self.FAIL
        if status == self.SUCCESS or status == self.WARN_EXECUTE:
            time.sleep(200/1000000.0)
            self.MMCM_Reprog_HW(Type, Tile_Id, Mult, 0, Div, clkout0_div, Clk0DivFrac)
            time.sleep(200/1000000.0)
            MMCM_Lock = self.MMCM_Rst_HW(Type, Tile_Id)
            if 0 == MMCM_Lock:
                logging.error(f"MMCM {Type_str} Tile {Tile_Id} is not locked after reset "
                              f"with Fin {Fplin} M={Mult}, Div={Div}, "
                              f"ClkoutDiv{clkout0_div}, try shutdown/startup the tile "
                              f"but it is likely you will need to re-configure the device")
        return status

    def LocalMemTrigger(self, type_id):
        if self.DAC == type_id:
            base_addr = self.DAC_SOURCE_I_BASEADDR
        else:
            base_addr = self.ADC_SINK_I_BASEADDR
        status = 0
        triggerofs = 0x4
        tileenableofs = 0xc
        channelenableofs = 0x8
        # get channel and tile enables
        ret, TileEnable = self.axi_read_words(base_addr + tileenableofs, 1, 0)
        status |= ret
        ret, ChanEnable = self.axi_read_words(base_addr + channelenableofs, 1, 0)
        status |= ret
        # reset enables
        ret = self.axi_write_words(base_addr + tileenableofs, 1, [0], 0)
        status |= ret
        ret = self.axi_write_words(base_addr + channelenableofs, 1, [0], 0)
        status |= ret
        ret = self.axi_write_words(base_addr + channelenableofs, 1, ChanEnable, 0)
        status |= ret
        ret = self.axi_write_words(base_addr + tileenableofs, 1, TileEnable, 0)
        status |= ret
        # trigger
        ret = self.axi_write_words(base_addr + triggerofs, 1, [1], 0)
        status |= ret
        return status

    def WriteDataToMemory(self, tile_id, block_id, data):
        base_address = self.DAC_SOURCE_I_BASEADDR
        data_offset = 0x8000
        channel_size = 0x8000
        channel_offset = (tile_id * channel_size * 4) + (channel_size * block_id)

        N = np.shape(data)[0]  # number of raw samples
        # take care of negative values
        data = [int(x) for x in data]
        data = [(0xFFFF + x) + 1 if x < 0 else x for x in data]
        formatted_data = []
        for k in range(0, N, 2):
            formatted_data.append((data[k+1] << 16) | data[k])
        ret = self.axi_write_words(base_address + data_offset + channel_offset,
                                   int(N/2) & 0xffffffff, formatted_data, 0)
        return ret

    def SetLocalMemSample(self, type_id, tile_id, block_id, num_samples):
        if self.DAC == type_id:
            base_addr = self.DAC_SOURCE_I_BASEADDR
            channel_offset = (tile_id * 16) + (block_id * 4)
        else:
            base_addr = self.ADC_SINK_I_BASEADDR
            if self.BOARD == "zcu208":
                if block_id == 1:
                    block_id = 2
            channel_offset = (tile_id * 16) + (block_id * 4)

        ret = self.axi_write_words(base_addr + self.LMEM0_ENDADDR + channel_offset,
                                   1, [int(num_samples)], 0)
        return ret

    def ReadDataFromMemory(self, tile_id, block_id, N, iq):
        base_addr = self.ADC_SINK_I_BASEADDR
        data_offset = 0x8000
        channel_size = 0x8000
        if self.BOARD == "zcu208":
            iq_offset = 0x8000
        else:
            iq_offset = 0
        channel_i_offset = (tile_id * channel_size * 4) + ((channel_size+iq_offset) * block_id)
        signal_out_i = []
        signal_out_q = []

        # API 32 bits but samples 16 bits
        ret, captures = self.axi_read_words(base_addr + data_offset + channel_i_offset,
                                            int(N / 2), 0)

        for i in range(np.shape(captures)[0]):
            signal_out_i.append(captures[i] & 0xFFFF)
            signal_out_i.append(captures[i] >> 16)
        signal_out_i = [x if (x & 0x8000) == 0 else (x - 0xFFFF) - 1 for x in signal_out_i]

        if iq != 0:
            ret, captures = self.axi_read_words(base_addr + data_offset + channel_i_offset + iq_offset,
                                                int(N / 2), 0)
            for i in range(np.shape(captures)[0]):
                signal_out_q.append(captures[i] & 0xFFFF)
                signal_out_q.append(captures[i] >> 16)
            signal_out_q = [x if (x & 0x8000) == 0 else (x - 0xFFFF) - 1 for x in signal_out_q]
        return [signal_out_i, signal_out_q]

    def closestbin(self, FS, fMHz, N):
        """
        Find closest coherent frequency to provided frequency in MHz given the sampling rate and number of samples

        :param FS: Sampling frequency
               fMHz: Frequncy in MHz
               N: Number of samples
        :return: f: coherent frequncy in MHz
        """
        Bin = (round((fMHz * N) / FS))
        logging.info("bin: ", Bin, "fmhz: ", fMHz, "N: ", N, "FS: ", FS)
        # to get coherent signal need prime number of cycles
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
                  107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
                  227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
                  349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                  467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
                  613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
                  751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883,
                  887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031,
                  1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
                  1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279,
                  1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423,
                  1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523,
                  1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627,
                  1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777,
                  1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907,
                  1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039,
                  2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161,
                  2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309,
                  2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423,
                  2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591,
                  2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707,
                  2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833,
                  2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969,
                  2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121,
                  3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271,
                  3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407,
                  3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541,
                  3547, 3557, 3559, 3571, 3581, 3583, 3593, 3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673,
                  3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821,
                  3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943,
                  3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049, 4051, 4057, 4073, 4079, 4091, 4093,
                  4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211, 4217, 4219, 4229, 4231, 4241,
                  4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349, 4357, 4363, 4373, 4391,
                  4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513, 4517, 4519, 4523,
                  4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657, 4663, 4673,
                  4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801, 4813, 4817,
                  4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973,
                  4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107,
                  5113, 5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279,
                  5281, 5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431,
                  5437, 5441, 5443, 5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563,
                  5569, 5573, 5581, 5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701,
                  5711, 5717, 5737, 5741, 5743, 5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849,
                  5851, 5857, 5861, 5867, 5869, 5879, 5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011,
                  6029, 6037, 6043, 6047, 6053, 6067, 6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151,
                  6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221, 6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299,
                  6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353, 6359, 6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427,
                  6449, 6451, 6469, 6473, 6481, 6491]
        n = 1
        while ((Bin >= primes[n]) & (n < len(primes))):
            n = n + 1
        if (Bin - primes[n - 1]) < (primes[n] - Bin):
            Bin = primes[n - 1]
        else:
            Bin = primes[n]
        f = (Bin * (FS / N))
        return f