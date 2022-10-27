%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
% SPDX-License-Identifier: BSD-3-Clause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Put the path of the python module here. It can be in any drive
current_folder = pwd;
if count(py.sys.path,current_folder) == 0
    %Put the path of the python module here. It can be in any drive
    insert(py.sys.path,uint32(0),current_folder);
end

%Import the python module in matlab
RFCLK=py.importlib.import_module('rfclk_client');
RFCLK=py.importlib.reload(RFCLK);

% SetIpAndPort
RFCLK.rfclk.SetIpAndPort("169.254.10.2", "9090")

%GetPythonLogLevels
PythonLogLevels = RFCLK.rfclk.GetPythonLogLevels()

%SetClientLogLevel
RFCLK.rfclk.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%SetServerLogLevel
RFCLK.rfclk.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%SetMetalLogLevel
metal_log_level = RFCLK.rfclk.GetEnum_metal_log_level()
RFCLK.rfclk.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

% XRFClk_Init
ret = RFCLK.rfclk.XRFClk_Init(uint32(486))

% XRFClk_ResetChip
ret = RFCLK.rfclk.XRFClk_ResetChip(uint32(0))

% XRFClk_SetConfigOnOneChipFromConfigId
ret = RFCLK.rfclk.XRFClk_SetConfigOnOneChipFromConfigId(uint32(0), uint32(0))

% XRFClk_GetConfigFromOneChip
ret = RFCLK.rfclk.XRFClk_GetConfigFromOneChip(uint32(0))

% XRFClk_SetConfigOnAllChipsFromConfigId
ret = RFCLK.rfclk.XRFClk_SetConfigOnAllChipsFromConfigId(uint32(0), uint32(0), uint32(0))

% XRFClk_WriteReg
ret = RFCLK.rfclk.XRFClk_WriteReg(uint32(0), uint32(0))

% XRFClk_ReadReg
DataVal = RFCLK.rfclk.XRFClk_ReadReg(uint32(0))
