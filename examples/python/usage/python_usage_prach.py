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
    import prach_client
    handle = prach_client.prach
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/dfe')
    from prach_server import PRACH
    handle = PRACH()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:PRACH@{ip_address}:{port}"
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
#  None
#Return:
#   Dictionary showing the log levels supported by logging library
#GetPythonLogLevels
PythonLogLevels = handle.GetPythonLogLevels()

#Description:
#   Set the python log level to the given level
#Input Arguments:
#    Log level to set
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
#   Return Dictionary equivalent of enum XDfePrach_StateId
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum XDfePrach_StateId
# GetEnum_XDfePrach_StateId
XDfePrach_StateId = handle.GetEnum_XDfePrach_StateId()

#Description:
#   Return Dictionary equivalent of structure XDfePrach_InternalChannelCfg
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of structure XDfePrach_InternalChannelCfg
# GetStruct_XDfePrach_InternalChannelCfg
XDfePrach_InternalChannelCfg = handle.GetStruct_XDfePrach_InternalChannelCfg()

#Description:
#   Return Dictionary equivalent of structure XDfePrach_ChannelCfg
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of structure XDfePrach_ChannelCfg
# GetStruct_XDfePrach_ChannelCfg
XDfePrach_ChannelCfg = handle.GetStruct_XDfePrach_ChannelCfg()

#Description:
#   Return Dictionary equivalent of enum metal_log_level
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum metal_log_level
# GetEnum_metal_log_level
metal_log_level = handle.GetEnum_metal_log_level()

#Description:
#   API initialise an instance of the driver.
#   Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
#   PRACH device with the name DeviceNodeName. The first available slot in
#   the instance array XDfePrach_Prach[] will be taken as a DeviceNodeName
#   object. On success it moves the state machine to a Ready state, while on
#   failure stays in a Not Ready state.
#C header declaration:
#   XDfePrach *XDfePrach_InstanceInit(const char *DeviceNodeName);
#Input Arguments:
#   DeviceNodeName: device node name.
#Return:
#   ret - 0 on success, 1 on failure
#   device_id - integer handle to initalized instance
#   DeviceNodeNameRet - device node name returned from driver
#                       which will be same as the passed value

DeviceNodeName = "a7e00000.xdfe_nr_prach"
ret, device_id, DeviceNodeName = handle.XDfePrach_InstanceInit(DeviceNodeName)

#Description:
#   Writes a value to register in a PRACH instance.
#C header declaration:
#   void XDfePrach_WriteReg(const XDfePrach *InstancePtr, u32 AddrOffset, u32 Data);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#   Data: is value to be written.
#Return:
#   None

handle.XDfePrach_WriteReg(device_id, 0x40, 0)

#Description:
#   Reads a value the register in a PRACH instance.
#C header declaration:
#   u32 XDfePrach_ReadReg(const XDfePrach *InstancePtr, u32 AddrOffset);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#Return:
#   ret: Register value.

ret = handle.XDfePrach_ReadReg(device_id, 0)

#Description:
#   Resets PRACH and puts block into a reset state.
#C header declaration:
#   void XDfePrach_Reset(XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfePrach_Reset(device_id)

#Description:
#   Reads configuration from device tree/xparameters.h and IP registers.
#   Removes S/W reset and moves the state machine to a Configured state.
#C header declaration:
#   void XDfePrach_Configure(XDfePrach *InstancePtr, XDfePrach_Cfg *Cfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Cfg: configuration data container.
#Return:
#   Cfg: configuration data container.

Cfg_in = handle.GetStruct_XDfePrach_Cfg()
Cfg_out = handle.XDfePrach_Configure(device_id, Cfg_in)

#Description:
#   DFE PRACH driver one time initialisation also moves the state machine to
#   an Initialised state.
#C header declaration:
#   void XDfePrach_Initialize(XDfePrach *InstancePtr, const XDfePrach_Init *Init);
#Input Arguments:
#   device_id: id of the opened device.
#   Init: initialisation data container.
#Return:
#   None

Init_in = handle.GetStruct_XDfePrach_Init()
Init_in['Sequence']['Length']=6
Init_out = handle.XDfePrach_Initialize(device_id, Init_in)

