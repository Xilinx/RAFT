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
CCF=py.importlib.import_module('ccf_client');
CCF=py.importlib.reload(CCF);

%%%%%% SetIPAndPort
%Input Arguments:
%    arg1: ipaddress of server
%    arg2: port number at server for pyro communication
%Return: None
CCF.ccf.SetIpAndPort("169.254.10.2", "9090")

%GetPythonLogLevels
%Description:
%   Return the logging levels supported by logging library in python
%Input Arguments:
%   None
%Return:
%   Dictionary showing the log levels supported by logging library
PythonLogLevels = CCF.ccf.GetPythonLogLevels()

%SetServerLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None
CCF.ccf.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% SetClientLogLevel
%Input Arguments:
%    arg1: PythonLogLevelsEnum
%Return: None
CCF.ccf.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%metal_log_level
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None
metal_log_level = CCF.ccf.GetEnum_metal_log_level()

%SetMetalLogLevel
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   Log level to set
%Return:
%   None
CCF.ccf.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

%GetEnum_XDfeCcf_StateId
%Description:
%   Return Dictionary equivalent of enum XDfeCcf_StateId
%Input Arguments:
%   None
%Return:
%   Dictionary equivalent of enum XDfeCcf_StateId
XDfeCcf_StateId = CCF.ccf.GetEnum_XDfeCcf_StateId()

%GetStruct_XDfeCcf_InternalCarrierCfg
%Description:
%   Return Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
%Input Arguments:
%   None
%Return:
%   Dictionary equivalent of structure XDfeCcf_InternalCarrierCfg
XDfeCcf_InternalCarrierCfg = CCF.ccf.GetStruct_XDfeCcf_InternalCarrierCfg()

%XDfeCcf_InstanceInit
%Description:
%   Initialises one instance of a channel filter driver.
%   Traverses "/sys/bus/platform/device" directory (in Linux), to find registered
%   CCF device with the name DeviceNodeName. The first available slot in
%   the instances array XDfeCcf_ChFilter[] will be taken as a DeviceNodeName
%   object. On success it moves the state machine to a Ready state, while on
%   failure stays in a Not Ready state.
%C header declaration:
%   XDfeCcf *XDfeCcf_InstanceInit(const char *DeviceNodeName);
%Input Arguments:
%   DeviceNodeName: device node name.
%Return:
%   ret - 0 on success, 1 on failure
%   device_id - integer handle to the initialized instance
%   DeviceNodeNameRet - device node name returned from driver
%                       which will be same as the passed value
%Notes:
%   The bytes conversion is already done inside xpyro client.

str = "a7c00000.xdfe_cc_filter"
ret = CCF.ccf.XDfeCcf_InstanceInit(str)
S= cell(ret)
ret{2}
device_id = ret{2}

%GetStruct_XDfeCcf_Version()
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Version
Version_struct = CCF.ccf.GetStruct_XDfeCcf_Version()

%GetStruct_XDfeCcf_Trigger
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Trigger
TriggerStruct = CCF.ccf.GetStruct_XDfeCcf_Trigger()

%GetStruct_XDfeCcf_CCSequence
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_CCSequence
CCSequenceStruct = CCF.ccf.GetStruct_XDfeCcf_CCSequence()

%GetStruct_XDfeCcf_ModelParameters
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_ModelParameters
ModelParamStruct = CCF.ccf.GetStruct_XDfeCcf_ModelParameters()

%GetStruct_XDfeCcf_CCCfg
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_CCCfg
CCCfgStruct = CCF.ccf.GetStruct_XDfeCcf_CCCfg()

%GetStruct_XDfeCcf_Cfg
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Cfg
Cfg =CCF.ccf.GetStruct_XDfeCcf_Cfg()

%GetStruct_XDfeCcf_Config
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Config
ConfigStruct = CCF.ccf.GetStruct_XDfeCcf_Config

%GetStruct_XDfeCcf_InterruptMask
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_InterruptMask
MaskStruct = CCF.ccf.GetStruct_XDfeCcf_InterruptMask()

%GetStruct_XDfeCcf_Coefficients
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Coefficients
Coeffs_in = CCF.ccf.GetStruct_XDfeCcf_Coefficients()

%XDfeCcf_WriteReg
%Description:
%   Writes value to register in a Ccf instance.
%C header declaration:
%   void XDfeCcf_WriteReg(const XDfeCcf *InstancePtr, u32 AddrOffset, u32 Data);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: address offset relative to instance base address.
%   Data: value to be written.
%Return:
%   None

