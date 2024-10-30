# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import Pyro4
import Pyro4.utils
import logging
import base64
import json
import sys

sys.excepthook = Pyro4.util.excepthook

class PM_Client(object):
    PM = None
    logger = None
    LogLevelsDict = {
        "DEBUG": 4,
        "INFO": 3,
        "WARNING": 2,
        "ERROR": 1,
        "CRITICAL": 0
    }

    def __init__(self):
        self.logger = self.GetLogger()
        self.logger.info("Inside Raft-PM Client Constructor")
        self.SetIpAndPort("127.0.0.1", "9090")
        return

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
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.handler_set = True
            logger.disabled = False
        return logger

    def SetIpAndPort(self, ipaddr, port):
        """
        API to inform PM Client the IP address and port number of PM Server.

        :param ipaddr: IP Address string
        :param port: Port number string
        :return: None
        """
        uri = f"PYRO:PM@{ipaddr}:{port}"
        self.logger.debug(f"SetIpAndPort({ipaddr}, {port})\n uri = {uri}")
        self.PM = Pyro4.Proxy(uri)
        pass

    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :return: Dictionary showing the log levels supported by logging library
        """
        self.logger.debug("GetPythonLogLevels()")
        PythonLogLevel = self.PM.GetPythonLogLevels()
        self.logger.debug(f"PythonLogLevel = {json.dumps(PythonLogLevel, indent=2)}")
        return PythonLogLevel

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param PythonLogLevel: Log level to set
        :return: None
        """
        self.logger.debug(f"SetServerLogLevel({PythonLogLevel})")
        self.PM.SetServerLogLevel(PythonLogLevel)
        return

    def SetClientLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param PythonLogLevel: Log level to set
        :return: None
        """
        if PythonLogLevel == self.LogLevelsDict["DEBUG"]:
            self.logger.setLevel(logging.DEBUG)
        elif PythonLogLevel == self.LogLevelsDict["INFO"]:
            self.logger.setLevel(logging.INFO)
        elif PythonLogLevel == self.LogLevelsDict["WARNING"]:
            self.logger.setLevel(logging.WARNING)
        elif PythonLogLevel == self.LogLevelsDict["ERROR"]:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.CRITICAL)
        return

    def GetBoardInfo(self):
        """
        Gets Board's Info

        :param : None
        :return: Board Info
        """
        self.logger.debug("GetBoardInfo()")
        return self.PM.GetBoardInfo()

    def GetPowerDomains(self):
        """
        Gets list of Power Domains.

        :param : None
        :return: Domains
        """
        self.logger.debug("GetPowerDomains()")
        return self.PM.GetPowerDomains()

    def GetRailsOfDomain(self, domainname):
        """
        Gets list of Rails given domain name.

        :param domainname: string of a "domainname"
        :return: Rails
        """
        self.logger.debug("GetRailsOfDomain()")
        return self.PM.GetRailsOfDomain(domainname)

    def GetRailDetails(self, railname):
        """
        Gets list of the rail's details given rail name.

        :param railname: string of a "railname"
        :return: Details of the Rail
        """
        self.logger.debug(f"GetRailDetails({railname})")
        return  self.PM.GetPowerSensorConf(railname)


    def GetValueOfRail(self, railname):
        """
        Gets list of the rail's sensor values given rail name.

        :param railname: string of a "railname"
        :return: Sensor values of the Rail
        """
        self.logger.debug(f"GetValueOfRail({railname})")
        return self.PM.GetPowerSensor(railname)

    def GetValueOfDomain(self, domainname):
        """
        Gets the domain's all rail sensor values given domain name.

        :param : string of a "domainname"
        :return: The domain's all rails sensor values of the Rail
        """
        self.logger.debug("GetValueOfDomain({domainname})")
        return self.PM.GetValueOfDomain(domainname)

    def GetPowersAll(self):
        """
        Gets the boards's all domain's and total power values

        :param : None
        :return: The boards's all domain's and total power values
        """
        self.logger.debug("GetPowersAll()")
        return self.PM.GetPowersAll()

    def GetValuesAll(self):
        """
        Gets the boards's all domain's rails sensor values

        :param : None
        :return: The board's all rails sensor values of the Rail
        """
        self.logger.debug("GetValuesAll()")
        return self.PM.GetValuesAll()

    def GetSysmonTemperatures(self):
        """
        Gets the Sysmon temperature values

        :param : None
        :return: The sysmon temperature values
        """
        self.logger.debug("GetSysmonTemperatures()")
        return self.PM.GetSysmonTemperatures()

    def GetPSTemperature(self):
        """
        Gets the PS temperature value

        :param : None
        :return: The PS temperature value
        """
        self.logger.debug("GetPSTemperature()")
        return self.PM.GetPSTemperature()

    def GetSystemStats(self):
        """
        Get the System Status value

        :param : None
        :return: The System Status value
        """
        self.logger.debug("GetSystemStats()")
        return self.PM.GetSystemStats()

    def ListPowerSensors(self):
        self.logger.debug("ListPowerSensors()")
        return self.PM.ListPowerSensors()

    def GetPowerSensor(self, name):
        self.logger.debug("GetPowerSensor()")
        return self.PM.GetPowerSensor(name)

    def GetCalPowerSensor(self, name):
        self.logger.debug("GetCalPowerSensor()")
        return self.PM.GetCalPowerSensor(name)

    def GetPowerSensorConf(self, name):
        self.logger.debug("GetPowerSensorConf()")
        return self.PM.GetPowerSensorConf(name)

    def SetPowerSensorConf(self, name, conf):
        self.logger.debug("SetPowerSensorConf()")
        return self.PM.SetPowerSensorConf(name, conf)

    def ListVoltages(self):
        self.logger.debug("ListVoltages()")
        return self.PM.ListVoltages()

    def EnableVoltage(self, name):
        self.logger.debug("EnableVoltage()")
        return self.PM.EnableVoltage(name)

    def DisableVoltage(self, name):
        self.logger.debug("DisableVoltage()")
        return self.PM.DisableVoltage(name)

    def GetRegulatorAll(self, name):
        self.logger.debug("GetRegulatorAll()")
        return self.PM.GetRegulatorAll(name)

    def GetVoltage(self, name):
        self.logger.debug("GetVoltage()")
        return self.PM.GetVoltage(name)

    def SetVoltage(self, name, value):
        self.logger.debug("SetVoltage()")
        return self.PM.SetVoltage(name, value)

    def SetBootVoltage(self, name, value):
        """
        Set boot voltage for the regulator.

        :name : voltage regulator name
        :value : voltage value in volt
        :return: Success mesage
        """
        self.logger.debug("SetBootVoltage()")
        return self.PM.SetBootVoltage(name, value)

    def RestoreVoltage(self, name):
        """
        Reset to typical voltage.

        :name : voltage output name
        :return: Success mesage
        """
        self.logger.debug("RestoreVoltage()")
        return self.PM.RestoreVoltage(name)

pm = PM_Client()