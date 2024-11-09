# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.
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
    import equ_client
    handle = equ_client.equ
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/dfe')
    from equ_server import EQU
    handle = EQU()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:EQU@{ip_address}:{port}"
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
#   return: Dictionary showing the log levels supported by logging library

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
#   Return Dictionary with all EQU macros in the equ header file
#Input Arguments:
#   None
#Return:
#   Dictionary with all EQU macros in the equ header file
#GetCcfMacro
equ_macro = handle.GetEquMacro()
print(equ_macro["XDFEEQU_MAX_NUM_INSTANCES"])
print(equ_macro["XST_SUCCESS"])
print(equ_macro["XST_FAILURE"])
print(equ_macro["XDFEEQU_NODE_NAME_MAX_LENGTH"])
print(equ_macro["XDFEEQU_ANT_NUM_MAX"])
print(equ_macro["XDFEEQU_CHANNEL_NUM"])
print(equ_macro["XDFEEQU_MAX_NUMBER_OF_UNITS_COMPLEX"])
print(equ_macro["XDFEEQU_MAX_NUMBER_OF_UNITS_REAL"])
print(equ_macro["XDFEEQU_NUM_COEFF"])
print(equ_macro["XDFEEQU_DATAPATH_MODE_REAL"])
print(equ_macro["XDFEEQU_DATAPATH_MODE_COMPLEX"])
print(equ_macro["XDFEEQU_DATAPATH_MODE_MATRIX"])

#Description:
#   Return Dictionary equivalent of enum XDfeEqu_StateId
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of enum XDfeEqu_StateId

#GetEnum_XDfeEqu_StateId
XDfeEqu_StateId = handle.GetEnum_XDfeEqu_StateId()

#Description:
#    Return Dictionary equivalent of enum metal_log_level
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of enum metal_log_level

#GetEnum_metal_log_level
metal_log_level = handle.GetEnum_metal_log_level()

#Description:
#   API initialises one instance of an Equalizer driver.
#   Traverse "/sys/bus/platform/device" directory (in Linux), to find registered
#   EQU device with the name DeviceNodeName. The first available slot in
#   the instances array XDfeEqu_ChFilter[] will be taken as a DeviceNodeName
#   object. On success it moves the state machine to a Ready state, while on
#   failure stays in a Not Ready state.
#C header declaration:
#   XDfeEqu *XDfeEqu_InstanceInit(const char *DeviceNodeName);
#Input Arguments:
#   DeviceNodeName: device node name.
#Return:
#   ret: 0 on success, 1 on failure
#   device_id: integer handle to initialized instance
#   DeviceNodeNameRet: device node name returned from driver
#                      which will be same as the passed value
#Note:
#   The bytes conversion is already done inside xpyro client.

DeviceNodeName = "a6080000.xdfe_equalizer"
ret, device_id, DeviceNodeName = handle.XDfeEqu_InstanceInit(DeviceNodeName)

#Description:
#   Writes value to register in an Equalizer instance.
#C header declaration:
#   void XDfeEqu_WriteReg(const XDfeEqu *InstancePtr, u32 AddrOffset, u32 Data);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#   Data: is value to be written.
#Return:
#   None

handle.XDfeEqu_WriteReg(device_id, 0, 0)

#Description:
#   Reads a value from the register using an Equalizer instance.
#C header declaration:
#   u32 XDfeEqu_ReadReg(const XDfeEqu *InstancePtr, u32 AddrOffset);
#Input Arguments:
#   device_id: id of the opened device.
#   AddrOffset: is address offset relative to instance base address.
#Return:
#   return: Register value.

ret = handle.XDfeEqu_ReadReg(device_id, 0)

#Description:
#   Resets Equalizer and puts block into a reset state.
#C header declaration:
#   void XDfeEqu_Reset(XDfeEqu *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeEqu_Reset(device_id)

#Description:
#   Reads configuration from device tree/xparameters.h and IP registers.
#   Removes S/W reset and moves the state machine to a Configured state.
#C header declaration:
#   void XDfeEqu_Configure(XDfeEqu *InstancePtr, XDfeEqu_Cfg *Cfg);
#Input Arguments:
#   device_id: id of the opened device.
#   Cfg: device config container.
#Return:
#   Cfg: device config container.

