#!/usr/bin/env python3
# Copyright (C) 2023 - 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023 - 2026, Advanced Micro Devices, Inc."

import os
import sys
import json
import logging
import Pyro4

# Ensure immediate flush for stdout
sys.stdout.reconfigure(line_buffering=True)

# Add required paths
sys.path.extend([
    '../../utils',
    '../../raft_services',
    '../../raft_services/power_management'
])

import board_identity
from pm import PM
from utils import get_ip_and_port

RAFT_DIR = '/usr/share/raft/'
BOARD_PATH = os.path.join(RAFT_DIR, 'xserver/raft_services/power_management/board')

# -------------------------
# Robust Logging Setup
# -------------------------
def setup_logging():
    # Remove existing handlers (e.g., Pyro4 may add its own)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create our own unbuffered stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    stdout_handler.flush = sys.stdout.flush

    logging.basicConfig(
        level=logging.INFO,
        handlers=[stdout_handler],
        force=True  # Python 3.8+: ensures config applies even if prior handlers exist
    )

setup_logging()

# -------------------------
# Utility functions
# -------------------------
def exit_program(msg="Critical Error: Unable to Run Raft-PM Server."):
    logging.error(msg)
    sys.exit(1)

def is_valid_json_file(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"Board JSON not found: {file_path}")
        return False
    try:
        with open(file_path, 'r') as file:
            json.load(file)
            return True
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON content: {file_path}")
        return False

# -------------------------
# Pyro4 Daemon
# -------------------------
def start_pyro_daemon():
    IPADDR, PORT = get_ip_and_port()
    logging.debug(f"Detected IPADDR={IPADDR}, PORT={PORT}")
    if not IPADDR:
        exit_program("No network interface found. Cannot start Pyro4 daemon.")

    try:
        board_name, board_revision = board_identity.get_board_identity()
    except board_identity.BoardIdentityError as exc:
        exit_program(str(exc))

    json_file = board_identity.resolve_board_json_path(
        BOARD_PATH, board_name, board_revision
    )

    if json_file is None or not is_valid_json_file(json_file):
        exit_program("Invalid or missing board configuration JSON.")

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    try:
        pm_obj = PM(json_data, board_name, board_revision)
        daemon = Pyro4.Daemon(host=IPADDR, port=PORT)
        uri = daemon.register(pm_obj, objectId="PM")

        logging.info("RAFT-PM Server started successfully.")
        logging.info(f"Listening on {IPADDR}:{PORT}")

        daemon.requestLoop()
    except Exception as e:
        exit_program(f"Pyro4 Daemon startup failed: {e}")

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    start_pyro_daemon()
