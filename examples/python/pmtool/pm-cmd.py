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
from pathlib import Path
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
        "Reagultor Voltage Measurement and Control": ["listvoltage", "enablevoltage", "disablevoltage", "getvoltage", "setvoltage", "setbootvoltage", "restorevoltage", "getregulator", "onregulator", "offregulator"],
        "Power Domains and Rails Info": ["listdomain", "listrail", "powervalue", "allvalue"],
        "GPIO Control": ["listgpio", "setgpio", "getgpio"],
        "Temperature Measurement": ["listtemperature", "gettemperature"],
        "Measurement Units": ["listunit", "getunit", "availablescale", "setscale"],
        "Miscellaneous": ["loglevel", "output-csv", "powerlog"]
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
    add_command("onregulator", "Turn On/Enable regulator by gpio controller", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to turn on"}})
    add_command("offregulator", "Turn Off/Disable regulator by gpio controller", voltage_action,
                arguments={"voltage_name": {"type": str, "help": "Voltage rail to turn off"}})

    add_command("listdomain", "List all power domains", domain_action)
    add_command("listrail", "List all power rails for specific domain", domain_action,
                arguments={"domain_name": {"type": str, "help": "Domain name to get rails"}})
    add_command("powervalue", "Get only 'power' values of all domains", domain_action)
    add_command("allvalue", "Get all values retrieved from power sensors in once", domain_action)

    add_command("listtemperature", "List all tmeperature sensors", temp_action)
    add_command("gettemperature", "Get temperature values for given sensor", temp_action,
                arguments={"temp_name": {"type": str, "help": "temp_name"}})

    add_command("listgpio", "List all gpios", gpio_action)
    add_command("setgpio", "Set gpio value", gpio_action,
                arguments={"gpio_name": {"type": str, "help": "gpio_name"},
                    "value": {"type": str, "choices": ["high", "low",], "help": "New gpio value"}})
    add_command("getgpio", "Get gpio value", gpio_action,
                arguments={"gpio_name": {"type": str, "help": "gpio_name"}})

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
                optional_arguments={"--path": {"type": str, "default": Path.home(), "help": "Path to save the output file"}})
    add_command(
    "powerlog",
    "Dump all power sensors to stdout (optional: log to file). Includes typical voltage mismatch check.",
    cmd_dump_power_log,
    optional_arguments={
        "--threshold": {
            "type": float,
            "default": 10.0,
            "help": "Voltage mismatch threshold percentage (default: 10.0)"
        },
        "--outfile": {
            "type": str,
            "default": None,
            "help": "Optional output filename (if not set, no file is written)"
        }
    })
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
        case "onregulator":
            print_response(client.onregulator(args.voltage_name))
        case "offregulator":
            print_response(client.offregulator(args.voltage_name))

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

def gpio_action(args):
    match args.command:
        case 'listgpio':
            print_response(client.listgpio())
        case 'setgpio':
            print_response(client.setgpio(args.gpio_name, args.value))
        case 'getgpio':
            print_response(client.getgpio(args.gpio_name))

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

