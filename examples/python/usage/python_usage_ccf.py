# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
def usage():
    # sys.argv[0] - usage python file name
    # sys.argv[1] - xclient/xcffi/xpyro
    # sys.argv[2] - host/board
    # sys.argv[3] - ip_address
    # sys.argv[4] - port
    # sys.argv[5] - "switchable" option integrated in xsa
    print(f"Usage: The application work in three modes xclient, xcffi and xpyro\n"
          f"python3 {sys.argv[0]} xclient host/board ip_address port switchable => Runs at host or board with xclient\n"
          f"sudo python3 {sys.argv[0]} xcffi switchable => Runs at board with xcffi\n"
          f"python3 {sys.argv[0]} xpyro host/board ip_address port switchable => Runs at host or board with xpyro\n"
          f"Example1: python3 {sys.argv[0]} xclient host 169.254.10.2 9090\n"
          f"Example2: python3 {sys.argv[0]} xclient host 169.254.10.2 9090 switchable ")

switchable_flag = False

# 'xcffi' option will run only in the board
if (len(sys.argv) ==  2):
    if (sys.argv[1] != 'xcffi'):
        usage()
        sys.exit()
elif (len(sys.argv) ==  3):
    if (sys.argv[1] != 'xcffi'):
        usage()
        sys.exit()
    elif (sys.argv[2] == 'switchable'):
            switchable_flag = True
elif (len(sys.argv) ==  5):
    pass
elif (len(sys.argv) ==  6):
    if (sys.argv[5] == 'switchable'):
        switchable_flag = True
else:
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
    import ccf_client
    handle = ccf_client.ccf
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/dfe')
    from ccf_server import CCF
    handle = CCF()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:CCF@{ip_address}:{port}"
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

#Description:
#   Return the logging levels supported by logging library in python
#Input Arguments:
#   None
#Return:
#   Dictionary showing the log levels supported by logging library

#GetPythonLogLevels
PythonLogLevels = handle.GetPythonLogLevels()

#Description:
#   Set the python log level to the given level
#Input Arguments:
#   Log level to set
#Return:
#   None
#SetServerLogLevel
handle.SetServerLogLevel(PythonLogLevels["DEBUG"])

#Description:
#   Set the metal log level to the given level
#Input Arguments:
#   Log level to set
#Return:
#   None
#SetMetalLogLevel
metal_log_level = handle.GetEnum_metal_log_level()
handle.SetMetalLogLevel(metal_log_level["METAL_LOG_EMERGENCY"])

#Description:
#   Return Dictionary equivalent of enum XDfeCcf_StateId
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum XDfeCcf_StateId
#GetEnum_XDfeCcf_StateId
XDfeCcf_StateId = handle.GetEnum_XDfeCcf_StateId()

#Description:
#   Return Dictionary equivalent of enum metal_log_level
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum metal_log_level
#GetEnum_metal_log_level
metal_log_level = handle.GetEnum_metal_log_level()

#Description:
#   Return Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
#GetStruct_XDfeCcf_InternalCarrierCfg
XDfeCcf_InternalCarrierCfg = handle.GetStruct_XDfeCcf_InternalCarrierCfg()

#Description:
#   Initialises one instance of a channel filter driver.
#   Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
#   CCF device with the name DeviceNodeName. The first available slot in
#   the instances array XDfeCcf_ChFilter[] will be taken as a DeviceNodeName
#   object. On success it moves the state machine to a Ready state, while on
#   failure stays in a Not Ready state.
#C header declaration:
#   XDfeCcf *XDfeCcf_InstanceInit(const char *DeviceNodeName);
#Input Arguments:
#   DeviceNodeName: device node name.
#Return:
#   ret - 0 on success, 1 on failure
#   device_id - integer handle to the initialized instance
#   DeviceNodeNameRet - device node name returned from driver
#                       which will be same as the passed value
#Notes:
#   The bytes conversion is already done inside xpyro client.

DeviceNodeName = "a7c00000.xdfe_cc_filter"

ret, device_id, DeviceNodeName = handle.XDfeCcf_InstanceInit(DeviceNodeName)

#Description:
#   Writes value to register in a Ccf instance.
#C header declaration:
#   void XDfeCcf_WriteReg(const XDfeCcf *InstancePtr, u32 AddrOffset, u32 Data);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: address offset relative to instance base address.
#   Data: value to be written.
#Return:
#   None

