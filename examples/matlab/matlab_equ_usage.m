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
EQU=py.importlib.import_module('equ_client');
EQU=py.importlib.reload(EQU);

%%%%%% SetIPAndPort
%Input Arguments:
%    arg1: ipaddress of server
%    arg2: port number at server for pyro communication
%Return: None
EQU.equ.SetIpAndPort("169.254.10.2", "9090")

%%%%%% GetPythonLogLevels
%Description:
%   Return the logging levels supported by logging library in python
%Input Arguments:
%   None
%Return:
%   return: Dictionary showing the log levels supported by logging library

PythonLogLevels = EQU.equ.GetPythonLogLevels()

%%%%%% SetServerLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%   PythonLogLevel: Log level to set
%Return:
%   None
EQU.equ.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% SetClientLogLevel
%Input Arguments:
%    arg1: PythonLogLevelsEnum
%Return: None
EQU.equ.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%%%%%% GetEnum_metal_log_level
%Description:
%    Return Dictionary equivalent of enum metal_log_level
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of enum metal_log_level

metal_log_level = EQU.equ.GetEnum_metal_log_level()

%%%%% SetMetalLogLevel
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   MetalLogLevel: Log level to set
%Return:
%   None

EQU.equ.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

%%%%%% GetEnum_XDfeEqu_StateId
%Description:
%   Return Dictionary equivalent of enum XDfeEqu_StateId
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of enum XDfeEqu_StateId

XDfeEqu_StateId = EQU.equ.GetEnum_XDfeEqu_StateId()

%%%%%% XDfeEqu_InstanceInit
%Description:
%   API initialises one instance of an Equalizer driver.
%   Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
%   EQU device with the name DeviceNodeName. The first available slot in
%   the instances array XDfeEqu_ChFilter[] will be taken as a DeviceNodeName
%   object. On success it moves the state machine to a Ready state, while on
%   failure stays in a Not Ready state.
%C header declaration:
%   XDfeEqu *XDfeEqu_InstanceInit(const char *DeviceNodeName);
%Input Arguments:
%   DeviceNodeName: device node name.
%Return:
%   ret: 0 on success, 1 on failure
%   device_id: integer handle to initialized instance
%   DeviceNodeNameRet: device node name returned from driver
%                      which will be same as the passed value
%Note:
%   The bytes conversion is already done inside xpyro client.

str = "a6080000.xdfe_equalizer"
ret = EQU.equ.XDfeEqu_InstanceInit(str)
device_id = ret{2}
S= cell(ret)

%%%%%% XDfeEqu_WriteReg
%Description:
%   Writes value to register in an Equalizer instance.
%C header declaration:
%   void XDfeEqu_WriteReg(const XDfeEqu *InstancePtr, u32 AddrOffset, u32 Data);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%   Data: is value to be written.
%Return:
%   None

EQU.equ.XDfeEqu_WriteReg(device_id, uint32(0), uint32(0))

%%%%%% XDfeEqu_ReadReg
%Description:
%   Reads a value from the register using an Equalizer instance.
%C header declaration:
%   u32 XDfeEqu_ReadReg(const XDfeEqu *InstancePtr, u32 AddrOffset);
%Input Arguments:
%   device_id: id of the opened device.
%   AddrOffset: is address offset relative to instance base address.
%Return:
%   return: Register value.

ret = EQU.equ.XDfeEqu_ReadReg(device_id, uint32(0))

%%%%%% XDfeEqu_Reset
%Description:
%   Resets Equalizer and puts block into a reset state.
%C header declaration:
%   void XDfeEqu_Reset(XDfeEqu *InstancePtr);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   None

EQU.equ.XDfeEqu_Reset(device_id)

%%%%%% XDfeEqu_Configure
%Description:
%   Reads configuration from device tree/xparameters.h and IP registers.
%   Removes S/W reset and moves the state machine to a Configured state.
%C header declaration:
%   void XDfeEqu_Configure(XDfeEqu *InstancePtr, XDfeEqu_Cfg *Cfg);
%Input Arguments:
%   device_id: id of the opened device.
%   Cfg: device config container.
%Return:
%   Cfg: device config container.

%%% XDfeEqu_Cfg python dictionary
%typedef struct {
%	u32 Major; /**< Major version number */
%	u32 Minor; /**< Minor version number */
%	u32 Revision; /**< Revision number */
%	u32 Patch; /**< Patch number */
%} XDfeEqu_Version;

