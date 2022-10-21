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
    import mix_client
    handle = mix_client.mix
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/dfe')
    from mix_server import MIX
    handle = MIX()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:MIX@{ip_address}:{port}"
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
#   Return Dictionary equivalent of enum XDfeMix_StateId
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum XDfeMix_StateId

#GetEnum_XDfeMix_StateId
XDfeMix_StateId = handle.GetEnum_XDfeMix_StateId()

#Description:
#   Return Dictionary equivalent of enum metal_log_level
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of enum metal_log_level

#GetEnum_metal_log_level
metal_log_level = handle.GetEnum_metal_log_level()

#Description:
#   API initialises one instance of a Mixer driver.
#   Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
#   XDfeMix device with the name DeviceNodeName. The first available slot in
#   the instances array XDfeMix_Mixer[] will be taken as a DeviceNodeName
#   object. On success it moves the state machine to a Ready state, while on
#   failure stays in a Not Ready state.
#C header declaration:
#   XDfeMix *XDfeMix_InstanceInit(const char *DeviceNodeName);
#Input Arguments:
#   DeviceNodeName: device node name.
#Return:
#   ret - 0 on success, 1 on failure
#   device_id - integer handle to initialized instance
#   DeviceNodeNameRet - device node name returned from driver
#                       which will be same as the passed value

DeviceNodeName = "a7c40000.xdfe_cc_mixer"
ret, device_id, DeviceNodeName = handle.XDfeMix_InstanceInit(DeviceNodeName)

#Description:
#   Writes a value to register in a Mixer instance.
#C header declaration:
#   void XDfeMix_WriteReg(const XDfeMix *InstancePtr, u32 AddrOffset, u32 Data);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#   Data: is value to be written.
#Return:
#   None

handle.XDfeMix_WriteReg(device_id, 0x20, 0x1001)

#Description:
#   Reads a value from the register from a Mixer instance.
#C header declaration:
#   u32 XDfeMix_ReadReg(const XDfeMix *InstancePtr, u32 AddrOffset);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#Return:
#   regval: Register value.

ret = handle.XDfeMix_ReadReg(device_id, 0)

#Description:
#   Resets and put block into a reset state.
#C header declaration:
#   void XDfeMix_Reset(XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeMix_Reset(device_id)
handle.XDfeMix_WriteReg(device_id, 0x20, 0x1001)

#Description:
#   Reads configuration from device tree/xparameters.h and IP registers.
#   Removes S/W reset and moves the state machine to a Configured state.
#C header declaration:
#   void XDfeMix_Configure(XDfeMix *InstancePtr, XDfeMix_Cfg *Cfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Cfg: configuration data container.
#Return:
#   Cfg: configuration data container.

Cfg_in = handle.GetStruct_XDfeMix_Cfg()
Cfg = handle.XDfeMix_Configure(device_id, Cfg_in)
handle.XDfeMix_WriteReg(device_id, 0x20, 0x1001)

#Description:
#   DFE Mixer driver one time initialisation and moves the state machine to
#   an Initialised state.
#C header declaration:
#   void XDfeMix_Initialize(XDfeMix *InstancePtr, const XDfeMix_Init *Init);
#Input Arguments:
#   device_id: id of the opened device.
#   Init: initialisation data container.
#Return:
#   Init: initialisation data container.

Init_in = handle.GetStruct_XDfeMix_Init()
Init_in['Sequence']['Length']=6
Init_out = handle.XDfeMix_Initialize(device_id, Init_in)

#Description:
#   Sets trigger configuration.
#C header declaration:
#   void XDfeMix_SetTriggersCfg(const XDfeMix *InstancePtr, XDfeMix_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   TriggerCfg: trigger configuration container.
#Return:
#   TriggerCfg: trigger configuration container.

TriggerCfg_in = handle.GetStruct_XDfeMix_TriggerCfg()
handle.XDfeMix_SetTriggersCfg(device_id, TriggerCfg_in)

#Description:
#   Activates Mixer and moves the state machine to an Activated state.
#C header declaration:
#   void XDfeMix_Activate(XDfeMix *InstancePtr, bool EnableLowPower);
#Input Arguments:
#   device_id: id of the opened device.
#   EnableLowPower: flag indicating low power.
#Return:
#   None