handle.XDfeCcf_WriteReg(device_id, 0x40, 0)

#Description:
#   Reads a value from register using a Ccf instance.
#C header declaration:
#   u32 XDfeCcf_ReadReg(const XDfeCcf *InstancePtr, u32 AddrOffset);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: address offset relative to instance base address
#Return:
#   regval: Register value.

ret = handle.XDfeCcf_ReadReg(device_id, 0)

#Description:
#   Resets channel filter and puts block into a reset state.
#C header declaration:
#   void XDfeCcf_Reset(XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeCcf_Reset(device_id)

#Description:
#   Read configuration from device tree/xparameters.h and IP registers.
#   Removes S/W reset and moves the state machine to a Configured state.
#C header declaration:
#   void XDfeCcf_Configure(XDfeCcf *InstancePtr, XDfeCcf_Cfg *Cfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Cfg: configuration data container
#Return:
#   Cfg: configuration data container

Cfg_in = handle.GetStruct_XDfeCcf_Cfg()
Cfg_out = handle.XDfeCcf_Configure(device_id, Cfg_in)

#Description:
#   DFE Ccf driver one time initialisation, also moves the state machine to
#   an Initialised state.
#C header declaration:
#   void XDfeCcf_Initialize(XDfeCcf *InstancePtr, const XDfeCcf_Init *Init);
#Input Arguments:
#   device_id: id of the opened device.
#   Init: initialisation data container
#Return:
#   Init: initialisation data container

Init_in = handle.GetStruct_XDfeCcf_Init()
Init_in['Sequence']['Length']=6
Init_out = handle.XDfeCcf_Initialize(device_id, Init_in)

#Description:
#   Set trigger configuration.
#C header declaration:
#   void XDfeCcf_SetTriggersCfg(const XDfeCcf *InstancePtr, XDfeCcf_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   TriggerCfg: is a trigger configuration container.
#Return:
#   TriggerCfg: is a trigger configuration container.

TriggerCfg_in = handle.GetStruct_XDfeCcf_TriggerCfg()
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
TriggerCfg_out = handle.XDfeCcf_SetTriggersCfg(device_id, TriggerCfg_in)

#Description:
#   Activates channel filter and moves the state machine to an Activated state.
#C header declaration:
#   void XDfeCcf_Activate(XDfeCcf *InstancePtr, bool EnableLowPower);
#Input Arguments:
#   device_id: id of the opened device.
#   EnableLowPower: flag indicating low power
#Return:
#   None

handle.XDfeCcf_Activate(device_id, 0)

#Description:
#   Gets a state machine state id. The state id is returned as a string.
#   The enum is mapped to a dictionary in python.
#C header declaration:
#   XDfeCcf_StateId XDfeCcf_GetStateID(XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   StateId: State machine StateID as a string

StateId = handle.XDfeCcf_GetStateID(device_id)
print(StateId)

#Description:
#   Returns the current CC configuration. Not used slot ID in a sequence
#   (Sequence.CCID[Index]) are represented as (-1), not the value in registers.
#C header declaration:
#   void XDfeCcf_GetCurrentCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrCCCfg: CC configuration container.
#Return:
#   CurrCCCfg: CC configuration container
#Note:
#   For a sequence conversion see XDfeCcf_AddCCtoCCCfg() comment.

CurrCCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CurrentCCCfg = handle.XDfeCcf_GetCurrentCCCfg(device_id, CurrCCCfg)

#Description:
#   Returns the current CC configuration for DL and UL in switchable mode.
#   Not used slot ID in a sequence (Sequence.CCID[Index]) are represented
#   as (-1), not the value in registers.
#C header declaration:
#   void XDfeCcf_GetCurrentCCCfgSwitchable(const XDfeCcf *InstancePtr,
#			     XDfeCcf_CCCfg *CCCfgDownlink,
#			     XDfeCcf_CCCfg *CCCfgUplink);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfgDownlink: Downlink CC configuration container.
#   CCCfgUplink: Uplink CC configuration container.
#Return:
#   CCCfgDownlink, CCCfgUplink: CC configuration container