#Description:
#   Set trigger configuration.
#C header declaration:
#   void XDfePrach_SetTriggersCfg(const XDfePrach *InstancePtr,
# 	XDfePrach_TriggerCfg *TriggerCfg)
#Input Arguments:
#   device_id: id of the opened device.
#   TriggerCfg: Trigger configuration container.
#Return:
#   TriggerCfg: Trigger configuration container.

TriggerCfg_in = handle.GetStruct_XDfePrach_TriggerCfg()
TriggerCfg_in["FrameInit"]["Mode"] = 1
TriggerCfg_out = handle.XDfePrach_SetTriggersCfg(device_id, TriggerCfg_in)

#Description:
#   Activates PRACH and moves the state machine to an Activated state.
#C header declaration:
#   void XDfePrach_Activate(XDfePrach *InstancePtr, bool EnableLowPower);
#Input Arguments:
#   device_id: id of the opened device.
#   EnableLowPower: flag indicating low power.
#Return:
#   None

handle.XDfePrach_Activate(device_id, 0)

#Description:
#   Gets a state machine state id.
#C header declaration:
#   XDfePrach_StateId XDfePrach_GetStateID(XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   StateId: State machine StateID as a string

StateId = handle.XDfePrach_GetStateID(device_id)
print(StateId)

#Description:
#   Returns the current CC configuration
#C header declaration:
#   void XDfePrach_GetCurrentCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrCCCfg: CC configuration container.
#Return:
#   CurrCCCfg: CC configuration container

CurrCCCfg = handle.GetStruct_XDfePrach_CCCfg()
CurrentCCCfg = handle.XDfePrach_GetCurrentCCCfg(device_id, CurrCCCfg)

#Description:
#   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
#   in XDfePrach_Configure(), array CCCfg->Sequence.CCID[] members are set to not
#   used value (-1) and the other CCCfg members are set to 0.
#C header declaration:
#   void XDfePrach_GetEmptyCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   CCCfg: CC configuration container

CCCfg = handle.XDfePrach_GetEmptyCCCfg(device_id)

#Description:
#   Return Dictionary equivalent of structure XDfePrach_InternalDUCDDCCfg
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of structure XDfePrach_InternalDUCDDCCfg

#GetStruct_XDfePrach_InternalDUCDDCCfg
XDfePrach_InternalDUCDDCCfg = handle.GetStruct_XDfePrach_InternalDUCDDCCfg()

#Description:
#   Returns the current CCID carrier configuration.
#C header declaration:
#   void XDfePrach_GetCarrierCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
#   s32 CCID, u32 *CCSeqBitmap, XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.


CCCfg = handle.GetStruct_XDfePrach_CCCfg()
CCSeqBitmap, CarrierCfg = handle.XDfePrach_GetCarrierCfg(device_id, CCCfg, 0)

#Description:
#   Set antenna configuration in CC configuration container.
#C header declaration:
#   void XDfePrach_SetAntennaCfgInCCCfg(const XDfePrach *InstancePtr,
#   XDfePrach_CCCfg *CCCfg, u32 *AntennaCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   AntennaCfg: Array of all antenna configurations.
#Return:
#   CCCfg: component carrier (CC) configuration container.


AntennaCfg=[1,1,1,1,1,1,0,0]
CCCfg = handle.XDfePrach_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)

#Description:
#   Adds specified CCID, with specified configuration, to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfePrach_AddCCtoCCCfg(XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg, s32 CCID,
#   u32 CCSeqBitmap, const XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfePrach_CCCfg()
CarrierCfg = handle.GetStruct_XDfePrach_CarrierCfg()
#ret, CCCfg = handle.XDfePrach_AddCCtoCCCfg(device_id, CCCfg, 0, 0, CarrierCfg)

#Description:
#   Removes specified CCID from a local CC configuration structure.
#C header declaration:
#   void XDfePrach_RemoveCCfromCCCfg(XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
# 	s32 CCID);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfePrach_CCCfg()
CCCfg = handle.XDfePrach_RemoveCCfromCCCfg(device_id, CCCfg, 0)

