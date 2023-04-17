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
RFDC=py.importlib.import_module('rfdc_client');
RFDC=py.importlib.reload(RFDC);

RFDC.rfdc.SetIpAndPort("169.254.10.2", "9090")

%GetPythonLogLevels
%Description:
%   Get the python log level
%Input Arguments:
%   None
%Return:
%   return: Python Log Level

PythonLogLevels = RFDC.rfdc.GetPythonLogLevels()

%SetClientLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%   PythonLogLevel: Log level to set
%Return:
%   None

RFDC.rfdc.SetClientLogLevel(PythonLogLevels{'DEBUG'})

%SetServerLogLevel
%Description:
%   Set the python log level to the given level
%Input Arguments:
%   PythonLogLevel: Log level to set
%Return:
%   None

RFDC.rfdc.SetServerLogLevel(PythonLogLevels{'DEBUG'})

%SetMetalLogLevel
%Description:
%   Set the metal log level to the given level
%Input Arguments:
%   MetalLogLevel: Log level to set
%Return:
%   None

metal_log_level = RFDC.rfdc.GetEnum_metal_log_level()
RFDC.rfdc.SetMetalLogLevel(metal_log_level{'METAL_LOG_EMERGENCY'})

% XRFdc_PLL_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_PLL_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_PLL_Settings

XRFdc_PLL_Settings = RFDC.rfdc.GetStruct_XRFdc_PLL_Settings()

% XRFdc_Tile_Clock_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Tile_Clock_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Tile_Clock_Settings

XRFdc_Tile_Clock_Settings = RFDC.rfdc.GetStruct_XRFdc_Tile_Clock_Settings()

% XRFdc_Distribution_Info
%Description:
%   Return Dictionary equivalent of structure XRFdc_Distribution_Info
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Distribution_Info

XRFdc_Distribution_Info = RFDC.rfdc.GetStruct_XRFdc_Distribution_Info()

% XRFdc_Distribution_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Distribution_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Distribution_Settings

XRFdc_Distribution_Settings = RFDC.rfdc.GetStruct_XRFdc_Distribution_Settings()

% XRFdc_MTS_DTC_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_MTS_DTC_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_MTS_DTC_Settings

XRFdc_MTS_DTC_Settings = RFDC.rfdc.GetStruct_XRFdc_MTS_DTC_Settings()

% XRFdc_MultiConverter_Sync_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config

XRFdc_MultiConverter_Sync_Config = RFDC.rfdc.GetStruct_XRFdc_MultiConverter_Sync_Config()

% XRFdc_MTS_Marker
%Description:
%   Return Dictionary equivalent of structure XRFdc_MTS_Marker
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_MTS_Marker

XRFdc_MTS_Marker = RFDC.rfdc.GetStruct_XRFdc_MTS_Marker()

% XRFdc_Signal_Detector_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Signal_Detector_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Signal_Detector_Settings

XRFdc_Signal_Detector_Settings = RFDC.rfdc.GetStruct_XRFdc_Signal_Detector_Settings()

% XRFdc_QMC_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_QMC_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_QMC_Settings

XRFdc_QMC_Settings = RFDC.rfdc.GetStruct_XRFdc_QMC_Settings()

% XRFdc_CoarseDelay_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_CoarseDelay_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_CoarseDelay_Settings

XRFdc_CoarseDelay_Settings = RFDC.rfdc.GetStruct_XRFdc_CoarseDelay_Settings()

% XRFdc_Mixer_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Mixer_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Mixer_Settings

XRFdc_Mixer_Settings = RFDC.rfdc.GetStruct_XRFdc_Mixer_Settings()

% XRFdc_Threshold_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Threshold_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Threshold_Settings

XRFdc_Threshold_Settings = RFDC.rfdc.GetStruct_XRFdc_Threshold_Settings()

% XRFdc_Calibration_Coefficients
%Description:
%   Return Dictionary equivalent of structure XRFdc_Calibration_Coefficients
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Calibration_Coefficients

XRFdc_Calibration_Coefficients = RFDC.rfdc.GetStruct_XRFdc_Calibration_Coefficients()

% XRFdc_Pwr_Mode_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings

XRFdc_Pwr_Mode_Settings = RFDC.rfdc.GetStruct_XRFdc_Pwr_Mode_Settings()

% XRFdc_DSA_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_DSA_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DSA_Settings

XRFdc_DSA_Settings = RFDC.rfdc.GetStruct_XRFdc_DSA_Settings()

% XRFdc_Cal_Freeze_Settings
%Description:
%   Return Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings

XRFdc_Cal_Freeze_Settings = RFDC.rfdc.GetStruct_XRFdc_Cal_Freeze_Settings()

% XRFdc_TileStatus
%Description:
%   Return Dictionary equivalent of structure XRFdc_TileStatus
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_TileStatus

XRFdc_TileStatus = RFDC.rfdc.GetStruct_XRFdc_TileStatus()

% XRFdc_IPStatus
%Description:
%   Return Dictionary equivalent of structure XRFdc_IPStatus
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_IPStatus

XRFdc_IPStatus = RFDC.rfdc.GetStruct_XRFdc_IPStatus()

% XRFdc_BlockStatus
%Description:
%   Return Dictionary equivalent of structure XRFdc_BlockStatus
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_BlockStatus

XRFdc_BlockStatus = RFDC.rfdc.GetStruct_XRFdc_BlockStatus()

% XRFdc_DACBlock_AnalogDataPath_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config

XRFdc_DACBlock_AnalogDataPath_Config = RFDC.rfdc.GetStruct_XRFdc_DACBlock_AnalogDataPath_Config()

% XRFdc_DACBlock_DigitalDataPath_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config

XRFdc_DACBlock_DigitalDataPath_Config = RFDC.rfdc.GetStruct_XRFdc_DACBlock_DigitalDataPath_Config()

% XRFdc_ADCBlock_AnalogDataPath_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config

XRFdc_ADCBlock_AnalogDataPath_Config = RFDC.rfdc.GetStruct_XRFdc_ADCBlock_AnalogDataPath_Config()

% XRFdc_ADCBlock_DigitalDataPath_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config

XRFdc_ADCBlock_DigitalDataPath_Config = RFDC.rfdc.GetStruct_XRFdc_ADCBlock_DigitalDataPath_Config()

% XRFdc_DACTile_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_DACTile_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DACTile_Config

XRFdc_DACTile_Config = RFDC.rfdc.GetStruct_XRFdc_DACTile_Config()

% XRFdc_ADCTile_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADCTile_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADCTile_Config

XRFdc_ADCTile_Config = RFDC.rfdc.GetStruct_XRFdc_ADCTile_Config()

% XRFdc_Config
%Description:
%   Return Dictionary equivalent of structure XRFdc_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_Config

XRFdc_Config = RFDC.rfdc.GetStruct_XRFdc_Config()

% XRFdc_DACBlock_AnalogDataPath
%Description:
%    Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath

XRFdc_DACBlock_AnalogDataPath = RFDC.rfdc.GetStruct_XRFdc_DACBlock_AnalogDataPath()