if (switchable_flag == True):
	CCCfgDownlink = handle.GetStruct_XDfeCcf_CCCfg()
	CCCfgUplink = handle.GetStruct_XDfeCcf_CCCfg()
	CCCfgDownlink, CCCfgUplink = handle.XDfeCcf_GetCurrentCCCfgSwitchable(device_id, CCCfgDownlink, CCCfgUplink)

#Description:
#   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
#   in XDfeCcf_Configure(), array CCCfg->Sequence.CCID[] members are set to not
#   used value (-1) and the other CCCfg members are set to 0.
#C header declaration:
#   void XDfeCcf_GetEmptyCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   CCCfg: CC configuration container

CCCfg = handle.XDfeCcf_GetEmptyCCCfg(device_id)

#Description:
#   Returns the current CCID carrier configuration.
#C header declaration:
#   void XDfeCcf_GetCarrierCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg,
#	s32 CCID, u32 *CCSeqBitmap, XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.

CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CCSeqBitmap, CarrierCfg = handle.XDfeCcf_GetCarrierCfg(device_id, CCCfg, 0)

#Description:
#   Set antenna configuration in CC configuration container.
#C header declaration:
#   void XDfeCcf_SetAntennaCfgInCCCfg(const XDfeCcf *InstancePtr,
#   XDfeCcf_CCCfg *CCCfg, u32 *AntennaCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   AntennaCfg: Array of all antenna configurations.
#Return:
#   CCCfg: component carrier (CC) configuration container.

AntennaCfg = handle.GetStruct_XDfeCcf_AntennaCfg()
AntennaCfg = {
	"Enable": [1,1,1,1,1,1,0,0],
}
CCCfg = handle.XDfeCcf_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)

#Description:
#   Updates antenna configuration to all antennas.
#C header declaration:
#   u32 XDfeCcf_UpdateAntennaCfg(XDfeCcf *InstancePtr, XDfeCcf_AntennaCfg *AntennaCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   AntennaCfg: Array of all antenna configurations.
#Return:
#   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeCcf_ClearEventStatus() before running this API.

AntennaCfg = handle.GetStruct_XDfeCcf_AntennaCfg()
AntennaCfg = {
	"Enable": [1,1,1,1,1,1,0,0],
}
ret = handle.XDfeCcf_UpdateAntennaCfg(device_id, AntennaCfg)

#Description:
#   Updates antenna configuration of all antennas. Applies gain to downlink only
#   in switchable mode.
#C header declaration:
#   u32 XDfeCcf_UpdateAntennaCfgSwitchable(XDfeCcf *InstancePtr,
#				       XDfeCcf_AntennaCfg *AntennaCfgDownlink,
#				       XDfeCcf_AntennaCfg *AntennaCfgUplink)
#Input Arguments:
#   device_id: id of the opened device.
#   AntennaCfgDownlink: Array of all downlink antenna configurations.
#   AntennaCfgUplink: Array of all uplink antenna configurations.
#Return:
#   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeCcf_ClearEventStatus() before running this API.

if (switchable_flag == True):
	AntennaCfgDL = handle.GetStruct_XDfeCcf_AntennaCfg()
	AntennaCfgDL = {"Enable": [1,1,1,1,1,1,0,0]}
	AntennaCfgUL = handle.GetStruct_XDfeCcf_AntennaCfg()
	AntennaCfgUL = {"Enable": [1,1,1,1,1,1,0,0]}
	ret = handle.XDfeCcf_UpdateAntennaCfgSwitchable(device_id, AntennaCfgDL, AntennaCfgUL)

#Description:
#   Adds specified CCID, with specified configuration, to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#
#   The returned CCCfg.Sequence is transleted as there is no explicite indication that
#   SEQUENCE[i] is not used - 0 can define the slot as either used or not used.
#   Sequence data that is returned in the CCIDSequence is not the same as what is
#   written in the registers. The translation is:
#       - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
#       - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
#       - a returned CCIDSequence->Length = length in register + 1
#C header declaration:
#   u32 XDfeCcf_AddCCtoCCCfg(XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg, s32 CCID,
#	u32 CCSeqBitmap, const XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CCCfg = handle.XDfeCcf_GetCurrentCCCfg(device_id, CCCfg)
CCID = 0x1
CCSeqBitmap = 0x2
CarrierCfg = handle.GetStruct_XDfeCcf_CarrierCfg()
Status = handle.GetStruct_XDfeCcf_Status()
Status['CCUpdate'] = 1
handle.XDfeCcf_ClearEventStatus(int(device_id), Status)
ret, CCCfg = handle.XDfeCcf_AddCCtoCCCfg(int(device_id), CCCfg, CCID, CCSeqBitmap, CarrierCfg)

