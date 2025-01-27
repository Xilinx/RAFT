# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim, Sree Parvathi Anish"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import os
import sys
import json
import argparse
import csv
import time
import datetime
sys.path.append('/usr/share/raft/xclient/raft_services')
from pm_client import PM_Client

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
    except IOError:
        print(f"I/O error while opening {csv_file} to write")


def print_response(response):
    print(json.dumps(response, indent=2))

def main():
    client = PM_Client()

    parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
    parser.add_argument("-c", "--command", required=True, choices=[
                        "boardinfo", "listfeature", "domains", "powervalue", "allvalue", "rails", "railvalue",
                        "listpower", "getpower", "getcalpower", "getinaconf", "setinaconf",
                        "listvoltage", "enablevoltage", "disablevoltage", "getvoltage", "setvoltage", "setbootvoltage", "restorevoltage", "getregulator",
                        "loglevel", "sysmon",
                        "output-csv",
                        "listunits", "getunit", "availablescales", "setscale"],
                        help="Specify the command (boardinfo, domains, rails or railvalue ...)")
    args, remaining_args = parser.parse_known_args()
    match args.command:
        case "boardinfo":
            print_response(client.getboardinfo())
        case "listfeature":
            print_response(client.listfeature())
        case "domains":
            print_response(client.listpowerdomain())
        case "powervalue":
            print_response(client.getpowerall())
        case "allvalue":
            print_response(client.getvalueall())
        case "rails":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.listrailsofdomain(target_args.target))
        case "railvalue":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getvalueofrail(target_args.target))
        case "loglevel":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=False, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target is None:
                print_response(client.logger.level)
            else:
                if target_args.target:
                    print(f"Target: {target_args.target}")
        case "sysmon":
            print_response(client.gettemperature('Versal'))
        case "listpower":
            print_response(client.listpower())
        case "getpower":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getpower(target_args.target))
        case "getcalpower":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getcalpower(target_args.target))
        case "getinaconf":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getpowerconf(target_args.target))
        case "setinaconf":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                value_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
                value_parser.add_argument('-l', '--list', type=json.loads, required=True, help="Specify the target")
                value_args, value_remining_args = value_parser.parse_known_args(target_remining_args)
                if value_args.list:
                    print_response(client.setpowerconf(target_args.target, value_args.list))
        case "listvoltage":
            print_response(client.listvoltage())
        case "enablevoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.enablevoltage(target_args.target))
        case "disablevoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.disablevoltage(target_args.target))
        case "getvoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getvoltage(target_args.target))
        case "setvoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                value_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
                value_parser.add_argument("-v", "--value", required=True, help="Specify the target")
                value_args, value_remining_args = value_parser.parse_known_args(target_remining_args)
                if value_args.value:
                    print_response(client.setvoltage(target_args.target, round(float(value_args.value), 3)))
        case "setbootvoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                value_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
                value_parser.add_argument("-v", "--value", required=True, help="Specify the target")
                value_args, value_remining_args = value_parser.parse_known_args(target_remining_args)
                if value_args.value:
                    print_response(client.setbootvoltage(target_args.target, round(float(value_args.value), 3)))
        case "restorevoltage":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                    print_response(client.restorevoltage(target_args.target))
        case "getregulator":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getregulator(target_args.target))
        case "listunits":
                print_response(client.listunit())
        case "getunit":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.getunit(target_args.target))
        case "availablescales":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                print_response(client.listscale(target_args.target))
        case "setscale":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            if target_args.target:
                value_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
                value_parser.add_argument("-v", "--value", required=True, help="Specify the target")
                value_args, value_remining_args = value_parser.parse_known_args(target_remining_args)
                if value_args.value:
                    print_response(client.setscale(target_args.target, value_args.value))
        case "output-csv":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-d", "--duration", required=True, help="Specify the duration in seconds")
            target_parser.add_argument("-s", "--samplingrate", required=True, help="Specify the sampling rate")
            target_parser.add_argument("-o", "--outputfilepath", default='/home/petalinux', help="Specify the path to write the file")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            print(f"target_args.duration = {target_args.duration}, target_remining_args.samplingrate = {target_args.samplingrate}")
            sample_rate = int(target_args.samplingrate)
            filepath = target_args.outputfilepath
            duration = int(target_args.duration)
            # Check the input arguments
            if (sample_rate < 1 or sample_rate > 12):
                print(f"sample rate should be between 1 and 12")
                sys.exit(1)
            if (duration <= 0):
                print(f"duration should be a positive value")
                sys.exit(1)
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
        case _:
            args = parser.parse_args(remaining_args)

if __name__ == "__main__":
    # call main
    main()

