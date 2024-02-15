# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import os
import platform
import sys
import subprocess
import time


RAFT_DIR = '/usr/share/raft/'

sys.path.append(RAFT_DIR + 'xserver/utils')
import logging
import json
from enum import Enum
from pmic_i2c import I2C_Client
from pmic_ina226 import INA226
#from pmic_spi import spi

class Rails:
    def __init__(self, Name, I2C_Bus, I2C_Address, Shunt_Resistor, Maximum_Current, Phase_Multiplier):
        self.name = Name
        self.i2c_bus = I2C_Bus
        self.i2c_address = I2C_Address
        self.shunt_resistor = Shunt_Resistor
        self.maximum_current = Maximum_Current
        self.phase_multiplier = Phase_Multiplier
        self._device_type = 0
        self._sensor = None

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['i2c_bus', 'i2c_address', 'shunt_resistor', 'maximum_current','phase_multiplier', '_device_type', '_sensor'] and v
        }
        return str(str_info)
    pass
class Domain:
    def __init__(self, Name, Rails):
        self.name = Name
        self.railnames = Rails
        self.rails = []
    
    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['railnames', 'rails'] and v
        }
        return str(str_info)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class DeviceType(Enum):
    INA226 = 1
    INA230 = 2
    SYSMON = 99
    #Possible other Power Monitor IC definitions here.

class SensorData:
    def __init__(self, name, domain_name, device, Shunt_Resistor, Maximum_Current , Phase_Multiplier):
        self.name = name
        self.domain_name = domain_name
        self.device = device
        self.shunt_resistor = Shunt_Resistor
        self.maximum_current = Maximum_Current
        self.phase_multiplier = Phase_Multiplier
        self.vbus = 0.0
        self.current = 0.0
        self.power = 0.0
        overflow = False
        
    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['domain_name', 'device', 'shunt_resistor', 'maximum_current','phase_multiplier'] and v
        }
        return str(str_info)

class PMIC(object):
    device_id = 0
    logger = None
    sensor_list = []

    def __init__(self, domains, sysmons):
        self.logger = self.GetLogger()
        for d in domains:
            for r in d.rails:
                if r._device_type == DeviceType.INA226:
                    r._sensor = SensorData(r.name, d.name, INA226(r.i2c_address, r.i2c_bus), r.shunt_resistor, r.maximum_current, r.phase_multiplier)
                #elif r._device_type == DeviceType.INAxxx: # Future developments
                #    r._sensor = SensorData(r.name, d.name, INA226(r.i2c_address, r.i2c_bus), r.shunt_resistor, r.maximum_current, r.phase_multiplier)
                else:
                    self.logger.error(f"PMIC: Wrong Device/Sensor Type. railname = {r.name}")
                self.sensor_list.append(r._sensor)
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
        """
        Initialize Board's sensor calibration values

        :param : None
        :return: True: Sensor initializations are successful
        """
        ret = True
        self.logger.debug("InitBoardInfo called")
        for s in self.sensor_list:
           ret &= s.device.initSensor(s.maximum_current, s.shunt_resistor, s.phase_multiplier)
        return ret

    def BoardInfo(self, eeprom):
        """
        Create Board's Info

        :param : None
        :return: Board info in json formatted
        """
        boardinfo = {}
        i2c = I2C_Client(eeprom.I2C_Bus, eeprom.I2C_Addr)
        result, eeprom_data = i2c.ReadRegister(0x00, 256)
        if result:
            offset = 0xA
            boardinfo["Language"] = eeprom_data[offset]
            #offset = 0xB
            #a = _struct_time(tm_year=96, tm_mday=1, tm_min= int.from_bytes(eeprom_data[offset:offset+2], "big"))
            #manu_time.tm_year = 96
            #manu_time.tm_mday = 1
            #manu_time.tm_min = int.from_bytes(eeprom_data[offset:offset+2], "big")
            #_time = time.mktime(a)
            #board["Manufacturing Date"] = time.ctime(_time)

            offset = 0xe
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Manufacturer"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')

            offset = offset + length + 1
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Product Name"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')

            offset = offset + length + 1
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Board Serial Number"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')
            
            offset = offset + length + 1
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Board Part Number"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')

            offset = offset + length + 1
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Board Revision"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')
        i2c.Release()
        return boardinfo

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

    def GetSensor(self, domainname, railname):
        """
        Get sensor object of given domain and rail name

        :param : None
        :return: sensor object, low level sensor handler.
        """
        sensor = None
        for _s in self.sensor_list:
            if _s.domain_name == domainname and _s.name == railname:
                sensor = _s
        return sensor

    def GetSensorValues(self, sensor):
        """
        Find and Get sensor object of given domain and rail name

        :param : None
        :return: Sensor Bus Voltage, Current and Power values
        """
        sensor.current = sensor.device.getCurrent()
        sensor.vbus = sensor.device.getBusVoltage()
        sensor.power = sensor.device.getPower()
        return sensor.vbus, sensor.current, sensor.power

    def __del__(self):
        self.logger.info("Inside PMIC Destructor")
