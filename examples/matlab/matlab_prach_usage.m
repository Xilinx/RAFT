%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
% SPDX-License-Identifier: BSD-3-Clause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Put the path of the python module here. It can be in any drive
current_folder = pwd
if count(py.sys.path,current_folder) == 0
    %Put the path of the python module here. It can be in any drive
    insert(py.sys.path,uint32(0),current_folder);
end

%Import the python module in matlab
%rehash toolboxcache
PRACH=py.importlib.import_module('prach_client');
PRACH=py.importlib.reload(PRACH);

%%%%%% SetIPAndPort
%Input Arguments:
%    arg1: ipaddress of server
%    arg2: port number at server for pyro communication
%Return: None
PRACH.prach.SetIpAndPort("169.254.10.2", "9090")

%%%%%% GetPythonLogLevels
%Description:
%   Return the logging levels supported by logging library in python
%Input Arguments:
%  None
%Return:
%   Dictionary showing the log levels supported by logging library
PythonLogLevels = PRACH.prach.GetPythonLogLevels()

%%%%%% SetServerLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%    Log level to set
%Return:
%   None
PRACH.prach.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% SetClientLogLevel
%Input Arguments:
%    arg1: PythonLogLevelsEnum
%Return: None
PRACH.prach.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% GetEnum_metal_log_level
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None
%SetMetalLogLevel
metal_log_level = PRACH.prach.GetEnum_metal_log_level()

%%%%% SetMetalLogLevel
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None
PRACH.prach.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

%%%%%% GetEnum_XDfePrach_StateId
%Description:
%   Return Dictionary equivalent of enum XDfePrach_StateId
%Input Arguments:
%   None
%Return:
%   Dictionary equivalent of enum XDfePrach_StateId
XDfePrach_StateId = PRACH.prach.GetEnum_XDfePrach_StateId()

%%%%%% XDfePrach_InstanceInit
%Description:
%   API initialise an instance of the driver.
%   Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
%   PRACH device with the name DeviceNodeName. The first available slot in
%   the instance array XDfePrach_Prach[] will be taken as a DeviceNodeName
%   object. On success it moves the state machine to a Ready state, while on
%   failure stays in a Not Ready state.
%C header declaration:
%   XDfePrach *XDfePrach_InstanceInit(const char *DeviceNodeName);
%Input Arguments:
%   DeviceNodeName: device node name.
%Return:
%   ret - 0 on success, 1 on failure
%   device_id - integer handle to initalized instance
%   DeviceNodeNameRet - device node name returned from driver
%                       which will be same as the passed value
str = "a7e00000.xdfe_nr_prach"
ret = PRACH.prach.XDfePrach_InstanceInit(str)
S= cell(ret)
device_id = ret{2}

%%%%%% XDfePrach_WriteReg
%Description:
%   Writes a value to register in a PRACH instance.
%C header declaration:
%   void XDfePrach_WriteReg(const XDfePrach *InstancePtr, u32 AddrOffset, u32 Data);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%   Data: is value to be written.
%Return:
%   None

PRACH.prach.XDfePrach_WriteReg(device_id, uint32(0x40), uint32(0))

%%%%%% XDfePrach_ReadReg
%Description:
%   Reads a value the register in a PRACH instance.
%C header declaration:
%   u32 XDfePrach_ReadReg(const XDfePrach *InstancePtr, u32 AddrOffset);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%Return:
%   ret: Register value.

PRACH.prach.XDfePrach_ReadReg(device_id, uint32(0))