handle.XDfeMix_Activate(device_id, 0)

#Description:
#   Gets a state machine state id. The state id is returned as a string.
#   The enum is mapped to a dictionary in python.
#C header declaration:
#   XDfeMix_StateId XDfeMix_GetStateID(XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   StateId: State machine StateID as a string

StateId = handle.XDfeMix_GetStateID(device_id)
print(StateId)

#Description:
#   Returns the current CC configuration. Not used slot ID in a sequence
#   (Sequence.CCID[Index]) are represented as (-1), not the value in registers.
#C header declaration:
#   void XDfeMix_GetCurrentCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CurrCCCfg: CC configuration container.
#Return:
#   CurrCCCfg: CC configuration container

CurrCCCfg = handle.GetStruct_XDfeMix_CCCfg()
CurrentCCCfg = handle.XDfeMix_GetCurrentCCCfg(device_id, CurrCCCfg)

#Description:
#   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
#   in XDfeMix_Configure(), array CCCfg->Sequence.CCID[] members are set to not
#   used value (-1) and the other CCCfg members are set to 0.
#C header declaration:
#   void XDfeMix_GetEmptyCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   CCCfg: CC configuration container

CCCfg = handle.XDfeMix_GetEmptyCCCfg(device_id)

#Description:
#   Return Dictionary equivalent of structure XDfeMix_InternalDUCDDCCfg
#Input Arguments:
#   None
#Return:
#   Dictionary equivalent of structure XDfeMix_InternalDUCDDCCfg

#GetStruct_XDfeMix_InternalDUCDDCCfg
XDfeMix_InternalDUCDDCCfg = handle.GetStruct_XDfeMix_InternalDUCDDCCfg()

#Description:
#   Returns the current CC sequence bitmap, CCID carrier configuration and
#   NCO configuration.
#C header declaration:
#   void XDfeMix_GetCarrierCfgAndNCO(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
#   s32 CCID, u32 *CCSeqBitmap, XDfeMix_CarrierCfg *CarrierCfg, XDfeMix_NCO *NCO);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.
#   NCO: NCO configuration container.

CCCfg = handle.GetStruct_XDfeMix_CCCfg()
CCSeqBitmap, CarrierCfg, NCO = handle.XDfeMix_GetCarrierCfgAndNCO(device_id, CCCfg, 0)

#Description:
#   Set antenna configuration in CC configuration container.
#C header declaration:
#   void XDfeMix_SetAntennaCfgInCCCfg(const XDfeMix *InstancePtr,
#	XDfeMix_CCCfg *CCCfg, u32 *AntennaCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   AntennaCfg: Array of all antenna configurations.
#Return:
#   CCCfg: component carrier (CC) configuration container.

AntennaCfg = handle.GetStruct_XDfeMix_AntennaCfg()
AntennaCfg = {
	"Gain": [1,1,1,1,1,1,0,0],
}
CCCfg = handle.XDfeMix_SetAntennaCfgInCCCfg(device_id, CCCfg, AntennaCfg)

#Description:
#   Updates antenna configuration to all antennas.
#C header declaration:
#   u32 XDfeMix_UpdateAntennaCfg(XDfeMix *InstancePtr,
#   XDfeMix_AntennaCfg *AntennaCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   AntennaCfg: Array of all antenna configurations.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeMix_ClearEventStatus() before running this API.

AntennaCfg = handle.GetStruct_XDfeMix_AntennaCfg()
AntennaCfg = {
	"Gain": [1,1,1,1,1,1,0,0],
}
ret = handle.XDfeMix_UpdateAntennaCfg(device_id, AntennaCfg)

#Description:
#   Adds specified CCID, with specified configuration, to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#
#   The returned CCCfg.Sequence is transleted as there is no explicit indication
#   that SEQUENCE[i] is not used - 0 can define the slot as either used or
#   not used. Sequence data that is returned in the CCIDSequence is not the same
#   as what is written in the registers. The translation is:
#   - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
#   - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
#   - a returned CCIDSequence->Length = length in register + 1
#C header declaration:
#   u32 XDfeMix_AddCCtoCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg, s32 CCID,
#   u32 CCSeqBitmap, const XDfeMix_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CCSeqBitmap: CC slot position container.
#   CarrierCfg: CC configuration container.
#   NCO: NCO configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfg: component carrier (CC) configuration container.