#Description:
#   Updates specified CCID, with specified configuration to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#C header declaration:
#   void XDfePrach_UpdateCCinCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
#   s32 CCID, const XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CarrierCfg: CC configuration container.
#Return:
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfePrach_CCCfg()
CarrierCfg = handle.GetStruct_XDfePrach_CarrierCfg()
CCSeqBitmap = 0xb
NCO = handle.GetStruct_XDfePrach_NCO()
CCCfg = handle.XDfePrach_UpdateCCinCCCfg(device_id, CCCfg, 0, CarrierCfg)

#Description:
#   Add specified CCID, with specified configuration.
#C header declaration:
#   u32 XDfePrach_AddCC(const XDfePrach *InstancePtr, u32 CCId,
#   const XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#   BitSequence: up to 16 defined slots into which a CC can be
#                allocated. The number of slots can be from 1 to 16 depending on
#                system initialization. The number of slots is defined by the
#                "sequence length" parameter which is provided during initialization.
#                The Bit offset within the CCSeqBitmap indicates the equivalent
#                Slot number to allocate. e.g. 0x0003  means the caller wants the
#                passed component carrier (CC) to be allocated to slots 0 and 1.
#   CarrierCfg: is a CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CarrierCfg: is a CC configuration container.

CarrierCfg_in = handle.GetStruct_XDfePrach_CarrierCfg()
BitSequence = 0xb
ret, CarrierCfg_out = handle.XDfePrach_AddCC(device_id, 0, BitSequence, CarrierCfg_in)

#Description:
#   Updates a CCID sequence.
#C header declaration:
#   u32 XDfePrach_UpdateCC(const XDfePrach *InstancePtr, u32 CCId,
#   const XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#   CarrierCfg: is carrier data container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

CarrierCfg_in = handle.GetStruct_XDfePrach_CarrierCfg()
ret = handle.XDfePrach_UpdateCC(device_id, 0, CarrierCfg_in)

#Description:
#   Reads all of the RC configuration back.
#C header declaration:
#   void XDfePrach_GetCurrentRCCfg(const XDfePrach *InstancePtr,
#   XDfePrach_RCCfg *RCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   RCCfg: RC configuration container.

RCCfg = handle.XDfePrach_GetCurrentRCCfg(device_id)

#Description:
#   Returns the empty CC configuration.
#C header declaration:
#   void XDfePrach_GetEmptyRCCfg(const XDfePrach *InstancePtr,
#   XDfePrach_RCCfg *RCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   RCCfg: RC configuration container.

RCCfg = handle.XDfePrach_GetEmptyRCCfg(device_id)

#Description:
#   Gets RACH channel configuration.
#C header declaration:
#   void XDfePrach_GetChannelCfg(const XDfePrach *InstancePtr, XDfePrach_RCCfg *RCCfg,
#   s32 RCId, XDfePrach_ChannelCfg *ChannelCfg)
#Input Arguments:
#   device_id: id of the opened device.
#   RCCfg: RC configuration container.
#   RCId: Chosen RACH channel Id.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure
#   ChannelCfg: RACH channel container.

CurrentRCCfg = handle.GetStruct_XDfePrach_RCCfg()
ChannelCfg = handle.XDfePrach_GetChannelCfg(device_id, CurrentRCCfg, 0)

#Description:
#   Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
#   physical channel RachChan.
#C header declaration:
#   u32 XDfePrach_AddRCtoRCCfg(const XDfePrach *InstancePtr, XDfePrach_RCCfg *CurrentRCCfg,
#   s32 CCID, u32 RCId, u32 RachChan, XDfePrach_DDCCfg *DdcCfg, XDfePrach_NCO *NcoCfg,
#	XDfePrach_Schedule *StaticSchedule);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrentRCCfg: current RACH configuration container
#   CCID: is CC Id.
#   RCId: is RC Id.
#   RachChan: is RACH channel.
#   DdcCfg: is DDC data container.
#   NcoCfg: is NCO data container.
#   Schedule: is Schedule data container.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure
#   CurrentRCCfg: current RACH configuration container

CurrentRCCfg = handle.GetStruct_XDfePrach_RCCfg()
DdcCfg = handle.GetStruct_XDfePrach_DDCCfg()
NcoCfg = handle.GetStruct_XDfePrach_NCO()
StaticSchedule = handle.GetStruct_XDfePrach_Schedule()
ret, CurrentCCCfg = handle.XDfePrach_AddRCtoRCCfg(device_id, CurrentRCCfg, 0, 0,
                                           0, DdcCfg, NcoCfg, StaticSchedule)