% XRFdc_DACBlock_DigitalDataPath
%Description:
%   Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config

XRFdc_DACBlock_DigitalDataPath = RFDC.rfdc.GetStruct_XRFdc_DACBlock_DigitalDataPath()

% XRFdc_ADCBlock_AnalogDataPath
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath

XRFdc_ADCBlock_AnalogDataPath = RFDC.rfdc.GetStruct_XRFdc_ADCBlock_AnalogDataPath()

% XRFdc_ADCBlock_DigitalDataPath
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath

XRFdc_ADCBlock_DigitalDataPath = RFDC.rfdc.GetStruct_XRFdc_ADCBlock_DigitalDataPath()

% XRFdc_DAC_Tile
%Description:
%   Return Dictionary equivalent of structure XRFdc_DAC_Tile
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_DAC_Tile

XRFdc_DAC_Tile = RFDC.rfdc.GetStruct_XRFdc_DAC_Tile()

% XRFdc_ADC_Tile
%Description:
%   Return Dictionary equivalent of structure XRFdc_ADC_Tile
%Input Arguments:
%   None
%Return:
%   return: Dictionary equivalent of structure XRFdc_ADC_Tile

XRFdc_ADC_Tile = RFDC.rfdc.GetStruct_XRFdc_ADC_Tile()

% XRFdc_LookupConfig
%Description:
%   Looks up the device configuration based on the unique device ID. A table
%   contains the configuration info for each device in the system.
%C header declaration:
%   XRFdc_Config *XRFdc_LookupConfig(u16 DeviceId);
%Input Arguments:
%   DeviceId: DeviceId contains the ID of the device to look up the configuration.
%Return:
%   ret: 0 on success, 1 on failure
%   config: XRFdc_Config container with values. Will be Null on failure.

ret = RFDC.rfdc.XRFdc_LookupConfig(uint32(0));
Config = ret{2};

% XRFdc_RegisterMetal
%Description:
%   Register/open the device and map RFDC to the IO region.
%C header declaration:
%   u32 XRFdc_RegisterMetal(XRFdc *InstancePtr, u16 DeviceId, struct metal_device **DevicePtr);
%Input Arguments:
%   DeviceId: DeviceId contains the ID of the device to register/map
%Return:
%   ret: XRFDC_SUCCESS on success, XRFDC_FAILURE if error occurs
%   inst_id: integer handle to the initialized instance

ret = RFDC.rfdc.XRFdc_RegisterMetal(uint32(0));
inst_id = ret{2}

