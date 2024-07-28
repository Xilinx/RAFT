# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim, Sree Parvathi Anish"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import sys
import json
import argparse
import csv
import time
sys.path.append('/usr/share/raft/xclient/raft_services')
from pm_client import PM_Client

# Specify the CSV file to write
csv_file = '/home/petalinux/pm-getvaluesall-output.csv'

def update_csv_data(csv_data, data):
    # Convert the dictionary to a list
    flat_data = []
    for pd in data["VCK190"]:
        for key, value in pd.items():
            total = value["Total Power"]
            for rails_item in value["Rails"]:
                for rails_key, rails_value in rails_item.items():
                    row_item = {"Rails": rails_key, "Power Domain": key}
                    row_item.update(rails_value)
                    row_item["Total Power"] = total
                    flat_data.append(row_item)
    csv_data.append(flat_data)
    return csv_data

def pm_csv_dump(csv_data):
    # Specify the order of the columns
    columns_order = ["Power Domain", "Rails", "Voltage", "Current", "Power", "Total Power"]

    try:
        with open(csv_file, 'w') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=columns_order, lineterminator='\n')
            csv_writer.writeheader()
            for data in csv_data:
                for row in data:
                    csv_writer.writerow(row)
                csv_writer.writerow({})
            print(f"The requested data is written to file - {csv_file}")
    except IOError:
        print(f"I/O error while opening {csv_file} to write")

def main():
    client = PM_Client()
    
    parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
    parser.add_argument("-c", "--command", required=True, choices=["boardinfo", "domains", "powervalue", "rails", "raildetail", "railvalue", "loglevel", "pstemp", "sysmon", "stats", "output-csv"],
                            help="Specify the command (boardinfo, domains, rails or railvalue)")

    args, remaining_args = parser.parse_known_args()

    if args.command:
        if args.command == "rails":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)

            if target_args.target:
                print(json.dumps(client.GetRailsOfDomain(target_args.target)))
        
        elif args.command == "railvalue":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)

            if target_args.target:
                print(json.dumps(client.GetValueOfRail(target_args.target)))
        elif args.command == "raildetail":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=True, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)

            if target_args.target:
                print(json.dumps(client.GetRailDetails(target_args.target)))

        elif args.command == "boardinfo":
            print(json.dumps(client.GetBoardInfo()))
        
        elif args.command == "domains":
            print(json.dumps(client.GetPowerDomains()))

        elif args.command == "powervalue":
            print(json.dumps(client.GetPowersAll()))

        elif args.command == "loglevel":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-t", "--target", required=False, help="Specify the target")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)

            if target_args.target is None:
                print(json.dumps(client.logger.level))
            else:
                if target_args.target:
                    print(f"Target: {target_args.target}")
        
        elif args.command == "sysmon":
            print(json.dumps(client.GetSysmonTemperatures()))
            
        elif args.command == "pstemp":
            print(json.dumps(client.GetPSTemperature()))

        elif args.command == "stats":
            print(json.dumps(client.GetSystemStats()))

        elif args.command == "output-csv":
            target_parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
            target_parser.add_argument("-d", "--duration", required=True, help="Specify the duration in seconds")
            target_parser.add_argument("-s", "--samplingrate", required=True, help="Specify the sampling rate")
            target_args, target_remining_args = target_parser.parse_known_args(remaining_args)
            print(f"target_args.duration = {target_args.duration}, target_remining_args.samplingrate = {target_args.samplingrate}")
            sample_rate = int(target_args.samplingrate)
            # Check the input arguments
            if (sample_rate < 1 or sample_rate > 12):
                print(f"sample rate should be between 1 and 12")
                sys.exit(1)
            if (int(target_args.duration) <= 0):
                print(f"duration should be a positive value")
                sys.exit(1)
            # Find the sleep time from the sample rate
            sleeptime = 1/sample_rate

            csv_data = []
            # Mark the start time
            start_time = time.time()
            while True:
                operation_start_time = time.time()
                values = client.GetValuesAll()
                csv_data = update_csv_data(csv_data, values)
                operation_exec_time = time.time() - operation_start_time
                # If operation execution time is higher than sleep time, no need to sleep
                if (sleeptime - operation_exec_time) > 0:
                    time.sleep(sleeptime -  operation_exec_time)
                if time.time() - start_time >= int(target_args.duration):
                    break
            pm_csv_dump(csv_data)
        
        else:
            args = parser.parse_args(remaining_args)

if __name__ == "__main__":
    # call main
    main()