#Description:
#   Removes an RC configuration entry from the RC_CONFIGURATION. RCId must be
#   same as the physical channel RachChan.
#C header declaration:
#   u32 XDfePrach_RemoveRCfromRCCfg(const XDfePrach *InstancePtr,
#   XDfePrach_RCCfg *CurrentRCCfg, u32 RCId);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrentRCCfg: current PRACH configuration container
#   RCId: is RC Id.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure
#   CurrentRCCfg: current PRACH configuration container

CurrentRCCfg = handle.GetStruct_XDfePrach_RCCfg()
ret, CurrentRCCfg = handle.XDfePrach_RemoveRCfromRCCfg(device_id, CurrentRCCfg, 0)

#Description:
#   Updates an RC entry to the RC_CONFIGURATION.
#C header declaration:
#   void XDfePrach_UpdateRCinRCCfg(const XDfePrach *InstancePtr, XDfePrach_RCCfg *CurrentRCCfg,
#   s32 CCID, u32 RCId, u32 RachChan, XDfePrach_DDCCfg *DdcCfg, XDfePrach_NCO *NcoCfg,
#	XDfePrach_Schedule *StaticSchedule);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrentRCCfg: current PRACH configuration container
#   CCID: is CC Id.
#   RCId: is RC Id.
#   RachChan: is PRACH channel.
#   DdcCfg: is DDC data container.
#   NcoCfg: is NCO data container.
#   Schedule: is Schedule data container.
#Return:
#   CurrentRCCfg: current PRACH configuration container

CurrentRCCfg = handle.GetStruct_XDfePrach_RCCfg()
DdcCfg = handle.GetStruct_XDfePrach_DDCCfg()
NcoCfg = handle.GetStruct_XDfePrach_NCO()
StaticSchedule = handle.GetStruct_XDfePrach_Schedule()
CurrentRCCfg = handle.XDfePrach_UpdateRCinRCCfg(device_id, CurrentRCCfg, 0, 0, 0,
                                         DdcCfg, NcoCfg, StaticSchedule)

#Description:
#   Writes local CC configuration to the shadow (NEXT) registers and triggers
#   copying from shadow to operational registers.
#C header declaration:
#   u32 XDfePrach_SetNextCfg(const XDfePrach *InstancePtr, XDfePrach_RCCfg *NextRCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   NextCCCfg: a CC configuration container.
#   NextRCCfg: a RC configuration container.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure

NextCCCfg = handle.GetStruct_XDfePrach_CCCfg()
NextRCCfg = handle.GetStruct_XDfePrach_RCCfg()
ret = handle.XDfePrach_SetNextCfg(device_id, NextCCCfg, NextRCCfg)

#Description:
#   Updates an RC entry to the RC_CONFIGURATION. RCId must be same as the
#   physical channel RachChan.
#C header declaration:
#   u32 XDfePrach_UpdateRCCfg(const XDfePrach *InstancePtr, s32 CCID, u32 RCId, u32 RachChan,
#   XDfePrach_DDCCfg *DdcCfg, XDfePrach_NCO *NcoCfg, XDfePrach_Schedule *StaticSchedule);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is CC Id.
#   RCId: is RC Id.
#   RachChan: is PRACH channel.
#   DdcCfg: is DDC data container.
#   NcoCfg: is NCO data container.
#   Schedule: is Schedule data container.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure

DdcCfg = handle.GetStruct_XDfePrach_DDCCfg()
NcoCfg = handle.GetStruct_XDfePrach_NCO()
StaticSchedule = handle.GetStruct_XDfePrach_Schedule()
ret = handle.XDfePrach_UpdateRCCfg(device_id, 0, 0, 0, DdcCfg, NcoCfg, StaticSchedule)

