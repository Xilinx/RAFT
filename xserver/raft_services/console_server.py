# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Dragan Cvetic"
__copyright__ = "Copyright 2022, Xilinx"

import sys
import subprocess
RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
from utils import xhelper_handle
from utils import get_python_log_levels


class CONSOLE(object):
    device_id = 0
    logger = None

    def __init__(self):
        self.logger = self.GetLogger()
        ret = xhelper_handle.XHelper_MetalInit(xhelper_handle.METAL_LOG_ERROR)
        if 0 != ret:
            self.logger.error(f"CONSOLE: XHelper_MetalInit failed. ret = {ret}")
        self.logger.info("Inside CONSOLE Constructor")
        pass

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :return: logger

        """
        log_level = logging.ERROR
        logging.basicConfig(format="%(levelname)s:%(message)s")
        logger = logging.getLogger(__name__)
        try:
            handler_set_check = getattr(logger, 'handler_set')
        except AttributeError:
            handler_set_check = False
        if not handler_set_check:
            logger.setLevel(log_level)
            logger.handler_set = True
            logger.disabled = False
        return logger

    # Log level
    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        return get_python_log_levels()

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"PythonLogLevel = {PythonLogLevel}")
        LogLevelsDict = get_python_log_levels()
        if PythonLogLevel == LogLevelsDict["DEBUG"]:
            self.logger.setLevel(logging.DEBUG)
        elif PythonLogLevel == LogLevelsDict["INFO"]:
            self.logger.setLevel(logging.INFO)
        elif PythonLogLevel == LogLevelsDict["WARNING"]:
            self.logger.setLevel(logging.WARNING)
        elif PythonLogLevel == LogLevelsDict["ERROR"]:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.CRITICAL)
        return

    def RaftConsole(self, str_cmd):
        """
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        """
        self.logger.debug(f"execute: " + str_cmd)
        ret = subprocess.getstatusoutput(str_cmd)
        status = ret[0]
        str_cmd_ret = ret[1]
        self.logger.debug(f"return: status: {status}, command output: {str_cmd_ret}")
        return status, str_cmd_ret

    def __del__(self):
        self.logger.info("Inside CONSOLE Destructor")
