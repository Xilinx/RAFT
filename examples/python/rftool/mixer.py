# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

from rftool import Rftool
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

rftool_handle = Rftool()
# SetBoardName
board_name = "zcu208"
rftool_handle.SetBoardName(board_name)
# SetIpAndPort
rftool_handle.SetIpAndPort("169.254.10.2", "9090")
# SetMetalLogLevel
metal_log_level = rftool_handle.GetEnum_metal_log_level()
rftool_handle.SetMetalLogLevel(metal_log_level["METAL_LOG_DEBUG"])
# GetPythonLogLevels
PythonLogLevels = rftool_handle.GetPythonLogLevels()
# SetClientLogLevel
rftool_handle.SetClientLogLevel(PythonLogLevels["ERROR"])

ret, inst_id = rftool_handle.Initialize()
# setup clocking
DistributionSettings = rftool_handle.GetStruct_XRFdc_Distribution_Settings()
if board_name == "zcu208":
    DistributionSettings["SourceTileId"] = 0
else:
    DistributionSettings["SourceTileId"] = 2
DistributionSettings["SourceType"] = 1
DistributionSettings["EdgeTypes"] = [0,1]
DistributionSettings["EdgeTileIds"] = [0,3]
DistributionSettings["DistRefClkFreq"] = 245.76
DistributionSettings["DistributedClock"] = 1
DistributionSettings["SampleRates"] = [[2211.86, 2211.86, 2211.86, 2211.86], [2211.86, 2211.86, 2211.86, 2211.86]]
ret = rftool_handle.XRFdc_SetClkDistribution(inst_id, DistributionSettings)

MixerSettingsADC = {
    "Freq": 0.0,
    "PhaseOffset": 0.0,
    "EventSource": 2,
    "CoarseMixFreq": 0x10,
    "MixerMode": 4,
    "FineMixerScale": 0,
    "MixerType": 1,
}
tile_id = 0
dac_block_id = 0
if board_name == "zcu208":
    if dac_block_id == 2:
        adc_block_id = 1
    else:
        adc_block_id = 0
else:
    adc_block_id = dac_block_id

N = 2048  # number of 16bit samples
f = 502.560
FS = 2211.86
FS_DAC = 2211.86
T = 1/FS_DAC
t = np.arange(0, (N * T), T)
sig = 0x1fff * np.cos(2 * np.pi * f * t)

ret, MixerSettingsADC = rftool_handle.XRFdc_SetMixerSettings(inst_id, 0, tile_id, adc_block_id, MixerSettingsADC)
print("rftool_handle.XRFdc_SetMixerSettings ret = ", ret)

ret = rftool_handle.XRFdc_UpdateEvent(inst_id, 0, tile_id, adc_block_id, 1)
print("rftool_handle.XRFdc_UpdateEvent ret = ", ret)

ret, df = rftool_handle.XRFdc_GetDecimationFactor(inst_id, tile_id, adc_block_id)
print(f"rftool_handle.XRFdc_GetDecimationFactor ret = {ret} Decimation factor = {df}")

ret = rftool_handle.SetMMCM(inst_id, 1, 0)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 1, 1)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 1, 2)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 1, 3)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 0, 0)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 0, 1)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 0, 2)
print("rftool_handle.SetMMCM ret = ", ret)

ret = rftool_handle.SetMMCM(inst_id, 0, 3)
print("rftool_handle.SetMMCM ret = ", ret)


# Ensure Channels Enabled
#First Tiles must be disabled (see pg269)
rftool_handle.lmem_wr32(0xb000000c, 0x0)
rftool_handle.lmem_wr32(0xb040000c, 0x0)
#Channels can now be enabled
rftool_handle.lmem_wr32(0xb0000008, 0xffff)
rftool_handle.lmem_wr32(0xb0400008, 0xffff)
#Enable all Tiles
rftool_handle.lmem_wr32(0xb000000c, 0xf)
rftool_handle.lmem_wr32(0xb040000c, 0xf)

rftool_handle.WriteDataToMemory(tile_id, dac_block_id, sig)
rftool_handle.SetLocalMemSample(1, tile_id, dac_block_id, N)
rftool_handle.LocalMemTrigger(1)

rftool_handle.SetLocalMemSample(0, tile_id, adc_block_id, N)
rftool_handle.LocalMemTrigger(0)
SigOut = rftool_handle.ReadDataFromMemory(tile_id, adc_block_id, N, 0)

rftool_handle.SetLocalMemSample(0, tile_id, adc_block_id, N)
rftool_handle.LocalMemTrigger(0)
SigOut = rftool_handle.ReadDataFromMemory(tile_id, adc_block_id, N, 0)

dft = np.abs(fft.fft(SigOut[0]))
fstp = FS/N
fx = np.arange(0, FS, fstp)
plt.plot(fx, dft)
plt.show()