%typedef struct {
%	u32 NumChannels;
%	u32 SampleWidth;
%	u32 ComplexModel;
%	u32 TuserWidth;
%} XDfeEqu_ModelParameters;

%typedef struct {
%	XDfeEqu_Version Version; /**< Logicore version */
%	XDfeEqu_ModelParameters ModelParams; /**< Logicore
%		parameterization */
%} XDfeEqu_Cfg;

% Cfg = py.dict(pyargs( ...
%     'Version', py.dict(pyargs( ...
%         'Major', uint32(0), ...
%         'Minor', uint32(0), ...
%         'Revision', uint32(0), ...
%         'Patch', uint32(0) ...
%     )), ...
%     'ModelParams', py.dict(pyargs( ...
%         'NumChannels', uint32(0), ...
%         'SampleWidth', uint32(0), ...
%         'ComplexModel', uint32(0), ...
%         'TuserWidth', uint32(0) ...
%     )) ...
% ));
Cfg = EQU.equ.GetStruct_XDfeEqu_Cfg()
Cfg = EQU.equ.XDfeEqu_Configure(device_id, Cfg)

%%%%%% XDfeEqu_Initialize
%Description:
%   DFE Equalizer driver one time initialisation and moves the state machine to
%   an Initialised state.
%C header declaration:
%   void XDfeEqu_Initialize(XDfeEqu *InstancePtr, const XDfeEqu_EqConfig *Config);
%Input Arguments:
%   device_id: id of the opened device.
%   Config: configuration data container.
%Return:
%   Config: configuration data container.

%typedef struct {
%	u32 Flush; /**< [0,1] Set high to flush the buffers */
%	u32 DatapathMode; /**< [real, complex, matrix]
%		Set depending on whether the equalizer is running in real,
%		complex or matrix mode.
%		Each of the 8 channels consists of 2 sub-channels (shown in
%		figure below in xDFEEqualizerCoefficientsT description).
%		In complex and matrix modes the 2 sub-channels form a single
%		filter channel acting on the real and imaginary parts of the
%		data.
%		In real mode the 2 sub-channels act as independent filter
%		channels acting on the 2 real samples at the input. */
%	u32 RealDatapathSet; /**< [0-3] Co-efficient set to use for real
%		datapath (Ha and Hb in complex and matrix mode. Ha, Hb, Hc
%		and Hd in real mode). In complex mode the datapath set is
%		limited to 0 or 2. */
%	u32 ImDatapathSet; /**< [0-3] Matrix mode only. Co-efficient set to use
%		for imaginary datapath (Hc and Hd). */
%} XDfeEqu_EqConfig;
% EqConfig = py.dict(pyargs('Flush', uint32(0), ...
%                           'DatapathMode',uint32(0), ...
%                           'RealDatapathSet', uint32(0), ...
%                           'ImDatapathSet', uint32(0)))
EqConfig = EQU.equ.GetStruct_XDfeEqu_EqConfig()
EqConfig = EQU.equ.XDfeEqu_Initialize(device_id, EqConfig)

%%%%%% XDfeEqu_SetTriggersCfg
%Description:
%   Set trigger configuration.
%C header declaration:
%   void XDfeEqu_SetTriggersCfg(const XDfeMix *InstancePtr, XDfeEqu_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%   TriggerCfg: is a trigger configuration container.
%Return:
%   TriggerCfg: is a triggger configuration container.

% typedef struct {
% 	u32 Enable; /**< [0,1], 0 = Disabled: Trigger disabled;
% 		1 = Enabled: Trigger enabled */
% 	u32 Source; /**< [0,1,2],
% 		0 = IMMEDIATE: write to the trigger configuration register
% 			immediately
% 		1 = TUSER: write on Edge detected on specified TUSER bit
% 		2 = TLAST: write on Edge detected on TLAST */
% 	u32 TUSERBit; /**< [0-7], Species which TUSER bit is used by
% 		the trigger */
% 	u32 Edge; /**< [0,1,2], 0 = Rising; 1 = Falling; 2 = Both */
% 	u32 OneShot; /**< [0,1],
% 		0 = Continuous: Once enabled trigger repeats continuously
% 		1 = OneShot: Once enabled trigger occurs once and then
% 			disables */
% } XDfeEqu_Trigger;
%
% typedef struct {
% 	XDfeEqu_Trigger Activate; /**< Toggle between "Initialized",
% 		ultra-low power state, and "Operational". One-shot trigger,
% 		disabled following a single event */
% 	XDfeEqu_Trigger LowPower; /**< Toggle between "Low-power"
% 		and "Operational" state */
% } XDfeEqu_TriggerCfg;

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
%     )) ...
% ));
TriggerCfg = EQU.equ.GetStruct_XDfeEqu_TriggerCfg()
TriggerCfg = EQU.equ.XDfeEqu_SetTriggersCfg(device_id, TriggerCfg)

