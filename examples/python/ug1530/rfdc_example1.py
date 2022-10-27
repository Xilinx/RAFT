# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

from common_example1 import get_ip
import sys
sys.path.append('../../xclient/rfdc')
import rfdc_client

# get handle
handle = rfdc_client.rfdc
handle.SetIpAndPort(get_ip(),"9090")

# Device setup
device_id = 0
ret, sConfig = handle.XRFdc_LookupConfig(device_id)
if ret == 0:
    ret, device_id = handle.XRFdc_RegisterMetal(device_id)
    if ret == 0:
        ret, sConfig = handle.XRFdc_CfgInitialize(device_id, sConfig)
        if ret != 0:
            print("RFDC: XRFdc_CfgInitialize failed.")
    else:
        print("RFDC: XRFdc_RegisterMetal failed.")
else:
    print("RFDC: XRFdc_LookupConfig failed.")

# API calls
#
#

# tile and block ranges
dac_tiles=range(0,1)
rx_tiles=range(0,1)
fb_tiles=range(2,2)
dac_blks=range(0,3)
rx_blks=range(0,3)
fb_blks=range(0,1)

# DAC Setting RF Frequency to 3600.0 MHz 
#
#
type = 1 # dac
nyquist_zone = 1 # odd
# mixer_settings = GetStruct_XRFdc_MixerSettings()
mixer_settings = {'Freq': 3600.0, 'PhaseOffset': 0.0, 'EventSource': 2, 'CoarseMixFreq': 0, 'MixerMode': 2, 'FineMixerScale': 2, 'MixerType': 2}

for tile in dac_tiles:
    for blk in dac_blks:
        handle.XRFdc_SetNyquistZone(device_id, type, tile, blk, nyquist_zone)
        handle.XRFdc_SetMixerSettings(device_id, type, tile, blk, mixer_settings)
        handle.XRFdc_ResetNCOPhase(device_id, type, tile, blk)
        handle.XRFdc_UpdateEvent(device_id, type, tile, blk, 1)

#  Rx ADC Mixer Settings
type = 0 # adc
nyquist_zone = 2 # even
# mixer_settings = GetStruct_XRFdc_MixerSettings()
mixer_settings = {'Freq': 332.15999999999985, 'PhaseOffset': 0.0, 'EventSource': 2, 'CoarseMixFreq': 0, 'MixerMode': 3, 'FineMixerScale': 1, 'MixerType': 2}

for tile in rx_tiles:
    for blk in rx_blks:
        handle.XRFdc_SetNyquistZone(device_id, type, tile, blk, nyquist_zone)
        handle.XRFdc_SetMixerSettings(device_id, type, tile, blk, mixer_settings)
        handle.XRFdc_ResetNCOPhase(device_id, type, tile, blk)
        handle.XRFdc_UpdateEvent(device_id, type, tile, blk, 1)

# Fb ADC Mixer Settings
type = 0 # adc
nyquist_zone = 2 # even
# mixer_settings = GetStruct_XRFdc_MixerSettings()
mixer_settings = {'Freq': 332.15999999999985, 'PhaseOffset': 0.0, 'EventSource': 2, 'CoarseMixFreq': 0, 'MixerMode': 3, 'FineMixerScale': 1, 'MixerType': 2}

for tile in fb_tiles:
    for blk in fb_blks:
        handle.XRFdc_SetNyquistZone(device_id, type, tile, blk, nyquist_zone)
        handle.XRFdc_SetMixerSettings(device_id, type, tile, blk, mixer_settings)
        handle.XRFdc_ResetNCOPhase(device_id, type, tile, blk)
        handle.XRFdc_UpdateEvent(device_id, type, tile, blk, 1)

# Rx Set Attenutation 
for tile in rx_tiles:
    for blk in rx_blks:
      handle.XRFdc_SetDSA(device_id, tile, blk, {'DisableRTS': 1, 'Attenuation': 0.0})

# Fb Set Attenuation
for tile in fb_tiles:
    for blk in fb_blks:
      handle.XRFdc_SetDSA(device_id, tile, blk, {'DisableRTS': 1, 'Attenuation': 0.0})

# DAC : Set Output Power and Disable Compensation
uAcurrent=40000
for tile in dac_tiles:
    for blk in dac_blks:
      handle.XRFdc_SetDACCompMode(device_id, tile, blk, 0)
      handle.XRFdc_SetDACVOP(device_id, tile, blk, uAcurrent)






