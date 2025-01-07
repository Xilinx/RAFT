# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import os
import sys
import logging
import dbm.dumb


RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
sys.path.append(RAFT_DIR + 'xserver/raft_services/power_management/devices')

from pmic import PMIC
from devices.stats import Stats
from devices.sysmon import Sysmon
from utils import get_python_log_levels
from pm_types import *


class PM(object):
    logger = None
    domains = []
    sensors = []
    voltages = []
    pmic = None
    sysmon = None
    status = None
    pdi_file = ""

    def __init__(self, json_data, board_name, eeprom):
        self.logger = self.GetLogger()
        self.boardeeprom = eeprom
        self.board_name = board_name
        board_data = json_data[board_name]
        self.pdi_file = None

        if 'FEATURE' in board_data:
            feature_list = board_data['FEATURE']['List']

        if 'powerdomain' in feature_list:
            if 'POWER DOMAIN' in board_data:
                for key, val in board_data['POWER DOMAIN'].items():
                    temp_d = Domain(**val)
                    for index, railname in enumerate(temp_d.railnames):
                        for k, v in board_data['POWER_SENSORS'].items():
                            if k == railname:
                                if temp_d.railnames[index] != v['Name']:
                                    temp_d.railnames[index] = v['Name']
                    self.domains.append(temp_d)

        if 'power' in feature_list:
            if 'POWER_SENSORS' in board_data:
                for k, v in board_data['POWER_SENSORS'].items():
                    temp_r = Rails(**v)
                    self.sensors.append(temp_r)

        if 'voltage' in feature_list:
            if 'VOLTAGE' in board_data:
                for k, v in board_data['VOLTAGE'].items():
                    tempVolt = Rails(**v)
                    self.voltages.append(tempVolt)

        if 'temp' in feature_list:
            if 'Temperature' in board_data:
                if "versal-isa" in board_data['Temperature']['Sensor']:
                    try:
                        self.sysmon = Sysmon(None, None, Sysmon_Device_Type.SYSFS)
                    except Exception as e:
                        print(e)
                elif "i2c" in board_data['Temperature']['Sensor']:
                    tokens = board_data['Temperature']['Sensor'].split("-")
                    address = tokens[3]
                    device_path = "/dev/i2c-" + tokens[2]
                    try:
                        self.sysmon = Sysmon(address, device_path, Sysmon_Device_Type.I2C)
                    except Exception as e:
                        print(e)

        if 'Boot Config' in board_data:
            self.pdi_file = board_data['Boot Config']['PDI']

        try:
            self.status = Stats()
            if self.status is None:
                self.logger.error(f"InitStats failed.")
        except Exception as e:
            self.logger.error(f"InitStats failed. ({e})")
            self.exit_program()

        try:
            self.pmic = PMIC(self.domains, self.sensors, self.voltages)
        except Exception as e:
            self.logger.error(f"InitPmic failed. ({e})")
            self.exit_program()

        if self.pmic is None:
            self.logger.error(f"PMIC not found.")
            self.exit_program()
        self.logger.info("Inside PM Constructor")

    @staticmethod
    def exit_program():
        logging.critical("CRITICAL ERROR: Unable to Run Pyro Server.\n")
        sys.exit(1)

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

    def GetBoardInfo(self):
        """
        Gets Board's Info

        :param : None
        :return: Board Info
        """
        data = {}
        if self.boardeeprom is None:
            data['Success'] = False
            data['Message'] = f'Board Eeprom undefined'
        else:
            data = self.pmic.GetBoardInfo(self.boardeeprom, self.pdi_file)
        return data

    def GetPSTemperature(self):
        """
        Gets SysCtl's Temperature Info

        :param : None
        :return: SysCtl's Temperature Info
        """
        return self.status.getTemperatures()

    def GetPowerDomains(self):
        """
        Gets list of Power Domains.

        :param : None
        :return: Domains
        """
        powerdomains = {}
        powerdomains['POWER DOMAINS'] = []
        for d in self.domains:
            powerdomains['POWER DOMAINS'].append({'name': d.name})
        return powerdomains

    def _find_domain(self, domainname):
        temp_d = None
        for d in self.domains:
            if d.name == domainname:
                temp_d = d
        return temp_d

    def GetRailsOfDomain(self, domainname):
        """
        Gets list of Rails given domain name.

        :param domainname: string of a "domainname"
        :return: Rails
        """
        data = {}
        domain = self._find_domain(domainname)
        if domain is None:
            data['Success'] = False
            data['Message'] = f'{domainname} does not exists'
        else:
            data[domainname] = []
            for name in domain.railnames:
                data[domainname].append({'name': name})
        return data

    def GetValueOfDomain(self, domainname):
        """
        Gets the domain's all rail sensor values given domain name.

        :param : string of a "domainname"
        :return: The domain's all rails sensor values of the Rail
        """
        total_power = 0.0
        data = {}
        domain = self._find_domain(domainname)
        if domain is None:
            data['Success'] = False
            data['Message'] = f'{domainname} does not exists'
        else:
            data[domainname] = {}
            data[domainname]['Rails'] = []
            for railname in domain.railnames:
                ps = self._find_power_sensor(railname)
                if ps is not None:
                    v, i, p = self.pmic.GetSensorValues(ps._sensor)
                    rail_value = {
                        railname: {
                        'Voltage': v,
                        'Current': i,
                        'Power': p
                        }
                    }
                    data[domainname]['Rails'].append(rail_value)
                    total_power += rail_value[railname]['Power']
            data[domainname]['Total Power'] = round(total_power, 4)
        return data

    def GetPowerValueOfDomain(self, domainname):
        """
        Gets the domain's power value given domain name.

        :param : string of a "domainname"
        :return: The domain's power value
        """
        domain_power = 0.0
        data = {}
        domain = self._find_domain(domainname)
        if domain is None:
            data['Success'] = False
            data['Message'] = f'{domainname} does not exists'
        else:
            data[domainname] = {}
            domain_power = 0.0
            for railname in domain.railnames:
                ps = self._find_power_sensor(railname)
                if ps is not None:
                    _, _, p = self.pmic.GetSensorValues(ps._sensor)
                    domain_power += p
            data[domainname]['Power'] = domain_power
        return data

    def GetPowersAll(self):
        """
        Gets the boards's all domain's and total power values

        :param : None
        :return: The boards's all domain's and total power values
        """
        data = {}
        data[self.board_name] = {}
        data[self.board_name]['Power Domains'] = []
        total_power = 0.0
        for domain in self.domains:
            temp_p = self.GetPowerValueOfDomain(domain.name)
            total_power += temp_p[domain.name]['Power']
            data[self.board_name]['Power Domains'].append(temp_p)
        data[self.board_name]['Total Power'] = round(total_power, 4)
        return data

    def GetValuesAll(self):
        """
        Gets the boards's all domain's rails sensor values

        :param : None
        :return: The board's all rails sensor values of the Rail
        """
        data = {}
        data[self.board_name] = []
        for domain in self.domains:
            data[self.board_name].append(self.GetValueOfDomain(domain.name))
        return data

    def GetSysmonTemperatures(self):
        data = {}
        if self.sysmon is None:
            data['Success'] = False
            data['Message'] = f"Sysmon is not available."
        else:
            temp, minimum, max_max, min_min = self.sysmon.ReadSysmonTemperatures()
            data['TEMP'] = temp
            data['MIN'] = minimum
            data['MAX_MAX'] = max_max
            data['MIN_MIN'] = min_min
        return data

    def GetSystemStats(self):
        data = {}
        data = self.status.getLastStatus()
        return data

    def ListPowerSensors(self):
        self.logger.info(f"ListPowerSensors()")
        data = {}
        list_ps = []
        for s in self.pmic.power_sensors:
            list_ps.append(s.name)
        data['power_sensors'] = list_ps
        return data

    def _find_power_sensor(self, sensor_name):
        temp_s = None
        for ps in self.pmic.power_sensors:
            if ps.name == sensor_name:
                temp_s = ps
        return temp_s
    
    def _error_message(message_str):
        data = {}
        data['Success'] = False
        data['Message'] = message_str

    def GetPowerSensor(self, sensor_name):
        self.logger.info(f"GetPowerSensor({sensor_name})")
        data = {}
        values = {}
        ps = self._find_power_sensor(sensor_name)
        if ps is None:
            data['Success'] = False
            data['Message'] = f'{sensor_name} does not exits'
            self.logger.error(f'GetPowerSensor({sensor_name}) does not exits')
        else:
            if ps._sensor is None:
                data['Success'] = False
                data['Message'] = f'{sensor_name} sensor is not defined'
                self.logger.error(f'GetPowerSensor({sensor_name}) sensor is not defined')
            else:
                v, i, p = self.pmic.GetSensorValues(ps._sensor)
                values['Voltage'] = v
                values['Current'] = i
                values['Power'] = p
                data[sensor_name] = values
        return data

    def GetPowerCalSensor(self, sensor_name):
        data = {}
        values = {}
        ps = self._find_power_sensor(sensor_name)
        if ps is None:
            data['Success'] = False
            data['Message'] = f'{sensor_name} does not exits'
            self.logger.error(f'GetPowerCalSensor({sensor_name}) does not exits')
        else:
            if ps._sensor is None:
                data['Success'] = False
                data['Message'] = f'{sensor_name} sensor is not defined'
                self.logger.error(f'GetPowerCalSensor({sensor_name}) sensor is not defined')
            else:
                v, i, p = self.pmic.GetSensorValues(ps._sensor)
                values['Voltage'] = v
                values['Current'] = i
                values['Power'] = p
                data[sensor_name] = values
        return data

    def GetPowerSensorConf(self, sensor_name):
        data = {}
        ps = self._find_power_sensor(sensor_name)
        if ps is None:
            data['Success'] = False
            data['Message'] = f'{sensor_name} does not exits'
            self.logger.error(f'GetPowerSensorConf({sensor_name}) does not exits')
        else:
            if ps._sensor is None:
                data['Success'] = False
                data['Message'] = f'{sensor_name} sensor is not defined'
                self.logger.error(f'GetPowerSensorConf({sensor_name}) sensor is not defined')
            else:
                data[sensor_name] = self.pmic.GetPowerSensorConf(ps._sensor)
        return data

    def SetPowerSensorConf(self, sensor_name, conf):
        data = {}
        ps = self._find_power_sensor(sensor_name)
        if ps is None:
            data['Success'] = False
            data['Message'] = f'{sensor_name} does not exits'
            self.logger.error(f'SetPowerSensorConf({sensor_name}) does not exits')
        else:
            if ps._sensor is None:
                data['Success'] = False
                data['Message'] = f'{sensor_name} sensor is not defined'
                self.logger.error(f'SetPowerSensorConf({sensor_name}) sensor is not defined')
            else:
                self.pmic.SetPowerSensorConf(ps._sensor, conf)
                data['Success'] = True
        return data

    def ListVoltages(self):
        self.logger.info(f"ListVoltages")
        data = {}
        list_v = []
        for v in self.pmic.voltages:
            voltage = {}
            voltage[v.name] = {
                'typical_volt' : v.typical_volt
            }
            list_v.append(voltage)
        data['voltages'] = list_v
        return data

    def _find_voltage(self, voltage_name):
        temp_voltage = None
        for v in self.pmic.voltages:
            if v.name == voltage_name:
                temp_voltage = v
        return temp_voltage

    def EnableVoltage(self, voltage_name):
        self.logger.info(f"EnableVoltage({voltage_name})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                data['Success'] = False
                data['Message'] = f'{voltage_name} regulator is not defined'
                self.logger.error(f'EnableVoltage({voltage_name}) regulator is not defined')
            else:
                self.pmic.EnableVoltage(v._output)
                data['Success'] = True
        return data

    def DisableVoltage(self, voltage_name):
        self.logger.info(f"DisableVoltage({voltage_name})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                data['Success'] = False
                data['Message'] = f'{voltage_name} regulator is not defined'
                self.logger.error(f'DisableVoltage({voltage_name}) regulator is not defined')
            else:
                self.pmic.DisableVoltage(v._output)
                data['Success'] = True
        return data

    def GetRegulatorAll(self, voltage_name):
        self.logger.info(f"GetRegulatorAll({voltage_name})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                data['Success'] = False
                data['Message'] = f'{voltage_name} regulator is not defined'
                self.logger.error(f'GetVoltage({voltage_name}) regulator is not defined')
            else:
                data[voltage_name] = self.pmic.GetRegulatorAll(v._output)
        return data

    def GetVoltage(self, voltage_name):
        self.logger.info(f"GetVoltage({voltage_name})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                data['Success'] = False
                data['Message'] = f'{voltage_name} pmbus regulator is not defined'
                self.logger.error(f'GetVoltage({voltage_name}) pmbus regulator is not defined')
            else:
                data[voltage_name] = self.pmic.GetVoltage(v._output)
        return data

    def SetVoltage(self, voltage_name, new_value):
        self.logger.info(f"SetVoltage({voltage_name}, {new_value})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'SetVoltage({voltage_name}, {new_value}) {voltage_name} does not exits')
            return data
        else:
            if new_value < v.minimum_volt:
                data['Success'] = False
                data['Message'] = f'asked value({new_value}) below minimum({v.minimum_volt}) for {v.name}'
                self.logger.error(f'SetVoltage({voltage_name}, {new_value}) asked value below minimum({v.minimum_volt})')
                return data
            elif new_value > v.maximum_volt:
                data['Success'] = False
                data['Message'] = f'asked value({new_value}) above maximum({v.maximum_volt}) for {v.name}'
                self.logger.error(f'SetVoltage({voltage_name}, {new_value}) asked value above maximum({v.maximum_volt})')
                return data
            else:
                if v._output is None:
                    data['Success'] = False
                    data['Message'] = f'{voltage_name} pmbus regulator is not defined'
                    self.logger.error(f'GetVoltage({voltage_name}) pmbus regulator is not defined')
                    return data
                else:
                    self.pmic.SetVoltage(v._output, new_value)
                    data['Success'] = True
        return data

    def SetBootVoltage(self, voltage_name, boot_value):
        self.logger.info(f"SetBootVoltage({voltage_name}, {boot_value})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'SetBootVoltage({voltage_name}, {boot_value}) {voltage_name} does not exits')
            return data
        else:
            if boot_value < v.minimum_volt:
                data['Success'] = False
                data['Message'] = f'asked value({boot_value}) below minimum({v.minimum_volt}) for {v.name}'
                self.logger.error(f'SetBootVoltage({voltage_name}, {boot_value}) asked value({boot_value}) below minimum({v.minimum_volt})')
                return data
            elif boot_value > v.maximum_volt:
                data['Success'] = False
                data['Message'] = f'asked value({boot_value}) above maximum({v.maximum_volt}) for {v.name}'
                self.logger.error(f'SetBootVoltage({voltage_name}, {boot_value}) asked value({boot_value}) above maximum({v.maximum_volt})')
                return data
            else:
                if v._output is None:
                    data['Success'] = False
                    data['Message'] = f'{voltage_name} pmbus regulator is not defined'
                    self.logger.error(f'SetBootVoltage({voltage_name}, {boot_value}) pmbus regulator is not defined')
                    return data

        directory = os.path.dirname(RAFT_DIR + '.raft/')
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        bootvoltage_path = os.path.join(directory, 'bootvoltage')

        try:
            with dbm.dumb.open(bootvoltage_path, 'c') as db:
                db[voltage_name] = "{:.3f}".format(round(boot_value, 3))
                data['Success'] = True
        except Exception as err:
            self.logger.error(f'SetBootVoltage({voltage_name}, {boot_value}) unknown error as {err}')
            data['Success'] = False
            data['Message'] = f"Unknown error: {err}"
        finally:
            db.sync()
            db.close()
        return data

    def RestoreVoltage(self, voltage_name):
        self.logger.info(f"RestoreVoltage({voltage_name})")
        data = {}
        v = self._find_voltage(voltage_name)
        if v is None:
            data['Success'] = False
            data['Message'] = f'{voltage_name} does not exits'
            self.logger.error(f'RestoreVoltage({voltage_name}) {voltage_name} does not exits')
        else:
            self.SetVoltage(voltage_name, v.typical_volt)
            directory = os.path.dirname(RAFT_DIR + '.raft/')
            bootvoltage_path = os.path.join(directory, 'bootvoltage')
            try:
                with dbm.dumb.open(bootvoltage_path, 'w') as db:
                    del db[voltage_name]
                    data['Success'] = True
            except KeyError:
                self.logger.error(f"RestoreVoltage({voltage_name}) voltage is not in bootvoltage list")
                data['Success'] = False
                data['Message'] = f"{voltage_name} voltage is not in bootvoltage list"
            finally:
                db.sync()
                db.close()
        return data

    def __del__(self):
        self.logger.info("Inside PM Destructor")
