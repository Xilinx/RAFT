# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2022, Xilinx"

import sys
def usage():
    # sys.argv[0] - usage python file name
    # sys.argv[1] - xclient/xcffi/xpyro
    # sys.argv[2] - host/board
    # sys.argv[3] - ip_address
    # sys.argv[4] - port
    print(f"Usage: The application work in three modes xclient, xcffi and xpyro\n"
          f"python3 {sys.argv[0]} xclient host/board ip_address port => Runs at host or board with xclient\n"
          f"sudo python3 {sys.argv[0]} xcffi => Runs at board with xcffi\n"
          f"python3 {sys.argv[0]} xpyro host/board ip_address port => Runs at host or board with xpyro\n"
          f"Example: python3 {sys.argv[0]} xclient host 169.254.10.2 9090")

# 'xcffi' option will run only in the board
if (len(sys.argv) ==  2):
    if (sys.argv[1] != 'xcffi'):
        usage()
        sys.exit()

elif (len(sys.argv) !=  5):
    usage()
    sys.exit()

# The 'xclient' option will run both in host and board
if (sys.argv[1] == 'xclient'):
    # For 'xclient' option the path of the xclient is required
    # The relative path in the host is given for host case
    if (sys.argv[2] == 'host'):
        sys.path.append('../../../xclient/dfe')
    # The location of xclient in the filesystem is given for the board case
    elif (sys.argv[2] == 'board'):
        sys.path.append('/usr/share/raft/xclient/dfe')
    else:
        usage()
        sys.exit()
    import ofdm_client
    handle = ofdm_client.ofdm
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/dfe')
    from ofdm_server import OFDM
    handle = OFDM()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:OFDM@{ip_address}:{port}"
    handle = Pyro4.Proxy(uri)
else:
    usage()
    sys.exit()

if (sys.argv[1] == 'xclient'):
    #SetIpAndPort
    handle.SetIpAndPort(ip_address, port)
    #GetPythonLogLevels
    PythonLogLevels = handle.GetPythonLogLevels()
    #SetClientLogLevel
    handle.SetClientLogLevel(PythonLogLevels["DEBUG"])

#GetPythonLogLevels
PythonLogLevels = handle.GetPythonLogLevels()

#SetServerLogLevel
handle.SetServerLogLevel(PythonLogLevels["DEBUG"])

#SetMetalLogLevel
metal_log_level = handle.GetEnum_metal_log_level()
handle.SetMetalLogLevel(metal_log_level["METAL_LOG_DEBUG"])

#GetEnum_XDfeOfdm_StateId
XDfeOfdm_StateId = handle.GetEnum_XDfeOfdm_StateId()

#GetEnum_metal_log_level
metal_log_level = handle.GetEnum_metal_log_level()

#GetStruct_XDfeOfdm_InternalCarrierCfg
XDfeOfdm_InternalCarrierCfg = handle.GetStruct_XDfeOfdm_InternalCarrierCfg()

#XDfeOfdm_InstanceInit
#XDfeOfdm *XDfeOfdm_InstanceInit(const char *DeviceNodeName);
#The bytes conversion is already done inside xpyro client.
DeviceNodeName = "a7e40000.xdfe_ofdm"

ret, device_id, DeviceNodeName = handle.XDfeOfdm_InstanceInit(DeviceNodeName)

#XDfeOfdm_WriteReg
#void XDfeOfdm_WriteReg(const XDfeOfdm *InstancePtr, u32 AddrOffset, u32 Data);
handle.XDfeOfdm_WriteReg(device_id, 0x40, 0)

#XDfeOfdm_ReadReg
#u32 XDfeOfdm_ReadReg(const XDfeOfdm *InstancePtr, u32 AddrOffset);
ret = handle.XDfeOfdm_ReadReg(device_id, 0)

#XDfeOfdm_Reset
#void XDfeOfdm_Reset(XDfeOfdm *InstancePtr);
handle.XDfeOfdm_Reset(device_id)

#XDfeOfdm_Configure
#void XDfeOfdm_Configure(XDfeOfdm *InstancePtr, XDfeOfdm_Cfg *Cfg);
Cfg_in = handle.GetStruct_XDfeOfdm_Cfg()
Cfg_out = handle.XDfeOfdm_Configure(device_id, Cfg_in)

#XDfeOfdm_Initialize
#void XDfeOfdm_Initialize(XDfeOfdm *InstancePtr, const XDfeOfdm_Init *Init);
Init_in = handle.GetStruct_XDfeOfdm_Init()
Init_in['CCSequenceLength']=6
Init_out = handle.XDfeOfdm_Initialize(device_id, Init_in)

