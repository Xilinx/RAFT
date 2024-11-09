# Copyright (C) 2021-2024 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Gerard Thomas Colman"
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

# # 'xcffi' option will run only in the board
if (len(sys.argv) ==  2):
    if (sys.argv[1] != 'xcffi'):
        usage()
        sys.exit()

elif (len(sys.argv) !=  5):
    print("here")
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
    import rfclk_client
    handle = rfclk_client.rfclk
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/rfdc')
    from rfclk_server import RFCLK
    handle = RFCLK()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:RFCLK@{ip_address}:{port}"
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

#GetPythonLogLevels
PythonLogLevels = handle.GetPythonLogLevels()

#SetServerLogLevel
handle.SetServerLogLevel(PythonLogLevels["DEBUG"])

#SetMetalLogLevel
metal_log_level = handle.GetEnum_metal_log_level()
handle.SetMetalLogLevel(metal_log_level["METAL_LOG_EMERGENCY"])

#GetRfclkMacro
rfclk_macro = handle.GetRfclkMacro()
print(rfclk_macro["XST_SUCCESS"])
print(rfclk_macro["XST_FAILURE"])
print(rfclk_macro["RFCLK_LMX2594_1"])
print(rfclk_macro["RFCLK_LMX2594_2"])
print(rfclk_macro["RFCLK_LMK"])
print(rfclk_macro["RFCLK_CHIP_NUM"])
print(rfclk_macro["LMK_COUNT"])
print(rfclk_macro["LMK_FREQ_NUM"])
print(rfclk_macro["LMX_ADC_NUM"])
print(rfclk_macro["LMX_DAC_NUM"])
print(rfclk_macro["LMX2594_COUNT"])
print(rfclk_macro["FREQ_LIST_STR_SIZE"])

#XRFClk_Init
ret = handle.XRFClk_Init(486)
print(ret)

#XRFClk_ResetChip
ret = handle.XRFClk_ResetChip(0)
print(ret)

#XRFClk_SetConfigOnOneChipFromConfigId
ret = handle.XRFClk_SetConfigOnOneChipFromConfigId(0,0)
print(ret)

#XRFClk_GetConfigFromOneChip
ret = handle.XRFClk_GetConfigFromOneChip(0)
print(ret)

#XRFClk_SetConfigOnAllChipsFromConfigId
ret = handle.XRFClk_SetConfigOnAllChipsFromConfigId(0,0,0)
print(ret)

#XRFClk_WriteReg
ret = handle.XRFClk_WriteReg(0,0)
print(ret)

#XRFClk_ReadReg
DataVal = handle.XRFClk_ReadReg(0)
print(DataVal)