#Description:
#   Removes specified CCID from a local CC configuration structure.
#C header declaration:
#   void XDfeCcf_RemoveCCfromCCCfg(XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg, s32 CCID);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCCfg: component carrier (CC) configuration container.
#Note:
#   For a sequence conversion see XDfeCcf_AddCCtoCCCfg comment.

CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CCCfg = handle.XDfeCcf_RemoveCCfromCCCfg(device_id, CCCfg, 0)

#Description:
#   Updates specified CCID, with specified configuration to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#C header declaration:
#   void XDfeCcf_UpdateCCinCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg,
# 	s32 CCID, const XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CarrierCfg: CC configuration container.
#Return:
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CarrierCfg = handle.GetStruct_XDfeCcf_CarrierCfg()
CCCfg = handle.XDfeCcf_UpdateCCinCCCfg(device_id, CCCfg, 0, CarrierCfg)

#Description:
#   Writes local CC configuration to the shadow (NEXT) registers and triggers
#   copying from shadow to operational registers.
#C header declaration:
#   u32 XDfeCcf_SetNextCCCfgAndTrigger(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
ret, CCCfg = handle.XDfeCcf_SetNextCCCfgAndTrigger(device_id, CCCfg)

#Description:
#   Writes local CC configuration to the shadow (NEXT) registers and triggers
#   copying from shadow to operational (CURRENT) registers.
#C header declaration:
#   u32 XDfeCcf_SetNextCCCfgAndTriggerSwitchable(const XDfeCcf *InstancePtr,
#					     XDfeCcf_CCCfg *CCCfgDownlink,
#					     XDfeCcf_CCCfg *CCCfgUplink)
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfgDownlink: Downlink CC configuration container.
#   CCCfgUplink: Uplink CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfgDownlink: Downlink CC configuration container.
#   CCCfgUplink: Uplink CC configuration container.

if (switchable_flag == True):
	CCCfgDownlink = handle.GetStruct_XDfeCcf_CCCfg()
	CCCfgUplink = handle.GetStruct_XDfeCcf_CCCfg()
	ret, CCCfgDownlink, CCCfgUplink = handle.XDfeCcf_SetNextCCCfgAndTriggerSwitchable(device_id, CCCfgDownlink, CCCfgUplink)

#Description:
#   Adds specified CCID, with specified configuration.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeCcf_AddCC(const XDfeCcf *InstancePtr, u32 CCID,
#   const XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: Channel ID.
#   CCSeqBitmap: up to 16 defined slots into which a CC can be
#                allocated. The number of slots can be from 1 to 16 depending on
#                system initialization. The number of slots is defined by the
#                "sequence length" parameter which is provided during initialization.
#                The Bit offset within the CCSeqBitmap indicates the equivalent
#                Slot number to allocate. e.g. 0x0003  means the caller wants the
#                passed component carrier (CC) to be allocated to slots 0 and 1.
#   CarrierCfg: is a CC configuration container.
#Return:
#   XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CarrierCfg: is a CC configuration container.

CarrierCfg_in = handle.GetStruct_XDfeCcf_CarrierCfg()
CCSeqBitmap = 0xb
ret, CarrierCfg_out = handle.XDfeCcf_AddCC(device_id, 0, CCSeqBitmap, CarrierCfg_in)

#Description:
#   Removes specified CCID.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeCcf_RemoveCC(const XDfeCcf *InstancePtr, u32 CCID);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeCcf_ClearEventStatus() before running this API.

ret = handle.XDfeCcf_RemoveCC(device_id, 0)

#Description:
#   Updates specified CCID carrier configuration; change gain or filter
#   coefficients set.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeCcf_UpdateCC(const XDfeCcf *InstancePtr, u32 CCID,
#   XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#   CarrierCfg: is a CC configuration container.
#Return:
#   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CarrierCfg - CC configuration container

CarrierCfg_in = handle.GetStruct_XDfeCcf_CarrierCfg()
ret, CarrierCfg_out = handle.XDfeCcf_UpdateCC(device_id, 0, CarrierCfg_in)

