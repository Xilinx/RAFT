# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import sys
import json
import sys
def usage():
    # sys.argv[0] - usage python file name
    # sys.argv[1] - xclient/xpyro
    # sys.argv[2] - host/board
    # sys.argv[3] - ip_address
    # sys.argv[4] - port
    print(f"Usage: The application work in three modes xclient and xpyro\n"
          f"python3 {sys.argv[0]} xclient host/board ip_address port => Runs at host or board with xclient\n"
          f"python3 {sys.argv[0]} xpyro host/board ip_address port => Runs at host or board with xpyro\n"
          f"Example: python3 {sys.argv[0]} xclient host 127.0.0.1 9090")

if (len(sys.argv) !=  5):
    usage()
    sys.exit()

# The 'xclient' option will run both in host and board
if (sys.argv[1] == 'xclient'):
    # For 'xclient' option the path of the xclient is required
    # The relative path in the host is given for host case
    if (sys.argv[2] == 'host'):
        sys.path.append('../../../xclient/raft_services')
    # The location of xclient in the filesystem is given for the board case
    elif (sys.argv[2] == 'board'):
        sys.path.append('/usr/share/raft/xclient/raft_services')
    else:
        usage()
        sys.exit()
    import pm_client
    handle = pm_client.pm
    ip_address = sys.argv[3]
    port = sys.argv[4]

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:PM@{ip_address}:{port}"
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


print(f'######## BOARD INFO ########')
#Description:
#   Gets Board info.
#Input Arguments:
#
#Return:
#   ret:BoardInfo in Json format.
ret = handle.GetBoardInfo()
print(json.dumps(ret, indent=2))
print(f'#################################')

print(f'######## LIST OF DOMAINS ########')

#Description:
#   Gets Power domains list.
#Input Arguments:
#   None
#Return:
#   ret: Power Domains in Json format.
ret = handle.GetPowerDomains()
print(json.dumps(ret, indent=2))
print(f'#################################')


print(f'######## LIST OF "PLD" RAILS ########')
domain_name = "FPD"

#Description:
#   Gets Rail list of asked domain
#Input Arguments:
#   domain_name: Domain Name
#Return:
#   ret: List of rails for asked domain.
ret = handle.GetRailsOfDomain(domain_name)
print(json.dumps(ret, indent=2))
print(f'#####################################')

print(f'######## DETAILS OF "VCCINT_PSFP" RAIL ########')
rail_name = "VCCINT_PSFP"

#Description:
#   Gets rail details.
#Input Arguments:
#   rail_name: Rail Name
#Return:
#   ret: List of rails for asked domain.
ret = handle.GetRailDetails(rail_name)
print(json.dumps(ret, indent=2))
print(f'###########################################')

print(f'######## VALUES OF "VCCINT_PSFP" RAIL ########')
rail_name = "VCCINT_PSFP"

#Description:
#   Gets power/sensor values of a rail.
#Input Arguments:
#   rail_name: Rail Name
#Return:
#   ret: List of rails for asked domain.
ret = handle.GetValueOfRail(rail_name)
print(json.dumps(ret, indent=2))
print(f'##########################################')

print(f'######## VALUES OF "PLD" DOMAIN ########')
domain_name = "PLD"

#Description:
#   Gets power/sensor values of a domain.
#Input Arguments:
#   rail_name: Domain Name
#Return:
#   ret: List of rails for asked domain.
ret = handle.GetValueOfDomain(domain_name)
print(json.dumps(ret, indent=2))
print(f'########################################')

print(f'######## GET ALL DOMAINS POWER VALUES AT ONCE ##########')
#Description:
#   Gets domains and total power values of the board.
#Input Arguments:
#   None
#Return:
#   ret: List of power values of the board.
ret = handle.GetPowersAll()
print(json.dumps(ret, indent=2))
print(f'########################################')

print(f'######## GET ALL DOMAINS VALUES AT ONCE ##########')
#Description:
#   Gets power/sensor values of the board.
#Input Arguments:
#   None
#Return:
#   ret: List of rails for asked domain.
ret = handle.GetValuesAll()
print(json.dumps(ret, indent=2))
print(f'########################################')


print(f'######## GET SYSMON TEMPERATURE VALUES ##########')
#Description:
#   Gets sysmon temperature values of Versal.
#Input Arguments:
#   None
#Return:
#   ret: Sysmon Temperature values
ret = handle.GetSysmonTemperatures()
print(json.dumps(ret, indent=2))
print(f'########################################')


print(f'######## GET PS TEMPERATURE VALUE ##########')
#Description:
#   Gets PS temperature value of Versal.
#Input Arguments:
#   None
#Return:
#   ret: PS Temperature values.
ret = handle.GetPSTemperature()
print(json.dumps(ret, indent=2))
print(f'########################################')


print(f'######## GET SYSTEM STATS ##########')
#Description:
#   Gets PS temperature value of Versal.
#Input Arguments:
#   None
#Return:
#   ret: PS Temperature values.
ret = handle.GetSystemStats()
print(json.dumps(ret, indent=2))
print(f'########################################')




