# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import os
import platform
import sys
import subprocess

if platform.machine() == 'x86_64':
    RAFT_DIR = '/usr/share/raft/'
else:
    RAFT_DIR = os.environ['RAFT_DIR']

sys.path.append(RAFT_DIR + 'xserver/utils')
#sys.path.append(os.environ['RAFT_DIR'] + 'xserver/utils')
import logging
import json
from enum import Enum
from pmic_i2c import I2C_Client
import pmic_ina226 as INA226
#from pmic_spi import spi

class DeviceType(Enum):
    INA226 = 1
    INA230 = 2
    SYSMON = 99
    #Possible other Power Monitor IC definitions here.

class SensorData:
    def __init__(self, tag, name, client ):
        self.tag = tag
        self.name = name
        self.client = client
        vshunt = 0
        vbus = 0
        current = 0
        power = 0
        overflow = False
   
    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['client'] and v
        }
        return str(str_info)



class PMIC(object):
    device_id = 0
    logger = None
    sensor_list = []

    def __init__(self, supplies):
        self.logger = self.GetLogger()
        for s in supplies:
            match s['device_type']:
                case 'INA226':
                    d_type = DeviceType.INA226
                    sensor = SensorData(s['domain_tag'], s['name'], I2C_Client(s['device'], s['addr'], d_type))
                    print(str(sensor))
                    self.sensor_list.append(sensor)
                case 'INA230':
                    d_type = DeviceType.INA230
                    sensor = SensorData(s['domain_tag'], s['name'], I2C_Client(s['addr'], d_type))
                    print(str(sensor))
                    self.sensor_list.append(sensor)
                case _:
                    self.logger.error("Wrong Device type")
        
        ret = self.InitBoard()

        if True != ret:
            self.logger.error(f"PMIC: InitBoardInfo failed. ret = {ret}")
        self.logger.info("Inside PMIC Constructor")
        pass

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :return: logger

        """
        log_level = logging.DEBUG
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

    def InitBoard(self):
        self.logger.debug("InitBoardInfo called")
        for s in self.sensor_list:
            s.client.Initialize()
        
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

    def ReadSensorVoltage(sensor):
        match sensor.client.device_type:
            case DeviceType.INA226:
                value = sensor.client.ReadReg(INA226.REG_BUSVOLTAGE)
                return float(value) * INA226.BUS_MILLIVOLTS_LSB / 1000
            case _:
                return 0
    def ReadSensorCurrent(sensor):
        match sensor.client.device_type:
            case DeviceType.INA226:
                pass
            case _:
                pass
        pass
    
    def ReadSensorSupplyVoltage(sensor):
        match sensor.client.device_type:
            case DeviceType.INA226:
                #sensor.client.
                pass
            case _:
                pass
        pass
    def ReadSensorShuntVoltage(sensor):
        match sensor.client.device_type:
            case DeviceType.INA226:
                pass
            case _:
                pass
        pass
    def ReadSensorPower(sensor):
        match sensor.client.device_type:
            case DeviceType.INA226:
                pass
            case _:
                pass
        pass



    def voltage(self):
        """Return the bus voltage in volts."""
        value = self._voltage_register()
        return float(value) * self.__BUS_MILLIVOLTS_LSB / 1000

    def supply_voltage(self):
        """Return the bus supply voltage in volts.

        This is the sum of the bus voltage and shunt voltage. A
        DeviceRangeError exception is thrown if current overflow occurs.
        """
        return self.voltage() + (float(self.shunt_voltage()) / 1000)

    def current(self):
        """Return the bus current in milliamps.

        A DeviceRangeError exception is thrown if current overflow occurs.
        """
        self._handle_current_overflow()
        return self._current_register() * self._current_lsb * 1000

    def power(self):
        """Return the bus power consumption in milliwatts.

        A DeviceRangeError exception is thrown if current overflow occurs.
        """
        self._handle_current_overflow()
        return self._power_register() * self._power_lsb * 1000

    def shunt_voltage(self):
        """Return the shunt voltage in millivolts.

        A DeviceRangeError exception is thrown if current overflow occurs.
        """
        self._handle_current_overflow()
        return self._shunt_voltage_register() * self.__SHUNT_MILLIVOLTS_LSB

  # print("Bus Voltage    : %.3f V" % ina.voltage())
   # print("Bus Current    : %.3f mA" % ina.current())
   # print("Supply Voltage : %.3f V" % ina.supply_voltage())
   # print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
   # print("Power          : %.3f mW" % ina.power())

    def GetSensor(self, tag, supplyname):
        sensor = None
        for _s in self.sensor_list:
            if _s.tag == tag and _s.name == supplyname:
                sensor = _s
        return sensor

    def GetSensorValues(self, sensor):
        ReadSensorVoltage(sensor)
        ReadSensorCurrent(sensor)
        ReadSensorSupplyVoltage(sensor)
        ReadSensorShuntVoltage(sensor)
        ReadSensorPower(sensor)
        return str(sensor)


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
        self.logger.info("Inside PMIC Destructor")
