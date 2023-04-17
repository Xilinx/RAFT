# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
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
        sys.path.append('../../../xclient/rfdc')
    # The location of xclient in the filesystem is given for the board case
    elif (sys.argv[2] == 'board'):
        sys.path.append('/usr/share/raft/xclient/rfdc')
    else:
        usage()
        sys.exit()
    import rfdc_client
    handle = rfdc_client.rfdc
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/rfdc')
    from rfdc_server import RFDC
    handle = RFDC()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:RFDC@{ip_address}:{port}"
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
#   Get the python log level
#Input Arguments:
#   None
#Return:
#   return: Python Log Level

#GetPythonLogLevels
PythonLogLevels = handle.GetPythonLogLevels()

#Description:
#   Set the python log level to the given level
#Input Arguments:
#   PythonLogLevel: Log level to set
#Return:
#   None

#SetServerLogLevel
handle.SetServerLogLevel(PythonLogLevels["DEBUG"])

#Description:
#   Set the metal log level to the given level
#Input Arguments:
#   MetalLogLevel: Log level to set
#Return:
#   None

#SetMetalLogLevel
metal_log_level = handle.GetEnum_metal_log_level()
handle.SetMetalLogLevel(metal_log_level["METAL_LOG_EMERGENCY"])

#Description:
#   Return Dictionary equivalent of structure XRFdc_PLL_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_PLL_Settings