#XDfeOfdm_SetTriggersCfg
#void XDfeOfdm_SetTriggersCfg(const XDfeCcf *InstancePtr, XDfeOfdm_TriggerCfg *TriggerCfg);
TriggerCfg_in = handle.GetStruct_XDfeOfdm_TriggerCfg()
TriggerCfg_in['Activate']['TriggerEnable'] = 0
TriggerCfg_in['Activate']['Mode'] = 0
TriggerCfg_in['Activate']['TuserEdgeLevel'] = 0
TriggerCfg_in['Activate']['StateOutput'] = 0
TriggerCfg_in['Activate']['TUSERBit'] = 0
TriggerCfg_in['CCUpdate']['TriggerEnable'] = 0
TriggerCfg_in['CCUpdate']['Mode'] = 0
TriggerCfg_in['CCUpdate']['TuserEdgeLevel'] = 0
TriggerCfg_in['CCUpdate']['StateOutput'] = 0
TriggerCfg_in['CCUpdate']['TUSERBit'] = 0
TriggerCfg_out = handle.XDfeOfdm_SetTriggersCfg(device_id, TriggerCfg_in)

#XDfeOfdm_Activate
#void XDfeOfdm_Activate(XDfeCcf *InstancePtr, bool EnableLowPower);
handle.XDfeOfdm_Activate(device_id, 0)

#XDfeOfdm_GetStateID
#XDfeOfdm_StateId XDfeOfdm_GetStateID(XDfeCcf *InstancePtr);
StateId = handle.XDfeOfdm_GetStateID(device_id)
print(StateId)

#XDfeOfdm_GetCurrentCCCfg
#void XDfeOfdm_GetCurrentCCCfg(const XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg);
CurrCCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
CurrentCCCfg = handle.XDfeOfdm_GetCurrentCCCfg(device_id, CurrCCCfg)

# XDfeOfdm_GetEmptyCCCfg
# void XDfeOfdm_GetEmptyCCCfg(const XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg);
CCCfg = handle.XDfeOfdm_GetEmptyCCCfg(device_id) #TODO

# XDfeOfdm_GetCarrierCfg
# void XDfeOfdm_GetCarrierCfg(const XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg,
#			   s32 CCID, u32 *CCSeqBitmap,
#			   XDfeOfdm_CarrierCfg *CarrierCfg);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
CCSeqBitmap, CarrierCfg = handle.XDfeOfdm_GetCarrierCfg(device_id, CCCfg, 0) #TODO

# XDfeOfdm_AddCCtoCCCfg
# u32 XDfeOfdm_AddCCtoCCCfg(XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg, s32 CCID,
#			 u32 CCSeqBitmap, const XDfeOfdm_CarrierCfg *CarrierCfg);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
CCCfg = handle.XDfeOfdm_GetCurrentCCCfg(device_id, CCCfg)
CCID = 0x1
CCSeqBitmap = 0x2
CarrierCfg = handle.GetStruct_XDfeOfdm_CarrierCfg()
Status = handle.GetStruct_XDfeOfdm_Status()
CarrierCfg['FftSize'] = 1024
Status['CCUpdate'] = 1
handle.XDfeOfdm_ClearEventStatus(int(device_id), Status)
FTSeq = handle.GetStruct_XDfeOfdm_FTSequence()
ret, CCCfg, FTSeq = handle.XDfeOfdm_AddCCtoCCCfg(int(device_id), CCCfg, CCID, CCSeqBitmap, CarrierCfg, FTSeq) #TODO

# XDfeOfdm_RemoveCCfromCCCfg
# void XDfeOfdm_RemoveCCfromCCCfg(XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg,
# 			       s32 CCID);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
ret, CCCfg, FTSeq = handle.XDfeOfdm_RemoveCCfromCCCfg(device_id, CCCfg, 0, FTSeq)#TODO

# XDfeOfdm_UpdateCCinCCCfg
# void XDfeOfdm_UpdateCCinCCCfg(const XDfeCcf *InstancePtr, XDfeOfdm_CCCfg *CCCfg,
# 			     s32 CCID, const XDfeOfdm_CarrierCfg *CarrierCfg);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
CarrierCfg = handle.GetStruct_XDfeOfdm_CarrierCfg()
#ret, CCCfg, FTSeq = handle.XDfeOfdm_UpdateCCinCCCfg(device_id, CCCfg, 0, CarrierCfg, FTSeq) #TODO

# XDfeOfdm_SetNextCCCfg
# void XDfeOfdm_SetNextCCCfg(const XDfeOfdm *InstancePtr,
#				  const XDfeOfdm_CCCfg *NextCCCfg);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
CCCfg = handle.XDfeOfdm_SetNextCCCfg(device_id, CCCfg)
print(f"------------------------------->XDfeOfdm_SetNextCCCfg")
print(CCCfg)

# XDfeOfdm_EnableCCUpdateTrigger
# u32 XDfeOfdm_EnableCCUpdateTrigger(const XDfeOfdm *InstancePtr);
ret = handle.XDfeOfdm_EnableCCUpdateTrigger(device_id)
print(f"------------------------------->XDfeOfdm_EnableCCUpdateTrigger")
print(ret)

# XDfeOfdm_SetNextCCCfgAndTrigger
# u32 XDfeOfdm_SetNextCCCfgAndTrigger(const XDfeCcf *InstancePtr,
#				   XDfeOfdm_CCCfg *CCCfg);
CCCfg = handle.GetStruct_XDfeOfdm_CCCfg()
ret, CCCfg = handle.XDfeOfdm_SetNextCCCfgAndTrigger(device_id, CCCfg)#TODO

