# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

from common_example1 import get_ip
import sys
sys.path.append('../../xclient/dfe')
import equ_client

# get handle
handle = equ_client.equ
handle.SetIpAndPort(get_ip(),"9090")
# Device setup
DeviceNodeName = "a6080000.xdfe_equalizer"
ret, device_id, _ = handle.XDfeEqu_InstanceInit(DeviceNodeName)


# API calls
#
#

# version
handle.XDfeEqu_GetVersions(device_id)

# reset
handle.XDfeEqu_Reset(device_id)

# configure
cfg = handle.GetStruct_XDfeEqu_Cfg()
handle.XDfeEqu_Configure(device_id,cfg)

# initialize
# 
init = handle.GetStruct_XDfeEqu_EqConfig()
init["Flush"]=0
init["DatapathMode"]=1
init["RealDatapathSet"]=0
init["ImDatapathSet"]=0
handle.XDfeEqu_Initialize(device_id,init)

# set triggers
tcfg = handle.GetStruct_XDfeEqu_TriggerCfg()
tcfg["Activate"]["Mode"]=1
tcfg["Activate"]["TuserEdgeLevel"]=0
tcfg["Activate"]["TUSERBit"]=0
tcfg["Update"]["Mode"]=1
tcfg["Update"]["TuserEdgeLevel"]=1
tcfg["Update"]["TUSERBit"]=0
handle.XDfeEqu_SetTriggersCfg(0,tcfg)

# activate
handle.XDfeEqu_Activate(device_id, 0)

# load coefficients
coeffs_unity = {
  "Num": 12, 
  "Set": 0, 
  "Coefficients": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
coeffs_tilt = {
  "Num": 12, 
  "Set": 1, 
  "Coefficients": [393, -4778, 10456, -15945, 13979, 30753, -3945, 6858, -4879, 190, 4024, 0, 5967, -6724, 5174, 1029, -14651, 11475, -3395, -1589, 5072, -6966, 4778, 0]
}

mode = 1      # complex
cmap = 3      # apply to coefficients for antenna 0,1
shift = 8
handle.XDfeEqu_LoadCoefficients(device_id, cmap, mode, shift, coeffs_unity)
handle.XDfeEqu_LoadCoefficients(device_id, cmap, mode, shift, coeffs_tilt)

# switch coefficients
cfg = handle.GetStruct_XDfeEqu_EqConfig()
cfg["Flush"]=0
cfg["DatapathMode"]=1
cfg["RealDatapathSet"]=1
cfg["ImDatapathSet"]=1
handle.XDfeEqu_Update(device_id,cfg)

# clear event status
status = handle.XDfeEqu_GetEventStatus(device_id)
handle.XDfeEqu_ClearEventStatus(device_id,status)


