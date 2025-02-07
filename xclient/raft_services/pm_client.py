# Copyright (C) 2023-2025 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2025, Advanced Micro Devices, Inc."

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

    def getboardinfo(self):
        """
        Gets Board's Info

        :param : None
        :return: Board Info
        """
        self.logger.debug("getboardinfo()")
        return self.PM.GetBoardInfo()

    def listfeature(self):
        """
        Gets feature list

        :param : None
        :return: Feature List
        """
        self.logger.debug("listfeature()")
        return self.PM.ListFeature()

    def listpowerdomain(self):
        """
        Gets list of Power Domains.

        :param : None
        :return: Domains
        """
        self.logger.debug("listpowerdomain()")
        return self.PM.ListPowerDomains()

    def listrailsofdomain(self, domainname):
        """
        Gets list of Rails given domain name.

        :param domainname: string of a "domainname"
        :return: Rails name list
        """
        self.logger.debug("listrailsofdomain()")
        return self.PM.ListRailsOfDomain(domainname)

    def getvalueofrail(self, railname):
        """
        Gets list of the rail's sensor values given rail name.

        :param railname: string of a "railname"
        :return: Sensor values of the Rail
        """
        self.logger.debug(f"getvalueofrail({railname})")
        return self.PM.GetPowerSensor(railname)

    def getvalueofdomain(self, domainname):
        """
        Gets the domain's all rail sensor values given domain name.

        :param : string of a "domainname"
        :return: The domain's all rails sensor values of the Rail
        """
        self.logger.debug("getvalueofdomain({domainname})")
        return self.PM.GetValueOfDomain(domainname)

    def getpowerall(self):
        """
        Gets the boards's all domain's and total power values

        :param : None
        :return: The boards's all domain's and total power values
        """
        self.logger.debug("getpowerall()")
        return self.PM.GetPowersAll()

    def getvalueall(self):
        """
        Gets the boards's all domain's rails sensor values

        :param : None
        :return: The board's all rails sensor values of the Rail
        """
        self.logger.debug("getvalueall()")
        return self.PM.GetValuesAll()

    def listtemperature(self):
        """
        Gets the Sysmon temperature values

        :param : None
        :return: The sysmon temperature values
        """
        self.logger.debug("listtemperature()")
        return self.PM.ListTemperatures()

    def gettemperature(self, name):
        """
        Gets the Sysmon temperature values

        :param : None
        :return: The sysmon temperature values
        """
        self.logger.debug("GetSysmonTemperatures()")
        return self.PM.GetTemperature(name)

    def listpower(self):
        self.logger.debug("ListPowerSensors()")
        return self.PM.ListPowerSensors()

    def getpower(self, name):
        self.logger.debug("GetPowerSensor()")
        return self.PM.GetPowerSensor(name)

    def getcalpower(self, name):
        self.logger.debug("GetCalPowerSensor()")
        return self.PM.GetCalPowerSensor(name)

    def getpowerconf(self, name):
        self.logger.debug("GetPowerSensorConf()")
        return self.PM.GetPowerSensorConf(name)

    def setpowerconf(self, name, conf):
        self.logger.debug("SetPowerSensorConf()")
        return self.PM.SetPowerSensorConf(name, conf)

    def listvoltage(self):
        self.logger.debug("ListVoltages()")
        return self.PM.ListVoltages()

    def enablevoltage(self, name):
        self.logger.debug("EnableVoltage()")
        return self.PM.EnableVoltage(name)

    def disablevoltage(self, name):
        self.logger.debug("DisableVoltage()")
        return self.PM.DisableVoltage(name)

    def getregulator(self, name):
        self.logger.debug("GetRegulator()")
        return self.PM.GetRegulator(name)

    def getvoltage(self, name):
        self.logger.debug("GetVoltage()")
        return self.PM.GetVoltage(name)

    def setvoltage(self, name, value):
        self.logger.debug("SetVoltage()")
        return self.PM.SetVoltage(name, value)

    def setbootvoltage(self, name, value):
        """
        Set boot voltage for the regulator.

        :name : voltage regulator name
        :value : voltage value in volt
        :return: Success mesage
        """
        self.logger.debug("SetBootVoltage()")
        return self.PM.SetBootVoltage(name, value)

    def restorevoltage(self, name):
        """
        Reset to typical voltage.

        :name : voltage output name
        :return: Success mesage
        """
        self.logger.debug("RestoreVoltage()")
        return self.PM.RestoreVoltage(name)

    def listunit(self):
        self.logger.debug("ListUnits()")
        return self.PM.ListUnits()

    def getunit(self, quantity):
        self.logger.debug("GetUnit()")
        return self.PM.GetUnit(quantity)

    def setscale(self, quantity, scale):
        self.logger.debug("SetScale()")
        return self.PM.SetScale(quantity, scale)

    def listscale(self, quantity):
        self.logger.debug("ListAvailableScales()")
        return self.PM.ListAvailableScales(quantity)

pm = PM_Client()