# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import sys
import json
import argparse
sys.path.append('/usr/share/raft/xclient/raft_services')
from pm_client import PM_Client


def main():
    client = PM_Client()
    
    parser = argparse.ArgumentParser(description="Power Management Client Module CLI")
    parser.add_argument("-c", "--command", required=True, choices=["boardinfo", "domains", "powervalue", "rails", "raildetail", "railvalue", "loglevel", "pstemp", "sysmon", "stats"],
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
        
        else:
            args = parser.parse_args(remaining_args)

if __name__ == "__main__":
    # call main
    main()

