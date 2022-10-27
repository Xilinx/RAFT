# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

from common_example1 import get_ip
import sys
sys.path.append('../../xclient/dfe')
import ccf_client

# get handle
handle = ccf_client.ccf
handle.SetIpAndPort(get_ip(),"9090")
# Device setup
DeviceNodeName = "a7c00000.xdfe_cc_filter"
ret, device_id, _ = handle.XDfeCcf_InstanceInit(DeviceNodeName)


# API calls
#
#

# version
handle.XDfeCcf_GetVersions(device_id)

# reset
handle.XDfeCcf_Reset(device_id)

# configure
cfg = handle.GetStruct_XDfeCcf_Cfg()
handle.XDfeCcf_Configure(device_id,cfg)

# initialize
# NOTE: would be easier if only supplied length HERE in Init Structure
init = handle.GetStruct_XDfeCcf_Init()
init["Sequence"]["Length"]=8
init["GainStage"]=1
handle.XDfeCcf_Initialize(device_id,init)

# set triggers
tcfg = handle.GetStruct_XDfeCcf_TriggerCfg()
tcfg["Activate"]["Mode"]=1
tcfg["Activate"]["TuserEdgeLevel"]=0
tcfg["Activate"]["TUSERBit"]=0
tcfg["CCUpdate"]["Mode"]=1
tcfg["CCUpdate"]["TuserEdgeLevel"]=1
tcfg["CCUpdate"]["TUSERBit"]=0
handle.XDfeCcf_SetTriggersCfg(0,tcfg)

# activate
handle.XDfeCcf_Activate(device_id, 0)

# load coefficients
coeffs = {
  "Num": 255,
  "Symmetric": 1,
  "Value": [
    0,     0,     0,     -28,     -133,     37,     -12,     -2,     15,     -22,     23,     -15,     2,     13,     -25,     28,
    -22,     7,     12,     -27,     34,     -29,     12,     9,     -29,     40,     -36,     20,     5,     -30,     45,     -45,
    28,     -1,     -29,     50,     -54,     39,     -9,     -26,     54,     -65,     51,     -19,     -22,     57,     -74,     65,
    -31,     -15,     58,     -84,     80,     -46,     -5,     57,     -92,     95,     -65,     8,     53,     -100,     112,     -85,
    25,     47,     -106,     130,     -108,     46,     36,     -110,     148,     -135,     72,     20,     -111,     166,     -165,
    104,     -1,     -108,     185,     -199,     142,     -30,     -100,     202,     -237,     189,     -69,     -85,     219,     -281,
    247,     -119,     -62,     234,     -334,     321,     -189,     -24,     247,     -399,     418,     -286,     33,     258,     -487,
    562,     -436,     129,     267,     -622,     798,     -699,     312,     274,     -885,     1301,     -1313,     789,     278,     -1760,
    3407,     -4906,     5953,     26710
  ]
}
cset = 0
shift = 8
handle.XDfeCcf_LoadCoefficients(device_id, cset, shift, coeffs)

# clear event status
status = handle.XDfeCcf_GetEventStatus(device_id)
handle.XDfeCcf_ClearEventStatus(device_id,status)

# do update
cccfg=handle.XDfeCcf_GetEmptyCCCfg(device_id)
ccid=0
bitmap=0xaa
carrier_cfg=handle.GetStruct_XDfeCcf_CarrierCfg()
carrier_cfg["Gain"]=8192
carrier_cfg["RealCoeffSet"]=cset
carrier_cfg["ImagCoeffSet"]=cset
ant_cfg=handle.GetStruct_XDfeCcf_AntennaCfg()
ant_cfg["Enable"]=[1,1,1,1,1,1,1,1]
cccfg=handle.XDfeCcf_SetAntennaCfgInCCCfg(device_id,cccfg,ant_cfg)
_,cccfg=handle.XDfeCcf_AddCCtoCCCfg(device_id, cccfg, ccid, bitmap, carrier_cfg)
handle.XDfeCcf_SetNextCCCfgAndTrigger(device_id,cccfg)

# clear event status ( CC Update will be set when complete)
status=handle.XDfeCcf_GetEventStatus(device_id)
handle.XDfeCcf_ClearEventStatus(device_id,status)