# XRFdc_PLL_Settings
XRFdc_PLL_Settings = handle.GetStruct_XRFdc_PLL_Settings()
print(XRFdc_PLL_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Tile_Clock_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Tile_Clock_Settings

# XRFdc_Tile_Clock_Settings
XRFdc_Tile_Clock_Settings = handle.GetStruct_XRFdc_Tile_Clock_Settings()
print(XRFdc_Tile_Clock_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Distribution_Info
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Distribution_Info

# XRFdc_Distribution
XRFdc_Distribution = handle.GetStruct_XRFdc_Distribution_Info()
print(XRFdc_Distribution)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Distribution_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Distribution_Settings

# XRFdc_Distribution_Settings
XRFdc_Distribution_Settings = handle.GetStruct_XRFdc_Distribution_Settings()
print(XRFdc_Distribution_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_MTS_DTC_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_MTS_DTC_Settings

# XRFdc_MTS_DTC_Settings
XRFdc_MTS_DTC_Settings = handle.GetStruct_XRFdc_MTS_DTC_Settings()
print(XRFdc_MTS_DTC_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_MultiConverter_Sync_Config

# XRFdc_MultiConverter_Sync_Config
XRFdc_MultiConverter_Sync_Config = handle.GetStruct_XRFdc_MultiConverter_Sync_Config()
print(XRFdc_MultiConverter_Sync_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_MTS_Marker
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_MTS_Marker

# XRFdc_MTS_Marker
XRFdc_MTS_Marker = handle.GetStruct_XRFdc_MTS_Marker()
print(XRFdc_MTS_Marker)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Signal_Detector_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Signal_Detector_Settings

# XRFdc_Signal_Detector_Settings
XRFdc_Signal_Detector_Settings = handle.GetStruct_XRFdc_Signal_Detector_Settings()
print(XRFdc_Signal_Detector_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_QMC_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_QMC_Settings

# XRFdc_QMC_Settings
XRFdc_QMC_Settings = handle.GetStruct_XRFdc_QMC_Settings()
print(XRFdc_QMC_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_CoarseDelay_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_CoarseDelay_Settings

# XRFdc_CoarseDelay_Settings
XRFdc_CoarseDelay_Settings = handle.GetStruct_XRFdc_CoarseDelay_Settings()
print(XRFdc_CoarseDelay_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Mixer_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Mixer_Settings

# XRFdc_Mixer_Settings
XRFdc_Mixer_Settings = handle.GetStruct_XRFdc_Mixer_Settings()
print(XRFdc_Mixer_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Threshold_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Threshold_Settings

# XRFdc_Threshold_Settings
XRFdc_Threshold_Settings = handle.GetStruct_XRFdc_Threshold_Settings()
print(XRFdc_Threshold_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Calibration_Coefficients
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Calibration_Coefficients

# XRFdc_Calibration_Coefficients
XRFdc_Calibration_Coefficients = handle.GetStruct_XRFdc_Calibration_Coefficients()
print(XRFdc_Calibration_Coefficients)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Pwr_Mode_Settings

# XRFdc_Pwr_Mode_Settings
XRFdc_Pwr_Mode_Settings = handle.GetStruct_XRFdc_Pwr_Mode_Settings()
print(XRFdc_Pwr_Mode_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DSA_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DSA_Settings

# XRFdc_DSA_Settings
XRFdc_DSA_Settings = handle.GetStruct_XRFdc_DSA_Settings()
print(XRFdc_DSA_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Cal_Freeze_Settings

# XRFdc_Cal_Freeze_Settings
XRFdc_Cal_Freeze_Settings = handle.GetStruct_XRFdc_Cal_Freeze_Settings()
print(XRFdc_Cal_Freeze_Settings)

#Description:
#   Return Dictionary equivalent of structure XRFdc_TileStatus
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_TileStatus

# XRFdc_TileStatus
XRFdc_TileStatus = handle.GetStruct_XRFdc_TileStatus()
print(XRFdc_TileStatus)

#Description:
#   Return Dictionary equivalent of structure XRFdc_IPStatus
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_IPStatus

# XRFdc_IPStatus
XRFdc_IPStatus = handle.GetStruct_XRFdc_IPStatus()
print(XRFdc_IPStatus)

#Description:
#   Return Dictionary equivalent of structure XRFdc_BlockStatus
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_BlockStatus

# XRFdc_BlockStatus
XRFdc_BlockStatus = handle.GetStruct_XRFdc_BlockStatus()
print(XRFdc_BlockStatus)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath_Config

# XRFdc_DACBlock_AnalogDataPath_Config
XRFdc_DACBlock_AnalogDataPath_Config = handle.GetStruct_XRFdc_DACBlock_AnalogDataPath_Config()
print(XRFdc_DACBlock_AnalogDataPath_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config

# XRFdc_DACBlock_DigitalDataPath_Config
XRFdc_DACBlock_DigitalDataPath_Config = handle.GetStruct_XRFdc_DACBlock_DigitalDataPath_Config()
print(XRFdc_DACBlock_DigitalDataPath_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath_Config

# XRFdc_ADCBlock_AnalogDataPath_Config
XRFdc_ADCBlock_AnalogDataPath_Config = handle.GetStruct_XRFdc_ADCBlock_AnalogDataPath_Config()
print(XRFdc_ADCBlock_AnalogDataPath_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath_Config

# XRFdc_ADCBlock_DigitalDataPath_Config
XRFdc_ADCBlock_DigitalDataPath_Config = handle.GetStruct_XRFdc_ADCBlock_DigitalDataPath_Config()
print(XRFdc_ADCBlock_DigitalDataPath_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DACTile_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DACTile_Config

# XRFdc_DACTile_Config
XRFdc_DACTile_Config = handle.GetStruct_XRFdc_DACTile_Config()
print(XRFdc_DACTile_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADCTile_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADCTile_Config

# XRFdc_ADCTile_Config
XRFdc_ADCTile_Config = handle.GetStruct_XRFdc_ADCTile_Config()
print(XRFdc_ADCTile_Config)

#Description:
#   Return Dictionary equivalent of structure XRFdc_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_Config

# XRFdc_Config
XRFdc_Config = handle.GetStruct_XRFdc_Config()
print(XRFdc_Config)

#Description:
#    Return Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DACBlock_AnalogDataPath

# XRFdc_DACBlock_AnalogDataPath
XRFdc_DACBlock_AnalogDataPath = handle.GetStruct_XRFdc_DACBlock_AnalogDataPath()
print(XRFdc_DACBlock_AnalogDataPath)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DACBlock_DigitalDataPath_Config

# XRFdc_DACBlock_DigitalDataPath
XRFdc_DACBlock_DigitalDataPath = handle.GetStruct_XRFdc_DACBlock_DigitalDataPath()
print(XRFdc_DACBlock_DigitalDataPath)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADCBlock_AnalogDataPath

# XRFdc_ADCBlock_AnalogDataPath
XRFdc_ADCBlock_AnalogDataPath = handle.GetStruct_XRFdc_ADCBlock_AnalogDataPath()
print(XRFdc_ADCBlock_AnalogDataPath)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADCBlock_DigitalDataPath

# XRFdc_ADCBlock_DigitalDataPath
XRFdc_ADCBlock_DigitalDataPath = handle.GetStruct_XRFdc_ADCBlock_DigitalDataPath()
print(XRFdc_ADCBlock_DigitalDataPath)

#Description:
#   Return Dictionary equivalent of structure XRFdc_DAC_Tile
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_DAC_Tile

# XRFdc_DAC_Tile
XRFdc_DAC_Tile = handle.GetStruct_XRFdc_DAC_Tile()
print(XRFdc_DAC_Tile)

#Description:
#   Return Dictionary equivalent of structure XRFdc_ADC_Tile
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XRFdc_ADC_Tile

# XRFdc_ADC_Tile
XRFdc_ADC_Tile = handle.GetStruct_XRFdc_ADC_Tile()
print(XRFdc_ADC_Tile)

#Description:
#   Looks up the device configuration based on the unique device ID. A table
#   contains the configuration info for each device in the system.
#C header declaration:
#   XRFdc_Config *XRFdc_LookupConfig(u16 DeviceId);
#Input Arguments:
#   DeviceId: DeviceId contains the ID of the device to look up the configuration.
#Return:
#   ret: 0 on success, 1 on failure
#   config: XRFdc_Config container with values. Will be Null on failure.

#XRFdc_Config *XRFdc_LookupConfig(u16 DeviceId);
ret, Config = handle.XRFdc_LookupConfig(0)

#Description:
#   Register/open the device and map RFDC to the IO region.
#C header declaration:
#   u32 XRFdc_RegisterMetal(XRFdc *InstancePtr, u16 DeviceId, struct metal_device **DevicePtr);
#Input Arguments:
#   DeviceId: DeviceId contains the ID of the device to register/map
#Return:
#   ret: XRFDC_SUCCESS on success, XRFDC_FAILURE if error occurs
#   inst_id: integer handle to the initialized instance

ret, inst_id = handle.XRFdc_RegisterMetal(0)

#Description:
#   Initializes a specific XRFdc instance such that the driver is ready to use.
#C header declaration:
#   u32 XRFdc_CfgInitialize(XRFdc *InstancePtr, XRFdc_Config *ConfigPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Config: DeviceId contains the ID of the device to look up the configuration.
#Return:
#   ret: XRFDC_SUCCESS if successful.
#   Config: XRFdc_Config container with values. Will be same as passed value

ret, Config = handle.XRFdc_CfgInitialize(inst_id, Config)

#Description:
#   The API Restarts the requested tile. It can restart a single tile and
#   alternatively can restart all the tiles. Existing register settings are not
#   lost or altered in the process. It just starts the requested tile(s).
#C header declaration:
#   u32 XRFdc_StartUp(XRFdc *InstancePtr, u32 Type, int Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3 and -1
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_StartUp(inst_id, 0, 0)

#Description:
#   The API stops the tile as requested. It can also stop all the tiles if
#   asked for. It does not clear any of the existing register settings. It just
#   stops the requested tile(s).
#C header declaration:
#   u32 XRFdc_Shutdown(XRFdc *InstancePtr, u32 Type, int Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3, and -1
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_Shutdown(inst_id, 0, 0)

#Description:
#   The API resets the requested tile. It can reset all the tiles as well. In
#   the process, all existing register settings are cleared and are replaced
#   with the settings initially configured (through the GUI).
#C header declaration:
#   u32 XRFdc_Reset(XRFdc *InstancePtr, u32 Type, int Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3, and -1.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_Reset(inst_id, 0, 0)

#Description:
#   The API starts the requested tile from a provided state and runs to the given
#   end state. It can restart a single tile and alternatively can restart all the
#   tiles. If starting from/ending at XRFDC_START_STATE_OFF/XRFDC_END_STATE_OFF,
#   register settings will be wiped.
#C header declaration:
#   u32 XRFdc_CustomStartUp(XRFdc *InstancePtr, u32 Type, int Tile_Id, u32 StartState, u32 EndState);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3, and -1.
#   StartState: StartState Valid values are XRFDC_START_STATE_*.
#   EndState: EndState Valid values are XRFDC_END_STATE_*.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

#ret = handle.XRFdc_CustomStartUp(0, 0, 0, 0)#TODO-TEST

#Description:
#   This function is used to wait for a tile to reach a given state.
#C header declaration:
#   u32 XRFdc_WaitForState(XRFdc *InstancePtr, u32 Type, u32 Tile, u32 State);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: represents ADC or DAC.
#   Tile_Id: Valid values are 0-3.
#   State: represents the state which the tile must reach.
#Return:
#   ret: XRFDC_SUCCESS if valid, XRFDC_FAILURE if not valid.

#ret = handle.XRFdc_WaitForState(0, 0, 0) #TODO-TEST

#Description:
#   The API returns the IP status.
#C header declaration:
#   u32 XRFdc_GetIPStatus(XRFdc *InstancePtr, XRFdc_IPStatus *IPStatusPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#Return:
#   ret: XRFDC_SUCCESS if successful
#   IPStatus: Dictionary equivalent to XRFdc_IPStatus structure

ret, IPStatus = handle.XRFdc_GetIPStatus(inst_id)

#Description:
#   The API returns the requested block status.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_GetBlockStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_BlockStatus *BlockStatusPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled.
#   BlockStatus: Dictionary equivalent of XRFdc_BlockStatus structure
#                through which the ADC/DAC block status is returned.

ret, BlockStatus = handle.XRFdc_GetBlockStatus(inst_id, 0, 0, 0)

#Description:
#   The API is used to update various mixer settings, fine, coarse, NCO etc.
#   Mixer/NCO settings passed are used to update the corresponding
#   block level registers. Driver structure is updated with the new values.
#C header declaration:
#   u32 XRFdc_SetMixerSettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
#   XRFdc_Mixer_Settings *MixerSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   MixerSettings: Dictionary in which the Mixer/NCO settings are passed
#       FineMixerScale in Mixer_Settings dictionary can have 3 values.
#       XRFDC_MIXER_SCALE_* represents the valid values.
#       XRFDC_MIXER_SCALE_AUTO - If mixer mode is R2C, Mixer Scale is
#       set to 1 and for other modes mixer scale is set to 0.7
#       XRFDC_MIXER_SCALE_1P0 - To set fine mixer scale to 1.
#       XRFDC_MIXER_SCALE_0P7 - To set fine mixer scale to 0.7.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   MixerSettings: Dictionary in which the Mixer/NCO settings are passed

MixerSettings = {
    "Freq": 1.0,
    "PhaseOffset": 0.0,
    "EventSource": 0,
    "CoarseMixFreq": 0,
    "MixerMode": 0,
    "FineMixerScale": 0,
    "MixerType": 0,
}
ret, MixerSettings = handle.XRFdc_SetMixerSettings(
    inst_id, 0, 0, 0, MixerSettings
)

#Description:
#   The API returns back Mixer/NCO settings to the caller.
#C header declaration:
#   u32 XRFdc_GetMixerSettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
#   XRFdc_Mixer_Settings *MixerSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#    ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#    MixerSettings: Dictionary in which the Mixer/NCO settings are passed
#       FineMixerScale in Mixer_Settings dictionary can have 3 values.
#       XRFDC_MIXER_SCALE_* represents the valid values.
#       XRFDC_MIXER_SCALE_AUTO - If mixer mode is R2C, Mixer Scale is
#       set to 1 and for other modes mixer scale is set to 0.7
#       XRFDC_MIXER_SCALE_1P0 - To set fine mixer scale to 1.
#       XRFDC_MIXER_SCALE_0P7 - To set fine mixer scale to 0.7.

ret, MixerSettings = handle.XRFdc_GetMixerSettings(inst_id, 0, 0, 0)

#Description:
#   This API is used to update various QMC settings, eg gain, phase, offset etc.
#   QMC settings passed are used to update the corresponding
#   block level registers. Driver structure is updated with the new values.
#C header declaration:
#   u32 XRFdc_SetQMCSettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_QMC_Settings *QMCSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   QMCSettings: Dictionary equivalent of XRFdc_QMC_Settings structure
#                in which the QMC settings are passed.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

QMCSettings = {
    "EnablePhase": 0,
    "EnableGain": 0,
    "GainCorrectionFactor": 0.0,
    "PhaseCorrectionFactor": 0.0,
    "OffsetCorrectionFactor": 0,
    "EventSource": 0,
}
ret, QMCSettings = handle.XRFdc_SetQMCSettings(inst_id, 0, 0, 0, QMCSettings)

#Description:
#   QMC settings are returned back to the caller through this API.
#C header declaration:
#   u32 XRFdc_GetQMCSettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_QMC_Settings *QMCSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   QMC_Settings: Dictionary equivalent of XRFdc_QMC_Settings structure
#                 in which the QMC settings are passed.

ret, QMCSettings = handle.XRFdc_GetQMCSettings(inst_id, 0, 0, 0)

#Description:
#   Coarse delay settings are returned back to the caller.
#C header declaration:
#   u32 XRFdc_GetCoarseDelaySettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
#	XRFdc_CoarseDelay_Settings *CoarseDelaySettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
#                        structure in which the CoarseDelay settings are passed.

ret, CoarseDelaySettings = handle.XRFdc_GetCoarseDelaySettings(inst_id, 0, 0, 0)

#Description:
#   Coarse delay settings passed are used to update the corresponding
#   block level registers. Driver structure is updated with the new values.
#C header declaration:
#   u32 XRFdc_SetCoarseDelaySettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
# 	XRFdc_CoarseDelay_Settings *CoarseDelaySettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
#                        structure in which the CoarseDelay settings are passed.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

CoarseDelaySettings = {"CoarseDelay": 0, "EventSource": 0}
ret, CoarseDelaySettings = handle.XRFdc_SetCoarseDelaySettings(
    inst_id, 0, 0, 0, CoarseDelaySettings
)

#Description:
#   Coarse delay settings are returned back to the caller.
#C header declaration:
#   u32 XRFdc_GetCoarseDelaySettings(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id,
#   XRFdc_CoarseDelay_Settings *CoarseDelaySettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   CoarseDelaySettings: Dictionary equivalent of XRFdc_CoarseDelay_Settings
#                        structure in which the CoarseDelay settings are passed.

ret, CoarseDelaySettings = handle.XRFdc_GetCoarseDelaySettings(
    inst_id, 0, 0, 0
)

#Description:
#   Interpolation factor are returned back to the caller.
#C header declaration:
#   u32 XRFdc_GetInterpolationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *InterpolationFactorPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   InterpolationFactor: the interpolation factor for DAC blocks.

ret, InterpolationFactor = handle.XRFdc_GetInterpolationFactor(
    inst_id, 0, 0
)

#Description:
#   Decimation factor are returned back to the caller for both actual and
#   observation FIFO.
#C header declaration:
#   u32 XRFdc_GetDecimationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *DecimationFactorPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   DecimationFactor: the decimation factor for DAC blocks.

ret, DecimationFactor = handle.XRFdc_GetDecimationFactor(inst_id, 0, 0)

#Description:
#
#C header declaration:
#   u32 XRFdc_GetDecimationFactorObs(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *DecimationFactorPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#

ret, DecimationFactor = handle.XRFdc_GetDecimationFactorObs(inst_id, 0, 0)

#Description:
#   This function returns the the number of fabric write valid words requested
#   for the block. For ADCs this is for both the actual and observation FIFO.
#   ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_GetFabWrVldWords(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   FabricDataRate: Fabric data rate for DAC block

#u32 XRFdc_GetFabWrVldWords(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
ret, FabricDataRate = handle.XRFdc_GetFabWrVldWords(inst_id, 0, 0, 0)

#Description:
#   This API returns the number of fabric write valid words requested
#   for the block. This is for the observation FIFO.
#C header declaration:
#   u32 XRFdc_GetFabWrVldWordsObs(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   FabricDataRate:  fabric data rate for DAC block

ret, FabricDataRate = handle.XRFdc_GetFabWrVldWordsObs(inst_id, 0, 0, 0)

#Description:
#   This function returns the number of fabric read valid words requested
#   for the block. For ADCs this is for both the actual and observation FIFO.
#C header declaration:
#   u32 XRFdc_GetFabRdVldWords(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   FabricDataRate: Fabric data rate for ADC/DAC block

ret, FabricDataRate = handle.XRFdc_GetFabRdVldWords(inst_id, 0, 0, 0)

#Description:
#   This function returns the number of fabric read valid words requested
#   for the block. This is for the observation FIFO.
#C header declaration:
#   u32 XRFdc_GetFabRdVldWordsObs(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *FabricDataRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   FabricDataRate: Fabric data rate for ADC/DAC block

ret, FabricDataRate = handle.XRFdc_GetFabRdVldWordsObs(inst_id, 0, 0, 0)

#Description:
#   Fabric data rate for the requested ADC block is set by writing to the
#   corresponding register. The function writes the number of valid read words
#   for the requested ADC block.
#C header declaration:
#   u32 XRFdc_SetFabRdVldWords(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 FabricRdVldWords);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   FabricRdVldWords: Read fabric rate to be set for ADC block.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetFabRdVldWords(inst_id, 0, 0, 0)

#Description:
#   Fabric data rate for the requested ADC block is set by writing to the
#   corresponding register. The function writes the number of valid read words
#   for the requested ADC block. This is for the observation FIFO.
#C header declaration:
#   u32 XRFdc_SetFabRdVldWordsObs(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 FabricRdVldWords);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   FabricRdVldWords: Read fabric rate to be set for ADC block.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetFabRdVldWordsObs(inst_id, 0, 0, 0)

#Description:
#   Fabric data rate for the requested DAC block is set by writing to the
#   corresponding register. The function writes the number of valid write words
#   for the requested DAC block.
#C header declaration:
#   u32 XRFdc_SetFabWrVldWords(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 FabricWrVldWords);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   FabricWrVldWords: write fabric rate to be set for DAC block
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetFabWrVldWords(inst_id, 0, 0, 0)

#Description:
#   Threshold settings are read from the corresponding registers and are passed
#   back to the caller. There can be two threshold settings:
#   threshold0 and threshold1. Both of them are independent of each other.
#   The function returns the requested threshold (which can be threshold0,
#   threshold1, or both.
#C header declaration:
#   u32 XRFdc_GetThresholdSettings(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id,
# 	XRFdc_Threshold_Settings *ThresholdSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   ThresholdSettings:  the register settings for thresholds are passed back

ret, ThresholdSettings = handle.XRFdc_GetThresholdSettings(inst_id, 0, 0)

#Description:
#   Threshold settings are updated into the relevant registers. Driver structure
#   is updated with the new values. There can be two threshold settings:
#   threshold0 and threshold1. Both of them are independent of each other.
#   The function returns the requested threshold (which can be threshold0,
#   threshold1, or both.
#   Only ADC blocks
#C header declaration:
#   u32 XRFdc_SetThresholdSettings(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id,
# 	XRFdc_Threshold_Settings *ThresholdSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   ThresholdSettings: the register settings
#                      for thresholds are passed to the API
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   ThresholdSettings: the register settings for thresholds are passed back

ThresholdSettings = {
    "UpdateThreshold": 4,
    "ThresholdMode": [0, 0],
    "ThresholdAvgVal": [0, 0],
    "ThresholdUnderVal": [0, 0],
    "ThresholdOverVal": [0, 0],
}
ret, ThresholdSettings = handle.XRFdc_SetThresholdSettings(
    inst_id, 0, 0, ThresholdSettings
)

#Description:
#   Decoder mode is updated into the relevant registers. Driver structure is
#   updated with the new values.
#   Only DAC blocks
#C header declaration:
#   u32 XRFdc_SetDecoderMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 DecoderMode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   DecoderMode: DecoderMode Valid values are 1 (Maximum SNR, for non-
#                randomized decoder), 2 (Maximum Linearity, for randomized decoder)
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetDecoderMode(inst_id, 0, 0, 0)

#Description:
#   This function will trigger the update event for an event.
#C header declaration:
#   u32 XRFdc_UpdateEvent(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 Event);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Event: Event is for which dynamic update event will trigger.
#          XRFDC_EVENT_* defines the different events.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_UpdateEvent(inst_id, 0, 0, 0, 0)

#Description:
#   Decoder mode is read and returned back.
#C header declaration:
#   u32 XRFdc_GetDecoderMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *DecoderModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   DecoderMode: Valid values are 1 (Maximum SNR, for non-randomized
#                decoder), 2 (Maximum Linearity, for randomized decoder)

ret, DecoderMode = handle.XRFdc_GetDecoderMode(inst_id, 0, 0)

#Description:
#   Resets the NCO phase of the current block phase accumulator.
#C header declaration:
#   u32 XRFdc_ResetNCOPhase(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_ResetNCOPhase(inst_id, 0, 0, 0)

#Description:
#   This Prints the offset of the register along with the content. This API is
#   meant to be used for debug purposes. It prints to the console the contents
#   of registers for the passed Tile_Id. If -1 is passed, it prints the contents
#   of the registers for all the tiles for the respective ADC or DAC
#C header declaration:
#   void XRFdc_DumpRegs(XRFdc *InstancePtr, u32 Type, int Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   None

handle.XRFdc_DumpRegs(inst_id, 0, 0)

#Description:
#   User-level API to setup multiband configuration.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_MultiBand(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 DigitalDataPathMask, u32 MixerInOutDataType,
#   u32 DataConverterMask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   DigitalDataPathMask: DigitalDataPathMask is the DataPath mask. First 4 bits represent
#                        4 data paths, 1 means enabled and 0 means disabled.
#   MixerInOutDataType: MixerInOutDataType is mixer data type, valid values are XRFDC_MB_DATATYPE_*
#   DataConverterMask: DataConverterMask is block enabled mask (input/output driving
#                      blocks). 1 means enabled and 0 means disabled.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_MultiBand(inst_id, 0, 0, 0, 0, 0)

#Description:
#   Get Data Converter connected for digital data path I
#C header declaration:
#   int XRFdc_GetConnectedIData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)

ret = handle.XRFdc_GetConnectedIData(inst_id, 0, 0, 0)

#Description:
#    Get Data Converter connected for digital data path Q
#C header declaration:
#   int XRFdc_GetConnectedQData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return Data converter Id. (XRFDC_BLK_ID_NONE if converter type, tile or block number is invalid)

ret = handle.XRFdc_GetConnectedQData(inst_id, 0, 0, 0)

#Description:
#   Set Data Converter connected for digital data path I and Q
#C header declaration:
#   void XRFdc_SetConnectedIQData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, int ConnectedIData,
# 	int ConnectedQData);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: #TODO
#   ConnectedIData: ConnectedIData is Converter Id to which DigitalPathI connected.
#   ConnectedQData: ConnectedQData is Converter Id to which DigitalPathQ connected.
#Return:
#   None

ret = handle.XRFdc_SetConnectedIQData(inst_id, 0, 0, 0, 0, 0)

#Description:
#   This function is the interrupt handler for the driver.
#   It must be connected to an interrupt system by the application such that it
#   can be called when an interrupt occurs.
#C header declaration:
#   u32 XRFdc_IntrHandler(u32 Vector, void *XRFdcPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Vector: Vector is interrupt vector number. Libmetal status handler
#           expects two parameters in the handler prototype, hence
#           kept this parameter. This is not used inside
#           the interrupt handler API.
#Return:
#   None

#u32 XRFdc_IntrHandler(u32 Vector, void *XRFdcPtr); #TODO

#Description:
#   This function clear the interrupts.
#C header declaration:
#   u32 XRFdc_IntrClr(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   IntrMask: IntrMask contains the interrupts to be cleared.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = handle.XRFdc_IntrClr(inst_id, 0, 0, 0, 0)

#Description:
#   This function returns the interrupt status read from Interrupt Status
#   Register(ISR).
#C header declaration:
#   u32 XRFdc_GetIntrStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *IntrStsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
#   IntrSts: the contents of the Interrupt Status Registers (FIFO interface,
#            Decoder interface, Data Path Interface).

ret, IntrSts = handle.XRFdc_GetIntrStatus(inst_id, 0, 0, 0)

#Description:
#   This function clears the interrupt mask.
#C header declaration:
#   u32 XRFdc_IntrDisable(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   IntrMask: IntrMask contains the interrupts to be disabled.
#             '1' disables an interrupt, and '0' remains no change.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = handle.XRFdc_IntrDisable(inst_id, 0, 0, 0, 0)

#Description:
#   This function sets the interrupt mask.
#C header declaration:
#   u32 XRFdc_IntrEnable(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 IntrMask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   IntrMask: IntrMask contains the interrupts to be enabled.
#             '1' enables an interrupt, and '0' disables.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.

ret = handle.XRFdc_IntrEnable(inst_id, 0, 0, 0, 0)

#Description:
#   This function gets a mask of enabled interrupts.
#C header declaration:
#   u32 XRFdc_GetEnabledInterrupts(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *IntrMask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not available.
#   IntrMask: mask of enabled interrupts.
#             '1' denotes an enabled interrupt, and '0' denotes a disabled interrupt

ret, IntrMask = handle.XRFdc_GetEnabledInterrupts(inst_id, 0, 0, 0)

#Description:
#   This API sets the threshold clear mode. The clear mode can be through
#   explicit DRP access (manual) or auto clear (QMC gain update event).
#   Only ADC blocks
#C header declaration:
#   u32 XRFdc_SetThresholdClrMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 ThresholdToUpdate, u32 ClrMode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   ThresholdToUpdate: Select which Threshold (Threshold0 or
#                      Threshold1 or both) to update.
#   ClrMode: ClrMode can be DRP access (manual) or auto clear (QMC gain
#            update event).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetThresholdClrMode(inst_id, 0, 0, 0, 0)

#Description:
#   This API is to clear the Sticky bit in threshold config registers.
#C header declaration:
#   u32 XRFdc_ThresholdStickyClear(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 ThresholdToUpdate);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   ThresholdToUpdate: Select which Threshold (Threshold0 or
#                      Threshold1 or both) to update.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_ThresholdStickyClear(inst_id, 1, 1, 0)

#Description:
#TODO
#C header declaration:
#   void XRFdc_SetStatusHandler(XRFdc *InstancePtr, void *CallBackRef, XRFdc_StatusHandler FunctionPtr);
#Input Arguments:
#
#Return:
#

ret = handle.XRFdc_SetStatusHandler()

#Description:
#   Enable and Disable the ADC/DAC FIFO. For ADCs this is for the actual and
#   observation FIFO.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_SetupFIFO(XRFdc *InstancePtr, u32 Type, int Tile_Id, u8 Enable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Enable: Enable valid values are 1 (FIFO enable) and 0 (FIFO Disable)
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetupFIFO(inst_id, 0, 0, 0)

#Description:
#   Enable and Disable the ADC/DAC FIFO.
#   For ADCs this is for the observtion FIFO.
#C header declaration:
#   u32 XRFdc_SetupFIFOObs(XRFdc *InstancePtr, u32 Type, int Tile_Id, u8 Enable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetupFIFOObs(inst_id, 0, 0, 0)

#Description:
#   Enable and Disable the ADC/DAC FIFO.
#   For ADCs this is for the observtion FIFO.
#C header declaration:
#   u32 XRFdc_SetupFIFOBoth(XRFdc *InstancePtr, u32 Type, int Tile_Id, u8 Enable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetupFIFOBoth(inst_id, 0, 0, 0)

#Description:
#   Current status of ADC/DAC FIFO. For ADCs this is for both the actual and
#   observations FIFOs.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_GetFIFOStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 *EnablePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)

ret, Enable = handle.XRFdc_GetFIFOStatus(inst_id, 0, 0)

#Description:
#   Current status of ADC/DAC FIFO. This is for both the actual and
#   observations FIFOs. ADC blocks only
#C header declaration:
#   u32 XRFdc_GetFIFOStatusObs(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 *EnablePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   Enable: valid values are 1 (FIFO enable) and 0 (FIFO Disable)

ret, Enable = handle.XRFdc_GetFIFOStatusObs(inst_id, 0, 0)

#Description:
#   Set the Nyquist zone.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_SetNyquistZone(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 NyquistZone);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   NyquistZone: valid values are 1 (Odd),2 (Even).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetNyquistZone(inst_id, 0, 0, 0, 0)

#Description:
#   Get the Nyquist zone.
#   Common API for ADC/DAC blocks
#C header declaration:
#   u32 XRFdc_GetNyquistZone(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *NyquistZonePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   NyquistZone: returned Nyquist zone

ret, NyquistZone = handle.XRFdc_GetNyquistZone(inst_id, 0, 0, 0)

#Description:
#   Get Output Current for DAC block.
#C header declaration:
#   u32 XRFdc_GetOutputCurr(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *OutputCurrPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.
#   OutputCurr: Return Output Current for DAC block

ret, OutputCurr = handle.XRFdc_GetOutputCurr(inst_id, 0, 0)

#Description:
#   This API is to set the decimation factor and also update the FIFO write
#   words w.r.t to decimation factor.
#C header declaration:
#   u32 XRFdc_SetDecimationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 DecimationFactor);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   DecimationFactor: DecimationFactor to be set for DAC block.
#                     XRFDC_INTERP_DECIM_* defines the valid values.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetDecimationFactor(inst_id, 0, 0, 0)

#Description:
#   This API is to set the decimation factor and also update the FIFO write
#   words w.r.t to decimation factor for the observation FIFO.
#C header declaration:
#   u32 XRFdc_SetDecimationFactorObs(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 DecimationFactor);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   DecimationFactor: DecimationFactor to be set for DAC block.
#                     XRFDC_INTERP_DECIM_* defines the valid values.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetDecimationFactorObs(inst_id, 0, 0, 0)

#Description:
#   This API is to set the interpolation factor and also update the FIFO read
#   words w.r.t to interpolation factor.
#   Only DAC blocks
#C header declaration:
#   u32 XRFdc_SetInterpolationFactor(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 InterpolationFactor);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   InterpolationFactor: InterpolationFactor to be set for DAC block.
#                        XRFDC_INTERP_DECIM_* defines the valid values.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetInterpolationFactor(inst_id, 0, 0, 0)

#Description:
#   This API is to set the divider for clock fabric out.
#   ADC and DAC Tiles
#C header declaration:
#   u32 XRFdc_SetFabClkOutDiv(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u16 FabClkDiv);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   FabClkDiv: FabClkDiv to be set for a tile.
#              XRFDC_FAB_CLK_* defines the valid divider values.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetFabClkOutDiv(inst_id, 0, 0, 0)

#Description:
#   This API is to set the Calibration mode.
#   Only for ADC blocks
#C header declaration:
#   u32 XRFdc_SetCalibrationMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u8 CalibrationMode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CalibrationMode: valid values are 1 and 2.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetCalibrationMode(inst_id, 0, 0, 0)

#Description:
#   This API is to get the Calibration mode.
#   Only for ADC blocks
#C header declaration:
#   u32 XRFdc_GetCalibrationMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u8 *CalibrationModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   CalibrationMode: calibration mode

ret, CalibrationMode = handle.XRFdc_GetCalibrationMode(inst_id, 0, 0)

#Description:
#   This function gets Clock source
#C header declaration:
#   u32 XRFdc_GetClockSource(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 *ClockSourcePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   ClockSource: return the clock source

ret, ClockSource = handle.XRFdc_GetClockSource(inst_id, 0, 0)

#Description:
#   This function gets PLL lock status
#C header declaration:
#   u32 XRFdc_GetPLLLockStatus(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 *LockStatusPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   LockStatus: return the PLL lock status

ret, LockStatus = handle.XRFdc_GetPLLLockStatus(inst_id, 0, 0)

#Description:
#   This API is used to get the PLL Configurations.
#C header declaration:
#   u32 XRFdc_GetPLLConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, XRFdc_PLL_Settings *PLLSettings);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   PLLSettings: dictionary equivalent of XRFdc_PLL_Settings structure to get
#                the PLL configurations

ret, PLLSettings = handle.XRFdc_GetPLLConfig(inst_id, 0, 0)

#Description:
#   This function used for dynamically switching between internal PLL and
#   external clock source and configuring the internal PLL
#   This API enables automatic selection of the VCO which will work in
#   IP version 2.0.1 and above. Using older version of IP this API is
#   not likely to work.
#C header declaration:
#   u32 XRFdc_DynamicPLLConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u8 Source, double RefClkFreq,
# 	double SamplingRate);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Source: Clock source internal PLL or external clock source
#   RefClkFreq: Reference Clock Frequency in MHz(102.40625MHz - 1.2GHz)
#   SamplingRate: Sampling Rate in MHz(0.1- 6.554GHz for DAC and
#   0.5/1.0 - 2.058/4.116GHz for ADC based on the device package).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_DynamicPLLConfig(inst_id, 0, 0, 0, 0, 0)

#Description:
#   This API is used to set the mode for the Inverse-Sinc filter.
#   Only DAC blocks
#C header declaration:
#   u32 XRFdc_SetInvSincFIR(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u16 Mode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Mode: Mode valid values are 0(disable),  1(1st Nyquist zone)
#         and 2(2nd Nyquist zone).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if block not enabled/invalid mode.

ret = handle.XRFdc_SetInvSincFIR(inst_id, 0, 0, 0)

#Description:
#   This API is used to get the Inverse-Sinc filter mode.
#   Only DAC blocks
#C header declaration:
#   u32 XRFdc_GetInvSincFIR(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u16 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: return the inv-sinc status. valid values
#         are 0(disable),  1(1st Nyquist zone) and 2(2nd Nyquist zone).

ret, Mode = handle.XRFdc_GetInvSincFIR(inst_id, 0, 0)

#Description:
#   This function is used to get the Coupling mode.
#C header declaration:
#   u32 XRFdc_GetCoupling(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
#   Tile_Id: Tile_Id indicates Tile number.
#   Block_Id: indicates Block number.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: return the link coupling mode

ret, Mode = handle.XRFdc_GetCoupling(inst_id, 0, 0, 0)

#Description:
#   This function is used to get the Link Coupling mode.
#C header declaration:
#   u32 XRFdc_GetLinkCoupling(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: return the link coupling mode

ret, Mode = handle.XRFdc_GetLinkCoupling(inst_id, 0, 0)

#Description:
#   This API is to get the divider for clock fabric out.
#   API is applicable for both ADC and DAC Tiles
#C header declaration:
#   u32 XRFdc_GetFabClkOutDiv(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u16 *FabClkDivPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   FabClkDiv: fabric clock for a tile. XRFDC_FAB_CLK_* defines the valid divider values.

ret, FabClkDiv = handle.XRFdc_GetFabClkOutDiv(inst_id, 0, 0)

#Description:
#   This function is used to set the IM3 Dither mode.
#C header declaration:
#   u32 XRFdc_SetDither(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Mode: set the link coupling mode
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_SetDither(inst_id, 0, 0, 0)

#Description:
#    This function is used to get the IM3 Dither mode.
#C header declaration:
#   u32 XRFdc_GetDither(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: get link coupling mode

ret, Mode = handle.XRFdc_GetDither(inst_id, 0, 0)

#Description:
#   This function is used to set the clock distribution
#C header declaration:
#   u32 XRFdc_SetClkDistribution(XRFdc *InstancePtr, XRFdc_Distribution_Settings *DistributionSettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   DistributionSettings: distribution settings dictionary
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if could not set distribution
#   DistributionSettings: Dictionary equivalent of XRFdc_Distribution_Settings

DistributionSettings = handle.GetStruct_XRFdc_Distribution_Settings()
ret, DistributionSettings = handle.XRFdc_SetClkDistribution(inst_id, DistributionSettings)

#Description:
#   This function is used to get the clock distribution
#C header declaration:
#   u32 XRFdc_GetClkDistribution(XRFdc *InstancePtr, XRFdc_Distribution_System_Settings *DistributionArrayPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if no valid distribution found.
#   DistributionSystemSettings: Dictionary equivalent of XRFdc_Distribution_Settings

ret, DistributionSystemSettings = handle.XRFdc_GetClkDistribution(inst_id)

#Description:
#   This API is to set the DAC Datapath mode.
#C header declaration:
#   u32 XRFdc_SetDataPathMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Mode: Mode valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / out of range.

ret = handle.XRFdc_SetDataPathMode(inst_id, 0, 0, 0)

#Description:
#   This API is to get the DAC Datapath mode.
#   This is only for DAC blocks
#C header declaration:
#   u32 XRFdc_GetDataPathMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: valid values are 0-3

ret, Mode = handle.XRFdc_GetDataPathMode(inst_id, 0, 0)

#Description:
#   This API is to set the DAC Image Reject Filter Pass mode.
#C header declaration:
#   u32 XRFdc_SetIMRPassMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Mode);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Mode: valid values are 0 (for low pass) 1 (for high pass).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled / bad parameter passed

ret = handle.XRFdc_SetIMRPassMode(inst_id, 0, 0, 0)

#Description:
#   This API is to get the DAC Image Reject Filter Pass mode.
#   This is only for DAC blocks
#C header declaration:
#   u32 XRFdc_GetIMRPassMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *ModePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Mode: 0 (for low pass) 1 (for high pass)

ret, Mode = handle.XRFdc_GetIMRPassMode(inst_id, 0, 0)

#Description:
#   This function is used to set the ADC Signal Detector Settings.
#C header declaration:
#   u32 XRFdc_SetSignalDetector(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Signal_Detector_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Settings: signal detector configurations dictionary
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if tile not enabled, or invalid values.
#   Settings: dictionary equivalent of XRFdc_Signal_Detector_Settings structure

Settings = {
    "Mode": 0,
    "TimeConstant": 0,
    "Flush": 0,
    "EnableIntegrator": 0,
    "Threshold": 0,
    "ThreshOnTriggerCnt": 0,
    "ThreshOffTriggerCnt": 0,
    "HysteresisEnable": 0,    
}
ret, Settings = handle.XRFdc_SetSignalDetector(inst_id, 0, 0, Settings)

#Description:
#   This function is used to get the ADC Signal Detector Settings.
#   This is only for DAC blocks
#C header declaration:
#   u32 XRFdc_GetSignalDetector(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Signal_Detector_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Settings: dictionary equivalent of XRFdc_Signal_Detector_Settings structure

ret, Settings = handle.XRFdc_GetSignalDetector(inst_id, 0, 0)

#Description:
#   This function is used to disable Calibration Coefficients override.
#   Only for ADC blocks
#C header declaration:
#   u32 XRFdc_DisableCoefficientsOverride(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CalibrationBlock: indicates the calibration block
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_DisableCoefficientsOverride(inst_id, 0, 0, 0)

#Description:
#   This function is used to set the ADC Calibration Coefficients.
#C header declaration:
#   u32 XRFdc_SetCalCoefficients(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock,
# 	XRFdc_Calibration_Coefficients *CoeffPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CalibrationBlock: indicates the block to be written to
#   Coeff: dictionary to the XRFdc_Calibration_Coefficients structure to set the calibration coefficients
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients

Coeff = {
    "Coeff0": 65484,
    "Coeff1": 65482,
    "Coeff2": 25,
    "Coeff3": 65514,
    "Coeff4": 0,
    "Coeff5": 0,
    "Coeff6": 0,
    "Coeff7": 0,
}
ret, Coeff = handle.XRFdc_SetCalCoefficients(inst_id, 0, 0, 0, Coeff)

#Description:
#   This function is used to get the ADC Calibration Coefficients.
#C header declaration:
#   u32 XRFdc_GetCalCoefficients(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 CalibrationBlock,
# 	XRFdc_Calibration_Coefficients *CoeffPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CalibrationBlock: indicates the block to be read from
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Coeff: Dictionary equivalent of XRFdc_Calibration_Coefficients structure to get the calibration coefficients

ret, Coeff = handle.XRFdc_GetCalCoefficients(inst_id, 0, 0, 0)

#Description:
#   This function is used to set calibration freeze settings.
#C header declaration:
#   u32 XRFdc_SetCalFreeze(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Cal_Freeze_Settings *CalFreezePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure

CalFreeze = {"CalFrozen": 0, "DisableFreezePin": 0, "FreezeCalibration": 0}
ret, CalFreeze = handle.XRFdc_SetCalFreeze(inst_id, 0, 0, CalFreeze)

#Description:
#   This function is used to get calibration freeze settings and status.
#   Only for ADC blocks
#C header declaration:
#   u32 XRFdc_GetCalFreeze(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_Cal_Freeze_Settings *CalFreezePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   CalFreeze: Dictionary equivalent of XRFdc_Cal_Freeze_Settings structure

ret, CalFreeze = handle.XRFdc_GetCalFreeze(inst_id, 0, 0)

#Description:
#   Set Output Current for DAC block.
#   Range 6425 - 32000 uA with 25 uA resolution.
#C header declaration:
#   u32 XRFdc_SetDACVOP(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 uACurrent);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   uACurrent: the current in uA.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_SetDACVOP(inst_id, 0, 0, 0)

#Description:
#   Sets VOP compatibility mode.
#C header declaration:
#   u32 XRFdc_SetDACCompMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Enable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Enable:  filled with whether the mode is enabled (1) or disabled(0).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_SetDACCompMode(inst_id, 0, 0, 0)

#Description:
#   Gets VOP compatibility mode.
#C header declaration:
#   u32 XRFdc_GetDACCompMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *EnabledPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Enabled: filled with whether the mode is enabled (1) or disabled(0).

ret, Enabled = handle.XRFdc_GetDACCompMode(inst_id, 0, 0)

#Description:
#   Set DSA for ADC block.
#   Range 0 - 11 dB with 0.5 dB resolution ES1 Si.
#   Range 0 - 27 dB with 1 dB resolution for Production Si.
#C header declaration:
#   u32 XRFdc_SetDSA(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_DSA_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Settings: Dictionary equivalent of XRFdc_DSA_Settings
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Settings: Dictionary equivalent of XRFdc_DSA_Settings

Settings = {"DisableRTS": 0, "Attenuation": -2.5}
ret, Settings = handle.XRFdc_SetDSA(inst_id, 0, 0, Settings)

#Description:
#   Get DSA for ADC block.
#C header declaration:
#   u32 XRFdc_GetDSA(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, XRFdc_DSA_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Settings: Dictionary equivalent of XRFdc_DSA_Settings

ret, Settings = handle.XRFdc_GetDSA(inst_id, 0, 0)

#Description:
#   Set The Power up/down mode of a given converter.
#C header declaration:
#   u32 XRFdc_SetPwrMode(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_Pwr_Mode_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Settings: Dictionary equivalent of XRFdc_DSA_Settings
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Settings: Dictionary equivalent of XRFdc_DSA_Settings

Settings = {
    "DisableIPControl": 0,
    "PwrMode": 0,
}
ret, Settings = handle.XRFdc_SetPwrMode(inst_id, 0, 0, 0, Settings)

#Description:
#   Get The Power up/down mode of a given converter.
#C header declaration:
#   u32 XRFdc_GetPwrMode(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, XRFdc_Pwr_Mode_Settings *SettingsPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3.
#   Settings: Dictionary equivalent of XRFdc_Pwr_Mode_Settings
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Settings: Dictionary equivalent of XRFdc_Pwr_Mode_Settings

Settings = {
    "DisableIPControl": 0,
    "PwrMode": 0,
}
ret, Settings = handle.XRFdc_SetPwrMode(inst_id, 0, 0, 0, Settings)

#Description:
#   Set the correct FIFO width for current mixer & rate change settings.
#C header declaration:
#   u32 XRFdc_ResetInternalFIFOWidth(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_ResetInternalFIFOWidth(inst_id, 0, 0, 0)

#Description:
#   Set the correct Observation FIFO width for current mixer & rate change settings.
#   ADC blocks only
#C header declaration:
#   u32 XRFdc_ResetInternalFIFOWidthObs(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs

ret = handle.XRFdc_ResetInternalFIFOWidthObs(inst_id, 0, 0)

#Description:
#   Execute Read modify Write
#C header declaration:
#   void XRFdc_ClrSetReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask, u16 Data);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   BaseAddr: Address of a block
#   RegAddr: Register offset value
#   Mask: Bit mask value
#   Data: Value to be written to register
#Return:
#   None

handle.XRFdc_ClrSetReg(inst_id, 0, 0, 0, 0)

#Description:
#   Execute Read and clear
#C header declaration:
#   void XRFdc_ClrReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   BaseAddr: Address of a block
#   RegAddr: Register offset value
#   Mask: Bit mask value
#Return:
#   None

handle.XRFdc_ClrReg(inst_id, 0, 0, 0)

#Description:
#   Execute Read and mask with the value
#C header declaration:
#   u16 XRFdc_RDReg(XRFdc *InstancePtr, u32 BaseAddr, u32 RegAddr, u16 Mask);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   BaseAddr: Address of a block
#   RegAddr: Register offset value
#   Mask: Bit mask value
#Return:
#   None

ret = handle.XRFdc_RDReg(inst_id, 0, 0, 0)

#Description:
#   Get ADC type is High Speed or Medium Speed
#C header declaration:
#   u32 XRFdc_IsHighSpeedADC(XRFdc *InstancePtr, u32 Tile);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3
#Return:
#   ret: 1 if ADC type is 4GSPS, otherwise 0 if quad or invalid tile.

ret = handle.XRFdc_IsHighSpeedADC(inst_id, 0)

#Description:
#   Checks whether DAC block is available or not
#C header declaration:
#   u32 XRFdc_IsDACBlockEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0 - 3
#Return:
#   ret: Return 1 if DAC block is available, otherwise 0

ret = handle.XRFdc_IsDACBlockEnabled(inst_id, 0, 0)

#Description:
#   Checks whether ADC block is available or not
#C header declaration:
#   u32 XRFdc_IsADCBlockEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return 1 if ADC block is available, otherwise 0

ret = handle.XRFdc_IsADCBlockEnabled(inst_id, 0, 0)

#Description:
#   Checks whether DAC Digital path is enabled or not
#C header declaration:
#   u32 XRFdc_IsDACDigitalPathEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return 1 if DAC digital path is enabled, otherwise 0

ret = handle.XRFdc_IsDACDigitalPathEnabled(inst_id, 0, 0)

#Description:
#   Checks whether ADC digital path is enabled or not
#C header declaration:
#   u32 XRFdc_IsADCDigitalPathEnabled(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return 1 if ADC digital path is enabled, otherwise 0.

ret = handle.XRFdc_IsADCDigitalPathEnabled(inst_id, 0, 0)

#Description:
#   Checks whether ADC/DAC Digital path is enabled or not
#C header declaration:
#   u32 XRFdc_CheckDigitalPathEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: XRFDC_SUCCESS if Digital path is enabled, XRFDC_FAILURE if Digital path is not enabled.

ret = handle.XRFdc_CheckDigitalPathEnabled(inst_id, 0, 0, 1)

#Description:
#   Get the RFDC IP Base Address
#C header declaration:
#   u32 XRFdc_Get_IPBaseAddr(XRFdc *InstancePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#Return:
#   ret: Return IP BaseAddress

ret = handle.XRFdc_Get_IPBaseAddr(inst_id)

#Description:
#   Get Tile BaseAddress
#C header declaration:
#   u32 XRFdc_Get_TileBaseAddr(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: Tile BaseAddress if valid, Return 0U if invalid/unavailable tile

ret = handle.XRFdc_Get_TileBaseAddr(inst_id, 0, 0)

#Description:
#   Get Block BaseAddress
#C header declaration:
#   u32 XRFdc_Get_BlockBaseAddr(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   :param inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Block BaseAddress, Return 0U if invalid/unavailable block

ret = handle.XRFdc_Get_BlockBaseAddr(inst_id, 0, 0, 0)

#Description:
#   Get Number of DAC Blocks enabled
#C header declaration:
#   u32 XRFdc_GetNoOfDACBlock(XRFdc *InstancePtr, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: number of DAC blocks enabled.

ret = handle.XRFdc_GetNoOfDACBlock(inst_id, 0)

#Description:
#   Get Number of ADC Blocks enabled.
#C header declaration:
#   u32 XRFdc_GetNoOfADCBlocks(XRFdc *InstancePtr, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: number of ADC blocks enabled.

ret = handle.XRFdc_GetNoOfADCBlocks(inst_id, 0)

#Description:
#   Get Mixer Input Data Type for ADC/DAC block.
#C header declaration:
#   u32 XRFdc_GetDataType(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: MixerInputDataType of ADC/DAC block. 0U if converter type, tile or block number is invalid

ret = handle.XRFdc_GetDataType(inst_id, 0, 0, 0)

#Description:
#   Get Data Width for ADC/DAC block.
#C header declaration:
#   u32 XRFdc_GetDataWidth(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile. Valid values are 0-3.
#Return:
#   ret: DataWidth of ADC/DAC block.

ret = handle.XRFdc_GetDataWidth(inst_id, 0, 0, 0)

#Description:
#   Get Inversesync filter for DAC block.
#C header declaration:
#   u32 XRFdc_GetInverseSincFilter(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Inversesync filter for DAC block. Return 0 if invalid

ret = handle.XRFdc_GetInverseSincFilter(inst_id, 0, 0)

#Description:
#   Get Mixed mode for DAC block.
#C header declaration:
#   u32 XRFdc_GetMixedMode(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: mixed mode for DAC block

ret = handle.XRFdc_GetMixedMode(inst_id, 0, 0)

#Description:
#   Get Master Tile for ADC/DAC tiles.
#C header declaration:
#   u32 XRFdc_GetMasterTile(XRFdc *InstancePtr, u32 Type);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#Return:
#   ret: Master Tile for ADC/DAC tiles. Returns XRFDC_TILE_ID_INV if converter type is invalid

ret = handle.XRFdc_GetMasterTile(inst_id, 0)

#Description:
#   Get Sysref source for ADC/DAC tile.
#C header declaration:
#   u32 XRFdc_GetSysRefSource(XRFdc *InstancePtr, u32 Type);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#Return:
#   ret: Sysref source for ADC/DAC tile. returns XRFDC_TILE_ID_INV if converter type is invalid

ret = handle.XRFdc_GetSysRefSource(inst_id, 0)

#Description:
#   Get Fabric Clock frequency.
#C header declaration:
#   double XRFdc_GetFabClkFreq(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3.
#Return:
#   ret: Fabric Clock frequency for ADC/DAC tile

ret = handle.XRFdc_GetFabClkFreq(inst_id, 0, 0)

#Description:
#   Get whether FIFO is enabled or not.
#C header declaration:
#   u32 XRFdc_IsFifoEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: Return 1 if FIFO is enabled, otherwise 0.

ret = handle.XRFdc_IsFifoEnabled(inst_id, 0, 0, 0)

#Description:
#   Set Data Converter connected for digital data path I and Q
#C header declaration:
#   void XRFdc_SetConnectedIQData(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id, int ConnectedIData,
#   int ConnectedQData);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: #TODO
#   ConnectedIData: ConnectedIData is Converter Id to which DigitalPathI connected.
#   ConnectedQData: ConnectedQData is Converter Id to which DigitalPathQ connected.
#Return:
#   None

ret = handle.XRFdc_SetConnectedIQData(inst_id, 0, 0, 0, 0, 0)

#Description:
#   Get Multiband Config data
#C header declaration:
#   u32 XRFdc_GetMultibandConfig(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: Multiband Configuration. Return 0 if invalid.

ret = handle.XRFdc_GetMultibandConfig(inst_id, 0, 0)

#Description:
#   Checks whether ADC/DAC block is enabled or not.
#C header declaration:
#   u32 XRFdc_CheckBlockEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, u32 Block_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#   Block_Id: Block_Id is ADC/DAC block number inside the tile.
#             Valid values are 0-3 in DAC/ADC-2GSPS and 0-1 in ADC-4GSPS
#Return:
#   ret: XRFDC_SUCCESS if block enabled, XRFDC_FAILURE if block is not enabled

ret = handle.XRFdc_CheckBlockEnabled(inst_id, 0, 0, 0)

#Description:
#   Checks whether ADC/DAC tile is enabled or not.
#C header declaration:
#   u32 XRFdc_CheckTileEnabled(XRFdc *InstancePtr, u32 Type, u32 Tile_Id);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if tile enabled, XRFDC_FAILURE if tile not enabled

ret = handle.XRFdc_CheckTileEnabled(inst_id, 0, 0)

#Description:
#   Gets ADC/DAC tile maximum sampling rate.
#C header declaration:
#   u32 XRFdc_GetMaxSampleRate(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, double *MaxSampleRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
#   Tile_Id: Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if found sampling rate, XRFDC_FAILURE if could not find sampling rate.
#   MaxSampleRate: maximum sample rate

ret, MaxSampleRate = handle.XRFdc_GetMaxSampleRate(inst_id, 0, 0)

#Description:
#   Gets ADC/DAC tile minimum sampling rate.
#C header declaration:
#   u32 XRFdc_GetMinSampleRate(XRFdc *InstancePtr, u32 Type, u32 Tile_Id, double *MinSampleRatePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC.
#   Tile_Id: Tile_Id Valid values are 0-3.
#Return:
#   ret: XRFDC_SUCCESS if found sampling rate XRFDC_FAILURE if could not find sampling rate.
#   MinSampleRate: minimum sample rate

ret, MinSampleRate = handle.XRFdc_GetMinSampleRate(inst_id, 0, 0)

#Description:
#   This API is used to get the driver version
#C header declaration:
#   double XRFdc_GetDriverVersion(void);
#Input Arguments:
#   None
#Return:
#   ret: Driver version number

version = handle.XRFdc_GetDriverVersion()

#Description:
#   This is the top level API which will be used for Multi-tile synchronization
#C header declaration:
#   u32 XRFdc_MultiConverter_Sync(XRFdc *InstancePtr, u32 Type, XRFdc_MultiConverter_Sync_Config *ConfigPtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: ADC or DAC. 0 for ADC and 1 for DAC
#   Config: Multi-tile sync config.
#Return:
#   ret: - XRFDC_MTS_OK if successful.
#        - XRFDC_MTS_TIMEOUT if timeout occurs.
#        - XRFDC_MTS_MARKER_RUN
#        - XRFDC_MTS_MARKER_MISM
#        - XRFDC_MTS_NOT_SUPPORTED if MTS is not supported.
#   Config: Multi-tile sync config.

Config = {
    "Offset": [0, 0, 0, 0],
    "Marker_Delay": 0,
    "Latency": [0, 0, 0, 0],
    "DTC_Set_T1": {
        "Num_Windows": [0, 0, 0, 0],
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "DTC_Code": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "Max_Overlap": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "RefTile": 0,
        "Min_Gap": [0, 0, 0, 0],
    },
    "SysRef_Enable": 0,
    "Target_Latency": 0,
    "Tiles": 0,
    "RefTile": 0,
    "DTC_Set_PLL": {
        "Num_Windows": [0, 0, 0, 0],
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "DTC_Code": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "Max_Overlap": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "RefTile": 0,
        "Min_Gap": [0, 0, 0, 0],
    },
}
ret, Config = handle.XRFdc_MultiConverter_Sync(inst_id, 0, Config)

#Description:
#   This API Initializes the multi-tile sync config structures.
#         Optionally allows target codes to be provided for the Pll/T1
#         analog sysref capture
#C header declaration:
#   u32 XRFdc_MultiConverter_Init(XRFdc_MultiConverter_Sync_Config *ConfigPtr, int *PLL_CodesPtr, int *T1_CodesPtr,
# 			      u32 RefTile);
#Input Arguments:
#   Config: Multi-tile sync config
#   PLL_Codes: PLL analog sysref capture.
#   T1_Codes: T1 analog sysref capture.
#Return:
#   Config: Multi-tile sync config
#   PLL_Codes: PLL analog sysref capture.
#   T1_Codes: T1 analog sysref capture.

Config = {
    "RefTile": 0,
    "Tiles": 0,
    "Target_Latency": 0,
    "Offset": [0, 0, 0, 0],
    "Latency": [0, 0, 0, 0],
    "Marker_Delay": 0,
    "SysRef_Enable": 0,
    "DTC_Set_PLL": {
        "RefTile": 0,
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "DTC_Code": [0, 0, 0, 0],
        "Num_Windows": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "Min_Gap": [0, 0, 0, 0],        
        "Max_Overlap": [0, 0, 0, 0],
    },
    "DTC_Set_T1": {
        "RefTile": 0,
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "DTC_Code": [0, 0, 0, 0],
        "Num_Windows": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "Min_Gap": [0, 0, 0, 0],        
        "Max_Overlap": [0, 0, 0, 0],
    },
}
PLL_Codes = [0, 0, 0, 0]
T1_Codes = [0, 0, 0, 0]
Config, PLL_Codes, T1_Codes = handle.XRFdc_MultiConverter_Init(
    Config, PLL_Codes, T1_Codes, 0
)
#Description:
#   This API is used to enable/disable the sysref.
#C header declaration:
#   u32 XRFdc_MTS_Sysref_Config(XRFdc *InstancePtr, XRFdc_MultiConverter_Sync_Config *DACSyncConfigPtr,
# 			    XRFdc_MultiConverter_Sync_Config *ADCSyncConfigPtr, u32 SysRefEnable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   DACSyncConfig: DAC Multi-Tile Sync config
#   ADCSyncConfig: ADC Multi-Tile Sync config structure
#   SysRefEnable: valid values are 0(disable) and 1(enable)
#Return:
#   ret: XRFDC_MTS_OK if successful.

ADCSyncConfig = DACSyncConfig = {
    "Offset": [0, 0, 0, 0],
    "Marker_Delay": 0,
    "Latency": [0, 0, 0, 0],
    "DTC_Set_T1": {
        "Num_Windows": [0, 0, 0, 0],
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "DTC_Code": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "Max_Overlap": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "RefTile": 0,
        "Min_Gap": [0, 0, 0, 0],
    },
    "SysRef_Enable": 0,
    "Target_Latency": 0,
    "Tiles": 0,
    "RefTile": 0,
    "DTC_Set_PLL": {
        "Num_Windows": [0, 0, 0, 0],
        "IsPLL": 0,
        "Target": [0, 0, 0, 0],
        "DTC_Code": [0, 0, 0, 0],
        "Scan_Mode": 0,
        "Max_Overlap": [0, 0, 0, 0],
        "Max_Gap": [0, 0, 0, 0],
        "RefTile": 0,
        "Min_Gap": [0, 0, 0, 0],
    },
}
ret, DACSyncConfig, ADCSyncConfig = handle.XRFdc_MTS_Sysref_Config(
    inst_id, DACSyncConfig, ADCSyncConfig, 0
)

#Description:
#  This API is used to enable/disable the sysref.
#C header declaration:
#   u32 XRFdc_GetMTSEnable(XRFdc *InstancePtr, u32 Type, u32 Tile, u32 *EnablePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: ADC or DAC. 0 for ADC and 1 for DAC.
#   Tile_Id: indicates Tile number (0-3).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_SUCCESS if error occurs.
#   Enable: valid values are 1 (enable) and 0 (disable).

ret, Enable = handle.XRFdc_GetMTSEnable(inst_id, 0, 0)

#Description:
#   Set data scaler for DAC block.
#C header declaration:
#   u32 XRFdc_SetDACDataScaler(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 Enable);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#   Enable: valid values are 1 (enable) and 0 (disable).
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs.

ret = handle.XRFdc_SetDACDataScaler(inst_id, 0, 0, 0)

#Description:
#   Get data scaler for DAC block.
#C header declaration:
#   u32 XRFdc_GetDACDataScaler(XRFdc *InstancePtr, u32 Tile_Id, u32 Block_Id, u32 *EnablePtr);
#Input Arguments:
#   inst_id: Id of the RFDC instance
#   Type: Type is ADC or DAC. 0 for ADC and 1 for DAC
#   Tile_Id: Valid values are 0-3
#Return:
#   ret: XRFDC_SUCCESS if successful, XRFDC_FAILURE if error occurs
#   Enable:  valid values are 1 (enable) and 0 (disable).

ret, Enable = handle.XRFdc_GetDACDataScaler(inst_id, 0, 0)

#s32 XRFdc_GetDeviceNameByDeviceId(char *DevNamePtr, u16 DevId);#TODO

#Description:
#   Gets whether the device is a DFE variant or not
#C header declaration:
#   u8 XRFdc_GetTileLayout(XRFdc *InstancePtr);
#Input Arguments:
#   inst_id: integer handle to the initialized instance
#Return:
#   tile_layout: - XRFDC_3ADC_2DAC_TILES if DFE variant.
#               - XRFDC_4ADC_4DAC_TILES if regular Gen 1/2/3.

tile_layout = handle.XRFdc_GetTileLayout(inst_id)