%%%%% XDfeEqu_SetTUserDelay
%Description:
%   Sets the delay, which will be added to TUSER and TLAST (delay matched
%   through the IP).
%C header declaration:
%   void XDfeEqu_SetTUserDelay(const XDfeEqu *InstancePtr, u32 Delay);
%Input Arguments:
%   device_id: id of the opened device.
%   Delay: requested delay variable.
%Return:
%   None

EQU.equ.XDfeEqu_SetTUserDelay(device_id, uint32(0))

%%%%%% XDfeEqu_Activate
%Description:
%   Activates channel Equalizer moves the state machine to an Activated state.
%C header declaration:
%   void XDfeEqu_Activate(XDfeEqu *InstancePtr, bool EnableLowPower);
%Input Arguments:
%   device_id: id of the opened device.
%   EnableLowPower: flag indicating low power.
%Return:
%   None

EQU.equ.XDfeEqu_Activate(device_id, uint32(0))

%%%%%% XDfeEqu_Update
%Description:
%   Return Dictionary equivalent of structure XDfeEqu_EqConfig
%C header declaration:
%   void XDfeEqu_Update(const XDfeEqu *InstancePtr, const XDfeEqu_EqConfig *Config);
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XDfeEqu_Coefficients

%typedef struct {
%	u32 Flush; /**< [0,1] Set high to flush the buffers */
%	u32 DatapathMode; /**< [real, complex, matrix]
%		Set depending on whether the equalizer is running in real,
%		complex or matrix mode.
%		Each of the 8 channels consists of 2 sub-channels (shown in
%		figure below in xDFEEqualizerCoefficientsT description).
%		In complex and matrix modes the 2 sub-channels form a single
%		filter channel acting on the real and imaginary parts of the
%		data.
%		In real mode the 2 sub-channels act as independent filter
%		channels acting on the 2 real samples at the input. */
%	u32 RealDatapathSet; /**< [0-3] Co-efficient set to use for real
%		datapath (Ha and Hb in complex and matrix mode. Ha, Hb, Hc
%		and Hd in real mode). In complex mode the datapath set is
%		limited to 0 or 2. */
%	u32 ImDatapathSet; /**< [0-3] Matrix mode only. Co-efficient set to use
%		for imaginary datapath (Hc and Hd). */
%} XDfeEqu_EqConfig;
% EqConfig = py.dict(pyargs('Flush', uint32(0), ...
%                           'DatapathMode',uint32(0), ...
%                           'RealDatapathSet', uint32(0), ...
%                           'ImDatapathSet', uint32(0)))
EqConfig = EQU.equ.GetStruct_XDfeEqu_EqConfig()
EqConfig = EQU.equ.XDfeEqu_Update(device_id, EqConfig)

%%%%%% XDfeEqu_GetTriggersCfg
%Description:
%   Returns current trigger configuration.
%C header declaration:
%   void XDfeEqu_GetTriggersCfg(const XDfeEqu *InstancePtr,
%   XDfeEqu_TriggerCfg *TriggerCfg);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   TriggerCfg: is a trigger configuration container.

% typedef struct {
% 	u32 Enable; /**< [0,1], 0 = Disabled: Trigger disabled;
% 		1 = Enabled: Trigger enabled */
% 	u32 Source; /**< [0,1,2],
% 		0 = IMMEDIATE: write to the trigger configuration register
% 			immediately
% 		1 = TUSER: write on Edge detected on specified TUSER bit
% 		2 = TLAST: write on Edge detected on TLAST */
% 	u32 TUSERBit; /**< [0-7], Species which TUSER bit is used by
% 		the trigger */
% 	u32 Edge; /**< [0,1,2], 0 = Rising; 1 = Falling; 2 = Both */
% 	u32 OneShot; /**< [0,1],
% 		0 = Continuous: Once enabled trigger repeats continuously
% 		1 = OneShot: Once enabled trigger occurs once and then
% 			disables */
% } XDfeEqu_Trigger;
%
% typedef struct {
% 	XDfeEqu_Trigger Activate; /**< Toggle between "Initialized",
% 		ultra-low power state, and "Operational". One-shot trigger,
% 		disabled following a single event */
% 	XDfeEqu_Trigger LowPower; /**< Toggle between "Low-power"
% 		and "Operational" state */
% } XDfeEqu_TriggerCfg;

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
%     )) ...
% ));

