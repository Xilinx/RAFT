%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
% Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
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
MIX=py.importlib.import_module('mix_client');
MIX=py.importlib.reload(MIX);

%%%%%% SetIPAndPort
%Input Arguments:
%    arg1: ipaddress of server
%    arg2: port number at server for pyro communication
%Return: None
MIX.mix.SetIpAndPort("169.254.10.2", "9090")

%%%%%% GetPythonLogLevels
%Description:
%   Return the logging levels supported by logging library in python
%Input Arguments:
%   None
%Return:
%   Dictionary showing the log levels supported by logging library

PythonLogLevels = MIX.mix.GetPythonLogLevels()

%%%%%% SetServerLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None

MIX.mix.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% SetClientLogLevel
%Input Arguments:
%    arg1: PythonLogLevelsEnum
%Return: None
MIX.mix.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% GetEnum_metal_log_level
%Description:
%   Return Dictionary equivalent of enum metal_log_level
%Input Arguments:
%   None
%Return:
%   Dictionary equivalent of enum metal_log_level

metal_log_level = MIX.mix.GetEnum_metal_log_level()

%%%%% SetMetalLogLevel
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None

MIX.mix.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

%%%%%% GetEnum_XDfeMix_StateId
%Description:
%   Return Dictionary equivalent of enum XDfeMix_StateId
%Input Arguments:
%   None
%Return:
%   Dictionary equivalent of enum XDfeMix_StateId

XDfeMix_StateId = MIX.mix.GetEnum_XDfeMix_StateId()

%%%%%% XDfeMix_InstanceInit
%Description:
%   API initialises one instance of a Mixer driver.
%   Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
%   XDfeMix device with the name DeviceNodeName. The first available slot in
%   the instances array XDfeMix_Mixer[] will be taken as a DeviceNodeName
%   object. On success it moves the state machine to a Ready state, while on
%   failure stays in a Not Ready state.
%C header declaration:
%   XDfeMix *XDfeMix_InstanceInit(const char *DeviceNodeName);
%Input Arguments:
%   DeviceNodeName: device node name.
%Return:
%   ret - 0 on success, 1 on failure
%   device_id - integer handle to initialized instance
%   DeviceNodeNameRet - device node name returned from driver
%                       which will be same as the passed value

str = "a7c40000.xdfe_cc_mixer"
ret = MIX.mix.XDfeMix_InstanceInit(str)
S= cell(ret)
device_id = ret{2}

%%%%%% XDfeMix_WriteReg
%Description:
%   Writes a value to register in a Mixer instance.
%C header declaration:
%   void XDfeMix_WriteReg(const XDfeMix *InstancePtr, u32 AddrOffset, u32 Data);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%   Data: is value to be written.
%Return:
%   None

MIX.mix.XDfeMix_WriteReg(device_id, uint32(0x20), uint32(0x1001))

%%%%%% XDfeMix_ReadReg
%Description:
%   Reads a value from the register from a Mixer instance.
%C header declaration:
%   u32 XDfeMix_ReadReg(const XDfeMix *InstancePtr, u32 AddrOffset);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%Return:
%   regval: Register value.

ret = MIX.mix.XDfeMix_ReadReg(device_id, uint32(0))

