#!/usr/bin/env python
# Copyright (C) 2023-2025 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim, Sree Parvathi Anish"
__copyright__ = "Copyright 2023-2025, Advanced Micro Devices, Inc."

import os
import sys
import json
import argparse
import csv
import time
import datetime
import operator
sys.path.append('/usr/share/raft/xclient/raft_services')
from pm_client import PM_Client

client = PM_Client()

class CustomHelpFormatter(argparse.HelpFormatter):
    """Custom formatter to show subcommand groups with proper argument types."""
    def __init__(self, prog, command_groups):
        super().__init__(prog)
        self.command_groups = command_groups  # Store command groups

    def _format_action(self, action):
        """Customize argument formatting to distinguish between positional and optional arguments."""
        if isinstance(action, argparse._SubParsersAction):
            parts = []
            for group_name, commands in self.command_groups.items():
                parts.append(f"\n  {group_name}:")
                for cmd in commands:
                    parts.append(f"    {cmd:<15} {action.choices[cmd].description}")
            return "\n".join(parts)
        # Distinguish between positional and optional arguments
        if action.option_strings:
            # Optional arguments (e.g., --flag, --option value)
            return f"  {', '.join(action.option_strings):<20} {action.help}"
        else:
            # Positional arguments (e.g., required ones)
            return f"  {action.dest:<20} {action.help}"
        return super()._format_action(action)

class CheckRange(argparse.Action):
    ops = {'inf': operator.gt,
           'min': operator.ge,
           'sup': operator.lt,
           'max': operator.le}

    def __init__(self, *args, **kwargs):
        if 'min' in kwargs and 'inf' in kwargs:
            raise ValueError('either min or inf, but not both')
        if 'max' in kwargs and 'sup' in kwargs:
            raise ValueError('either max or sup, but not both')
        for name in self.ops:
            if name in kwargs:
                setattr(self, name, kwargs.pop(name))
        super().__init__(*args, **kwargs)

    def interval(self):
        if hasattr(self, 'min'):
            l = f'[{self.min}'
        elif hasattr(self, 'inf'):
            l = f'({self.inf}'
        else:
            l = '(-infinity'

        if hasattr(self, 'max'):
            u = f'{self.max}]'
        elif hasattr(self, 'sup'):
            u = f'{self.sup})'
        else:
            u = '+infinity)'
        return f'valid range: {l}, {u}'

    def __call__(self, parser, namespace, values, option_string=None):
        for name, op in self.ops.items():
            if hasattr(self, name) and not op(values, getattr(self, name)):
                raise argparse.ArgumentError(self, self.interval())
            setattr(namespace, self.dest, values)

def print_response(response):
    if response['status'] == 'success':
        if not response['data']:
            print(json.dumps(response['status'], indent=2))
        else:
            print(json.dumps(response['data'], indent=2))
        sys.exit(os.EX_OK)
    else:
        print(json.dumps(response['message'], indent=2))
        sys.exit(os.EX_SOFTWARE)