CarrierCfg = handle.GetStruct_XDfeMix_CarrierCfg()
NCO = handle.GetStruct_XDfeMix_NCO()
CCID = 0x0
CCSeqBitmap = 0x1
CurrCCCfg = handle.GetStruct_XDfeMix_CCCfg()
CurrentCCCfg = handle.XDfeMix_GetCurrentCCCfg(int(device_id), CurrCCCfg)
ret, CurrentCCCfg = handle.XDfeMix_AddCCtoCCCfg(int(device_id), CurrentCCCfg, CCID, CCSeqBitmap, CarrierCfg, NCO)

#Description:
#   Removes specified CCID from a local CC configuration structure.
#C header declaration:
#   void XDfeMix_RemoveCCfromCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
#   s32 CCID);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#Return:
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfeMix_CCCfg()
CCCfg = handle.XDfeMix_RemoveCCfromCCCfg(device_id, CCCfg, 0)

#Description:
#   Updates specified CCID, with specified configuration to a local CC
#   configuration structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#C header declaration:
#   void XDfeMix_UpdateCCinCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
#   s32 CCID, const XDfeMix_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   CCID: Channel ID.
#   CarrierCfg: CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CarrierCfg: is a CC configuration container.

CCCfg = handle.GetStruct_XDfeMix_CCCfg()
CarrierCfg = handle.GetStruct_XDfeMix_CarrierCfg()
ret, CCCfg = handle.XDfeMix_UpdateCCinCCCfg(device_id, CCCfg, 0, CarrierCfg)

#Description:
#   Writes local CC configuration to the shadow (NEXT) registers and triggers
#   copying from shadow to operational registers.
#C header declaration:
#   u32 XDfeMix_SetNextCCCfgAndTrigger(const XDfeMix *InstancePtr,
#	XDfeMix_CCCfg *CCCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CCCfg: component carrier (CC) configuration container.

CCCfg = handle.GetStruct_XDfeMix_CCCfg()
ret, CCCfg = handle.XDfeMix_SetNextCCCfgAndTrigger(device_id, CCCfg)

#Description:
#   Adds specified CCID, with specified configuration.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeMix_AddCC(XDfeMix *InstancePtr, s32 CCID, u32 CCSeqBitmap,
#	const XDfeMix_CarrierCfg *CarrierCfg, const XDfeMix_NCO *NCO);
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
#   NCO: NCO configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CarrierCfg: is a CC configuration container.
#Note:
#   Clear event status with XDfeMix_ClearEventStatus() before running this API.

CarrierCfg_in = handle.GetStruct_XDfeMix_CarrierCfg()
BitSequence = 0xb
NCO = handle.GetStruct_XDfeMix_NCO()
ret, CarrierCfg_out = handle.XDfeMix_AddCC(device_id, 0, BitSequence, CarrierCfg_in, NCO)

#Description:
#   Removes specified CCID.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeMix_RemoveCC(const XDfeMix *InstancePtr, u32 CCID);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeMix_ClearEventStatus() before running this API.

ret = handle.XDfeMix_RemoveCC(device_id, 0)

#Description:
#   Moves specified CCID from one NCO to another aligning phase to make it
#   transparent.
#   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
#C header declaration:
#   u32 XDfeMix_MoveCC(const XDfeMix *InstancePtr, u32 CCID, u32 Rate,
#   u32 FromNCO, u32 ToNCO);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#   Rate: is a NCO rate value.
#   FromNCO: is a NCO value moving from.
#   ToNCO: is a NCO value moving to.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeMix_ClearEventStatus() before running this API.

ret = handle.XDfeMix_MoveCC(device_id, 0, 0, 0, 0)