#Description:
#   Updates specified antenna TDM slot enablement.
#   Initiates CC update (enable CCUpdate trigger one-shot).
#C header declaration:
#   u32 XDfeCcf_UpdateAntenna(const XDfeCcf *InstancePtr, u32 Ant, bool Enabled);
#Input Arguments:
#   device_id: id of the opened device.
#   Ant: is antenna ID.
#   Enabled: flag indicating enable status of the antenna.
#Return:
#   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeCcf_ClearEventStatus() before running this API.

ret = handle.XDfeCcf_UpdateAntenna(device_id, 0, 0)

#Description:
#   Return current trigger configuration.
#C header declaration:
#   void XDfeCcf_GetTriggersCfg(const XDfeCcf *InstancePtr,
#	XDfeCcf_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   TriggerCfg: is a trigger configuration container.

TriggerCfg_out = handle.XDfeCcf_GetTriggersCfg(device_id)

#Description:
#   Get specified CCID carrier configuration.
#C header declaration:
#   void XDfeCcf_GetCC(const XDfeCcf *InstancePtr, u32 CCID,
#	XDfeCcf_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   CarrierCfg: is a trigger configuration container.

CarrierCfg_out = handle.XDfeCcf_GetCC(device_id, 0)

#Description:
#   Return a list indicating which coefficient sets are currently in use.
#C header declaration:
#   void XDfeCcf_GetActiveSets(const XDfeCcf *InstancePtr, u32 *IsActive);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   IsActive: variable indicating an activation status.

IsActive = handle.XDfeCcf_GetActiveSets(device_id)

#Description:
#   Writes the coefficient set defined into the register map and commit them
#   to the hard block's internal coefficient memory for the specified Set.
#C header declaration:
#   void XDfeCcf_LoadCoefficients(const XDfeCcf *InstancePtr, u32 Set, u32 Shift,
#   const XDfeCcf_Coefficients *Coeffs);
#Input Arguments:
#   device_id: id of the opened device.
#   Set: coefficient set Id
#   Shift: is a coefficient shift value.
#   Coeffs: an array of filter coefficients
#Return:
#   Coeffs: an array of filter coefficients