#Description:
#   Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
#   physical channel RachChan.
#C header declaration:
#   u32 XDfePrach_AddRCCfg(const XDfePrach *InstancePtr, #u32 CCId, u32 RCId, u32 RachChan,
#   XDfePrach_DDCCfg *DdcCfg,XDfePrach_NCO *NcoCfg, XDfePrach_Schedule *StaticSchedule);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is CC Id.
#   RCId: is RC Id.
#   RachChan: is RACH channel.
#   DdcCfg: is DDC data container.
#   NcoCfg: is NCO data container.
#   StaticSchedule: is Schedule data container.
#Return:
#   ret: XST_SUCCESS on succes, XST_FAILURE on failure
#   DdcCfg: is DDC data container.
#   NcoCfg: is NCO data container.
#   Schedule: is Schedule data container.

DdcCfg = {"DecimationRate": 0, "SCS": 0, "RachGain": [0, 0, 0, 0, 0, 0]}
NcoCfg = {
    "PhaseOffset": 0,
    "PhaseAcc": 0,
    "DualModCount": 0,
    "DualModSel": 0,
    "Frequency": 0,
    "NcoGain": 0,
}
StaticSchedule = {
    "PatternPeriod": 0,
    "FrameID": 0,
    "SubframeID": 0,
    "SlotId": 0,
    "Duration": 0,
    "Repeats": 0,
}
ret, DdcCfg, NcoCfg, StaticSchedule = handle.XDfePrach_AddRCCfg(
    device_id, 0, 0, 0, DdcCfg, NcoCfg, StaticSchedule
)

#Description:
#   Move specified RCID from one NCO & Decimation Channel to another NCO &&
#   Decimation Channel.
#C header declaration:
#   u32 XDfePrach_MoveRC(const XDfePrach *InstancePtr, u32 RCId, u32 ToChannel);
#Input Arguments:
#   device_id: id of the opened device.
#   RCId: is RC Id.
#   ToChannel: is destination channel Id.
#Return:
#   ret: XST_SUCCESS on succes, XST_FAILURE on failure

ret = handle.XDfePrach_MoveRC(device_id, 0, 0)

#Description:
#   Return current trigger configuration.
#C header declaration:
#   void XDfePrach_GetTriggersCfg(const XDfePrach *InstancePtr,
#   XDfePrach_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   TriggerCfg: Trigger configuration container

TriggerCfg_out = handle.XDfePrach_GetTriggersCfg(device_id)

#Description:
#   Get specified CCID carrier configuration from either Current or Next.
#C header declaration:
#   void XDfePrach_GetCC(const XDfePrach *InstancePtr, u32 CCID,
# 	XDfePrach_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Next: is next or current data flag.
#   CCID: is component carrier id number.
#Return:
#   CarrierCfg: Carrier config container.

CarrierCfg_out = handle.XDfePrach_GetCC(device_id, 0, 0)

#Description:
#   Get PRACH Status.
#C header declaration:
#   void XDfePrach_GetStatus(const XDfePrach *InstancePtr, XDfePrach_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: Status data container.

Status = handle.XDfePrach_GetStatus(device_id)

#Description:
#   Clear the PRACH status registers.
#C header declaration:
#   void XDfePrach_ClearStatus(const XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None


handle.XDfePrach_ClearStatus(device_id)

#Description:
#   Captures phase for all phase accumulators in associated AXI-lite registers.
#C header declaration:
#   void XDfePrach_CapturePhase(const XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfePrach_CapturePhase(device_id)

#Description:
#   Reads the captured phase for a given Rach Channel.
#C header declaration:
#   void XDfePrach_GetCapturePhase(const XDfePrach *InstancePtr, u32 RachChan,
# 	XDfePrach_NCO *CapturedPhase);
#Input Arguments:
#   device_id: id of the opened device.
#   RachChan: is RACH channel Id.
#Return:
#   NCO data container.

CapturedPhase = handle.XDfePrach_GetCapturePhase(device_id, 0)

#Description:
#   Gets interrupt mask status.
#C header declaration:
#   void XDfePrach_GetInterruptMask(const XDfePrach *InstancePtr,
# 	XDfePrach_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Mask: interrupt masks container.

InterruptMask_out = handle.XDfePrach_GetInterruptMask(device_id)

#Description:
#   Sets interrupt mask.
#C header declaration:
#   void XDfePrach_SetInterruptMask(const XDfePrach *InstancePtr,
# 	const XDfePrach_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#   Mask: interrupt masks container.
#         0 - does not mask coresponding interrupt
#         1 - masks coresponding interrupt
#Return:
#   None