% XRFdc_CfgInitialize
%Description:
%   Initializes a specific XRFdc instance such that the driver is ready to use.
%C header declaration:
%   u32 XRFdc_CfgInitialize(XRFdc *InstancePtr, XRFdc_Config *ConfigPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Config: DeviceId contains the ID of the device to look up the configuration.
%Return:
%   ret: XRFDC_SUCCESS if successful.
%   Config: XRFdc_Config container with values. Will be same as passed value

ret = RFDC.rfdc.XRFdc_CfgInitialize(inst_id, Config);

% XRFdc_GetDriverVersion
%Description:
%   This API is used to get the driver version
%C header declaration:
%   double XRFdc_GetDriverVersion(void);
%Input Arguments:
%   None
%Return:
%   ret: Driver version number

version = RFDC.rfdc.XRFdc_GetDriverVersion();

% XRFdc_GetNoOfDACBlock
%Description:
%   Get Number of DAC Blocks enabled
%C header declaration:
%   u32 XRFdc_GetNoOfDACBlock(XRFdc *InstancePtr, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: number of DAC blocks enabled.

ret = RFDC.rfdc.XRFdc_GetNoOfDACBlock(inst_id, uint32(0));

% XRFdc_ClrSetReg
%Description:
%   Execute Read modify Write
%C header declaration:
%   void XRFdc_ClrSetReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask, u16 Data);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   BaseAddr: Address of a block
%   RegAddr: Register offset value
%   Mask: Bit mask value
%   Data: Value to be written to register
%Return:
%   None

RFDC.rfdc.XRFdc_ClrSetReg(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_ClrReg
%Description:
%   Execute Read and clear
%C header declaration:
%   void XRFdc_ClrReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   BaseAddr: Address of a block
%   RegAddr: Register offset value
%   Mask: Bit mask value
%Return:
%   None

RFDC.rfdc.XRFdc_ClrReg(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_RDReg
%Description:
%   Execute Read and mask with the value
%C header declaration:
%   u16 XRFdc_RDReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   BaseAddr: Address of a block
%   RegAddr: Register offset value
%   Mask: Bit mask value
%Return:
%   None

ret = RFDC.rfdc.XRFdc_RDReg(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_IsHighSpeedADC
%Description:
%   Get ADC type is High Speed or Medium Speed
%C header declaration:
%   u32 XRFdc_IsHighSpeedADC(XRFdc *InstancePtr, u32 Tile);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3
%Return:
%   ret: 1 if ADC type is 4GSPS, otherwise 0 if quad or invalid tile.

ret = RFDC.rfdc.XRFdc_IsHighSpeedADC(inst_id, uint32(0));

% XRFdc_IsDACBlockEnabled
%Description:
%   Checks whether DAC block is available or not
%C header declaration:
%   u32 XRFdc_IsDACBlockEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0 - 3
%Return:
%   ret: Return 1 if DAC block is available, otherwise 0

ret = RFDC.rfdc.XRFdc_IsDACBlockEnabled(inst_id, uint32(0), uint32(0));

% XRFdc_IsADCBlockEnabled
%Description:
%   Checks whether ADC block is available or not
%C header declaration:
%   u32 XRFdc_IsADCBlockEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return 1 if ADC block is available, otherwise 0

ret = RFDC.rfdc.XRFdc_IsADCBlockEnabled(inst_id, uint32(0), uint32(0));

% XRFdc_IsDACDigitalPathEnabled
%Description:
%   Checks whether DAC Digital path is enabled or not
%C header declaration:
%   u32 XRFdc_IsDACDigitalPathEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return 1 if DAC digital path is enabled, otherwise 0

ret = RFDC.rfdc.XRFdc_IsDACDigitalPathEnabled(inst_id, uint32(0), uint32(0));

% XRFdc_IsADCDigitalPathEnabled
%Description:
%   Checks whether ADC digital path is enabled or not
%C header declaration:
%   u32 XRFdc_IsADCDigitalPathEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return 1 if ADC digital path is enabled, otherwise 0.

ret = RFDC.rfdc.XRFdc_IsADCDigitalPathEnabled(inst_id, uint32(0), uint32(0));

% XRFdc_CheckDigitalPathEnabled
%Description:
%   Checks whether ADC/DAC Digital path is enabled or not
%C header declaration:
%   u32 XRFdc_CheckDigitalPathEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: XRFDC_SUCCESS if Digital path is enabled, XRFDC_FAILURE if Digital path is not enabled.

ret = RFDC.rfdc.XRFdc_CheckDigitalPathEnabled(inst_id, uint32(0), uint32(0), uint32(1));

% XRFdc_Get_IPBaseAddr
%Description:
%   Get the RFDC IP Base Address
%C header declaration:
%   u32 XRFdc_Get_IPBaseAddr(XRFdc *InstancePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%Return:
%   ret: Return IP BaseAddress

ret = RFDC.rfdc.XRFdc_Get_IPBaseAddr(inst_id);

% XRFdc_Get_TileBaseAddr
%Description:
%   Get Tile BaseAddress
%C header declaration:
%   u32 XRFdc_Get_TileBaseAddr(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: Tile BaseAddress if valid, Return 0U if invalid/unavailable tile

ret = RFDC.rfdc.XRFdc_Get_TileBaseAddr(inst_id, uint32(0), uint32(0));

% XRFdc_Get_BlockBaseAddr
%Description:
%   Get Number of DAC Blocks enabled
%C header declaration:
%   u32 XRFdc_GetNoOfDACBlock(XRFdc *InstancePtr, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: number of DAC blocks enabled.

ret = RFDC.rfdc.XRFdc_Get_BlockBaseAddr(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetNoOfDACBlock
%Description:
%   Get Number of DAC Blocks enabled
%C header declaration:
%   u32 XRFdc_GetNoOfDACBlock(XRFdc *InstancePtr, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: number of DAC blocks enabled.

ret = RFDC.rfdc.XRFdc_GetNoOfDACBlock(inst_id, uint32(0));

% XRFdc_GetNoOfADCBlocks
%Description:
%   Get Number of ADC Blocks enabled.
%C header declaration:
%   u32 XRFdc_GetNoOfADCBlocks(XRFdc *InstancePtr, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: number of ADC blocks enabled.

ret = RFDC.rfdc.XRFdc_GetNoOfADCBlocks(inst_id, uint32(0));

% XRFdc_GetDataType
%Description:
%   Get Mixer Input Data Type for ADC/DAC block.
%C header declaration:
%   u32 XRFdc_GetDataType(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: MixerInputDataType of ADC/DAC block. 0U if converter type, tile or block number is invalid


ret = RFDC.rfdc.XRFdc_GetDataType(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetDataWidth
%Description:
%   Get Data Width for ADC/DAC block.
%C header declaration:
%   u32 XRFdc_GetDataWidth(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0-3.
%Return:
%   ret: DataWidth of ADC/DAC block.

ret = RFDC.rfdc.XRFdc_GetDataWidth(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetInverseSincFilter
%Description:
%   Get Inversesync filter for DAC block.
%C header declaration:
%   u32 XRFdc_GetInverseSincFilter(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Inversesync filter for DAC block. Return 0 if invalid

ret = RFDC.rfdc.XRFdc_GetInverseSincFilter(inst_id, uint32(0), uint32(0));

% XRFdc_GetMixedMode
%Description:
%   Get Mixed mode for DAC block.
%C header declaration:
%   u32 XRFdc_GetMixedMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: mixed mode for DAC block

ret = RFDC.rfdc.XRFdc_GetMixedMode(inst_id, uint32(0), uint32(0));

% XRFdc_GetMasterTile
%Description:
%   Get Master Tile for ADC/DAC tiles.
%C header declaration:
%   u32 XRFdc_GetMasterTile(XRFdc *InstancePtr, u32 Type);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%Return:
%   ret: Master Tile for ADC/DAC tiles. Returns XRFDC_TILE_ID_INV if converter type is invalid

ret = RFDC.rfdc.XRFdc_GetMasterTile(inst_id, uint32(0));

% XRFdc_GetSysRefSource
%Description:
%   Get Sysref source for ADC/DAC tile.
%C header declaration:
%   u32 XRFdc_GetSysRefSource(XRFdc *InstancePtr, u32 Type);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%Return:
%   ret: Sysref source for ADC/DAC tile. returns XRFDC_TILE_ID_INV if converter type is invalid


ret = RFDC.rfdc.XRFdc_GetSysRefSource(inst_id, uint32(0));

% XRFdc_GetFabClkFreq
%Description:
%   Get Fabric Clock frequency.
%C header declaration:
%   double XRFdc_GetFabClkFreq(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3.
%Return:
%   ret: Fabric Clock frequency for ADC/DAC tile

ret = RFDC.rfdc.XRFdc_GetFabClkFreq(inst_id, uint32(0), uint32(0)) ;

% XRFdc_IsFifoEnabled
%Description:
%   Get whether FIFO is enabled or not.
%C header declaration:
%   u32 XRFdc_IsFifoEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return 1 if FIFO is enabled, otherwise 0.

ret = RFDC.rfdc.XRFdc_IsFifoEnabled(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetConnectedIData
%Description:
%   Get Data Converter connected for digital data path I
%C header declaration:
%   int XRFdc_GetConnectedIData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)

ret = RFDC.rfdc.XRFdc_GetConnectedIData(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetConnectedQData
%Description:
%    Get Data Converter connected for digital data path Q
%C header declaration:
%   int XRFdc_GetConnectedQData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)

ret = RFDC.rfdc.XRFdc_GetConnectedQData(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetConnectedIQData
%Description:
%   Set Data Converter connected for digital data path I and Q
%C header declaration:
%   void XRFdc_SetConnectedIQData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, int ConnectedIData,
% 	int ConnectedQData);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: %TODO
%   ConnectedIData: ConnectedIData is Converter Id to which DigitalPathI connected.
%   ConnectedQData: ConnectedQData is Converter Id to which DigitalPathQ connected.
%Return:
%   None

ret = RFDC.rfdc.XRFdc_SetConnectedIQData(inst_id, uint32(0), uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_GetMultibandConfig
%Description:
%   Get Multiband Config data
%C header declaration:
%   u32 XRFdc_GetMultibandConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: Multiband Configuration. Return 0 if invalid.

ret = RFDC.rfdc.XRFdc_GetMultibandConfig(inst_id, uint32(0), uint32(0));

% XRFdc_CheckBlockEnabled
%Description:
%   Checks whether ADC/DAC block is enabled or not.
%C header declaration:
%   u32 XRFdc_CheckBlockEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: XRFDC_SUCCESS if block enabled, XRFDC_FAILURE if block is not enabled

ret = RFDC.rfdc.XRFdc_CheckBlockEnabled(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_CheckTileEnabled
%Description:
%   Checks whether ADC/DAC tile is enabled or not.
%C header declaration:
%   u32 XRFdc_CheckTileEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if tile enabled, XRFDC_FAILURE if tile not enabled

ret = RFDC.rfdc.XRFdc_CheckTileEnabled(inst_id, uint32(0), uint32(0));

% XRFdc_GetMaxSampleRate
%Description:
%   Gets ADC/DAC tile maximum sampling rate.
%C header declaration:
%   u32 XRFdc_GetMaxSampleRate(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, double *MaxSampleRatePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
%   Tile_Id: Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if found sampling rate, XRFDC_FAILURE if could not find sampling rate.
%   MaxSampleRate: maximum sample rate

MaxSampleRate = RFDC.rfdc.XRFdc_GetMaxSampleRate(inst_id, uint32(0), uint32(0));

% XRFdc_GetMinSampleRate
%Description:
%   Gets ADC/DAC tile minimum sampling rate.
%C header declaration:
%   u32 XRFdc_GetMinSampleRate(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, double *MinSampleRatePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
%   Tile_Id: Tile_Id Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if found sampling rate XRFDC_FAILURE if could not find sampling rate.
%   MinSampleRate: minimum sample rate

MinSampleRate = RFDC.rfdc.XRFdc_GetMinSampleRate(inst_id, uint32(0), uint32(0));

% XRFdc_StartUp
%Description:
%   The API Restarts the requested tile. It can restart a single tile and
%   alternatively can restart all the tiles. Existing register settings are not
%   lost or altered in the process. It just starts the requested tile(s).
%C header declaration:
%   u32 XRFdc_StartUp(XRFdc *InstancePtr, u32 Type, int Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3 and -1
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_StartUp(inst_id, uint32(0), uint32(0));

% XRFdc_Shutdown
%Description:
%   The API stops the tile as requested. It can also stop all the tiles if
%   asked for. It does not clear any of the existing register settings. It just
%   stops the requested tile(s).
%C header declaration:
%   u32 XRFdc_Shutdown(XRFdc *InstancePtr, u32 Type, int Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3, and -1
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_Shutdown(inst_id, uint32(0), uint32(0));

% XRFdc_Reset
%Description:
%   The API resets the requested tile. It can reset all the tiles as well. In
%   the process, all existing register settings are cleared and are replaced
%   with the settings initially configured (through the GUI).
%C header declaration:
%   u32 XRFdc_Reset(XRFdc *InstancePtr, u32 Type, int Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3, and -1.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_Reset(inst_id, uint32(0), uint32(0));

% XRFdc_GetIPStatus
%Description:
%   The API returns the IP status.
%C header declaration:
%   u32 XRFdc_GetIPStatus(XRFdc *InstancePtr, XRFdc_IPStatus *IPStatusPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%Return:
%   ret: XRFDC_SUCCESS if successful
%   IPStatus: Dictionary equivalent to XRFdc_IPStatus structure

IPStatus = RFDC.rfdc.XRFdc_GetIPStatus(inst_id);

% XRFdc_GetBlockStatus
%Description:
%   The API returns the requested block status.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_GetBlockStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_BlockStatus *BlockStatusPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Tile_Id Valid values are 0-3.
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled.
%   BlockStatus: Dictionary equivalent of XRFdc_BlockStatus structure
%                through which the ADC/DAC block status is returned.

BlockStatus = RFDC.rfdc.XRFdc_GetBlockStatus(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetMixerSettings
%Description:
%   The API returns back Mixer/NCO settings to the caller.
%C header declaration:
%   u32 XRFdc_GetMixerSettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
%   XRFdc_Mixer_Settings *MixerSettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%    ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%    MixerSettings: Dictionary in which the Mixer/NCO settings are passed
%       FineMixerScale in Mixer_Settings dictionary can have 3 values.
%       XRFDC_MIXER_SCALE_* represents the valid values.
%       XRFDC_MIXER_SCALE_AUTO - If mixer mode is R2C, Mixer Scale is
%       set to 1 and for other modes mixer scale is set to 0.7
%       XRFDC_MIXER_SCALE_1P0 - To set fine mixer scale to 1.
%       XRFDC_MIXER_SCALE_0P7 - To set fine mixer scale to 0.7.

MixerSettings = RFDC.rfdc.XRFdc_GetMixerSettings(inst_id, uint32(0), uint32(0), uint32(0));
MixerSettings = py.dict(pyargs('Freq', 0.0, 'PhaseOffset', 0.0, 'EventSource', uint32(0), 'CoarseMixFreq', uint32(4), 'MixerMode', uint32(3), 'FineMixerScale', uint32(0), 'MixerType', uint32(1)));

% XRFdc_GetMasterTile
%Description:
%   Get Master Tile for ADC/DAC tiles.
%C header declaration:
%   u32 XRFdc_GetMasterTile(XRFdc *InstancePtr, u32 Type);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%Return:
%   ret: Master Tile for ADC/DAC tiles. Returns XRFDC_TILE_ID_INV if converter type is invalid

ret = RFDC.rfdc.XRFdc_GetMasterTile(inst_id, uint32(0));

% XRFdc_SetCoarseDelaySettings
%Description:
%   Coarse delay settings passed are used to update the corresponding
%   block level registers. Driver structure is updated with the new values.
%C header declaration:
%   u32 XRFdc_SetCoarseDelaySettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
% 	XRFdc_CoarseDelay_Settings *CoarseDelaySettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
%                        structure in which the CoarseDelay settings are passed.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

CoarseDelaySettings = py.dict(pyargs('CoarseDelay', uint32(0), 'EventSource',uint32(0)));
CoarseDelaySettings = RFDC.rfdc.XRFdc_SetCoarseDelaySettings(inst_id, uint32(0), uint32(0), uint32(0), CoarseDelaySettings);

% XRFdc_GetCoarseDelaySettings
%Description:
%   Coarse delay settings are returned back to the caller.
%C header declaration:
%   u32 XRFdc_GetCoarseDelaySettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
%   XRFdc_CoarseDelay_Settings *CoarseDelaySettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
%                        structure in which the CoarseDelay settings are passed.

CoarseDelaySettings = RFDC.rfdc.XRFdc_GetCoarseDelaySettings(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetInterpolationFactor
%Description:
%   Interpolation factor are returned back to the caller.
%C header declaration:
%   u32 XRFdc_GetInterpolationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *InterpolationFactorPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   InterpolationFactor: the interpolation factor for DAC blocks.

InterpolationFactor = RFDC.rfdc.XRFdc_GetInterpolationFactor(inst_id, uint32(0), uint32(0));

% XRFdc_GetDecimationFactor
%Description:
%   Decimation factor are returned back to the caller for both actual and
%   observation FIFO.
%C header declaration:
%   u32 XRFdc_GetDecimationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *DecimationFactorPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   DecimationFactor: the decimation factor for DAC blocks.

DecimationFactor = RFDC.rfdc.XRFdc_GetDecimationFactor(inst_id, uint32(0), uint32(0));

% XRFdc_GetFabWrVldWords
%Description:
%   This function returns the the number of fabric write valid words requested
%   for the block. For ADCs this is for both the actual and observation FIFO.
%   ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_GetFabWrVldWords(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   FabricDataRate: Fabric data rate for DAC block

FabricDataRate = RFDC.rfdc.XRFdc_GetFabWrVldWords(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetFabRdVldWords
%Description:
%   This function returns the number of fabric read valid words requested
%   for the block. For ADCs this is for both the actual and observation FIFO.
%C header declaration:
%   u32 XRFdc_GetFabRdVldWords(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   FabricDataRate: Fabric data rate for ADC/DAC block

FabricDataRate = RFDC.rfdc.XRFdc_GetFabRdVldWords(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetFabRdVldWords
%Description:
%   Fabric data rate for the requested ADC block is set by writing to the
%   corresponding register. The function writes the number of valid read words
%   for the requested ADC block.
%C header declaration:
%   u32 XRFdc_SetFabRdVldWords(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 FabricRdVldWords);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   FabricRdVldWords: Read fabric rate to be set for ADC block.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetFabRdVldWords(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetFabWrVldWords
%Description:
%   Fabric data rate for the requested DAC block is set by writing to the
%   corresponding register. The function writes the number of valid write words
%   for the requested DAC block.
%C header declaration:
%   u32 XRFdc_SetFabWrVldWords(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 FabricWrVldWords);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   FabricWrVldWords: write fabric rate to be set for DAC block
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetFabWrVldWords(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetThresholdSettings
%Description:
%   Threshold settings are read from the corresponding registers and are passed
%   back to the caller. There can be two threshold settings:
%   threshold0 and threshold1. Both of them are independent of each other.
%   The function returns the requested threshold (which can be threshold0,
%   threshold1, or both.
%C header declaration:
%   u32 XRFdc_GetThresholdSettings(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id,
% 	XRFdc_Threshold_Settings *ThresholdSettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   ThresholdSettings:  the register settings for thresholds are passed back

ThresholdSettings = RFDC.rfdc.XRFdc_GetThresholdSettings(inst_id, uint32(0), uint32(0));

% XRFdc_SetDecoderMode
%Description:
%   Decoder mode is updated into the relevant registers. Driver structure is
%   updated with the new values.
%   Only DAC blocks
%C header declaration:
%   u32 XRFdc_SetDecoderMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 DecoderMode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   DecoderMode: DecoderMode Valid values are 1 (Maximum SNR, for non-
%                randomized decoder), 2 (Maximum Linearity, for randomized decoder)
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetDecoderMode(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_UpdateEvent
%Description:
%   This function will trigger the update event for an event.
%C header declaration:
%   u32 XRFdc_UpdateEvent(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 Event);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Event: Event is for which dynamic update event will trigger.
%          XRFDC_EVENT_* defines the different events.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_UpdateEvent(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_GetDecoderMode
%Description:
%   Decoder mode is read and returned back.
%C header declaration:
%   u32 XRFdc_GetDecoderMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *DecoderModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   DecoderMode: Valid values are 1 (Maximum SNR, for non-randomized
%                decoder), 2 (Maximum Linearity, for randomized decoder)

DecoderMode = RFDC.rfdc.XRFdc_GetDecoderMode(inst_id, uint32(0), uint32(0));

% XRFdc_ResetNCOPhase
%Description:
%   Resets the NCO phase of the current block phase accumulator.
%C header declaration:
%   u32 XRFdc_ResetNCOPhase(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_ResetNCOPhase(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_DumpRegs
%Description:
%   This Prints the offset of the register along with the content. This API is
%   meant to be used for debug purposes. It prints to the console the contents
%   of registers for the passed Tile_Id. If -1 is passed, it prints the contents
%   of the registers for all the tiles for the respective ADC or DAC
%C header declaration:
%   void XRFdc_DumpRegs(XRFdc *InstancePtr, u32 Type, int Tile_Id);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   None

RFDC.rfdc.XRFdc_DumpRegs(inst_id, uint32(0), uint32(0));

% XRFdc_MultiBand
%Description:
%   User-level API to setup multiband configuration.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_MultiBand(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 DigitalDataPathMask, u32 MixerInOutDataType,
%   u32 DataConverterMask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   DigitalDataPathMask: DigitalDataPathMask is the DataPath mask. First 4 bits represent
%                        4 data paths, 1 means enabled and 0 means disabled.
%   MixerInOutDataType: MixerInOutDataType is mixer data type, valid values are XRFDC_MB_DATATYPE_*
%   DataConverterMask: DataConverterMask is block enabled mask (input/output driving
%                      blocks). 1 means enabled and 0 means disabled.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_MultiBand(inst_id, uint32(0), uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_IntrClr
%Description:
%   This function clear the interrupts.
%C header declaration:
%   u32 XRFdc_IntrClr(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   IntrMask: IntrMask contains the interrupts to be cleared.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = RFDC.rfdc.XRFdc_IntrClr(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_GetIntrStatus
%Description:
%   This function returns the interrupt status read from Interrupt Status
%   Register(ISR).
%C header declaration:
%   u32 XRFdc_GetIntrStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *IntrStsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
%   IntrSts: the contents of the Interrupt Status Registers (FIFO interface,
%            Decoder interface, Data Path Interface).

IntrSts = RFDC.rfdc.XRFdc_GetIntrStatus(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_IntrDisable
%Description:
%   This function clears the interrupt mask.
%C header declaration:
%   u32 XRFdc_IntrDisable(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   IntrMask: IntrMask contains the interrupts to be disabled.
%             '1' disables an interrupt, and '0' remains no change.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = RFDC.rfdc.XRFdc_IntrDisable(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_IntrEnable
%Description:
%   This function sets the interrupt mask.
%C header declaration:
%   u32 XRFdc_IntrEnable(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   IntrMask: IntrMask contains the interrupts to be enabled.
%             '1' enables an interrupt, and '0' disables.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = RFDC.rfdc.XRFdc_IntrEnable(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_GetEnabledInterrupts
%Description:
%   This function gets a mask of enabled interrupts.
%C header declaration:
%   u32 XRFdc_GetEnabledInterrupts(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *IntrMask);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
%   IntrMask: mask of enabled interrupts.
%             '1' denotes an enabled interrupt, and '0' denotes a disabled interrupt

IntrMask = RFDC.rfdc.XRFdc_GetEnabledInterrupts(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetThresholdClrMode
%Description:
%   This API sets the threshold clear mode. The clear mode can be through
%   explicit DRP access (manual) or auto clear (QMC gain update event).
%   Only ADC blocks
%C header declaration:
%   u32 XRFdc_SetThresholdClrMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 ThresholdToUpdate, u32 ClrMode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   ThresholdToUpdate: Select which Threshold (Threshold0 or
%                      Threshold1 or both) to update.
%   ClrMode: ClrMode can be DRP access (manual) or auto clear (QMC gain
%            update event).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetThresholdClrMode(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_ThresholdStickyClear
%Description:
%   This API is to clear the Sticky bit in threshold config registers.
%C header declaration:
%   u32 XRFdc_ThresholdStickyClear(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 ThresholdToUpdate);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   ThresholdToUpdate: Select which Threshold (Threshold0 or
%                      Threshold1 or both) to update.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_ThresholdStickyClear(inst_id, uint32(1), uint32(1), uint32(0));

% XRFdc_SetStatusHandler
%TODO

ret = RFDC.rfdc.XRFdc_SetStatusHandler();

% XRFdc_SetupFIFO
%Description:
%   Enable and Disable the ADC/DAC FIFO. For ADCs this is for the actual and
%   observation FIFO.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_SetupFIFO(XRFdc *InstancePtr, u32 Type, int Tile_Id, u8 Enable);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Enable: Enable valid values are 1 (FIFO enable) and 0 (FIFO Disable)
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetupFIFO(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetFIFOStatus
%Description:
%   Current status of ADC/DAC FIFO. For ADCs this is for both the actual and
%   observations FIFOs.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_GetFIFOStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 *EnablePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)

Enable = RFDC.rfdc.XRFdc_GetFIFOStatus(inst_id, uint32(0), uint32(0));

% XRFdc_SetNyquistZone
%Description:
%   Set the Nyquist zone.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_SetNyquistZone(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 NyquistZone);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   NyquistZone: valid values are 1 (Odd),2 (Even).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetNyquistZone(inst_id, uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_GetNyquistZone
%Description:
%   Get the Nyquist zone.
%   Common API for ADC/DAC blocks
%C header declaration:
%   u32 XRFdc_GetNyquistZone(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *NyquistZonePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   NyquistZone: returned Nyquist zone

NyquistZone = RFDC.rfdc.XRFdc_GetNyquistZone(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetOutputCurr
%Description:
%   Get Output Current for DAC block.
%C header declaration:
%   u32 XRFdc_GetOutputCurr(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *OutputCurrPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   OutputCurr: Return Output Current for DAC block

OutputCurr = RFDC.rfdc.XRFdc_GetOutputCurr(inst_id, uint32(0), uint32(0));

% XRFdc_SetDecimationFactor
%Description:
%   This API is to set the decimation factor and also update the FIFO write
%   words w.r.t to decimation factor.
%C header declaration:
%   u32 XRFdc_SetDecimationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 DecimationFactor);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   DecimationFactor: DecimationFactor to be set for DAC block.
%                     XRFDC_INTERP_DECIM_* defines the valid values.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetDecimationFactor(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetInterpolationFactor
%Description:
%   This API is to set the interpolation factor and also update the FIFO read
%   words w.r.t to interpolation factor.
%   Only DAC blocks
%C header declaration:
%   u32 XRFdc_SetInterpolationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 InterpolationFactor);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   InterpolationFactor: InterpolationFactor to be set for DAC block.
%                        XRFDC_INTERP_DECIM_* defines the valid values.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetInterpolationFactor(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetFabClkOutDiv
%Description:
%   This API is to set the divider for clock fabric out.
%   ADC and DAC Tiles
%C header declaration:
%   u32 XRFdc_SetFabClkOutDiv(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u16 FabClkDiv);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   FabClkDiv: FabClkDiv to be set for a tile.
%              XRFDC_FAB_CLK_* defines the valid divider values.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetFabClkOutDiv(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetCalibrationMode
%Description:
%   This API is to set the Calibration mode.
%   Only for ADC blocks
%C header declaration:
%   u32 XRFdc_SetCalibrationMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u8 CalibrationMode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CalibrationMode: valid values are 1 and 2.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = RFDC.rfdc.XRFdc_SetCalibrationMode(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetCalibrationMode
%Description:
%   This API is to get the Calibration mode.
%   Only for ADC blocks
%C header declaration:
%   u32 XRFdc_GetCalibrationMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u8 *CalibrationModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   CalibrationMode: calibration mode


CalibrationMode = RFDC.rfdc.XRFdc_GetCalibrationMode(inst_id, uint32(0), uint32(0));

% XRFdc_GetClockSource
%Description:
%   This function gets Clock source
%C header declaration:
%   u32 XRFdc_GetClockSource(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 *ClockSourcePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   ClockSource: return the clock source

ClockSource = RFDC.rfdc.XRFdc_GetClockSource(inst_id, uint32(0), uint32(0));

% XRFdc_GetPLLLockStatus
%Description:
%   This function gets PLL lock status
%C header declaration:
%   u32 XRFdc_GetPLLLockStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 *LockStatusPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   LockStatus: return the PLL lock status

LockStatus = RFDC.rfdc.XRFdc_GetPLLLockStatus(inst_id, uint32(0), uint32(0));

% XRFdc_GetPLLConfig
%Description:
%   This API is used to get the PLL Configurations.
%C header declaration:
%   u32 XRFdc_GetPLLConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, XRFdc_PLL_Settings *PLLSettings);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   PLLSettings: dictionary equivalent of XRFdc_PLL_Settings structure to get
%                the PLL configurations

PLLSettings = RFDC.rfdc.XRFdc_GetPLLConfig(inst_id, uint32(0), uint32(0));

% XRFdc_DynamicPLLConfig
%Description:
%   This function used for dynamically switching between internal PLL and
%   external clock source and configuring the internal PLL
%   This API enables automatic selection of the VCO which will work in
%   IP version 2.0.1 and above. Using older version of IP this API is
%   not likely to work.
%C header declaration:
%   u32 XRFdc_DynamicPLLConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 Source, double RefClkFreq,
% 	double SamplingRate);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%   Source: Clock source internal PLL or external clock source
%   RefClkFreq: Reference Clock Frequency in MHz(102.40625MHz - 1.2GHz)
%   SamplingRate: Sampling Rate in MHz(0.1- 6.554GHz for DAC and
%   0.5/1.0 - 2.058/4.116GHz for ADC based on the device package).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs


ret = RFDC.rfdc.XRFdc_DynamicPLLConfig(inst_id, uint32(0), uint32(0), uint32(0), uint32(0), uint32(0));

% XRFdc_SetInvSincFIR
%Description:
%   This API is used to set the mode for the Inverse-Sinc filter.
%   Only DAC blocks
%C header declaration:
%   u32 XRFdc_SetInvSincFIR(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u16 Mode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Mode: Mode valid values are 0(disable),  1(1st Nyquist zone)
%         and 2(2nd Nyquist zone).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled/invalid mode.

ret = RFDC.rfdc.XRFdc_SetInvSincFIR(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetInvSincFIR
%Description:
%   This API is used to get the Inverse-Sinc filter mode.
%   Only DAC blocks
%C header declaration:
%   u32 XRFdc_GetInvSincFIR(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u16 *ModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Mode: return the inv-sinc status. valid values
%         are 0(disable),  1(1st Nyquist zone) and 2(2nd Nyquist zone).

Mode = RFDC.rfdc.XRFdc_GetInvSincFIR(inst_id, uint32(0), uint32(0));

% XRFdc_GetLinkCoupling
%Description:
%   This function is used to get the Link Coupling mode.
%C header declaration:
%   u32 XRFdc_GetLinkCoupling(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Mode: return the link coupling mode

Mode = RFDC.rfdc.XRFdc_GetLinkCoupling(inst_id, uint32(0), uint32(0));

% XRFdc_GetFabClkOutDiv
%Description:
%   This API is to get the divider for clock fabric out.
%   API is applicable for both ADC and DAC Tiles
%C header declaration:
%   u32 XRFdc_GetFabClkOutDiv(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u16 *FabClkDivPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
%   Tile_Id: Valid values are 0-3
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   FabClkDiv: fabric clock for a tile. XRFDC_FAB_CLK_* defines the valid divider values.

FabClkDiv = RFDC.rfdc.XRFdc_GetFabClkOutDiv(inst_id, uint32(0), uint32(0));

% XRFdc_SetDither
%Description:
%   This function is used to set the IM3 Dither mode.
%C header declaration:
%   u32 XRFdc_SetDither(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Mode: set the link coupling mode
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = RFDC.rfdc.XRFdc_SetDither(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetDither
%Description:
%    This function is used to get the IM3 Dither mode.
%C header declaration:
%   u32 XRFdc_GetDither(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Mode: get link coupling mode

Mode = RFDC.rfdc.XRFdc_GetDither(inst_id, uint32(0), uint32(0));

% XRFdc_GetClkDistribution
%Description:
%   This function is used to get the clock distribution
%C header declaration:
%   u32 XRFdc_GetClkDistribution(XRFdc *InstancePtr, XRFdc_Distribution_System_Settings *DistributionArrayPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if no valid distribution found.
%   DistributionSystemSettings: Dictionary equivalent of XRFdc_Distribution_Settings

DistributionSystemSettings = RFDC.rfdc.XRFdc_GetClkDistribution(inst_id)

%XRFdc_SetClkDistribution
%Description:
%   This function is used to set the clock distribution
%C header declaration:
%   u32 XRFdc_SetClkDistribution(XRFdc *InstancePtr, XRFdc_Distribution_Settings *DistributionSettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   DistributionSettings: distribution settings dictionary
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if could not set distribution
%   DistributionSettings: Dictionary equivalent of XRFdc_Distribution_Settings

ret = RFDC.rfdc.XRFdc_SetClkDistribution(inst_id, XRFdc_Distribution_Settings)

% XRFdc_SetDataPathMode
%Description:
%   This API is to set the DAC Datapath mode.
%C header declaration:
%   u32 XRFdc_SetDataPathMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Mode: Mode valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / out of range.

ret = RFDC.rfdc.XRFdc_SetDataPathMode(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetDataPathMode
%Description:
%   This API is to get the DAC Datapath mode.
%   This is only for DAC blocks
%C header declaration:
%   u32 XRFdc_GetDataPathMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Mode: valid values are 0-3

Mode = RFDC.rfdc.XRFdc_GetDataPathMode(inst_id, uint32(0), uint32(0));

% XRFdc_SetIMRPassMode
%Description:
%   This API is to set the DAC Image Reject Filter Pass mode.
%C header declaration:
%   u32 XRFdc_SetIMRPassMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Mode: valid values are 0 (for low pass) 1 (for high pass).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / bad parameter passed

ret = RFDC.rfdc.XRFdc_SetIMRPassMode(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetIMRPassMode
%Description:
%   This API is to get the DAC Image Reject Filter Pass mode.
%   This is only for DAC blocks
%C header declaration:
%   u32 XRFdc_GetIMRPassMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Mode: 0 (for low pass) 1 (for high pass)

Mode = RFDC.rfdc.XRFdc_GetIMRPassMode(inst_id, uint32(0), uint32(0));

% XRFdc_GetSignalDetector
%Description:
%   This function is used to get the ADC Signal Detector Settings.
%   This is only for DAC blocks
%C header declaration:
%   u32 XRFdc_GetSignalDetector(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Signal_Detector_Settings *SettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Settings: dictionary equivalent of XRFdc_Signal_Detector_Settings structure

Settings = RFDC.rfdc.XRFdc_GetSignalDetector(inst_id, uint32(0), uint32(0));

% XRFdc_DisableCoefficientsOverride
%Description:
%   This function is used to disable Calibration Coefficients override.
%   Only for ADC blocks
%C header declaration:
%   u32 XRFdc_DisableCoefficientsOverride(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CalibrationBlock: indicates the calibration block
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = RFDC.rfdc.XRFdc_DisableCoefficientsOverride(inst_id, uint32(0), uint32(0), uint32(0))    ;

Coeff = py.dict(pyargs('Coeff0', uint32(65484), ...
'Coeff1',uint32(65482), 'Coeff2', uint32(25),...
'Coeff3', uint32(65514), 'Coeff5',uint32(0), ...
'Coeff6', uint32(0),'Coeff7', uint32(0) ));

% XRFdc_SetCalCoefficients
%Description:
%   This function is used to set the ADC Calibration Coefficients.
%C header declaration:
%   u32 XRFdc_SetCalCoefficients(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock,
% 	XRFdc_Calibration_Coefficients *CoeffPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CalibrationBlock: indicates the block to be written to
%   Coeff: dictionary to the XRFdc_Calibration_Coefficients structure to set the calibration coefficients
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients

Coeff = RFDC.rfdc.XRFdc_SetCalCoefficients(inst_id, uint32(0), uint32(0), uint32(0), Coeff);

% XRFdc_GetCalCoefficients
%Description:
%   This function is used to get the ADC Calibration Coefficients.
%C header declaration:
%   u32 XRFdc_GetCalCoefficients(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock,
% 	XRFdc_Calibration_Coefficients *CoeffPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CalibrationBlock: indicates the block to be read from
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients

Coeff = RFDC.rfdc.XRFdc_GetCalCoefficients(inst_id, uint32(0), uint32(0), uint32(0));

CalFreeze = py.dict(pyargs('CalFrozen',uint32(0), 'DisableFreezePin', uint32(0), 'FreezeCalibration', uint32(0)));

% XRFdc_SetCalFreeze
%Description:
%   This function is used to set calibration freeze settings.
%C header declaration:
%   u32 XRFdc_SetCalFreeze(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Cal_Freeze_Settings *CalFreezePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure

CalFreeze = RFDC.rfdc.XRFdc_SetCalFreeze(inst_id, uint32(0), uint32(0), CalFreeze);

% XRFdc_GetCalFreeze
%Description:
%   This function is used to get calibration freeze settings and status.
%   Only for ADC blocks
%C header declaration:
%   u32 XRFdc_GetCalFreeze(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Cal_Freeze_Settings *CalFreezePtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure

CalFreeze = RFDC.rfdc.XRFdc_GetCalFreeze(inst_id, uint32(0), uint32(0));

% XRFdc_SetDACVOP
%Description:
%   Set Output Current for DAC block.
%   Range 6425 - 32000 uA with 25 uA resolution.
%C header declaration:
%   u32 XRFdc_SetDACVOP(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 uACurrent);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   uACurrent: the current in uA.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = RFDC.rfdc.XRFdc_SetDACVOP(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_SetDACCompMode
%Description:
%   Sets VOP compatibility mode.
%C header declaration:
%   u32 XRFdc_SetDACCompMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Enable);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Enable:  filled with whether the mode is enabled (1) or disabled(0).
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = RFDC.rfdc.XRFdc_SetDACCompMode(inst_id, uint32(0), uint32(0), uint32(0));

% XRFdc_GetDACCompMode
%Description:
%   Gets VOP compatibility mode.
%C header declaration:
%   u32 XRFdc_GetDACCompMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *EnabledPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Enabled: filled with whether the mode is enabled (1) or disabled(0).

Enabled = RFDC.rfdc.XRFdc_GetDACCompMode(inst_id, uint32(0), uint32(0));

Settings = py.dict(pyargs('DisableRTS',uint32(0), 'Attenuation', -2.5));

% XRFdc_SetDSA
%Description:
%   Set DSA for ADC block.
%   Range 0 - 11 dB with 0.5 dB resolution ES1 Si.
%   Range 0 - 27 dB with 1 dB resolution for Production Si.
%C header declaration:
%   u32 XRFdc_SetDSA(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_DSA_Settings *SettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   Settings: Dictionary equivalent of XRFdc_DSA_Settings
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Settings: Dictionary equivalent of XRFdc_DSA_Settings

Settings = RFDC.rfdc.XRFdc_SetDSA(inst_id, uint32(0), uint32(0), Settings);

% XRFdc_GetDSA
%Description:
%   Get DSA for ADC block.
%C header declaration:
%   u32 XRFdc_GetDSA(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_DSA_Settings *SettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
%   Settings: Dictionary equivalent of XRFdc_DSA_Settings

Settings = RFDC.rfdc.XRFdc_GetDSA(inst_id, uint32(0), uint32(0));

ThresholdSettings = py.dict(pyargs('UpdateThreshold',uint32(4), ...
    'ThresholdMode', py.list({uint32(0), uint32(0)}), 'ThresholdAvgVal', py.list({uint32(0), uint32(0)}), ...
    'ThresholdUnderVal', py.list({uint32(0), uint32(0)}), 'ThresholdOverVal', py.list({uint32(0), uint32(0)})));

% XRFdc_SetThresholdSettings
%Description:
%   Threshold settings are updated into the relevant registers. Driver structure
%   is updated with the new values. There can be two threshold settings:
%   threshold0 and threshold1. Both of them are independent of each other.
%   The function returns the requested threshold (which can be threshold0,
%   threshold1, or both.
%   Only ADC blocks
%C header declaration:
%   u32 XRFdc_SetThresholdSettings(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id,
% 	XRFdc_Threshold_Settings *ThresholdSettingsPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Tile_Id: Valid values are 0-3
%   Block_Id: Block_Id is ADC/DAC block number inside the tile.
%             Valid values are 0-3.
%   ThresholdSettings: the register settings
%                      for thresholds are passed to the API
%Return:
%   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
%   ThresholdSettings: the register settings for thresholds are passed back

ThresholdSettings = RFDC.rfdc.XRFdc_SetThresholdSettings(inst_id, uint32(0), uint32(0), ThresholdSettings);

    Config = py.dict(pyargs( ...
        'Offset', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
        'Marker_Delay', uint32(0), ...
        'Latency', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
        'DTC_Set_T1', { ...
            'Num_Windows', py.list({uint32(2), uint32(3), uint32(4), uint32(5)}), ...
            'IsPLL', uint32(0), ...
            'Target', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'DTC_Code', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Scan_Mode', uint32(3), ...
            'Max_Overlap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Max_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'RefTile', uint32(0), ...
            'Min_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}) ...
        }, ...
        'SysRef_Enable', uint32(0), ...
        'Target_Latency', uint32(0), ...
        'Tiles', uint32(0), ...
        'RefTile', uint32(0), ...
        'DTC_Set_PLL', { ...
            'Num_Windows', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'IsPLL', uint32(0), ...
            'Target', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'DTC_Code', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Scan_Mode', uint32(0), ...
            'Max_Overlap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Max_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'RefTile', uint32(23), ...
            'Min_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}) ...
        } ...
    ));


DTC_Set_T1 = py.dict(pyargs( ...
            'Num_Windows', py.list({uint32(2), uint32(3), uint32(4), uint32(5)}), ...
            'IsPLL', uint32(0), ...
            'Target', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'DTC_Code', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Scan_Mode', uint32(3), ...
            'Max_Overlap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Max_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'RefTile', uint32(0), ...
            'Min_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}) ...
        ));
DTC_Set_PLL = py.dict(pyargs( ...
            'Num_Windows', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'IsPLL', uint32(0), ...
            'Target', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'DTC_Code', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Scan_Mode', uint32(7), ...
            'Max_Overlap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}), ...
            'Max_Gap', py.list({uint32(4), uint32(3), uint32(34), uint32(43)}), ...
            'RefTile', uint32(43), ...
            'Min_Gap', py.list({uint32(0), uint32(0), uint32(0), uint32(0)}) ...
            ));
update(Config,py.dict(pyargs('DTC_Set_T1',DTC_Set_T1)));
update(Config,py.dict(pyargs('DTC_Set_PLL',DTC_Set_PLL)));
Config1 = Config;

% XRFdc_MultiConverter_Sync
%Description:
%   This is the top level API which will be used for Multi-tile synchronization
%C header declaration:
%   u32 XRFdc_MultiConverter_Sync(XRFdc *InstancePtr, u32 Type, XRFdc_MultiConverter_Sync_Config *ConfigPtr);
%Input Arguments:
%   inst_id: Id of the RFDC instance
%   Type: ADC or DAC. 0 for ADC and 1 for DAC
%   Config: Multi-tile sync config.
%Return:
%   ret: - XRFDC_MTS_OK if successful.
%        - XRFDC_MTS_TIMEOUT if timeout occurs.
%        - XRFDC_MTS_MARKER_RUN
%        - XRFDC_MTS_MARKER_MISM
%        - XRFDC_MTS_NOT_SUPPORTED if MTS is not supported.
%   Config: Multi-tile sync config.

Config = RFDC.rfdc.XRFdc_MultiConverter_Sync(inst_id, uint32(0), Config1);

PLL_Codes = py.list({uint32(0), uint32(0), uint32(0), uint32(0)});
T1_Codes = py.list({uint32(0), uint32(0), uint32(0), uint32(0)});

%PLL_Codes = py.None
%T1_Codes = py.None

% XRFdc_MultiConverter_Init
%Description:
%   This API Initializes the multi-tile sync config structures.
%         Optionally allows target codes to be provided for the Pll/T1
%         analog sysref capture
%C header declaration:
%   u32 XRFdc_MultiConverter_Init(XRFdc_MultiConverter_Sync_Config *ConfigPtr, int *PLL_CodesPtr, int *T1_CodesPtr,
% 			      u32 RefTile);
%Input Arguments:
%   Config: Multi-tile sync config
%   PLL_Codes: PLL analog sysref capture.
%   T1_Codes: T1 analog sysref capture.
%Return:
%   Config: Multi-tile sync config
%   PLL_Codes: PLL analog sysref capture.
%   T1_Codes: T1 analog sysref capture.

MultConverterInitRet = RFDC.rfdc.XRFdc_MultiConverter_Init(Config1, PLL_Codes, T1_Codes, uint32(0));

celldisp(cell(MultConverterInitRet(1,3))); % To convert to cell

tile_layout = RFDC.rfdc.XRFdc_GetTileLayout(inst_id);