CCF.ccf.XDfeCcf_WriteReg(device_id, uint32(0), uint32(0))

%XDfeCcf_ReadReg
%Description:
%   Reads a value from register using a Ccf instance.
%C header declaration:
%   u32 XDfeCcf_ReadReg(const XDfeCcf *InstancePtr, u32 AddrOffset);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: address offset relative to instance base address
%Return:
%   regval: Register value.

ret = CCF.ccf.XDfeCcf_ReadReg(device_id, uint32(0))

%XDfeCcf_Reset
%Description:
%   Resets channel filter and puts block into a reset state.
%C header declaration:
%   void XDfeCcf_Reset(XDfeCcf *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

CCF.ccf.XDfeCcf_Reset(device_id)

%XDfeCcf_Configure
%Description:
%   Read configuration from device tree/xparameters.h and IP registers.
%   Removes S/W reset and moves the state machine to a Configured state.
%C header declaration:
%   void XDfeCcf_Configure(XDfeCcf *InstancePtr, XDfeCcf_Cfg *Cfg);
%Input Arguments:
%   device_id: id of the opened device.
%   Cfg: configuration data container
%Return:
%   Cfg: configuration data container

%%% config python dictionary
%typedef struct {
%   u32 Major; /**< Major version number */
%   u32 Minor; /**< Minor version number */
%   u32 Revision; /**< Revision number */
%   u32 Patch; /**< Patch number */
%} XDfeCcf_Version;
%typedef struct {
%   u32 NumAntenna; /**< [1-8] */
%   u32 NumCCPerAntenna; /**< [1-8] */
%   u32 NumAntSlot; /**< [1-8] */
%} XDfeCcf_ModelParameters;
%typedef struct {
%   XDfeCcf_Version Version; /**< Logicore version */
%   XDfeCcf_ModelParameters ModelParams; /**< Logicore
%       parameterization */
%} XDfeCcf_Cfg;

% Cfg = py.dict(pyargs( ...
%    'Version', py.dict(pyargs( ...
%        'Major', uint32(0), ...
%        'Minor', uint32(0), ...
%        'Revision', uint32(0), ...
%        'Patch', uint32(0) ...
%    )), ...
%    'ModelParams', py.dict(pyargs( ...
%        'NumAntenna', uint32(0), ...
%        'NumCCPerAntenna', uint32(0), ...
%        'AntenaInterleave', uint32(0) ...
%    )) ...
%));
Cfg_in =CCF.ccf.GetStruct_XDfeCcf_Cfg()
Cfg = CCF.ccf.XDfeCcf_Configure(device_id, Cfg_in)

%XDfeCcf_Initialize
%Description:
%   DFE Ccf driver one time initialisation, also moves the state machine to
%   an Initialised state.
%C header declaration:
%   void XDfeCcf_Initialize(XDfeCcf *InstancePtr, const XDfeCcf_Init *Init);
%Input Arguments:
%   device_id: id of the opened device.
%   Init: initialisation data container
%Return:
%   Init: initialisation data container


%GetStruct_XDfeCcf_Init
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_Init
%%% Init python dictionary

%typedef struct {
%   XDfeCcf_CCSequence Sequence;
%   u32 GainStage; /**< [0,1] Enable gain stage */
%} XDfeCcf_Init;

Init_in = CCF.ccf.GetStruct_XDfeCcf_Init()
update(Init_in, py.dict(pyargs('Sequence', py.dict((pyargs('Length',int32(6)))))))
Init = CCF.ccf.XDfeCcf_Initialize(device_id, Init_in)

%XDfeCcf_SetTriggersCfg
%Description:
%   Set trigger configuration.
%C header declaration:
%   void XDfeCcf_SetTriggersCfg(const XDfeCcf *InstancePtr, XDfeCcf_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   TriggerCfg: is a trigger configuration container.
%Return:
%   TriggerCfg: is a trigger configuration container.

%GetStruct_XDfeCcf_TriggerCfg
%Input Arguments: None
%Return: Dictionary equivalent of structure XDfeCcf_TriggerCfg

%TriggerCfg python dictionary
% typedef struct {
% 	XDfeCcf_Trigger Activate; /**< Toggle between "Initialized",
% 		ultra-low power state, and "Operational". One-shot trigger,
% 		disabled following a single event */
% 	XDfeCcf_Trigger LowPower; /**< Toggle between "Low-power"
% 		and "Operational" state */
% 	XDfeCcf_Trigger CCUpdate; /**< Transition to next CC
% 		configuration. Will initiate flush based on CC configuration */
% } XDfeCcf_TriggerCfg;
%TriggerCfg = py.dict(pyargs( ...
%    'Activate', py.dict(pyargs( ...
%            'Enable', uint32(1), ...
%            'Source', uint32(1), ...
%            'TUSERBit', uint32(1), ...
%            'OneShot', uint32(1), ...
%            'Edge', uint32(1) ...
%    )), ...
%    'LowPower', py.dict(pyargs( ...
%            'Enable', uint32(1), ...
%            'Source', uint32(2), ...
%            'TUSERBit', uint32(3), ...
%            'OneShot', uint32(4), ...
%            'Edge', uint32(5) ...
%    )), ...
%    'CCUpdate', py.dict(pyargs( ...
%            'Enable', uint32(1), ...
%            'Source', uint32(2), ...
%            'TUSERBit', uint32(3), ...
%            'OneShot', uint32(4), ...
%            'Edge', uint32(5) ...
%    )) ...
%));
TriggerCfg_in = CCF.ccf.GetStruct_XDfeCcf_TriggerCfg()
TriggerCfg = CCF.ccf.XDfeCcf_SetTriggersCfg(device_id, TriggerCfg_in)

%XDfeCcf_Activate
%Description:
%   Activates channel filter and moves the state machine to an Activated state.
%C header declaration:
%   void XDfeCcf_Activate(XDfeCcf *InstancePtr, bool EnableLowPower);
%Input Arguments:
%   device_id: id of the opened device.
%   EnableLowPower: flag indicating low power
%Return:
%   None
CCF.ccf.XDfeCcf_Activate(device_id, uint32(0))

%XDfeCcf_GetCurrentCCCfg
%Description:
%   Returns the current CC configuration. Not used slot ID in a sequence
%   (Sequence.CCID[Index]) are represented as (-1), not the value in registers.
%C header declaration:
%   void XDfeCcf_GetCurrentCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CurrCCCfg: CC configuration container.
%Return:
%   CurrCCCfg: CC configuration container
%Note:
%   For a sequence conversion see XDfeCcf_AddCCtoCCCfg() comment.
CurrCCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
CurrentCCCfg = CCF.ccf.XDfeCcf_GetCurrentCCCfg(device_id, CurrCCCfg)

%XDfeCcf_GetEmptyCCCfg
%Description:
%   Returns configuration structure CCCfg with CCCfg->Sequence.Length value set
%   in XDfeCcf_Configure(), array CCCfg->Sequence.CCID[] members are set to not
%   used value (-1) and the other CCCfg members are set to 0.
%C header declaration:
%   void XDfeCcf_GetEmptyCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   CCCfg: CC configuration container
CCCfg = CCF.ccf.XDfeCcf_GetEmptyCCCfg(device_id)

%XDfeCcf_GetCarrierCfg
%Description:
%   Returns the current CCID carrier configuration.
%C header declaration:
%   void XDfeCcf_GetCarrierCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg,
%	s32 CCID, u32 *CCSeqBitmap, XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.
CCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
ret = CCF.ccf.XDfeCcf_GetCarrierCfg(device_id, CCCfg, uint32(0))

%XDfeCcf_AddCCtoCCCfg
%Description:
%   Adds specified CCID, with specified configuration, to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%
%   The returned CCCfg.Sequence is transleted as there is no explicite indication that
%   SEQUENCE[i] is not used - 0 can define the slot as either used or not used.
%   Sequence data that is returned in the CCIDSequence is not the same as what is
%   written in the registers. The translation is:
%       - CCIDSequence.CCID[i] = -1    - if [i] is unused slot
%       - CCIDSequence.CCID[i] = CCID  - if [i] is used slot
%       - a returned CCIDSequence->Length = length in register + 1
%C header declaration:
%   u32 XDfeCcf_AddCCtoCCCfg(XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg, s32 CCID,
%	u32 CCSeqBitmap, const XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CCSeqBitmap: CC slot position container.
%   CarrierCfg: CC configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CCCfg: component carrier (CC) configuration container.
CCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
CCCfg = CCF.ccf.XDfeCcf_GetCurrentCCCfg(device_id, CCCfg)
CCF.ccf.XDfeCcf_ClearEventStatus(device_id)
CCID = int32(1)
CCSeqBitmap = uint32(2)
CarrierCfg = CCF.ccf.GetStruct_XDfeCcf_CarrierCfg()
ret = CCF.ccf.XDfeCcf_AddCCtoCCCfg(device_id, CCCfg, CCID, CCSeqBitmap, CarrierCfg)

%XDfeCcf_RemoveCCfromCCCfg
%Description:
%   Removes specified CCID from a local CC configuration structure.
%C header declaration:
%   void XDfeCcf_RemoveCCfromCCCfg(XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg, s32 CCID);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%Return:
%   CCCfg: component carrier (CC) configuration container.
%Note:
%   For a sequence conversion see XDfeCcf_AddCCtoCCCfg comment.
CCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
CCCfg = CCF.ccf.XDfeCcf_RemoveCCfromCCCfg(device_id, CCCfg, int32(0))

%XDfeCcf_UpdateCCinCCCfg
%Description:
%   Updates specified CCID, with specified configuration to a local CC
%   configuration structure.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%C header declaration:
%   void XDfeCcf_UpdateCCinCCCfg(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg,
% 	s32 CCID, const XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%   CCID: Channel ID.
%   CarrierCfg: CC configuration container.
%Return:
%   CCCfg: component carrier (CC) configuration container.
CCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
CarrierCfg = CCF.ccf.GetStruct_XDfeCcf_CarrierCfg()
ret = CCF.ccf.XDfeCcf_UpdateCCinCCCfg(device_id, CCCfg, uint32(0), CarrierCfg)

%XDfeCcf_SetNextCCCfgAndTrigger
%Description:
%   Writes local CC configuration to the shadow (NEXT) registers and triggers
%   copying from shadow to operational registers.
%C header declaration:
%   u32 XDfeCcf_SetNextCCCfgAndTrigger(const XDfeCcf *InstancePtr, XDfeCcf_CCCfg *CCCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCCfg: component carrier (CC) configuration container.
%Return:
%   ret: XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CCCfg: component carrier (CC) configuration container.
CCCfg = CCF.ccf.GetStruct_XDfeCcf_CCCfg()
ret = CCF.ccf.XDfeCcf_SetNextCCCfgAndTrigger(device_id, CCCfg)

%XDfeCcf_AddCC
%Description:
%   Adds specified CCID, with specified configuration.
%   If there is insufficient capacity for the new CC the function will return
%   an error.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeCcf_AddCC(const XDfeCcf *InstancePtr, u32 CCID,
%   const XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: Channel ID.
%   CCSeqBitmap: up to 16 defined slots into which a CC can be
%                allocated. The number of slots can be from 1 to 16 depending on
%                system initialization. The number of slots is defined by the
%                "sequence length" parameter which is provided during initialization.
%                The Bit offset within the CCSeqBitmap indicates the equivalent
%                Slot number to allocate. e.g. 0x0003  means the caller wants the
%                passed component carrier (CC) to be allocated to slots 0 and 1.
%   CarrierCfg: is a CC configuration container.
%Return:
%   XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CarrierCfg: is a CC configuration container.

%%% CarrierCfg python dictionary
%typedef struct {
%   u32 Enable; /**< [0,1] (Private) Enable/Disable CC while still
%           reserving its slot in the TDM - set by helper functions
%           when building the configuration the TDM */
%   u32 Flush; /**< [0,1] (Private) Indicate CC should be flush following
%           configuration update - set by helper functions when
%           building the configuration channel_id? */
%   u32 MappedId; /**< [0-7] (Private) Defines the hardblock ID value to be
%           used for the CC. Used to map arbitary/system CCID
%           values to available hard block TID values. Enumerated
%           incrementally from 0 to max supported CC for a given
%           IP configuration */
%   u32 Rate; /**< [1,2,4,8] Sample "rate" (period) of CC */
%   u32 Gain; /**< [0-(1<<16)-1] Gain setting for this CC */
%   u32 ImagCoeffSet; /**< [0-7] Identify the coefficient set for the
%                   complex data on this CC */
%   u32 RealCoeffSet; /**< [0-7] Identify the coefficient set for the real
%                data on this CC */
%} XDfeCcf_CarrierCfg;
% CarrierCfg = py.dict(pyargs('Enable', uint32(0), ...
%                             'Flush',uint32(0), ...
%                             'MappedId', uint32(0),...
%                             'Rate', uint32(0), ...
%                             'Gain',uint32(0), ...
%                             'ImagCoeffSet', uint32(0), ...
%                             'RealCoeffSet', uint32(0)));
bitsequence = 0xb
CarrierCfg_in = CCF.ccf.GetStruct_XDfeCcf_CarrierCfg()
ret = CCF.ccf.XDfeCcf_AddCC(device_id,uint32(0),bitsequence,CarrierCfg_in)

%XDfeCcf_RemoveCC
%Description:
%   Removes specified CCID.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeCcf_RemoveCC(const XDfeCcf *InstancePtr, u32 CCID);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   XST_SUCCESS if successful, XST_FAILURE if error occurs.
%Note:
%   Clear event status with XDfeCcf_ClearEventStatus() before running this API.
ret = CCF.ccf.XDfeCcf_RemoveCC(device_id, uint32(0));

%XDfeCcf_UpdateCC
%Description:
%   Updates specified CCID carrier configuration; change gain or filter
%   coefficients set.
%   Initiates CC update (enable CCUpdate trigger TUSER Single Shot).
%C header declaration:
%   u32 XDfeCcf_UpdateCC(const XDfeCcf *InstancePtr, u32 CCID,
%   XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%   CarrierCfg: is a CC configuration container.
%Return:
%   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
%   CarrierCfg - CC configuration container
%%% CarrierCfg python dictionary
%typedef struct {
%   u32 Enable; /**< [0,1] (Private) Enable/Disable CC while still
%           reserving its slot in the TDM - set by helper functions
%           when building the configuration the TDM */
%   u32 Flush; /**< [0,1] (Private) Indicate CC should be flush following
%           configuration update - set by helper functions when
%           building the configuration channel_id? */
%   u32 MappedId; /**< [0-7] (Private) Defines the hardblock ID value to be
%           used for the CC. Used to map arbitary/system CCID
%           values to available hard block TID values. Enumerated
%           incrementally from 0 to max supported CC for a given
%           IP configuration */
%   u32 Rate; /**< [1,2,4,8] Sample "rate" (period) of CC */
%   u32 Gain; /**< [0-(1<<16)-1] Gain setting for this CC */
%   u32 ImagCoeffSet; /**< [0-7] Identify the coefficient set for the
%                   complex data on this CC */
%   u32 RealCoeffSet; /**< [0-7] Identify the coefficient set for the real
%                data on this CC */
%} XDfeCcf_CarrierCfg;
% CarrierCfg = py.dict(pyargs('Enable', uint32(0), ...
%                             'Flush',uint32(0), ...
%                             'MappedId', uint32(0),...
%                             'Rate', uint32(0), ...
%                             'Gain',uint32(0), ...
%                             'ImagCoeffSet', uint32(0), ...
%                             'RealCoeffSet', uint32(0)));
CarrierCfg_in = CCF.ccf.GetStruct_XDfeCcf_CarrierCfg()
ret = CCF.ccf.XDfeCcf_UpdateCC(device_id, uint32(0), CarrierCfg_in);
retval = ret{1}
CarrierCfg = ret{2}

%XDfeCcf_UpdateAntenna
%Description:
%   Updates specified antenna TDM slot enablement.
%   Initiates CC update (enable CCUpdate trigger one-shot).
%C header declaration:
%   u32 XDfeCcf_UpdateAntenna(const XDfeCcf *InstancePtr, u32 Ant, bool Enabled);
%Input Arguments:
%   device_id: id of the opened device.
%   Ant: is antenna ID.
%   Enabled: flag indicating enable status of the antenna.
%Return:
%   ret - XST_SUCCESS if successful, XST_FAILURE if error occurs.
%Note:
%   Clear event status with XDfeCcf_ClearEventStatus() before running this API.
ret = CCF.ccf.XDfeCcf_UpdateAntenna(device_id, uint32(0), uint32(0));

%XDfeCcf_GetTriggersCfg
%Description:
%   Return current trigger configuration.
%C header declaration:
%   void XDfeCcf_GetTriggersCfg(const XDfeCcf *InstancePtr,
%	XDfeCcf_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   TriggerCfg: is a trigger configuration container.

%%% TriggerCfg python dictionary
%typedef struct {
%   u32 Enable; /**< [0,1], 0 = Disabled: Trigger disabled;
%       1 = Enabled: Trigger enabled */
%   u32 Source; /**< [0,1,2],
%       0 = IMMEDIATE: write to the trigger configuration register
%                      immediately
%       1 = TUSER: write on Edge detected on specified TUSER bit
%       2 = TLAST: write on Edge detected on TLAST */
%   u32 TUSERBit; /**< [0-7], Species which TUSER bit is used by
%                    the trigger */
%   u32 Edge; /**< [0,1,2], 0 = Rising; 1 = Falling; 2 = Both */
%   u32 OneShot; /**< [0,1],
%       0 = Continuous: Once enabled trigger repeats continuously
%       1 = OneShot: Once enabled trigger occurs once and then
%           disables */
%} XDfeCcf_Trigger;
%typedef struct {
%   XDfeCcf_Trigger Activate; /**< Toggle between "Initialized",
%       ultra-low power state, and "Operational". One-shot trigger,
%       disabled following a single event */
%   XDfeCcf_Trigger LowPower; /**< Toggle between "Low-power"
%       and "Operational" state */
%   XDfeCcf_Trigger CCUpdate; /**< Transition to next CC
%       configuration. Will initiate flush based on CC configuration */
%} XDfeCcf_TriggerCfg;

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

TriggerCfg = CCF.ccf.XDfeCcf_GetTriggersCfg(device_id)
%Python dictionary can be converted to matlab structure as below
TriggerCfg_m = struct(TriggerCfg)

%XDfeCcf_GetCC
%Description:
%   Get specified CCID carrier configuration.
%C header declaration:
%   void XDfeCcf_GetCC(const XDfeCcf *InstancePtr, u32 CCID,
%	XDfeCcf_CarrierCfg *CarrierCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   CCID: is a Channel ID.
%Return:
%   CarrierCfg: is a trigger configuration container.

%%% CarrierCfg python dictionary
%typedef struct {
%   u32 Enable; /**< [0,1] (Private) Enable/Disable CC while still
%           reserving its slot in the TDM - set by helper functions
%           when building the configuration the TDM */
%   u32 Flush; /**< [0,1] (Private) Indicate CC should be flush following
%           configuration update - set by helper functions when
%           building the configuration channel_id? */
%   u32 MappedId; /**< [0-7] (Private) Defines the hardblock ID value to be
%           used for the CC. Used to map arbitary/system CCID
%           values to available hard block TID values. Enumerated
%           incrementally from 0 to max supported CC for a given
%           IP configuration */
%   u32 Rate; /**< [1,2,4,8] Sample "rate" (period) of CC */
%   u32 Gain; /**< [0-(1<<16)-1] Gain setting for this CC */
%   u32 ImagCoeffSet; /**< [0-7] Identify the coefficient set for the
%                   complex data on this CC */
%   u32 RealCoeffSet; /**< [0-7] Identify the coefficient set for the real
%                data on this CC */
%} XDfeCcf_CarrierCfg;
% CarrierCfg = py.dict(pyargs('Enable', uint32(0), ...
%                             'Flush',uint32(0), ...
%                             'MappedId', uint32(0),...
%                             'Rate', uint32(0), ...
%                             'Gain',uint32(0), ...
%                             'ImagCoeffSet', uint32(0), ...
%                             'RealCoeffSet', uint32(0)))
CarrierCfg = CCF.ccf.XDfeCcf_GetCC(device_id, uint32(0))
%Python dictionary can be converted to matlab structure as below
CarrierCfg_m = struct(CarrierCfg)

%%%%%% XDfeCcf_GetActiveSets
%Input Arguments:
%    arg1: device_id
%    arg2: IsActive
%Return:
%    Value1: IsActive
% IsActive = py.list({uint32(0), ...
%                     uint32(0), ...
%                     uint32(0), ...
%                     uint32(0), ...
%                     uint32(0), ...
%                     uint32(0), ...
%                     uint32(0), ...
%                     uint32(0)})
IsActive = CCF.ccf.XDfeCcf_GetActiveSets(device_id)

%XDfeCcf_LoadCoefficients
%Description:
%   Writes the coefficient set defined into the register map and commit them
%   to the hard blocks internal coefficient memory for the specified Set.
%C header declaration:
%   void XDfeCcf_LoadCoefficients(const XDfeCcf *InstancePtr, u32 Set, u32 Shift,
%   const XDfeCcf_Coefficients *Coeffs);
%Input Arguments:
%   device_id: id of the opened device.
%   Set: coefficient set Id
%   Shift: is a coefficient shift value.
%   Coeffs: an array of filter coefficients
%Return:
%   Coeffs: an array of filter coefficients.

%%% Filter python dictionary
%typedef struct {
%   u32 Num; /**< [0-(128|256)]. True number of coefficients,
%           when non-symmetric max is 128. */
%   u32 Symmetric; /**< [0,1] Select the use of symetric or non-symetric
%             filter */
%   u32 Value[128]; /**< [Signed real numbers]. Array of coefficients, when
%              symmetric only the first (Num+1)/2 coefficients
%              are provided */
%} XDfeCcf_Coefficients;

%Coeffs_in = py.dict(pyargs('Num', uint32(7), ...
%                           'Symmetric',uint32(1), ...
%                           'Value', py.list({int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(32767), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0), ...
%                                             int16(0)})));
                                         
Coeffs_in = CCF.ccf.GetStruct_XDfeCcf_Coefficients()
update(Coeffs_in, py.dict(pyargs('Num', uint32(7))))
ret = CCF.ccf.XDfeCcf_LoadCoefficients(device_id, uint32(0), ...
                                       uint32(0), Coeffs_in)

%XDfeCcf_GetEventStatus
%Description:
%   Get event status
%C header declaration:
%   void XDfeCcf_GetEventStatus(const XDfeCcf *InstancePtr, XDfeCcf_Status *Status);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   Status: event status
% Status = py.list({uint32(0), ...
%                   uint32(0), ...
%                   uint32(0), ...
%                   uint32(0), ...
%                   uint32(0), ...
%                   uint32(0), ...
%                   uint32(0), ...
%                   uint32(0)})
Status = CCF.ccf.XDfeCcf_GetEventStatus(device_id)

%XDfeCcf_ClearEventStatus
%Description:
%   Clears event status.XDfeCcf_ClearEventStatus
%C header declaration:
%   void XDfeCcf_ClearEventStatus(const XDfeCcf *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%   Status: event status.
%       0 - does not clear corresponding event status
%       1 - clears corresponding event status
%Return:
%   None
CCF.ccf.XDfeCcf_ClearEventStatus(device_id)

%XDfeCcf_SetInterruptMask
%Description:
%   Sets interrupt masks.
%C header declaration:
%   void XDfeCcf_SetInterruptMask(const XDfeCcf *InstancePtr,
%	const XDfeCcf_InterruptMask *Mask);
%Input Arguments:
%   device_id: id of the opened device.
%   Mask: interrupt mask value
%       0 - does not mask corresponding interrupt
%       1 - masks corresponding interrupt
%Return:
%   None

% typedef struct {
% 	u32 Overflow; /**< [0,1] Mask overflow events */
% 	u32 CCUpdate; /**< [0,1] Mask CC update events */
% 	u32 CCSequenceError; /**< [0,1] Mask CC sequence mismatch events */
% } XDfeCcf_InterruptMask;

% Mask = py.dict(pyargs('Overflow', uint32(0), ...
%                      'CCUpdate', uint32(0), ...
%                      'CCSequenceError', uint32(0)));                 
MaskStruct = CCF.ccf.GetStruct_XDfeCcf_InterruptMask()
Mask = CCF.ccf.XDfeCcf_SetInterruptMask(device_id, MaskStruct)

%XDfeCcf_GetVersions
%Description:
%   This API is used to get the driver version.
%C header declaration:
%   void XDfeCcf_GetVersions(const XDfeCcf *InstancePtr, XDfeCcf_Version *SwVersion,
%	XDfeCcf_Version *HwVersion);
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
Version = CCF.ccf.XDfeCcf_GetVersions(device_id)
Version = cell(Version)
celldisp(Version)

%XDfeCcf_Deactivate
%Description:
%   Deactivates channel filter and moves the state machine to Initialised state.
%C header declaration:
%   void XDfeCcf_Deactivate(XDfeCcf *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None
CCF.ccf.XDfeCcf_Deactivate(device_id)

%XDfeCcf_InstanceClose
%Description:
%   Closes the instances of a channel filter driver and moves the state
%   machine to a Not Ready state.
%C header declaration:
%   void XDfeCcf_InstanceClose(XDfeCcf *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None
CCF.ccf.XDfeCcf_InstanceClose(device_id)