#Coeffs_in = handle.GetStruct_XDfeCcf_Coeffs()
Coeffs_in = {
    "Num": 7,
    "Symmetric": 1,
    "Value": [0, 0, 0, (2 ** 15) - 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
Coeffs_out = handle.XDfeCcf_LoadCoefficients(device_id, 0, 8, Coeffs_in)

#Description:
#   Get overflow event status
#C header declaration:
#   void XDfeCcf_GetOverflowStatus(const XDfeCcf *InstancePtr,
#			       XDfeCcf_OverflowStatus *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: overflow event status
OverflowStatus = handle.XDfeCcf_GetOverflowStatus(device_id)

#Description:
#   Sets uplink/downlink register bank.
#C header declaration:
#   void XDfeCcf_SetRegBank(const XDfeCcf *InstancePtr,
#                  u32 RegBank)
#Input Arguments:
#   device_id: id of the opened device.
#   RegBank: Register bank value to be set.
#Return:
#   None

if (switchable_flag == True):
	RegBank = 1
	handle.XDfeCcf_SetRegBank(device_id, RegBank)
	RegBank = 0
	handle.XDfeCcf_SetRegBank(device_id, RegBank)

#Description:
#   Gets event status.
#C header declaration:
#   void XDfeCcf_GetEventStatus(const XDfeCcf *InstancePtr, XDfeCcf_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: event status

Status = handle.XDfeCcf_GetEventStatus(device_id)

#Description:
#   Clears event status.XDfeCcf_ClearEventStatus
#C header declaration:
#   void XDfeCcf_ClearEventStatus(const XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#   Status: event status.
#       0 - does not clear corresponding event status
#       1 - clears corresponding event status
#Return:
#   None

Status_in = handle.GetStruct_XDfeCcf_Status()
handle.XDfeCcf_ClearEventStatus(device_id, Status_in)

#Description:
#   Sets interrupt masks.
#C header declaration:
#   void XDfeCcf_SetInterruptMask(const XDfeCcf *InstancePtr,
#	const XDfeCcf_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#   Mask: interrupt mask value
#       0 - does not mask corresponding interrupt
#       1 - masks corresponding interrupt
#Return:
#   None

Mask_in = handle.GetStruct_XDfeCcf_InterruptMask()
handle.XDfeCcf_SetInterruptMask(device_id, Mask_in)

#Description:
#   Get Interrupt mask
#C header declaration:
#   void XDfeCcf_GetInterruptMask(const XDfeCcf *InstancePtr,
#	const XDfeCcf_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Mask: interrupt mask value.

Mask_out = handle.XDfeCcf_GetInterruptMask(device_id)

#Description:
#   Reads the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeCcf_GetTUserDelay(const XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   ret: Delay value

ret = handle.XDfeCcf_GetTUserDelay(device_id)
print (ret)

#Description:
#   Gets calculated TDataDelay value for CCID from current CC configuration.
#C header declaration:
#   u32 XDfeCcf_GetTDataDelay(const XDfeCcf *InstancePtr, u32 Tap);
#Input Arguments:
#   device_id: id of the opened device.
#   Tap: is a tap variable.
#   CCID: CC ID.
#   Symmetric: Select symetric (1) or non-symetric (0) filter.
#   Num: Number of coefficients values.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   TDataDelay: Delay value container.

CCID = 0x0
CCSeqBitmap = 0x1
CarrierCfg_in = handle.GetStruct_XDfeCcf_CarrierCfg()
CarrierCfg_in['Gain']=0
CarrierCfg_in['ImagCoeffSet']=0
CarrierCfg_in['RealCoeffSet']=0
Status = handle.GetStruct_XDfeCcf_Status()
Status['CCUpdate'] = 1
handle.XDfeCcf_ClearEventStatus(device_id, Status)
CarrierCfg_out = handle.XDfeCcf_AddCC(device_id, CCID, CCSeqBitmap, CarrierCfg_in)
print(CarrierCfg_out)
CCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CCCfg = handle.XDfeCcf_GetCurrentCCCfg(device_id, CCCfg)
Tap = 0
Symmetric = 1
Num = 26
ret, DataLatency = handle.XDfeCcf_GetTDataDelay(device_id, Tap, CCID, Symmetric, Num)
print (DataLatency)

#Description:
#   Gets calculated TDataDelay value for CCID.
#C header declaration:
#   u32 XDfeCcf_GetTDataDelayFromCCCfg(XDfeCcf *InstancePtr, u32 Tap, s32 CCID,
#   XDfeCcf_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Tap: is a tap variable.
#   CCID: CC ID.
#   CCCfg: Component carrier (CC) configuration container.
#   Symmetric: Select symetric (1) or non-symetric (0) filter.
#   Num: Number of coefficients values.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   TDataDelay: Delay value container.

CurrCCCfg = handle.GetStruct_XDfeCcf_CCCfg()
CurrentCCCfg = handle.XDfeCcf_GetCurrentCCCfg(device_id, CurrCCCfg)
ret, DataLatency = handle.XDfeCcf_GetTDataDelayFromCCCfg(device_id,  Tap, CCID, CurrentCCCfg, Symmetric, Num)
print (DataLatency)

#Description:
#   This API is used to get the driver version.
#C header declaration:
#   void XDfeCcf_GetVersions(const XDfeCcf *InstancePtr, XDfeCcf_Version *SwVersion,
#	XDfeCcf_Version *HwVersion);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   SwVersion: driver version numbers.
#   HwVersion: HW version numbers.

SwVersion_out, HwVersion_out = handle.XDfeCcf_GetVersions(device_id)

#Description:
#   Deactivates channel filter and moves the state machine to Initialised state.
#C header declaration:
#   void XDfeCcf_Deactivate(XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeCcf_Deactivate(device_id)

#Description:
#   Sets the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeCcf_SetTUserDelay(const XDfeCcf *InstancePtr, u32 Delay);
#Input Arguments:
#   device_id: id of the opened device.
#   Delay: requested delay variable.
#Return:
#   None

handle.XDfeCcf_SetTUserDelay(device_id, 10)

#Description:
#   Closes the instances of a channel filter driver and moves the state
#   machine to a Not Ready state.
#C header declaration:
#   void XDfeCcf_InstanceClose(XDfeCcf *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeCcf_InstanceClose(device_id)