TriggerCfg = EQU.equ.XDfeEqu_GetTriggersCfg(device_id)


%%%%%% XDfeEqu_LoadCoefficients
%Description:
%   Sets Equalizer filter coefficients in Real, Complex or Matrix mode.
%C header declaration:
%   void XDfeEqu_LoadCoefficients(const XDfeEqu *InstancePtr, u32 ChannelField,
%	u32 Mode, const XDfeEqu_Coefficients *EqCoeffs);
%Input Arguments:
%   device_id: id of the opened device.
%   ChannelField: is a flag in which bits indicate the channel is enabled.
%   Mode: is an equalizer mode.
%   Shift: is a coefficient shift value.
%   EqCoeffs: is equalizer coefficients container.
%Return:
%   EqCoeffs: is equalizer coefficients container.

%typedef struct {
%	u32 Num; /**< [1-6] Number of active units. 1 - 6 in real mode.
%		1 - 3 in complex and matrix mode. */
%	u32 Set; /**< [0-3] Co-efficient set that the co-efficients apply to */
%	s16 Coefficients[24]; /**< Signed real numbers. Array of
%		Co-efficients */
%} XDfeEqu_Coefficients;
Equ_Coeff = py.dict(pyargs('Num', uint32(1), ...
                           'Set', uint32(3), ...
                           'Coefficients', py.list({int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(32767), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0), ...
                                                    int16(0)}) ...
					))

Equ_Coeff = EQU.equ.XDfeEqu_LoadCoefficients(device_id, ...
                          uint32(0), uint32(0), uint32(8), Equ_Coeff);

%%%%%% XDfeEqu_GetEventStatus
%Description:
%   Gets Equalizer event status
%C header declaration:
%   void XDfeEqu_GetEventStatus(const XDfeEqu *InstancePtr, XDfeEqu_Status *Status);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   Status: event status

Status = EQU.equ.XDfeEqu_GetEventStatus(device_id)

%%%%%% XDfeEqu_ClearEventStatus
%Description:
%   Clears Equalizer status. The channel status will be cleared for any
%   IStatus or QStatus not equal 0.
%C header declaration:
%   void XDfeEqu_ClearEventStatus(const XDfeEqu *InstancePtr,
%	const XDfeEqu_Status *Status);
%Input Arguments:
%   device_id: id of the opened device.
%   Status: event status.
%Return:
%   None
EQU.equ.XDfeEqu_ClearEventStatus(device_id, Status)

%%%%%% XDfeEqu_SetInterruptMask
%Description:
%   Enables an Equalizer status for channel ID.
%C header declaration:
%   void XDfeEqu_SetInterruptMask(const XDfeEqu *InstancePtr,
%	const XDfeEqu_InterruptMask *InterruptMask);
%Input Arguments:
%   device_id: id of the opened device.
%   InterruptMask: interrupt mask value
%Return:
%   None

Mask = EQU.equ.GetStruct_XDfeEqu_InterruptMask()
Mask = EQU.equ.XDfeEqu_SetInterruptMask(device_id, Mask)

%%%%%% XDfeEqu_GetActiveSets
%Description:
%   Gets used coefficients settings.
%C header declaration:
%   void XDfeEqu_GetActiveSets(const XDfeEqu *InstancePtr, u32 *RealSet,
%   u32 *ImagSet);
%Input Arguments:
%   device_id: id of the opened device.
%Return:
%   RealSet: Real value
%   ImagSet: Imaginary value

%%% CarrierCfg python dictionary

ret = EQU.equ.XDfeEqu_GetActiveSets(device_id)

%%%%%% XDfeEqu_GetVersions
%Description:
%   This API is used to get the driver version.
%C header declaration:
%   void XDfeEqu_GetVersions(const XDfeMix *InstancePtr,
%   XDfeEqu_Version *SwVersion, XDfeEqu_Version *HwVersion);
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
Version = EQU.equ.XDfeEqu_GetVersions(device_id)
Version = cell(Version)
celldisp(Version)