def cmd_dump_power_log(args):
    import sys
    import os
    import datetime
    import re

    # ----------------------------
    # Helpers
    # ----------------------------
    def is_error_string(x):
        return isinstance(x, str) and x.strip().lower().startswith("error")

    def unwrap(resp):
        """
        PM API returns:
          {"status":"success|fail","data":...,"message":"..."}
        But in error cases we may get:
          "Error: ...."
        Returns: (ok, data, message)
        """
        if is_error_string(resp):
            return (False, None, resp.strip())

        if not isinstance(resp, dict):
            return (False, None, f"Unexpected response type: {type(resp)}")

        status = resp.get("status", None)
        data = resp.get("data", None)
        msg = resp.get("message", "")

        if status != "success":
            if is_error_string(msg):
                return (False, data, msg.strip())
            return (False, data, msg or "Operation failed")

        return (True, data, msg or "OK")

    def fatal(msg, exit_code):
        print(f"FATAL: {msg}", file=sys.stderr)
        sys.exit(exit_code)

    def vrm_rail_name(sensor_rail):
        """
        Multiphase rails are enumerated with a SINGLE digit suffix:
          VCCINT_1, VCCINT_2, ... -> VRM rail is VCCINT
        Rails like VCC_MIPI_507 are NOT multiphase.
        """
        m = re.match(r"^(.*)_([0-9])$", sensor_rail)
        if m:
            return m.group(1)
        return sensor_rail

    def parse_listvoltage_payload(payload):
        """
        payload example:
        [
          {"VCCINT": {"typical_volt": 0.8}},
          {"VCC_LPD": {"typical_volt": 0.88}}
        ]
        Returns dict: rail -> typical_volt(float)
        """
        typical = {}
        if not isinstance(payload, list):
            return typical

        for item in payload:
            if not isinstance(item, dict):
                continue
            for rail, info in item.items():
                if not isinstance(info, dict):
                    continue
                tv = info.get("typical_volt", None)
                if tv is None:
                    continue
                try:
                    typical[rail] = float(tv)
                except Exception:
                    pass
        return typical

    # ----------------------------
    # Args
    # ----------------------------
    try:
        threshold_pct = float(getattr(args, "threshold", 10.0))
    except Exception:
        fatal("Invalid --threshold value", os.EX_USAGE)

    outfile = getattr(args, "outfile", None)
    log = None

    # ----------------------------
    # Output function (stdout always, file optional)
    # ----------------------------
    def out(line):
        print(line)
        if log is not None:
            log.write(line + "\n")

    # ----------------------------
    # listfeature check
    # ----------------------------
    try:
        ok, features, msg = unwrap(client.listfeature())
    except Exception as e:
        fatal(f"listfeature exception: {e}", os.EX_UNAVAILABLE)

    if not ok:
        fatal(f"listfeature failed: {msg}", os.EX_UNAVAILABLE)

    if not isinstance(features, list):
        fatal("listfeature returned unexpected format", os.EX_SOFTWARE)

    if "power" not in features:
        fatal("Power feature not supported (missing 'power' in listfeature)", os.EX_UNAVAILABLE)

    # ----------------------------
    # listpower
    # ----------------------------
    try:
        ok, rails_info, msg = unwrap(client.listpower())
    except Exception as e:
        fatal(f"listpower exception: {e}", os.EX_UNAVAILABLE)

    if not ok:
        fatal(f"listpower failed: {msg}", os.EX_UNAVAILABLE)

    if not isinstance(rails_info, list):
        fatal("listpower returned unexpected format (expected list)", os.EX_SOFTWARE)

    rails = []
    try:
        for item in rails_info:
            if isinstance(item, dict):
                rails.extend(item.keys())
    except Exception:
        fatal("listpower returned malformed list", os.EX_SOFTWARE)

    if not rails:
        fatal("listpower returned empty list (no sensors found)", os.EX_UNAVAILABLE)

    # ----------------------------
    # listvoltage (typical map) - not fatal if missing
    # ----------------------------
    typical_map = {}
    try:
        vok, vpayload, vmsg = unwrap(client.listvoltage())
        if vok:
            typical_map = parse_listvoltage_payload(vpayload)
    except Exception:
        typical_map = {}

    # ----------------------------
    # Open log file only if requested
    # ----------------------------
    if outfile:
        try:
            log = open(outfile, "w")
        except OSError as e:
            fatal(f"Failed to write log file '{outfile}': {e}", os.EX_CANTCREAT)

    # ----------------------------
    # Print header
    # ----------------------------
    partial_error = False
    out(f"Power log generated at: {datetime.datetime.now()}")
    out(f"Voltage mismatch threshold: {threshold_pct:.1f}%")
    out("")

    header = (
        f"{'RAIL':20} "
        f"{'SENS_V(V)':10} "
        f"{'DEF_V(V)':10} "
        f"{'CURR(A)':10} "
        f"{'POWER(W)':10} "
        f"{'STATUS':14} "
        f"COMMENT"
    )
    sep = (
        f"{'-'*20} "
        f"{'-'*10} "
        f"{'-'*10} "
        f"{'-'*10} "
        f"{'-'*10} "
        f"{'-'*14} "
        f"{'-'*40}"
    )

    out(header)
    out(sep)

    # ----------------------------
    # Per-rail dump
    # ----------------------------
    for rail in rails:
        status = "OK"
        comment = ""

        # getpower
        try:
            pok, pdata, pmsg = unwrap(client.getpower(rail))
        except Exception as e:
            pok, pdata, pmsg = (False, None, f"Error: exception: {e}")

        if not pok:
            out(
                f"{rail:20} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'ERROR':14} "
                f"{pmsg}"
            )
            partial_error = True
            continue

        if not isinstance(pdata, dict):
            out(
                f"{rail:20} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'N/A':10} "
                f"{'ERROR':14} "
                f"Error: malformed getpower data"
            )
            partial_error = True
            continue

        sens_v = pdata.get("Voltage", None)
        curr = pdata.get("Current", None)
        pw = pdata.get("Power", None)

        # typical voltage lookup (via listvoltage)
        vrm_name = vrm_rail_name(rail)
        if vrm_name != rail:
            comment = f"VRM={vrm_name}"

        typ_v = typical_map.get(vrm_name, None)
        if typ_v is None:
            comment = (comment + " | " if comment else "") + "VRM_NOT_FOUND"

        # compare sensor voltage vs typical
        try:
            if sens_v is not None and typ_v is not None:
                sens_v_f = float(sens_v)
                typ_v_f = float(typ_v)

                if typ_v_f != 0.0:
                    diff_pct = abs(sens_v_f - typ_v_f) / abs(typ_v_f) * 100.0
                    if diff_pct > threshold_pct:
                        status = "WARN"
                        comment = (comment + " | " if comment else "") + f"Vdiff={diff_pct:.1f}%"
                else:
                    status = "TYP_ZERO"
        except Exception:
            status = "BAD_VOLT_FMT"

        # output row
        sens_v_out = "N/A" if sens_v is None else str(sens_v)
        typ_v_out = "N/A" if typ_v is None else str(typ_v)
        curr_out = "N/A" if curr is None else str(curr)
        pw_out = "N/A" if pw is None else str(pw)

        out(
            f"{rail:20} "
            f"{sens_v_out:10} "
            f"{typ_v_out:10} "
            f"{curr_out:10} "
            f"{pw_out:10} "
            f"{status:14} "
            f"{comment}"
        )

    # ----------------------------
    # Cleanup
    # ----------------------------
    if log is not None:
        log.close()
        print(f"\nLog written to: {outfile}")

    if partial_error:
        sys.exit(os.EX_SOFTWARE)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    # call main
    main()

