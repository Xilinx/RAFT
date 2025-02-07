# Copyright (C) 2023-2025 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2025, Advanced Micro Devices, Inc."

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
    #handle.SetClientLogLevel(PythonLogLevels["DEBUG"])


def print_response(response):
    if ret['status'] == 'success':
        print(json.dumps(ret['data'], indent=2))
    else:
        print(json.dumps(ret['message'], indent=2))

def print_header(section_name):
    print(f'\n######## {section_name} ########')

print_header("GET BOARD INFO")
#Description:
#   Gets Board info.
#Input Arguments:
#
#Return:
#   ret:BoardInfo in dict format.
ret = handle.getboardinfo()
print(json.dumps(ret, indent=2))

print_header("LIST OF FEATURES")
#Description:
#   Lists feature info.
#Input Arguments:
#
#Return:
#   ret:Features in list format.
list_features = handle.listfeature()
print(json.dumps(list_features, indent=2))

if 'powerdomain' in list_features['data']:
    print_header("LIST OF DOMAINS")
    #Description:
    #   Lists Power domains.
    #Input Arguments:
    #   None
    #Return:
    #   ret: Power Domains List.
    list_domains = handle.listpowerdomain()
    print(json.dumps(list_domains, indent=2))

    if list_domains['data']:
        print_header(f'LIST OF "{list_domains['data'][0]}" RAILS')
        #Description:
        #   Gets Rail list of asked domain
        #Input Arguments:
        #   domain_name: Domain Name
        #Return:
        #   ret: List of rails for asked domain.
        list_rails = handle.listrailsofdomain(list_domains['data'][0])
        print(json.dumps(list_rails, indent=2))

        if list_rails['data']:
            print_header(f'VALUES OF "{list_rails['data'][0]}" RAIL')
            #Description:
            #   Gets power/sensor values of a rail.
            #Input Arguments:
            #   rail_name: Rail Name
            #Return:
            #   ret: List of rails for asked domain.
            ret = handle.getvalueofrail(list_rails['data'][0])
            print(json.dumps(ret, indent=2))

        print_header(f'######## VALUES OF "{list_domains['data'][0]}" DOMAIN ########')
        #Description:
        #   Gets power/sensor values of a domain.
        #Input Arguments:
        #   rail_name: Domain Name
        #Return:
        #   ret: List of rails for asked domain.
        ret = handle.getvalueofdomain(list_domains['data'][0])
        print(json.dumps(ret, indent=2))

        print_header(f'######## GET ALL DOMAINS POWER VALUES AT ONCE ##########')
        #Description:
        #   Gets domains and total power values of the board.
        #Input Arguments:
        #   None
        #Return:
        #   ret: List of power values of the board.
        ret = handle.getpowerall()
        print(json.dumps(ret, indent=2))

        print_header(f'######## GET ALL DOMAINS VALUES AT ONCE ##########')
        #Description:
        #   Gets power/sensor values of the board.
        #Input Arguments:
        #   None
        #Return:
        #   ret: List of rails for asked domain.
        ret = handle.getvalueall()
        print(json.dumps(ret, indent=2))

if 'power' in list_features['data']:
    print_header(f'######## LIST POWER SENSORS ##########')
    #Description:
    #   List of power sensors
    #Input Arguments:
    #   None
    #Return:
    #   ret: list of power sensors
    list_power = handle.listpower()
    print(json.dumps(list_power, indent=2))


    if list_power['data']:
        # Get first power sensor name from list of power sensors
        power_sensor = [key for key in list_power['data'][0]][0]
        print_header(f'######## GET "{power_sensor}" POWER SENSOR ##########')
        #Description:
        #   Gets power sensor values.
        #Input Arguments:
        #   Power sensor name
        #Return:
        #   ret: Power sensor values
        ret = handle.getpower(power_sensor)
        print(json.dumps(ret, indent=2))

if 'voltage' in list_features['data']:
    print_header(f'######## LIST VOLTAGES ##########')
    #Description:
    #   List of voltages.
    #Input Arguments:
    #   None
    #Return:
    #   ret: list of voltages
    list_voltage = handle.listvoltage()
    print(json.dumps(list_voltage, indent=2))


    if list_voltage['data']:
        # Get first voltage name from list of voltages
        voltage = [key for key in list_voltage['data'][0]][0]
        print_header(f'######## GET {voltage} VOLTAGE ##########')
        #Description:
        #   Gets voltage value.
        #Input Arguments:
        #   Voltage regulator name
        #Return:
        #   ret: Voltage value
        ret = handle.getvoltage(voltage)
        print(json.dumps(ret, indent=2))

        print_header(f'######## GET "{voltage}" REGULATOR ##########')
        #Description:
        #   Gets voltage regulator telemetry values.
        #Input Arguments:
        #   Voltage regulator name
        #Return:
        #   ret: voltage regulator telemetry values
        ret = handle.getregulator(voltage)
        print(json.dumps(ret, indent=2))

if 'temp' in list_features['data']:
    print_header(f'######## LIST TEMPERATURES ##########')
    #Description:
    #   List of temperature names.
    #Input Arguments:
    #   None
    #Return:
    #   ret: List Temperature devices
    list_temp = handle.listtemperature()
    print(json.dumps(list_temp, indent=2))

    if list_temp['data']:
        print_header(f'######## GET TEMPERATURE of {list_temp['data'][0]} ##########')
        #Description:
        #   Gets sysmon temperature values of Versal.
        #Input Arguments:
        #   None
        #Return:
        #   ret: Versal's Temperature values
        ret = handle.gettemperature(list_temp['data'][0])
        print(json.dumps(ret, indent=2))