#Description:
#   Updates specified CCID, with a configuration defined in CarrierCfg
#   structure.
#   If there is insufficient capacity for the new CC the function will return
#   an error.
#C header declaration:
#   u32 XDfeMix_UpdateCC(const XDfeMix *InstancePtr, s32 CCID,
#	const XDfeMix_CarrierCfg *CarrierCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#   CarrierCfg: is a CC configuration container.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

CarrierCfg_in = handle.GetStruct_XDfeMix_CarrierCfg()
ret = handle.XDfeMix_UpdateCC(device_id, 0, CarrierCfg_in)

#Description:
#   Sets antenna gain. Initiate CC update (enable CCUpdate trigger TUSER
#   Single Shot).
#C header declaration:
#   u32 XDfeMix_SetAntennaGain(const XDfeMix *InstancePtr, u32 AntennaId, u32 AntennaGain);
#Input Arguments:
#   device_id: id of the opened device.
#   AntennaId: is an antenna ID.
#   AntennaGain: is an antenna gain.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#Note:
#   Clear event status with XDfeMix_ClearEventStatus() before running this API.

ret = handle.XDfeMix_SetAntennaGain(device_id, 0, 0)

#Description:
#   Returns current trigger configuration.
#C header declaration:
#   void XDfeMix_GetTriggersCfg(const XDfeMix *InstancePtr, XDfeMix_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   TriggerCfg: trigger configuration container

TriggerCfg_out = handle.XDfeMix_GetTriggersCfg(device_id)

#Description:
#   Gets DUC/DDC status for a specified CCID.
#C header declaration:
#   void XDfeMix_GetDUCDDCStatus(const XDfeMix *InstancePtr, u32 CCID, XDfeMix_DUCDDCStatus *DUCDDCStatus);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   DUCDDCStatus: DUC/DDC status container.

DUCDDCStatus_out = handle.XDfeMix_GetDUCDDCStatus(device_id, 0)

#Description:
#   Gets Mixer status for a specified CCID.
#C header declaration:
#   void XDfeMix_GetMixerStatus(const XDfeMix *InstancePtr, u32 CCID,
#   XDfeMix_MixerStatus *MixerStatus);
#Input Arguments:
#   device_id: id of the opened device.
#   CCID: is a Channel ID.
#Return:
#   DUCDDCStatus: DUC/DDC status container.

MixerStatus_out = handle.XDfeMix_GetMixerStatus(device_id, 0)

#Description:
#   Gets interrupt mask status.
#C header declaration:
#   void XDfeMix_GetInterruptMask(const XDfeMix *InstancePtr,
#   XDfeMix_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Mask: interrupt masks container.

InterruptMask_out = handle.XDfeMix_GetInterruptMask(device_id)

#Description:
#   Sets interrupt mask.
#C header declaration:
#   void XDfeMix_SetInterruptMask(const XDfeMix *InstancePtr,
#   const XDfeMix_InterruptMask *Mask);
#Input Arguments:
#   device_id: id of the opened device.
#   Mask: interrupt masks flags container.
#         0 - does not mask corresponding interrupt
#         1 - masks corresponding interrupt
#Return:
#   None

InterruptMask_in = handle.GetStruct_XDfeMix_InterruptMask()
InterruptMask_in['DUCDDCOverflow'] = 1
InterruptMask_in['MixerOverflow'] = 1
InterruptMask_in['CCUpdate'] = 1
InterruptMask_in['CCSequenceError'] = 1
handle.XDfeMix_SetInterruptMask(device_id, InterruptMask_in)

#Description:
#   Gets event status.
#C header declaration:
#   void XDfeMix_GetEventStatus(const XDfeMix *InstancePtr, XDfeMix_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: event status container.

EventStatus_out = handle.XDfeMix_GetEventStatus(device_id)

#Description:
#   Clears event status.
#C header declaration:
#   void XDfeMix_ClearEventStatus(const XDfeMix *InstancePtr, const XDfeMix_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#   Status: Clear event status container.
#           0 - does not clear corresponding event status
#           1 - clear corresponding event status
#Return:
#   None

Status_in = handle.GetStruct_XDfeMix_Status()
Status_in['DUCDDCOverflow'] = 1
Status_in['MixerOverflow'] = 1
Status_in['CCUpdate'] = 1
Status_in['CCSequenceError'] = 1
handle.XDfeMix_ClearEventStatus(device_id, Status_in)