Cfg_in = handle.GetStruct_XDfeEqu_Cfg()
Cfg = handle.XDfeEqu_Configure(device_id, Cfg_in)

#Description:
#   DFE Equalizer driver one time initialisation and moves the state machine to
#   an Initialised state.
#C header declaration:
#   void XDfeEqu_Initialize(XDfeEqu *InstancePtr, const XDfeEqu_EqConfig *Config);
#Input Arguments:
#   device_id: id of the opened device.
#   Config: configuration data container.
#Return:
#   Config: configuration data container.

EqConfig_in = handle.GetStruct_XDfeEqu_EqConfig()
handle.XDfeEqu_Initialize(device_id, EqConfig_in)

#Description:
#   Set trigger configuration.
#C header declaration:
#   void XDfeEqu_SetTriggersCfg(const XDfeMix *InstancePtr, XDfeEqu_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#   TriggerCfg: is a trigger configuration container.
#Return:
#   TriggerCfg: is a triggger configuration container.

TriggerCfg_in = handle.GetStruct_XDfeEqu_TriggerCfg()
handle.XDfeEqu_SetTriggersCfg(device_id, TriggerCfg_in)

#Description:
#   Sets the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   void XDfeEqu_SetTUserDelay(const XDfeEqu *InstancePtr, u32 Delay);
#Input Arguments:
#   device_id: id of the opened device.
#   Delay: requested delay variable.
#Return:
#   None

Delay = 0
handle.XDfeEqu_SetTUserDelay(device_id, Delay)

#Description:
#   Activates channel Equalizer moves the state machine to an Activated state.
#C header declaration:
#   void XDfeEqu_Activate(XDfeEqu *InstancePtr, bool EnableLowPower);
#Input Arguments:
#   device_id: id of the opened device.
#   EnableLowPower: flag indicating low power.
#Return:
#   None

handle.XDfeEqu_Activate(device_id,0)

#Description:
#    Gets a state machine state id. The state id is returned as a string.
#    The enum is mapped to a dictionary in python.
#C header declaration:
#   XDfeEqu_StateId XDfeEqu_GetStateID(XDfeEqu *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   StateId: State machine StateID as a string

StateId = handle.XDfeEqu_GetStateID(device_id)
print(StateId)

#Description:
#   Return Dictionary equivalent of structure XDfeEqu_EqConfig
#C header declaration:
#   void XDfeEqu_Update(const XDfeEqu *InstancePtr, const XDfeEqu_EqConfig *Config);
#Input Arguments:
#   None
#Return:
#   return: Dictionary equivalent of structure XDfeEqu_Coefficients

EqConfig_in = handle.GetStruct_XDfeEqu_EqConfig()
handle.XDfeEqu_Update(device_id, EqConfig_in)

#Description:
#   Returns current trigger configuration.
#C header declaration:
#   void XDfeEqu_GetTriggersCfg(const XDfeEqu *InstancePtr,
#   XDfeEqu_TriggerCfg *TriggerCfg);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   TriggerCfg: is a trigger configuration container.

TriggerCfg_out = handle.XDfeEqu_GetTriggersCfg(device_id)

#Description:
#   Sets Equalizer filter coefficients in Real, Complex or Matrix mode.
#C header declaration:
#   void XDfeEqu_LoadCoefficients(const XDfeEqu *InstancePtr, u32 ChannelField,
#	u32 Mode, const XDfeEqu_Coefficients *EqCoeffs);
#Input Arguments:
#   device_id: id of the opened device.
#   ChannelField: is a flag in which bits indicate the channel is enabled.
#   Mode: is an equalizer mode.
#   Shift: is a coefficient shift value.
#   EqCoeffs: is equalizer coefficients container.
#Return:
#   EqCoeffs: is equalizer coefficients container.