InterruptMask_in = handle.GetStruct_XDfePrach_InterruptMask()
InterruptMask_in['DecimatorOverflow'] = 1
InterruptMask_in['MixerOverflow'] = 1
InterruptMask_in['DecimatorOverrun'] = 1
InterruptMask_in['SelectorOverrun'] = 1
InterruptMask_in['RachUpdate'] = 1
InterruptMask_in['CCSequenceError'] = 1
InterruptMask_in['FrameInitTrigger'] = 1
InterruptMask_in['FrameError'] = 1
handle.XDfePrach_SetInterruptMask(device_id, InterruptMask_in)

#Description:
#   Gets event status.
#C header declaration:
#   void XDfePrach_GetEventStatus(const XDfePrach *InstancePtr, XDfePrach_StatusMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: event status container.

EventStatus_out = handle.XDfePrach_GetEventStatus(device_id)

#Description:
#   Gets event status.
#C header declaration:
#   void XDfePrach_ClearEventStatus(const XDfePrach *InstancePtr,
#   const XDfePrach_StatusMask *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: event status container.

Status_in = handle.GetStruct_XDfePrach_StatusMask()
Status_in['DecimatorOverflow'] = 1
Status_in['MixerOverflow'] = 1
Status_in['DecimatorOverrun'] = 1
Status_in['SelectorOverrun'] = 1
Status_in['RachUpdate'] = 1
Status_in['CCSequenceError'] = 1
Status_in['FrameInitTrigger'] = 1
Status_in['FrameError'] = 1
handle.XDfePrach_ClearEventStatus(device_id, Status_in)

#Description:
#   Remove a CCID from sequence.
#C header declaration:
#   u32 XDfePrach_RemoveCC(const XDfePrach *InstancePtr, u32 CCId);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

ret = handle.XDfePrach_RemoveCC(device_id, 0)

#Description:
#   Removes an RC configuration entry from the RC_CONFIGURATION.
#C header declaration:
#   u32 XDfePrach_RemoveRC(const XDfePrach *InstancePtr, u32 RCId);
#Input Arguments:
#   device_id: id of the opened device.
#   RCId: is RC Id.
#Return:
#   ret: XST_SUCCESS on success, XST_FAILURE on failure

ret = handle.XDfePrach_RemoveRC(device_id, 0)

#Description:
#   Reads the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfePrach_GetTUserDelay(const XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   ret: Delay value

ret = handle.XDfePrach_GetTUserDelay(device_id)

#Description:
#   Returns CONFIG.DATA_LATENCY.VALUE + tap, where the tap is between 0
#   and 23 in real mode and between 0 and 11 in complex/matrix mode.
#C header declaration:
#   u32 XDfePrach_GetTDataDelay(const XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   ret: data latency value.

ret = handle.XDfePrach_GetTDataDelay(device_id)

#Description:
#   This API gets the driver and HW design version.
#C header declaration:
#   void XDfePrach_GetVersions(const XDfePrach *InstancePtr, XDfePrach_Version *SwVersion,
# 	XDfePrach_Version *HwVersion);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   SwVersion: driver version numbers.
#   HwVersion: HW version numbers.

SwVersion_out, HwVersion_out = handle.XDfePrach_GetVersions(device_id)

#Description:
#   Deactivates PRACH and moves the state machine to Initialised state.
#C header declaration:
#   void XDfePrach_Deactivate(XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfePrach_Deactivate(device_id)

#Description:
#   Sets the delay, which will be added to TUSER and TLAST (delay matched through the IP).
#C header declaration:
#   u32 XDfePrach_SetTUserDelay(const XDfePrach *InstancePtr, u32 Delay);
#Input Arguments:
#   device_id: id of the opened device.
#   Delay: requested delay variable.
#Return:
#   None

handle.XDfePrach_SetTUserDelay(device_id, 10)

#Description:
#   API closes the instances of a PRACH driver and moves the state machine to
#   a Not Ready state.
#C header declaration:
#   void XDfePrach_InstanceClose(XDfePrach *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfePrach_InstanceClose(device_id)