%%%%%% XDfeMix_Reset
%Description:
%   Resets and put block into a reset state.
%C header declaration:
%   void XDfeMix_Reset(XDfeMix *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

MIX.mix.XDfeMix_Reset(device_id)
MIX.mix.XDfeMix_WriteReg(device_id, uint32(0x20), uint32(0x1001))

%%%%%% XDfeMix_Configure
%Description:
%   Reads configuration from device tree/xparameters.h and IP registers.
%   Removes S/W reset and moves the state machine to a Configured state.
%C header declaration:
%   void XDfeMix_Configure(XDfeMix *InstancePtr, XDfeMix_Cfg *Cfg);
%Input Arguments:
%   device_id: id of the opened device.
%   Cfg: configuration data container.
%Return:
%   Cfg: configuration data container.

%%% XDfeMix_Cfg python dictionary
%typedef struct {
%	u32 Major; /**< Major version number */
%	u32 Minor; /**< Minor version number */
%	u32 Revision; /**< Revision number */
%	u32 Patch; /**< Patch number */
%} XDfeMix_Version;

% typedef struct {
% 	u32 Mode; /**< [0,1] 0=downlink, 1=uplink */
% 	u32 NumAntenna; /**< [1,2,4,8] */
% 	u32 MaxUseableCcids; /**< [4,8] */
% 	u32 Lanes; /**< [1-4] */
% 	u32 AntennaInterleave; /**< [1,2,4,8] */
% 	u32 MixerCps; /**< [1,2,4] */
% 	u32 DataIWidth; /**< [16,24] */
% 	u32 DataOWidth; /**< [16,24] */
% 	u32 TUserWidth; /**< [0-64] */
% } XDfeMix_ModelParameters;

%typedef struct {
%	XDfeMix_Version Version; /**< Logicore version */
%	XDfeMix_ModelParameters ModelParams; /**< Logicore
%		parameterization */
%} XDfeMix_Cfg;

% Cfg_in = py.dict(pyargs( ...
%    'Version', py.dict(pyargs( ...
%        'Major', uint32(0), ...
%        'Minor', uint32(0), ...
%        'Revision', uint32(0), ...
%        'Patch', uint32(0) ...
%    )), ...
%    'ModelParams', py.dict(pyargs( ...
%        'Mode', uint32(0), ...
%        'NumAntenna', uint32(0), ...
%        'MaxUseableCcids', uint32(0), ...
%        'Lanes', uint32(0), ...
%        'AntennaInterleave', uint32(0), ...
%        'MixerCps', uint32(0), ...
%        'DataIWidth', uint32(0), ...
%        'DataOWidth', uint32(0), ...
%        'TUserWidth', uint32(0) ...
%    )) ...
% ));
Cfg_in = MIX.mix.GetStruct_XDfeMix_Cfg()
Cfg = MIX.mix.XDfeMix_Configure(device_id, Cfg_in)
MIX.mix.XDfeMix_WriteReg(device_id, uint32(0x20), uint32(0x1001))

%%%%%% XDfeMix_Initialize
%Description:
%   DFE Mixer driver one time initialisation and moves the state machine to
%   an Initialised state.
%C header declaration:
%   void XDfeMix_Initialize(XDfeMix *InstancePtr, const XDfeMix_Init *Init);
%Input Arguments:
%   device_id: id of the opened device.
%   Init: initialisation data container.
%Return:
%   Init: initialisation data container.

% typedef struct {
% 	XDfeMix_CCSequence Sequence;
% } XDfeMix_Init;
% typedef struct {
% 	u32 Length; /**< [1-16] Sequence length */
% 	s32 CCID[XDFEMIX_SEQ_LENGTH_MAX]; /**< [0-15].Array of CCID's
% 		arranged in the order the CCIDs are required to be processed
% 		in the channel filter */
% } XDfeMix_CCSequence;

Init_in = MIX.mix.GetStruct_XDfeMix_Init()
Seq = MIX.mix.GetStruct_XDfeMix_CCSequence()
update(Seq, py.dict(pyargs('Length', uint32(6))))

update(Init_in, py.dict(pyargs('Sequence', py.dict(Seq))))

MIX.mix.XDfeMix_Initialize(device_id, Init_in)

%%%%%% XDfeMix_SetTriggersCfg
%Description:
%   Sets trigger configuration.
%C header declaration:
%   void XDfeMix_SetTriggersCfg(const XDfeMix *InstancePtr, XDfeMix_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   TriggerCfg: trigger configuration container.
%Return:
%   TriggerCfg: trigger configuration container.

%typedef struct {
%	u32 Enable; /**< [0,1], 0 = Disabled: Trigger disabled;
%		1 = Enabled: Trigger enabled */
%	u32 Source; /**< [0,1,2],
%		0 = IMMEDIATE: write to the trigger configuration register
%			immediately
%		1 = TUSER: write on Edge detected on specified TUSER bit
%		2 = TLAST: write on Edge detected on TLAST */
%	u32 TUSERBit; /**< [0-7], Species which TUSER bit is used by
%		the trigger */
%	u32 Edge; /**< [0,1,2], 0 = Rising; 1 = Falling; 2 = Both */
%	u32 OneShot; /**< [0,1],
%		0 = Continuous: Once enabled trigger repeats continuously
%		1 = OneShot: Once enabled trigger occurs once and then
%			disables */
%} XDfeMix_Trigger;
TriggerCfg_in =MIX.mix.GetStruct_XDfeMix_TriggerCfg()
MIX.mix.XDfeMix_SetTriggersCfg(device_id, TriggerCfg_in)

%%%%%% XDfeMix_Activate
%Description:
%   Activates Mixer and moves the state machine to an Activated state.
%C header declaration:
%   void XDfeMix_Activate(XDfeMix *InstancePtr, bool EnableLowPower);
%Input Arguments:
%   device_id: id of the opened device.
%   EnableLowPower: flag indicating low power.
%Return:
%   None

MIX.mix.XDfeMix_Activate(device_id, uint32(0))

%%%%%% XDfeMix_GetCurrentCCCfg
%Description:
%   Returns the current CC configuration. Not used slot ID in a sequence
%   (Sequence.CCID[Index]) are represented as (-1), not the value in registers.
%C header declaration:
%   void XDfeMix_GetCurrentCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CurrCCCfg: CC configuration container.
%Return:
%   CurrCCCfg: CC configuration container

CurrCCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
CurrentCCCfg = MIX.mix.XDfeMix_GetCurrentCCCfg(device_id, CurrCCCfg)

%%%%%% XDfeMix_GetEmptyCCCfg
%Description:
%   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
%   in XDfeMix_Configure(), array CCCfg->Sequence.CCID[] members are set to not
%   used value (-1) and the other CCCfg members are set to 0.
%C header declaration:
%   void XDfeMix_GetEmptyCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   CCCfg: CC configuration container

CCCfg = MIX.mix.XDfeMix_GetEmptyCCCfg(device_id)

%%%%%% XDfeMix_GetCarrierCfgAndNCO
%Description:
%   Returns the current CC sequence bitmap, CCID carrier configuration and
%   NCO configuration.
%C header declaration:
%   void XDfeMix_GetCarrierCfgAndNCO(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
%   s32 CCID, u32 *CCSeqBitmap, XDfeMix_CarrierCfg *CarrierCfg, XDfeMix_NCO *NCO);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.
%   NCO: NCO configuration container.

CCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
ret = MIX.mix.XDfeMix_GetCarrierCfgAndNCO(device_id, CCCfg, int32(0))

%%%%%% XDfeMix_AddCCtoCCCfg
%Description:
%   Adds specified CCID, with specified configuration, to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%
%   The returned CCCfg.Sequence is transleted as there is no explicit indication
%   that SEQUENCE[i] is not used - 0 can define the slot as either used or
%   not used. Sequence data that is returned in the CCIDSequence is not the same
%   as what is written in the registers. The translation is:
%   - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
%   - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
%   - a returned CCIDSequence->Length = length in register + 1
%C header declaration:
%   u32 XDfeMix_AddCCtoCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg, s32 CCID,
%   u32 CCSeqBitmap, const XDfeMix_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.
%   NCO: NCO configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CCCfg: component carrier (CC) configuration container.

CCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
CarrierCfg = MIX.mix.GetStruct_XDfeMix_CarrierCfg()
%ret = MIX.mix.XDfeMix_AddCCtoCCCfg(device_id, CCCfg, int32(0), uint32(0), CarrierCfg)

%%%%%% XDfeMix_RemoveCCfromCCCfg
%Description:
%   Removes specified CCID from a local CC configuration structure.
%C header declaration:
%   void XDfeMix_RemoveCCfromCCCfg(XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
%   s32 CCID);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCCfg: component carrier (CC) configuration container.

CCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
CCCfg = MIX.mix.XDfeMix_RemoveCCfromCCCfg(device_id, CCCfg, int32(0))

%%%%%% XDfeMix_UpdateCCinCCCfg
%Description:
%   Updates specified CCID, with specified configuration to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%C header declaration:
%   void XDfeMix_UpdateCCinCCCfg(const XDfeMix *InstancePtr, XDfeMix_CCCfg *CCCfg,
%   s32 CCID, const XDfeMix_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CarrierCfg: CC configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CarrierCfg: is a CC configuration container.

CCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
CarrierCfg = MIX.mix.GetStruct_XDfeMix_CarrierCfg()
ret = MIX.mix.XDfeMix_UpdateCCinCCCfg(device_id, CCCfg, int32(0), CarrierCfg)

%%%%%% XDfeMix_SetNextCCCfgAndTrigger
%Description:
%   Writes local CC configuration to the shadow (NEXT) registers and triggers
%   copying from shadow to operational registers.
%C header declaration:
%   u32 XDfeMix_SetNextCCCfgAndTrigger(const XDfeMix *InstancePtr,
%	XDfeMix_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CCCfg: component carrier (CC) configuration container.

CCCfg = MIX.mix.GetStruct_XDfeMix_CCCfg()
ret = MIX.mix.XDfeMix_SetNextCCCfgAndTrigger(device_id, CCCfg)

%%%%%% XDfeMix_AddCC
%Description:
%   Adds specified CCID, with specified configuration.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeMix_AddCC(XDfeMix *InstancePtr, s32 CCID, u32 CCSeqBitmap,
%	const XDfeMix_CarrierCfg *CarrierCfg, const XDfeMix_NCO *NCO);
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
%   NCO: NCO configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CarrierCfg: is a CC configuration container.
%Note:
%   Clear event status with XDfeMix_ClearEventStatus() before running this API.

CarrierCfg_in = MIX.mix.GetStruct_XDfeMix_CarrierCfg()
bitsequence = uint32(0xb)
NCO = MIX.mix.GetStruct_XDfeMix_NCO()
ret = MIX.mix.XDfeMix_AddCC(device_id, uint32(0), bitsequence, CarrierCfg_in, NCO)

%%%%%% XDfeMix_RemoveCC
%Description:
%   Removes specified CCID.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeMix_RemoveCC(const XDfeMix *InstancePtr, u32 CCID);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%Note:
%   Clear event status with XDfeMix_ClearEventStatus() before running this API.

ret = MIX.mix.XDfeMix_RemoveCC(device_id, uint32(0));

%%%%%% XDfeMix_MoveCC
%Description:
%   Moves specified CCID from one NCO to another aligning phase to make it
%   transparent.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeMix_MoveCC(const XDfeMix *InstancePtr, u32 CCID, u32 Rate,
%   u32 FromNCO, u32 ToNCO);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%   Rate: is a NCO rate value.
%   FromNCO: is a NCO value moving from.
%   ToNCO: is a NCO value moving to.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%Note:
%   Clear event status with XDfeMix_ClearEventStatus() before running this API.

%%% CarrierCfg python dictionary
ret = MIX.mix.XDfeMix_MoveCC(device_id, uint32(0), uint32(0), uint32(0), ...
                       uint32(0));

%%%%%% XDfeMix_UpdateCC
%Description:
%   Updates specified CCID, with a configuration defined in CarrierCfg
%   structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%C header declaration:
%   u32 XDfeMix_UpdateCC(const XDfeMix *InstancePtr, s32 CCID,
%	const XDfeMix_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%   CarrierCfg: is a CC configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.

%%% CarrierCfg python dictionary
CarrierCfg_in = MIX.mix.GetStruct_XDfeMix_CarrierCfg()
ret = MIX.mix.XDfeMix_UpdateCC(device_id, int32(0), CarrierCfg_in)

%%%%%% XDfeMix_SetAntennaGain
%Description:
%   Sets antenna gain. Initiate CC update (enable CCUpdate trigger TUSER
%   Single Shot).
%C header declaration:
%   u32 XDfeMix_SetAntennaGain(const XDfeMix *InstancePtr, u32 AntennaId, u32 AntennaGain);
%Input Arguments:
%   device_id: id of the opened device.
%   AntennaId: is an antenna ID.
%   AntennaGain: is an antenna gain.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%Note:
%   Clear event status with XDfeMix_ClearEventStatus() before running this API.

ret = MIX.mix.XDfeMix_SetAntennaGain(device_id, uint32(0), uint32(0));

%%%%%% XDfeMix_GetTriggersCfg
%Description:
%   Returns current trigger configuration.
%C header declaration:
%   void XDfeMix_GetTriggersCfg(const XDfeMix *InstancePtr, XDfeMix_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   TriggerCfg: trigger configuration container

%%% TriggerCfg python dictionary
%typedef struct {
%	u32 Enable; /**< [0,1], 0 = Disabled: Trigger disabled;
%		1 = Enabled: Trigger enabled */
%	u32 Source; /**< [0,1,2],
%		0 = IMMEDIATE: write to the trigger configuration register
%			immediately
%		1 = TUSER: write on Edge detected on specified TUSER bit
%		2 = TLAST: write on Edge detected on TLAST */
%	u32 TUSERBit; /**< [0-7], Species which TUSER bit is used by
%		the trigger */
%	u32 Edge; /**< [0,1,2], 0 = Rising; 1 = Falling; 2 = Both */
%	u32 OneShot; /**< [0,1],
%		0 = Continuous: Once enabled trigger repeats continuously
%		1 = OneShot: Once enabled trigger occurs once and then
%			disables */
%} XDfeMix_Trigger;
%
%typedef struct {
%	XDfeMix_Trigger Activate; /**< Toggle between "Initialized",
%		ultra-low power state, and "Operational". One-shot trigger,
%		disabled following a single event */
%	XDfeMix_Trigger LowPower; /**< Toggle between "Low-power"
%		and "Operational" state */
%	XDfeMix_Trigger CCUpdate; /**< Transition to next CC
%		configuration. Will initiate flush based on CC configuration */
%} XDfeMix_TriggerCfg;

% TriggerCfg = py.dict(pyargs( ...
%     'Activate', py.dict(pyargs( ...
%             'Enable', uint32(0), ...
%             'Source', uint32(0), ...
%             'TUSERBit', uint32(0), ...
%             'OneShot', uint32(0), ...
%             'Edge', uint32(0) ...
%     )), ...
%     'LowPower', py.dict(pyargs( ...
%             'Enable', uint32(0), ...
%             'Source', uint32(0), ...
%             'TUSERBit', uint32(0), ...
%             'OneShot', uint32(0), ...
%             'Edge', uint32(0) ...
%     )), ...
%     'CCUpdate', py.dict(pyargs( ...
%             'Enable', uint32(0), ...
%             'Source', uint32(0), ...
%             'TUSERBit', uint32(0), ...
%             'OneShot', uint32(0), ...
%             'Edge', uint32(0) ...
%     )) ...
% ));

TriggerCfg = MIX.mix.XDfeMix_GetTriggersCfg(device_id)
%Python dictionary can be converted to matlab structure as below
TriggerCfg_m = struct(TriggerCfg)

%%%%%% XDfeMix_GetDUCDDCStatus
%Description:
%   Gets DUC/DDC status for a specified CCID.
%C header declaration:
%   void XDfeMix_GetDUCDDCStatus(const XDfeMix *InstancePtr, u32 CCID, XDfeMix_DUCDDCStatus *DUCDDCStatus);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   DUCDDCStatus: DUC/DDC status container.

%%% DUCDDCStatus python dictionary
%typedef struct {
%	u32 RealOverflowStage; /**< [0-3] First stage in which overflow
%		in real data has occurred. */
%	u32 ImagOverflowStage; /**< [0-3] First stage in which overflow
%		in imaginary data has occurred. */
%	u32 FirstAntennaOverflowing; /**< [0-7] Lowest antenna in which
%		overflow has occurred. */
%	u32 FirstCCIDOverflowing; /**< [0-7] Lowest CCID in which overflow has
%		occurred. */
%} XDfeMix_DUCDDCStatus;

% DUCDDCStatus = py.dict(pyargs('RealOverflowStage', uint32(0), ...
%                               'ImagOverflowStage',uint32(0), ...
%                               'FirstAntennaOverflowing', uint32(0), ...
%                               'FirstCCIDOverflowing', uint32(0)))

DUCDDCStatus = MIX.mix.XDfeMix_GetDUCDDCStatus(device_id, uint32(0))
%Python dictionary can be converted to matlab structure as below
DUCDDCStatus_m = struct(DUCDDCStatus)

%%%%%% XDfeMix_GetMixerStatus
%Description:
%   Gets Mixer status for a specified CCID.
%C header declaration:
%   void XDfeMix_GetMixerStatus(const XDfeMix *InstancePtr, u32 CCID,
%   XDfeMix_MixerStatus *MixerStatus);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   DUCDDCStatus: DUC/DDC status container.

%typedef struct {
%	u32 AdderStage; /**< [0,1] First adder stage in which overflow in real
%		or imaginary data has occurred. */
%	u32 AdderAntenna; /**< [0-7] Lowest antenna in which overflow has
%		occurred. */
%	u32 MixCCID; /**< [0-7] Lowest CCID on which overflow has occurred
%		in mixer. */
%	u32 MixAntenna; /**< [0-7] Lowest antenna in which overflow has
%		occurred. */
%} XDfeMix_MixerStatus;
% MixerStatus = py.dict(pyargs('AdderStage', uint32(0), ...
%                              'AdderAntenna',uint32(0), ...
%                              'MixCCID', uint32(0), ...
%                              'MixAntenna', uint32(0)))
MixerStatus = MIX.mix.XDfeMix_GetMixerStatus(device_id, uint32(0))

%%%%%% XDfeMix_GetInterruptMask
%Description:
%   Gets interrupt mask status.
%C header declaration:
%   void XDfeMix_GetInterruptMask(const XDfeMix *InstancePtr,
%   XDfeMix_InterruptMask *Mask);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   Mask: interrupt masks container.

%%% XDfeMix_InterruptMask python dictionary
%typedef struct {
%	u32 DUCDDCOverflow; /**< [0,1] Mask overflow in DUC/DDC */
%	u32 MixerOverflow; /**< [0,1] Mask overflow in mixer */
%	u32 DLCCUpdate; /**< [0,1] Mask downlink update interrupt */
%	u32 DLCCSequenceError; /**< [0,1] Mask downlink sequence error */
%	u32 ULCCUpdate; /**< [0,1] Mask uplink update interrupt */
%	u32 ULCCSequenceError; /**< [0,1] Mask uplink sequence error */
%} XDfeMix_InterruptMask;

% Flags = py.dict(pyargs('DUCDDCOverflow', uint32(0), ...
%                        'MixerOverflow',uint32(0), ...
%                        'DLCCUpdate', uint32(0), ...
%                        'DLCCSequenceError',uint32(0), ...
%                        'ULCCUpdate', uint32(0), ...
%                        'ULCCSequenceError', uint32(0)))
Flags = MIX.mix.XDfeMix_GetInterruptMask(device_id)

%%%%%% XDfeMix_SetInterruptMask
%Description:
%   Sets interrupt mask.
%C header declaration:
%   void XDfeMix_SetInterruptMask(const XDfeMix *InstancePtr,
%   const XDfeMix_InterruptMask *Mask);
%Input Arguments:
%   device_id: id of the opened device.
%   Mask: interrupt masks flags container.
%         0 - does not mask corresponding interrupt
%         1 - masks corresponding interrupt
%Return:
%   None

%%% XDfeMix_InterruptMask python dictionary
%typedef struct {
%	u32 DUCDDCOverflow; /**< [0,1] Mask overflow in DUC/DDC */
%	u32 MixerOverflow; /**< [0,1] Mask overflow in mixer */
%	u32 DLCCUpdate; /**< [0,1] Mask downlink update interrupt */
%	u32 DLCCSequenceError; /**< [0,1] Mask downlink sequence error */
%	u32 ULCCUpdate; /**< [0,1] Mask uplink update interrupt */
%	u32 ULCCSequenceError; /**< [0,1] Mask uplink sequence error */
%} XDfeMix_InterruptMask;

% InterruptMask_in = py.dict(pyargs('DUCDDCOverflow', uint32(0), ...
%                        'MixerOverflow',uint32(0), ...
%                        'DLCCUpdate', uint32(0), ...
%                        'DLCCSequenceError',uint32(0), ...
%                        'ULCCUpdate', uint32(0), ...
%                        'ULCCSequenceError', uint32(0)))
InterruptMask_in = MIX.mix.GetStruct_XDfeMix_InterruptMask()
Flags = MIX.mix.XDfeMix_SetInterruptMask(device_id, InterruptMask_in)

%%%%%% XDfeMix_GetVersions
%Description:
%   Deactivates Mixer and moves the state machine to Initialised state.
%C header declaration:
%   void XDfeMix_GetVersions(const XDfeMix *InstancePtr, XDfeMix_Version *SwVersion,
%	XDfeMix_Version *HwVersion);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   SwVersion: driver version numbers.
%   HwVersion: HW version numbers.

%SwVersion_in = {
%    "Major": 0,
%    "Minor": 0,
%    "Revision": 0,
%    "Patch": 0,
%}
%HwVersion_in = {
%    "Major": 0,
%    "Minor": 0,
%    "Revision": 0,
%    "Patch": 0,
%}
% SwVersion_in = py.dict(pyargs('Major', uint32(0), ...
%                               'Minor', uint32(0), ...
%                               'Revision', uint32(0), ...
%                               'Patch', uint32(0)));
% HwVersion_in = py.dict(pyargs('Major', uint32(0), ...
%                               'Minor', uint32(0), ...
%                               'Revision', uint32(0), ...
%                               'Patch', uint32(0)));
Version = MIX.mix.XDfeMix_GetVersions(device_id)
Version = cell(Version)
celldisp(Version)