#XDfeOfdm_AddCC
#u32 XDfeOfdm_AddCC(const XDfeCcf *InstancePtr, u32 CCID,
#		  const XDfeOfdm_CarrierCfg *CarrierCfg);
Status = handle.GetStruct_XDfeOfdm_Status()
Status['CCUpdate'] = 1
handle.XDfeOfdm_ClearEventStatus(int(device_id), Status)
CarrierCfg_in = handle.GetStruct_XDfeOfdm_CarrierCfg()
CCSeqBitmap = 0xb
FTSeq = handle.GetStruct_XDfeOfdm_FTSequence()
FTSeq['Length'] = 2
FTSeq['CCID'] = [1,2,3,4, 0,0,0,0, 0,0,0,0, 0,0,0,0]
CCID = 0x5
CCSeqBitmap = 0x17
CarrierCfg_in = handle.GetStruct_XDfeOfdm_CarrierCfg()
CarrierCfg_in['Numerology'] = 1
CarrierCfg_in['NumSubcarriers'] = 0x5
CarrierCfg_in['ScaleFactor'] = 0x55
CarrierCfg_in['OutputDelay'] = 0x3455
CarrierCfg_in['FftSize'] = 1024
ret = handle.XDfeOfdm_AddCC(device_id, 0, CCSeqBitmap, CarrierCfg_in, FTSeq)

#XDfeOfdm_RemoveCC
#u32 XDfeOfdm_RemoveCC(const XDfeCcf *InstancePtr, u32 CCID);
ret = handle.XDfeOfdm_RemoveCC(device_id, 0, FTSeq)#TODO

#XDfeOfdm_UpdateCC
#u32 XDfeOfdm_UpdateCC(const XDfeCcf *InstancePtr, u32 CCID,
#                      XDfeOfdm_CarrierCfg *CarrierCfg);
CarrierCfg_in = handle.GetStruct_XDfeOfdm_CarrierCfg()
#ret, CarrierCfg_out = handle.XDfeOfdm_UpdateCC(device_id, 0, CarrierCfg_in, FTSeq)#TODO

#XDfeOfdm_GetTriggersCfg
#void XDfeOfdm_GetTriggersCfg(const XDfeCcf *InstancePtr,
#			                XDfeOfdm_TriggerCfg *TriggerCfg);
TriggerCfg_out = handle.XDfeOfdm_GetTriggersCfg(device_id)

#XDfeOfdm_GetEventStatus
#void XDfeOfdm_GetEventStatus(const XDfeCcf *InstancePtr, XDfeOfdm_Status *Status);
Status = handle.XDfeOfdm_GetEventStatus(device_id)

#XDfeOfdm_ClearEventStatus
#void XDfeOfdm_ClearEventStatus(const XDfeCcf *InstancePtr);
Status_in = handle.GetStruct_XDfeOfdm_Status()
handle.XDfeOfdm_ClearEventStatus(device_id, Status_in)

#XDfeOfdm_SetInterruptMask
#void XDfeOfdm_SetInterruptMask(const XDfeCcf *InstancePtr,
#	            		       const XDfeOfdm_InterruptMask *Mask);
Mask_in = handle.GetStruct_XDfeOfdm_InterruptMask()
handle.XDfeOfdm_SetInterruptMask(device_id, Mask_in)

#XDfeOfdm_GetInterruptMask
#void XDfeOfdm_GetInterruptMask(const XDfeCcf *InstancePtr,
#	            		       const XDfeOfdm_InterruptMask *Mask);
Mask_out = handle.XDfeOfdm_GetInterruptMask(device_id)

#XDfeOfdm_Deactivate
#void XDfeOfdm_Deactivate(XDfeCcf *InstancePtr);
handle.XDfeOfdm_Deactivate(device_id)

#void XDfeOfdm_SetTUserDelay(const XDfeOfdm *InstancePtr, u32 Delay);
TUserDelay = 0x123
handle.XDfeOfdm_SetTUserDelay(device_id, TUserDelay)

#u32 XDfeOfdm_GetTUserDelay(const XDfeOfdm *InstancePtr);
delay = handle.XDfeOfdm_GetTUserDelay(device_id)

#u32 XDfeOfdm_GetDataLatency(const XDfeOfdm *InstancePtr);
delay = handle.XDfeOfdm_GetDataLatency(device_id)

#XDfeOfdm_GetVersions
#void XDfeOfdm_GetVersions(const XDfeCcf *InstancePtr, XDfeOfdm_Version *SwVersion,
#			              XDfeOfdm_Version *HwVersion);
SwVersion_out, HwVersion_out = handle.XDfeOfdm_GetVersions(device_id)

#XDfeOfdm_InstanceClose
#void XDfeOfdm_InstanceClose(XDfeOfdm *InstancePtr);
handle.XDfeOfdm_InstanceClose(device_id)