%%%%%% XDfePrach_Reset
%Description:
%   Resets PRACH and puts block into a reset state.
%C header declaration:
%   void XDfePrach_Reset(XDfePrach *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

PRACH.prach.XDfePrach_Reset(device_id)

%%%%%% XDfePrach_Configure
%Description:
%   Reads configuration from device tree/xparameters.h and IP registers.
%   Removes S/W reset and moves the state machine to a Configured state.
%C header declaration:
%   void XDfePrach_Configure(XDfePrach *InstancePtr, XDfePrach_Cfg *Cfg);
%Input Arguments:
%   device_id: id of the opened device.
%   Cfg: configuration data container.
%Return:
%   Cfg: configuration data container.

Cfg_in = PRACH.prach.GetStruct_XDfePrach_Cfg()
Cfg_out = PRACH.prach.XDfePrach_Configure(device_id, Cfg_in)

%%%%%% XDfePrach_Initialize
%Description:
%   DFE PRACH driver one time initialisation also moves the state machine to
%   an Initialised state.
%C header declaration:
%   void XDfePrach_Initialize(XDfePrach *InstancePtr, const XDfePrach_Init *Init);
%Input Arguments:
%   device_id: id of the opened device.
%   Init: initialisation data container.
%Return:
%   None
Init_in = PRACH.prach.GetStruct_XDfePrach_Init()
Seq = PRACH.prach.GetStruct_XDfePrach_CCSequence()
update(Seq, py.dict(pyargs('Length', uint32(6))))
update(Init_in, py.dict(pyargs('Sequence', py.dict(Seq))))
Init_out = PRACH.prach.XDfePrach_Initialize(device_id, Init_in)

%%%%%% XDfePrach_SetTriggersCfg
%Description:
%   Set trigger configuration.
%C header declaration:
%   void XDfePrach_SetTriggersCfg(const XDfePrach *InstancePtr,
% 	XDfePrach_TriggerCfg *TriggerCfg)
%Input Arguments:
%   device_id: id of the opened device.
%   TriggerCfg: Trigger configuration container.
%Return:
%   TriggerCfg: Trigger configuration container.
Mode = PRACH.prach.GetStruct_XDfePrach_Trigger()
update(Mode, py.dict(pyargs('Mode', uint32(1))))
TriggerCfg_in = PRACH.prach.GetStruct_XDfePrach_TriggerCfg()
update(TriggerCfg_in, py.dict(pyargs('FrameInit', Mode)))
TriggerCfg_out = PRACH.prach.XDfePrach_SetTriggersCfg(device_id, TriggerCfg_in)

%%%%%% XDfePrach_Activate
%Description:
%   Activates PRACH and moves the state machine to an Activated state.
%C header declaration:
%   void XDfePrach_Activate(XDfePrach *InstancePtr, bool EnableLowPower);
%Input Arguments:
%   device_id: id of the opened device.
%   EnableLowPower: flag indicating low power.
%Return:
%   None

PRACH.prach.XDfePrach_Activate(device_id, uint32(0))

%%%%%% XDfePrach_GetCurrentCCCfg
%Description:
%   Returns the current CC configuration
%C header declaration:
%   void XDfePrach_GetCurrentCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CurrCCCfg: CC configuration container.
%Return:
%   CurrCCCfg: CC configuration container

CurrCCCfg = PRACH.prach.GetStruct_XDfePrach_CCCfg()
CurrentCCCfg = PRACH.prach.XDfePrach_GetCurrentCCCfg(device_id, CurrCCCfg)

%%%%%% XDfePrach_GetEmptyCCCfg
%Description:
%   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
%   in XDfePrach_Configure(), array CCCfg->Sequence.CCID[] members are set to not
%   used value (-1) and the other CCCfg members are set to 0.
%C header declaration:
%   void XDfePrach_GetEmptyCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   CCCfg: CC configuration container

CCCfg = PRACH.prach.XDfePrach_GetEmptyCCCfg(device_id)

%%%%%% XDfePrach_GetCarrierCfg
%Description:
%   Returns the current CCID carrier configuration.
%C header declaration:
%   void XDfePrach_GetCarrierCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
%   s32 CCID, u32 *CCSeqBitmap, XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.

CCCfg = PRACH.prach.GetStruct_XDfePrach_CCCfg()
ret = PRACH.prach.XDfePrach_GetCarrierCfg(device_id, CCCfg, int32(0))

%%%%%% XDfePrach_AddCCtoCCCfg
%Description:
%   Adds specified CCID, with specified configuration, to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfePrach_AddCCtoCCCfg(XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg, s32 CCID,
%   u32 CCSeqBitmap, const XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CCCfg: component carrier (CC) configuration container.

CarrierCfg = PRACH.prach.GetStruct_XDfePrach_CarrierCfg()
%ret = PRACH.prach.XDfePrach_AddCCtoCCCfg(device_id, CCCfg, int32(0), uint32(0), CarrierCfg)

%%%%%% XDfePrach_RemoveCCfromCCCfg
%Description:
%   Removes specified CCID from a local CC configuration structure.
%C header declaration:
%   void XDfePrach_RemoveCCfromCCCfg(XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
% 	s32 CCID);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCCfg: component carrier (CC) configuration container.

CCCfg = PRACH.prach.GetStruct_XDfePrach_CCCfg()
CCCfg = PRACH.prach.XDfePrach_RemoveCCfromCCCfg(device_id, CCCfg, int32(0))

%%%%%% XDfePrach_UpdateCCinCCCfg
%Description:
%   Updates specified CCID, with specified configuration to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%C header declaration:
%   void XDfePrach_UpdateCCinCCCfg(const XDfePrach *InstancePtr, XDfePrach_CCCfg *CCCfg,
%   s32 CCID, const XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CarrierCfg: CC configuration container.
%Return:
%   CCCfg: component carrier (CC) configuration container.

CCCfg = PRACH.prach.GetStruct_XDfePrach_CCCfg()
CarrierCfg = PRACH.prach.GetStruct_XDfePrach_CarrierCfg()
ret = PRACH.prach.XDfePrach_UpdateCCinCCCfg(device_id, CCCfg, uint32(0), ...
                CarrierCfg)

%%%%%% XDfePrach_AddCC
%Description:
%   Add specified CCID, with specified configuration.
%C header declaration:
%   u32 XDfePrach_AddCC(const XDfePrach *InstancePtr, u32 CCId,
%   const XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%   BitSequence: up to 16 defined slots into which a CC can be
%                allocated. The number of slots can be from 1 to 16 depending on
%                system initialization. The number of slots is defined by the
%                "sequence length" parameter which is provided during initialization.
%                The Bit offset within the CCSeqBitmap indicates the equivalent
%                Slot number to allocate. e.g. 0x0003  means the caller wants the
%                passed component carrier (CC) to be allocated to slots 0 and 1.
%   CarrierCfg: is a CC configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CarrierCfg: is a CC configuration container.

CarrierCfg_in = PRACH.prach.GetStruct_XDfePrach_CarrierCfg()
BitSequence = uint32(0xb)
CarrierCfg_out = PRACH.prach.XDfePrach_AddCC(device_id, uint32(0), BitSequence, CarrierCfg_in)

%%%%%% XDfePrach_UpdateCC
%Description:
%   Updates a CCID sequence.
%C header declaration:
%   u32 XDfePrach_UpdateCC(const XDfePrach *InstancePtr, u32 CCId,
%   const XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%   CarrierCfg: is carrier data container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

CarrierCfg_in = PRACH.prach.GetStruct_XDfePrach_CarrierCfg()
ret = PRACH.prach.XDfePrach_UpdateCC(device_id, uint32(0), CarrierCfg_in)

%%%%%% XDfePrach_AddRCCfg
%Description:
%   Adds a new RC entry to the RC_CONFIGURATION. RCId must be same as the
%   physical channel RachChan.
%C header declaration:
%   u32 XDfePrach_AddRCCfg(const XDfePrach *InstancePtr, %u32 CCId, u32 RCId, u32 RachChan,
%   XDfePrach_DDCCfg *DdcCfg,XDfePrach_NCO *NcoCfg, XDfePrach_Schedule *StaticSchedule);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is CC Id.
%   RCId: is RC Id.
%   RachChan: is RACH channel.
%   DdcCfg: is DDC data container.
%   NcoCfg: is NCO data container.
%   StaticSchedule: is Schedule data container.
%Return:
%   ret: XST_SUCCESS on succes, XST_FAILURE on failure
%   DdcCfg: is DDC data container.
%   NcoCfg: is NCO data container.
%   Schedule: is Schedule data container.

% DdcCfg = py.dict(pyargs( ...
%     'DecimationRate', uint32(0), ...
%     'SCS', uint32(0), ...
%     'RachGain', py.list({uint32(0), uint32(0), uint32(0), uint32(0), uint32(0), uint32(0)}) ...
%     ))
NcoCfg = py.dict(pyargs( ...
    'PhaseOffset', uint32(0), ...
    'PhaseAcc', uint32(0), ...
    'DualModCount', uint32(0), ...
    'DualModSel', uint32(0), ...
    'Frequency', uint32(0), ...
    'NcoGain', uint32(0) ...
    ))
StaticSchedule = py.dict(pyargs( ...
    'PatternPeriod', uint32(0), ...
    'FrameID', uint32(0), ...
    'SubframeID', uint32(0), ...
    'SlotId', uint32(0), ...
    'Duration', uint32(0), ...
    'Repeats', uint32(0) ...
    ))
DdcCfg = PRACH.prach.GetStruct_XDfePrach_DDCCfg()
ret = PRACH.prach.XDfePrach_AddRCCfg(device_id, uint32(0), uint32(0), uint32(0), DdcCfg, NcoCfg, StaticSchedule)

%%%%%% XDfePrach_MoveRC
%Description:
%   Move specified RCID from one NCO & Decimation Channel to another NCO &&
%   Decimation Channel.
%C header declaration:
%   u32 XDfePrach_MoveRC(const XDfePrach *InstancePtr, u32 RCId, u32 ToChannel);
%Input Arguments:
%   device_id: id of the opened device.
%   RCId: is RC Id.
%   ToChannel: is destination channel Id.
%Return:
%   ret: XST_SUCCESS on succes, XST_FAILURE on failure

ret = PRACH.prach.XDfePrach_MoveRC(device_id, uint32(0), uint32(0))

%%%%%% XDfePrach_GetTriggersCfg
%Description:
%   Return current trigger configuration.
%C header declaration:
%   void XDfePrach_GetTriggersCfg(const XDfePrach *InstancePtr,
%   XDfePrach_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   TriggerCfg: Trigger configuration container

TriggerCfg_out = PRACH.prach.XDfePrach_GetTriggersCfg(device_id)

%%%%%% XDfePrach_GetCC
%Description:
%   Get specified CCID carrier configuration from either Current or Next.
%C header declaration:
%   void XDfePrach_GetCC(const XDfePrach *InstancePtr, u32 CCID,
% 	XDfePrach_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   Next: is next or current data flag.
%   CCID: is component carrier id number.
%Return:
%   CarrierCfg: Carrier config container.

CarrierCfg_out = PRACH.prach.XDfePrach_GetCC(device_id, uint32(0), uint32(0))

%%%%%% XDfePrach_GetStatus
%Description:
%   Get PRACH Status.
%C header declaration:
%   void XDfePrach_GetStatus(const XDfePrach *InstancePtr, XDfePrach_Status *Status);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   Status: Status data container.

Status = PRACH.prach.XDfePrach_GetStatus(device_id)

%%%%%% XDfePrach_ClearStatus
%Description:
%   Clear the PRACH status registers.
%C header declaration:
%   void XDfePrach_ClearStatus(const XDfePrach *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

PRACH.prach.XDfePrach_ClearStatus(device_id)

%%%%%% XDfePrach_CapturePhase
%Description:
%   Captures phase for all phase accumulators in associated AXI-lite registers.
%C header declaration:
%   void XDfePrach_CapturePhase(const XDfePrach *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

PRACH.prach.XDfePrach_CapturePhase(device_id)

%%%%%% XDfePrach_GetCapturePhase
%Description:
%   Reads the captured phase for a given Rach Channel.
%C header declaration:
%   void XDfePrach_GetCapturePhase(const XDfePrach *InstancePtr, u32 RachChan,
% 	XDfePrach_NCO *CapturedPhase);
%Input Arguments:
%   device_id: id of the opened device.
%   RachChan: is RACH channel Id.
%Return:
%   NCO data container.

CapturedPhase = PRACH.prach.XDfePrach_GetCapturePhase(device_id, uint32(0))

%%%%%% XDfePrach_GetInterruptMask
%Description:
%   Gets interrupt mask status.
%C header declaration:
%   void XDfePrach_GetInterruptMask(const XDfePrach *InstancePtr,
% 	XDfePrach_InterruptMask *Mask);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   Mask: interrupt masks container.

Flags = PRACH.prach.XDfePrach_GetInterruptMask(device_id)

%%%%%% XDfePrach_SetInterruptMask
%Description:
%   Sets interrupt mask.
%C header declaration:
%   void XDfePrach_SetInterruptMask(const XDfePrach *InstancePtr,
% 	const XDfePrach_InterruptMask *Mask);
%Input Arguments:
%   device_id: id of the opened device.
%   Mask: interrupt masks container.
%         0 - does not mask coresponding interrupt
%         1 - masks coresponding interrupt
%Return:
%   None

Flags_in = PRACH.prach.GetStruct_XDfePrach_InterruptMask()
PRACH.prach.XDfePrach_SetInterruptMask(device_id, Flags_in)

%%%%%% XDfePrach_RemoveCC
%Description:
%   Remove a CCID from sequence.
%C header declaration:
%   u32 XDfePrach_RemoveCC(const XDfePrach *InstancePtr, u32 CCId);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

ret = PRACH.prach.XDfePrach_RemoveCC(device_id, uint32(0))

%%%%%% XDfePrach_RemoveRC
%Description:
%   Removes an RC configuration entry from the RC_CONFIGURATION.
%C header declaration:
%   u32 XDfePrach_RemoveRC(const XDfePrach *InstancePtr, u32 RCId);
%Input Arguments:
%   device_id: id of the opened device.
%   RCId: is RC Id.
%Return:
%   ret: XST_SUCCESS on success, XST_FAILURE on failure

ret = PRACH.prach.XDfePrach_RemoveRC(device_id, uint32(0))

%%%%%% XDfePrach_GetVersions
%Description:
%   This API gets the driver and HW design version.
%C header declaration:
%   void XDfePrach_GetVersions(const XDfePrach *InstancePtr, XDfePrach_Version *SwVersion,
% 	XDfePrach_Version *HwVersion);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   SwVersion: driver version numbers.
%   HwVersion: HW version numbers.

%SwVersion = {
%    "Major": 0,
%    "Minor": 0,
%    "Revision": 0,
%    "Patch": 0,
%}
%HwVersion = {
%    "Major": 0,
%    "Minor": 0,
%    "Revision": 0,
%    "Patch": 0,
%}
Version = PRACH.prach.XDfePrach_GetVersions(device_id)
Version = cell(Version)
celldisp(Version)

%%%%%% XDfePrach_Deactivate
%Description:
%   Deactivates PRACH and moves the state machine to Initialised state.
%C header declaration:
%   void XDfePrach_Deactivate(XDfePrach *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

PRACH.prach.XDfePrach_Deactivate(device_id)

%%%%%% XDfePrach_InstanceClose
%Description:
%   API closes the instances of a PRACH driver and moves the state machine to
%   a Not Ready state.
%C header declaration:
%   void XDfePrach_InstanceClose(XDfePrach *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

PRACH.prach.XDfePrach_InstanceClose(device_id)
