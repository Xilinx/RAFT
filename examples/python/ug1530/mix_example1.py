# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

from common_example1 import get_ip
import sys
sys.path.append('../../xclient/dfe')
import mix_client

# get handle
handle = mix_client.mix
handle.SetIpAndPort(get_ip(),"9090")
# Device setup
DeviceNodeName = "a7c40000.xdfe_cc_mixer"
ret, device_id, _ = handle.XDfeMix_InstanceInit(DeviceNodeName)


# API calls
#
#

# version
handle.XDfeMix_GetVersions(device_id)

# reset
handle.XDfeMix_Reset(device_id)

# configure
cfg = handle.GetStruct_XDfeMix_Cfg()
handle.XDfeMix_Configure(device_id,cfg)

# initialize
# NOTE: would be easier if only supplied length HERE in Init Structure
init = handle.GetStruct_XDfeMix_Init()
init["Sequence"]["Length"]=8
handle.XDfeMix_Initialize(device_id,init)

# set triggers
tcfg = handle.GetStruct_XDfeMix_TriggerCfg()
tcfg["Activate"]["Mode"]=1
tcfg["Activate"]["TuserEdgeLevel"]=0
tcfg["Activate"]["TUSERBit"]=0
tcfg["CCUpdate"]["Mode"]=1
tcfg["CCUpdate"]["TuserEdgeLevel"]=1
tcfg["CCUpdate"]["TUSERBit"]=0
handle.XDfeMix_SetTriggersCfg(0,tcfg)

# activate
handle.XDfeMix_Activate(device_id, 0)

# clear event status
status = handle.XDfeMix_GetEventStatus(device_id)
handle.XDfeMix_ClearEventStatus(device_id,status)

# do update
cccfg=handle.XDfeMix_GetEmptyCCCfg(device_id)
ccid=0
bitmap=0x55
nco_cfg=handle.GetStruct_XDfeMix_NCO()
nco_cfg["FrequencyCfg"]["FrequencyControlWord"]=0x1a0aaaaa
# TODO: add dual modulus count
carrier_cfg=handle.GetStruct_XDfeMix_CarrierCfg()
carrier_cfg["DUCDDCCfg"]["NCOIdx"]=0
carrier_cfg["DUCDDCCfg"]["CCGain"]=3
ant_cfg=handle.GetStruct_XDfeMix_AntennaCfg()
ant_cfg["Gain"]=[3,3,3,3,3,3,3,3]
cccfg=handle.XDfeMix_SetAntennaCfgInCCCfg(device_id,cccfg,ant_cfg)
_,cccfg=handle.XDfeMix_AddCCtoCCCfg(device_id, cccfg, ccid, bitmap, carrier_cfg,nco_cfg)
handle.XDfeMix_SetNextCCCfgAndTrigger(device_id,cccfg)

# clear event status ( CC Update will be set when complete)
status=handle.XDfeMix_GetEventStatus(device_id)
handle.XDfeMix_ClearEventStatus(device_id,status)