#Description:
#   Reads the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeMix_GetTUserDelay(const XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   ret: Delay value

ret = handle.XDfeMix_GetTUserDelay(device_id)

#Description:
#   Returns data latency + tap.
#C header declaration:
#   u32 XDfeMix_GetTDataDelay(const XDfeMix *InstancePtr, u32 Tap, u32 *TDataDelay);
#Input Arguments:
#   device_id: id of the opened device.
#   Tap: Tap value.
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   TDataDelay: Returned Data latency value.

Tap = 0
ret, TDataDelay = handle.XDfeMix_GetTDataDelay(device_id, Tap)

#Description:
#   Returns predefined Central Tap value for chosen RATE.
#C header declaration:
#   u32 XDfeMix_GetCenterTap(const XDfeMix *InstancePtr, u32 Rate, u32 *CenterTap);
#Input Arguments:
#   device_id: id of the opened device.
#   Rate: Interpolation/decimation rate index value [1-5].
#Return:
#   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
#   CenterTap: Returned Central Tap value.

Rate = 1
ret, CenterTap = handle.XDfeMix_GetCenterTap(device_id, Rate)

#Description:
#   Deactivates Mixer and moves the state machine to Initialised state.
#C header declaration:
#   void XDfeMix_GetVersions(const XDfeMix *InstancePtr, XDfeMix_Version *SwVersion,
#	XDfeMix_Version *HwVersion);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

SwVersion_out, HwVersion_out = handle.XDfeMix_GetVersions(device_id)

#Description:
#   Adds specified auxiliary NCO, with specified configuration, to a local CCCfg.
#C header declaration:
#   void XDfeMix_AddAuxNCOtoCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
#			      const s32 AuxId, const XDfeMix_NCO *NCO,
#			      const XDfeMix_AuxiliaryCfg *AuxCfg)
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   AuxId: Channel ID.
#   NCO: Auxiliary NCO configuration container.
#   AuxCfg: Auxiliary NCO configuration container.
#Return:
#   CCCfg: component carrier (CC) configuration container.
CurrCCCfg = handle.GetStruct_XDfeMix_CCCfg()
CurrentCCCfg = handle.XDfeMix_GetCurrentCCCfg(int(device_id), CurrCCCfg)
NCO = handle.GetStruct_XDfeMix_NCO()
AuxiliaryCfg = handle.GetStruct_XDfeMix_AuxiliaryCfg()
AuxId = 1
CurrentCCCfg = handle.XDfeMix_AddAuxNCOtoCCCfg(device_id, CurrentCCCfg, AuxId, NCO, AuxiliaryCfg)
AuxId = 2
CurrentCCCfg = handle.XDfeMix_AddAuxNCOtoCCCfg(device_id, CurrentCCCfg, AuxId, NCO, AuxiliaryCfg)

#Description:
#   Disables specified auxiliary NCO configuration structure.
#C header declaration:
#   void XDfeMix_RemoveAuxNCOfromCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
#			      const s32 AuxId)
#Input Arguments:
#   device_id: id of the opened device.
#   CCCfg: component carrier (CC) configuration container.
#   AuxId: Channel ID.
#Return:
#   CCCfg: component carrier (CC) configuration container.
AuxId = 1
CurrentCCCfg = handle.XDfeMix_RemoveAuxNCOfromCCCfg(device_id, CurrentCCCfg, AuxId)

#Description:
#   Deactivates Mixer and moves the state machine to Initialised state.
#C header declaration:
#   void XDfeMix_Deactivate(XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeMix_Deactivate(device_id)

#Description:
#   Sets the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeMix_SetTUserDelay(const XDfeMix *InstancePtr, u32 Delay);
#Input Arguments:
#   device_id: id of the opened device.
#   Delay: requested delay variable.
#Return:
#   None

handle.XDfeMix_SetTUserDelay(device_id, 10)

#Description:
#   API closes the instances of a Mixer driver and moves the state machine to
#   a Not Ready state.
#C header declaration:
#   void XDfeMix_InstanceClose(XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeMix_InstanceClose(device_id)