EqCoeffs = {
    "Num": 10,
    "Set": 0,
    "Coefficients": [0, 0, 0, (2 ** 15) - 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
handle.XDfeEqu_LoadCoefficients(device_id, 0, 0, 8, EqCoeffs)

#Description:
#   Gets Equalizer event status
#C header declaration:
#   void XDfeEqu_GetEventStatus(const XDfeEqu *InstancePtr, XDfeEqu_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   Status: event status

Status_out = handle.XDfeEqu_GetEventStatus(device_id)

#Description:
#   Clears Equalizer status. The channel status will be cleared for any
#   IStatus or QStatus not equal 0.
#C header declaration:
#   void XDfeEqu_ClearEventStatus(const XDfeEqu *InstancePtr,
#	const XDfeEqu_Status *Status);
#Input Arguments:
#   device_id: id of the opened device.
#   Status: event status.
#Return:
#   None

handle.XDfeEqu_ClearEventStatus(device_id, Status_out)

#Description:
#   Enables an Equalizer status for channel ID.
#C header declaration:
#   void XDfeEqu_SetInterruptMask(const XDfeEqu *InstancePtr,
#	const XDfeEqu_InterruptMask *InterruptMask);
#Input Arguments:
#   device_id: id of the opened device.
#   InterruptMask: interrupt mask value
#Return:
#   None

Mask_in = handle.GetStruct_XDfeEqu_InterruptMask()
handle.XDfeEqu_SetInterruptMask(device_id, Mask_in)

#Description:
#   Gets interrupt mask.
#C header declaration:
#   void XDfeEqu_GetInterruptMask(const XDfeEqu *InstancePtr,
#	XDfeEqu_InterruptMask *InterruptMask);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   InterruptMask: Equalizer interrupt mask container.

Mask_out = handle.XDfeEqu_GetInterruptMask(device_id)

#Description:
#   Gets used coefficients settings.
#C header declaration:
#   void XDfeEqu_GetActiveSets(const XDfeEqu *InstancePtr, u32 *RealSet,
#   u32 *ImagSet);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   RealSet: Real value
#   ImagSet: Imaginary value

RealSet, ImagSet = handle.XDfeEqu_GetActiveSets(device_id)

#Description:
#   Reads the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeEqu_GetTUserDelay(const XDfeEqu *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   ret: Delay value

ret = handle.XDfeEqu_GetTUserDelay(device_id)

#Description:
#   Returns CONFIG.DATA_LATENCY.VALUE + tap, where the tap is between 0
#   and 23 in real mode and between 0 and 11 in complex/matrix mode.
#C header declaration:
#   u32 XDfeEqu_GetTDataDelay(const XDfeEqu *InstancePtr, u32 Tap);
#Input Arguments:
#   device_id: id of the opened device.
#   Tap: is a tap variable.
#Return:
#   ret: data latency value.

Tap = 0
ret = handle.XDfeEqu_GetTDataDelay(device_id, Tap)

#Description:
#   This API is used to get the driver version.
#C header declaration:
#   void XDfeEqu_GetVersions(const XDfeMix *InstancePtr,
#   XDfeEqu_Version *SwVersion, XDfeEqu_Version *HwVersion);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   SwVersion: driver version numbers.
#   HwVersion: HW version numbers.

SwVersion_out, HwVersion_out = handle.XDfeEqu_GetVersions(device_id)

#Description:
#   Deactivates Equalizer and moves the state machine to Initialised state.
#C header declaration:
#   void XDfeEqu_Deactivate(XDfeEqu *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeEqu_Deactivate(0)

#Description:
#   Sets the delay, which will be added to TUSER and TLAST (delay matched
#   through the IP).
#C header declaration:
#   u32 XDfeEqu_SetTUserDelay(const XDfeEqu *InstancePtr, u32 Delay);
#Input Arguments:
#   device_id: id of the opened device.
#   Delay: requested delay variable.
#Return:
#   None

handle.XDfeEqu_SetTUserDelay(device_id, 10)

#Description:
#   API closes the instance of an Equalizer driver.
#C header declaration:
#   void XDfeEqu_InstanceClose(XDfeMix *InstancePtr);
#Input Arguments:
#   device_id: id of the opened device.
#Return:
#   None

handle.XDfeEqu_InstanceClose(device_id)