def main():
    # Define command groups
    command_groups = {
        "System Information": ["boardinfo", "listfeature"],
        "Power Sensor Measurement and Control": ["listpower", "getpower", "getcalpower", "getinaconf", "setinaconf"],
        "Reagultor Voltage Measurement and Control": ["listvoltage", "enablevoltage", "disablevoltage", "getvoltage", "setvoltage", "setbootvoltage", "restorevoltage", "getregulator"],
        "Power Domains and Rails Info": ["listdomain", "listrail", "powervalue", "allvalue"],
        "Temperature Measurement": ["listtemperature", "gettemperature"],
        "Measurement Units": ["listunit", "getunit", "availablescale", "setscale"],
        "Miscellaneous": ["loglevel", "output-csv"]
    }
    # Create main parser
    parser = argparse.ArgumentParser(
        description="RAFT-PM CLI tool for system monitoring and power management",
        formatter_class=lambda prog: CustomHelpFormatter(prog, command_groups)
    )
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    # Function to create subcommands with a description and execution logic
    def add_command(name, description, func, arguments=None, optional_arguments=None):
        cmd_parser = subparsers.add_parser(name, help=description, description=description)
        # Add required arguments
        if arguments:
            for arg_name, arg_options in arguments.items():
                cmd_parser.add_argument(arg_name, **arg_options)
        # Add optional arguments
        if optional_arguments:
            for arg_name, arg_options in optional_arguments.items():
                cmd_parser.add_argument(arg_name, **arg_options)

        cmd_parser.set_defaults(func=func)

    # 🌟 Add commands with arguments
    add_command("boardinfo", "Display board information", system_action)
    add_command("listfeature", "Show available system feature", system_action)

    add_command("listpower", "List all power sensors", power_action)
    add_command("getpower", "Get power sensor value", power_action,
                arguments={"sensor_name": {"type": str, "help": "Specify the power sensor name (e.g., VCCINT, VCCSOC)"}})
    add_command("getcalpower", "Get calibrated power sensor values", power_action,
                arguments={"sensor_name": {"type": str, "help": "Specify the power sensor name (e.g., VCCINT, VCCSOC)"}})
    add_command("getinaconf", "Retrieve INA configuration", power_action,
                arguments={"sensor_name": {"type": str, "help": "Specify the power sensor name (e.g., VCCINT, VCCSOC)"}})
    add_command("setinaconf", "Set INA configuration", power_action,
                arguments={"sensor_name": {"type": str, "help": "Specify the power sensor name (e.g., VCCINT, VCCSOC)"},
                            "value": {"type": lambda arg: [int(token) if token.isdigit() else None if token.lower() == 'x' else token for token in arg.split(' ')], "help": "Set INA configuration value in decimal values e.g., '1 2 3 4'"}})

    add_command("listvoltage", "List available voltage regulators", voltage_action)
    add_command("enablevoltage", "Enable a specific voltage regulator output", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to enable"}})
    add_command("disablevoltage", "Disable a specific voltage regulator output", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to disable"}})
    add_command("getvoltage", "Get current voltage level", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to set"}})
    add_command("setvoltage", "Set a new voltage level", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to set"},
                           "value": {"type": float, "help": "New voltage value"}})
    add_command("setbootvoltage", "Set boot voltage level", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to set"},
                           "value": {"type": float, "help": "New voltage value"}})
    add_command("restorevoltage", "Restore default voltage value", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to set"}})
    add_command("getregulator", "Get ragulators all available telemetry data", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to get"}})

    add_command("listdomain", "List all power domains", domain_action)
    add_command("listrail", "List all power rails for specific domain", domain_action,
                arguments={"domain_name": {"type": str, "help": "Domain name to get rails"}})
    add_command("powervalue", "Get only 'power' values of all domains", domain_action)
    add_command("allvalue", "Get all values retrieved from power sensors in once", domain_action)

    add_command("listtemperature", "List all tmeperature sensors", temp_action)
    add_command("gettemperature", "Get temperature values for given sensor", temp_action,
                arguments={"temp_name": {"type": str, "help": "temp_name"}})

    add_command("listunit", "List available measurement units", unit_action)
    add_command("getunit", "Get unit details",  unit_action,
                arguments={"quantity": {"type": str, "choices": ["voltage", "current", "power", "temperature"], "help": "quantity"}})
    add_command("availablescale", "Show available scaling options", unit_action,
                arguments={"quantity": {"type": str, "choices": ["voltage", "current", "power", "temperature"], "help": "quantity"}})
    add_command("setscale", "Set measurement scale", unit_action,
                arguments={"quantity": {"type": str, "choices": ["voltage", "current", "power", "temperature"], "help": "quantity"},
                           "scale": {"type": str, "help": "Scaling factor to apply"}})

    add_command("loglevel", "Set logging level", log_action, {
        "level": {"type": str, "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "help": "Logging level"}
    })
    add_command("output-csv", "Time-series allvalue output results in CSV format", outputcsv_action,
                arguments={"duration": {"type": int, "min": 1, "action": CheckRange, "help": "Duration time value"},
                           "sampling_rate": {"type": int, "min": 1, "max": 12, "action": CheckRange, "help": "Sampling rate value"}},
                optional_arguments={"--path": {"type": str, "default": "/home/petalinux", "help": "Path to save the output file"}})
    # Parse arguments
    args = parser.parse_args()
    # Execute the corresponding function
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

def system_action(args):
    match args.command:
        case 'boardinfo':
            print_response(client.getboardinfo())
        case 'listfeature':
            print_response(client.listfeature())

def power_action(args):
    match args.command:
        case "listpower":
            print_response(client.listpower())
        case "getpower":
            print_response(client.getpower(args.sensor_name))
        case "getcalpower":
            print_response(client.getcalpower(args.sensor_name))
        case "getinaconf":
            print_response(client.getpowerconf(args.sensor_name))
        case "setinaconf":
            print_response(client.setpowerconf(args.sensor_name, args.value))

def voltage_action(args):
    match args.command:
        case "listvoltage":
            print_response(client.listvoltage())
        case "enablevoltage":
            print_response(client.enablevoltage(args.voltage_name))
        case "disablevoltage":
            print_response(client.disablevoltage(args.voltage_name))
        case "getvoltage":
            print_response(client.getvoltage(args.voltage_name))
        case "setvoltage":
            print_response(client.setvoltage(args.voltage_name, args.value))
        case "setbootvoltage":
            print_response(client.setbootvoltage(args.voltage_name, args.value))
        case "restorevoltage":
            print_response(client.restorevoltage(args.voltage_name))
        case "getregulator":
            print_response(client.getregulator(args.voltage_name))

def domain_action(args):
    match args.command:
        case "listdomain":
            print_response(client.listpowerdomain())
        case "listrail":
            print_response(client.listrailsofdomain(args.domain_name))
        case "powervalue":
            print_response(client.getpowerall())
        case "allvalue":
            print_response(client.getvalueall())

def temp_action(args):
    match args.command:
        case 'listtemperature':
            print_response(client.listtemperature())
        case 'gettemperature':
            print_response(client.gettemperature(args.temp_name))

def unit_action(args):
    match args.command:
        case "listunit":
            print_response(client.listunit())
        case "getunit":
            print_response(client.getunit(args.quantity))
        case "availablescale":
            print_response(client.listscale(args.quantity))
        case "setscale":
            print_response(client.setscale(args.quantity, args.scale))

def log_action(args):
    print(client.logger.level)

def outputcsv_action(args):
    sample_rate = int(args.sampling_rate)
    filepath = args.path
    duration = int(args.duration)
    # Check the input arguments
    if not os.path.exists(filepath):
        print(f"The path {filepath} is valid.")
        sys.exit(1)
    # Find the sleep time from the sample rate
    sleeptime = 1/sample_rate
    csv_data = []
    # Mark the start time
    start_datetime = datetime.datetime.now()
    start_time = time.time()
    while True:
        operation_start_time = time.time()
        ret = client.getvalueall()
        if ret["status"] == "success":
            csv_data, columns_order = update_csv_data(csv_data, ret["data"], sample_rate, duration)
        operation_exec_time = time.time() - operation_start_time
        # If operation execution time is higher than sleep time, no need to sleep
        if (sleeptime - operation_exec_time) > 0:
            time.sleep(sleeptime -  operation_exec_time)
        if time.time() - start_time >= duration:
            break
    filename = start_datetime.strftime(f"pmtool_s-{sample_rate}_d-{duration}_%Y-%m-%d_%H-%M-%S.csv")
    pm_csv_dump(csv_data, columns_order, filepath, filename)

def update_csv_data(csv_data, data, sample_rate, duration):
    # Convert the dictionary to a list
    columns_order = []
    row_item = {}
    write_timestamp = 1
    for k, domain_list in data.items():
        for index, domain in enumerate(domain_list):
            for key, value in domain.items():
                for rails_item in value["Rails"]:
                    for rails_key, rails_value in rails_item.items():
                        if write_timestamp == 1:
                            columns_order.append("Timestamp")
                            start_time = datetime.datetime.now()
                            row_item.update({"Timestamp" : start_time})
                            write_timestamp = 0
                        column_name = f"{key}-{rails_key}-{list(rails_value.keys())[0]}"
                        columns_order.append(column_name)
                        row_item.update({f"{column_name}": rails_value['Voltage']})
                        column_name = f"{key}-{rails_key}-{list(rails_value.keys())[1]}"
                        columns_order.append(column_name)
                        row_item.update({f"{column_name}": rails_value['Current']})
                        column_name = f"{key}-{rails_key}-{list(rails_value.keys())[2]}"
                        columns_order.append(column_name)
                        row_item.update({f"{column_name}": rails_value['Power']})
        column_name = f"{key}-TotalPower"
        columns_order.append(column_name)
        row_item.update({f"{column_name}": value["Total Power"]})
    csv_data.append(row_item)
    return csv_data, columns_order

def pm_csv_dump(csv_data, columns_order, filepath, filename):
    csv_file = f"{filepath}/{filename}"
    try:
        with open(csv_file, 'w') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=columns_order, lineterminator='\n')
            csv_writer.writeheader()
            for row in csv_data:
                    csv_writer.writerow(row)
            print(f"The requested data is written to file - {csv_file}")
            sys.exit(os.EX_OK)
    except IOError:
        print(f"I/O error while opening {csv_file} to write")
        sys.exit(os.EX_SOFTWARE)

if __name__ == "__main__":
    # call main
    main()

