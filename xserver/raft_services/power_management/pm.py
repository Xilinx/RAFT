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

class HardwareError(Exception):
    pass

class PM(object):
    logger = None
    domains = []
    sensors = []
    voltages = []
    scales = None
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
            self.feature_list = board_data['FEATURE']['List']

        self.unit_config = {
            "voltage": {
                "base_unit": "V",
                "available_scales": {
                    "base": 1,
                    "milli": 1e-3,
                }
            },
            "current": {
                "base_unit": "A",
                "available_scales": {
                    "base": 1,
                    "milli": 1e-3,
                    "micro": 1e-6,
                }
            },
            "power": {
                "base_unit": "W",
                "available_scales": {
                    "base": 1,
                    "milli": 1e-3,
                }
            },
            "temperature": {
                "base_unit": "C",
                "available_scales": {
                    "base": 1,
                    "milli": 1e-3,
                }
            }
        }
        self.scales = {param: "base" for param in self.unit_config}

        if 'powerdomain' in self.feature_list:
            if 'POWER DOMAIN' in board_data:
                for key, val in board_data['POWER DOMAIN'].items():
                    temp_d = Domain(**val)
                    for index, railname in enumerate(temp_d.railnames):
                        for k, v in board_data['POWER_SENSORS'].items():
                            if k == railname:
                                if temp_d.railnames[index] != v['Name']:
                                    temp_d.railnames[index] = v['Name']
                    self.domains.append(temp_d)

        if 'power' in self.feature_list:
            if 'POWER_SENSORS' in board_data:
                for k, v in board_data['POWER_SENSORS'].items():
                    temp_r = Rails(**v)
                    self.sensors.append(temp_r)

        if 'voltage' in self.feature_list:
            if 'VOLTAGE' in board_data:
                for k, v in board_data['VOLTAGE'].items():
                    tempVolt = Rails(**v)
                    self.voltages.append(tempVolt)

        if 'temp' in self.feature_list:
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

    def handle_request(self, process_function, *args, **kwargs):
        try:
            caller_name = sys._getframe(1).f_code.co_name.lower()
            if 'voltage' in caller_name:
                if 'voltage' not in self.feature_list:
                    raise Exception(f"Unsupported feature: voltage")
            if 'regulator' in caller_name:
                if 'voltage' not in self.feature_list:
                    raise Exception(f"Unsupported feature: voltage")
            if 'power' in caller_name:
                if 'power' not in self.feature_list:
                    raise Exception(f"Unsupported feature: power")
            if 'temp' in caller_name:
                if 'temperature' not in self.feature_list:
                    raise Exception(f"Unsupported feature: temperature")
            if 'domain' in caller_name:
                if 'powerdomain' not in self.feature_list:
                    raise Exception(f"Unsupported feature: powerdomain")

            data = process_function(*args, **kwargs)
            return {
                "status": "success",
                "data": data,
                "message": "Operation completed successfully."
            }
        except HardwareError as e:
            return {
                "status": "failure",
                "data": None,
                "message": f"Hardware error: {str(e)}"
            }
        except ValueError as e:
            self.logger.error(f'{sys._getframe(1).f_code.co_name}{args} : {str(e)}')
            return {
                "status": "failure",
                "data": None,
                "message": f"Value error: {str(e)}"
            }
        except Exception as e:
            self.logger.error(f'{sys._getframe(1).f_code.co_name}{args} : {str(e)}')
            return {
                "status": "failure",
                "data": None,
                "message": f"Unexpected error: {str(e)}"
            }

    # Call APIs
    def GetBoardInfo(self):
        self.logger.info(f"GetBoardInfo()")
        return self.handle_request(self._get_board_info)

    def ListFeature(self):
        self.logger.info(f"GetBoardInfo()")
        return self.handle_request(self._list_feature)


    def ListPowerDomains(self):
        self.logger.info(f"ListPowerSensors()")
        return self.handle_request(self._list_power_domains)

    def ListRailsOfDomain(self, domain_name):
        self.logger.info(f"ListRailsOfDomain()")
        return self.handle_request(self._list_rails_of_domain, domain_name)

    def GetValueOfDomain(self, domain_name):
        self.logger.info(f"GetValueOfDomain()")
        return self.handle_request(self._get_value_of_domain, domain_name)

    def GetPowersAll(self):
        self.logger.info(f"GetPowersAll()")
        return self.handle_request(self._get_powers_all)

    def GetValuesAll(self):
        self.logger.info(f"GetValuesAll()")
        return self.handle_request(self._get_values_all)

    """
    Power Sensor APIs
    """
    def ListPowerSensors(self):
        self.logger.info(f"ListPowerSensors()")
        return self.handle_request(self._list_power_sensor)

    def GetPowerSensor(self, sensor_name):
        self.logger.info(f"GetPowerSensor({sensor_name})")
        return self.handle_request(self._get_power_sensor, sensor_name)

    def GetCalPowerSensor(self, sensor_name):
        self.logger.info(f"GetCalPowerSensor({sensor_name})")
        return self.handle_request(self._get_cal_power_sensor, sensor_name)

    def GetPowerSensorConf(self, sensor_name):
        self.logger.info(f"GetPowerSensorConf({sensor_name})")
        return self.handle_request(self._get_power_sensor_conf, sensor_name)

    def SetPowerSensorConf(self, sensor_name, conf):
        self.logger.info(f"SetPowerSensorConf({sensor_name, conf})")
        return self.handle_request(self._set_power_sensor_conf, sensor_name, conf)

    """
    Voltage Regulator APIs
    """
    def ListVoltages(self):
        self.logger.info(f"ListVoltages")
        return self.handle_request(self._list_voltages)

    def EnableVoltage(self, voltage_name):
        self.logger.info(f"EnableVoltage({voltage_name})")
        return self.handle_request(self._enable_voltage, voltage_name)

    def DisableVoltage(self, voltage_name):
        self.logger.info(f"DisableVoltage({voltage_name})")
        return self.handle_request(self._disable_voltage, voltage_name)

    def GetRegulator(self, voltage_name):
        self.logger.info(f"GetRegulator({voltage_name})")
        return self.handle_request(self._get_regulator, voltage_name)

    def GetVoltage(self, voltage_name):
        self.logger.info(f"GetVoltage({voltage_name})")
        return self.handle_request(self._get_voltage, voltage_name)

    def SetVoltage(self, voltage_name, new_value):
        self.logger.info(f"SetVoltage({voltage_name}, {new_value})")
        return self.handle_request(self._set_voltage, voltage_name, new_value)

    def SetBootVoltage(self, voltage_name, new_value):
        self.logger.info(f"SetBootVoltage({voltage_name}, {new_value})")
        return self.handle_request(self._set_boot_voltage, voltage_name, new_value)

    def RestoreVoltage(self, voltage_name, new_value):
        self.logger.info(f"SetVoltage({voltage_name}, {new_value})")
        return self.handle_request(self._restore_voltage, voltage_name, new_value)

    def GetSysmonTemperatures(self):
        self.logger.info(f"GetSysmonTemperatures()")
        return self.handle_request(self._get_temperatures)

    def ListUnits(self):
        self.logger.info(f"ListUnits()")
        return self.handle_request(self._list_units)

    def GetUnit(self, quantity):
        self.logger.info(f"GetUnit()")
        return self.handle_request(self._get_unit, quantity)

    def GetAvailableScales(self, quantity):
        self.logger.info(f"GetAvailableUnits()")
        return self.handle_request(self._get_available_scales, quantity)

    def SetScale(self, quantity, unit):
        self.logger.info(f"SetUnit()")
        return self.handle_request(self._set_scale, quantity, unit)

    def _list_units(self):
        if self.scales is None:
            raise Exception(f'Unsupported feature: Enable "Units" in config')
        return {
            param: {
                "current_scale": self.scales[param],
                "current_unit": self._get_unit(param),
                "available_scales": list(self.unit_config[param]["available_scales"].keys()),
                "base_unit": self.unit_config[param]["base_unit"]
            }
            for param in self.unit_config
        }

    def _get_unit(self, quantity):
        if self.scales is None:
            raise Exception(f'Unsupported feature: Enable "Units" in config')
        if quantity not in self.scales:
            raise ValueError(f"Unsupported quantity: {quantity}")
        scale = self.scales[quantity]
        base_unit = self.unit_config[quantity]["base_unit"]

        # Define prefixes for scales
        scale_prefix_map = {
            "base": "",
            "milli": "m",
            "micro": "µ",
            "kilo": "k",
        }

        # Return the correctly formatted unit
        prefix = scale_prefix_map.get(scale, "")
        return f"{prefix}{base_unit}"

    def _set_scale(self, quantity, scale):
        if self.scales is None:
            raise Exception(f'Unsupported feature: Enable "Units" in config')
        if quantity not in self.unit_config:
            raise ValueError(f"Unsupported quantity: {quantity}")
        if scale not in self.unit_config[quantity]["available_scales"]:
            raise ValueError(f"Unsupported scale for {quantity}: {scale}")
        self.scales[quantity] = scale
    
    def _get_available_scales(self, quantity):
        if self.scales is None:
            raise Exception(f'Unsupported feature: Enable "Units" in config')
        if quantity not in self.unit_config:
            raise ValueError(f"Unsupported value: {quantity}")
        return list(self.unit_config[quantity]["available_scales"].keys())

    def _scale(self, value, quantity):
        if value is None:
            return value
        if self.scales is None:
            return value
        if quantity not in self.scales:
            raise ValueError(f"Unsupported value: {quantity}")
        scale = self.scales[quantity]
        factor = self.unit_config[quantity]["available_scales"][scale]
        return round((value / factor), 3)

    def _unscale(self, value, quantity):
        if value is None:
            return value
        if self.scales is None:
            return value
        if quantity not in self.scales:
            raise ValueError(f"Unsupported value: {quantity}")
        scale = self.scales[quantity]
        factor = self.unit_config[quantity]["available_scales"][scale]
        return round((value * factor), 3)

    ## Process functions
    def _get_board_info(self):
        if self.boardeeprom is None:
            raise ValueError(f'Board Eeprom undefined')
        else:
            return self.pmic.GetBoardInfo(self.boardeeprom, self.pdi_file)

    def _list_feature(self):
        if len(self.feature_list) == 0:
            raise ValueError(f"Feature list is empty")
        return self.feature_list

    def __find_domain(self, domain_name):
        temp_d = None
        for d in self.domains:
            if d.name == domain_name:
                temp_d = d
        return temp_d

    def _list_power_domains(self):
        data = []
        for d in self.domains:
            data.append(d.name)
        if len(data) == 0:
            raise Exception(f'Power domains list is empty')
        return data

    def _list_rails_of_domain(self, domain_name):
        data = []
        domain = self.__find_domain(domain_name)
        if domain is None:
            raise ValueError(f'{domain_name} does not exists')
        else:
            for railname in domain.railnames:
                data.append(railname)
            if len(data) == 0:
                raise Exception(f'Rails list is empty')
        return data

    def _get_value_of_domain(self, domain_name):
        total_power = 0.0
        data = {}
        domain = self.__find_domain(domain_name)
        if domain is None:
            raise ValueError(f'{domain_name} does not exists')
        else:
            data[domain_name] = {}
            data[domain_name]['Rails'] = []
            for railname in domain.railnames:
                ps = self.__find_power_sensor(railname)
                if ps is None:
                    raise Exception(f'{domain_name} sensor is not defined')
                else:
                    v, i, p = self.pmic.GetSensorValues(ps._sensor)
                    rail_value = {
                        railname: {
                        'Voltage': self._scale(v, "voltage"),
                        'Current': self._scale(i, "current"),
                        'Power': self._scale(p, "power")
                        }
                    }
                    data[domain_name]['Rails'].append(rail_value)
                    total_power += self._scale(rail_value[railname]['Power'], "power")
            data[domain_name]['Total Power'] = total_power
        return data

    def _get_power_value_of_domain(self, domain_name):
        domain_power = 0.0
        data = {}
        domain = self.__find_domain(domain_name)
        if domain is None:
            raise ValueError(f'{domain_name} does not exists')
        else:
            data[domain_name] = {}
            domain_power = 0.0
            for railname in domain.railnames:
                ps = self.__find_power_sensor(railname)
                if ps is None:
                    raise Exception(f'{railname} sensor is not defined')
                else:
                    _, _, p = self.pmic.GetSensorValues(ps._sensor)
                    domain_power += self._scale(p, "power")
            data[domain_name]['Power'] = domain_power
        return data

    def _get_powers_all(self):
        data = {}
        data[self.board_name] = {}
        data[self.board_name]['Power Domains'] = []
        total_power = 0.0
        for domain in self.domains:
            temp_p = self._get_power_value_of_domain(domain.name)
            total_power += self._scale(temp_p[domain.name]['Power'], "power")
            data[self.board_name]['Power Domains'].append(temp_p)
        data[self.board_name]['Total Power'] = total_power
        return data

    def _get_values_all(self):
        data = {}
        data[self.board_name] = []
        for domain in self.domains:
            data[self.board_name].append(self._get_value_of_domain(domain.name))
        return data

    def __find_power_sensor(self, sensor_name):
        temp_s = None
        for ps in self.pmic.power_sensors:
            if ps.name == sensor_name:
                temp_s = ps
        return temp_s

    def _list_power_sensor(self):
        data = []
        if len(self.pmic.power_sensors) == 0:
            raise ValueError(f"Power Sensor list is empty")
        for s in self.pmic.power_sensors:
            data.append(s.name)
        return data

    def _get_power_sensor(self, sensor_name):
        ps = self.__find_power_sensor(sensor_name)
        if ps is None:
            raise ValueError(f'{sensor_name} does not exits')
        else:
            if ps._sensor is None:
                raise Exception(f'{sensor_name} sensor is not defined')
            else:
                v, i, p = self.pmic.GetSensorValues(ps._sensor)
                data = {
                    'Voltage' : self._scale(v, "voltage"),
                    'Current' : self._scale(i, "current"),
                    'Power' : self._scale(p, "power")
                }
        return data

    def _get_cal_power_sensor(self, sensor_name):
        ps = self.__find_power_sensor(sensor_name)
        if ps is None:
            raise ValueError(f'{sensor_name} does not exits')
        else:
            if ps._sensor is None:
                raise Exception(f'{sensor_name} sensor is not defined')
            else:
                v, i, p = self.pmic.GetSensorValues(ps._sensor)
                data = {
                    'Voltage' : self._scale(v, "voltage"),
                    'Current' : self._scale(i, "current"),
                    'Power' : self._scale(p, "power")
                }
        return data

    def _get_power_sensor_conf(self, sensor_name):
        ps = self.__find_power_sensor(sensor_name)
        if ps is None:
            raise ValueError(f'{sensor_name} does not exits')
        else:
            if ps._sensor is None:
                raise Exception(f'{sensor_name} sensor is not defined')
        return self.pmic.GetPowerSensorConf(ps._sensor)

    def _set_power_sensor_conf(self, sensor_name, conf):
        ps = self.__find_power_sensor(sensor_name)
        if ps is None:
            raise ValueError(f'{sensor_name} does not exits')
        else:
            if ps._sensor is None:
                raise Exception(f'{sensor_name} sensor is not defined')
        return self.pmic.SetPowerSensorConf(ps._sensor, conf)

    def __find_voltage(self, voltage_name):
        temp_voltage = None
        for v in self.pmic.voltages:
            if v.name == voltage_name:
                temp_voltage = v
        return temp_voltage

    def _list_voltages(self):
        if len(self.pmic.voltages) == 0:
            raise ValueError(f"Voltage list is empty")
        data = []
        for v in self.pmic.voltages:
            data.append({
                v.name : {
                    'typical_volt' : self._scale(v.typical_volt, "voltage")
                }
            })
        return data

    def _enable_voltage(self, voltage_name):
        self.logger.info(f"EnableVoltage({voltage_name})")
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                raise Exception(f'{voltage_name} regulator is not defined')
            else:
                self.pmic.EnableVoltage(v._output)

    def _disable_voltage(self, voltage_name):
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                raise Exception(f'{voltage_name} regulator is not defined')
            else:
                self.pmic.DisableVoltage(v._output)

    def _get_regulator(self, voltage_name):
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                raise Exception(f'{voltage_name} regulator is not defined')
            else:
                regulator_vals = self.pmic.GetRegulator(v._output)
                data = {
                    "vin" : self._scale(regulator_vals[0], "voltage"),
                    "iin" : self._scale(regulator_vals[1], "current"),
                    "vout" : self._scale(regulator_vals[2], "voltage"),
                    "iout" : self._scale(regulator_vals[3], "current"),
                    "temp" : self._scale(regulator_vals[4], "temperature"),
                    "pout" : self._scale(regulator_vals[5], "power"),
                    "pin" : self._scale(regulator_vals[6], "power"),
                }
        return data

    def _get_voltage(self, voltage_name):
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if v._output is None:
                raise Exception(f'{voltage_name} regulator is not defined')
            else:
                data = {"Voltage" : self._scale(self.pmic.GetVoltage(v._output), "voltage")}
        return data

    def _set_voltage(self, voltage_name, new_value):
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if new_value < self._scale(v.minimum_volt, "voltage"):
                raise ValueError(f'asked value({new_value}) below minimum({self._scale(v.minimum_volt, "voltage")}) for {v.name}')
            elif new_value > self._scale(v.maximum_volt, "voltage"):
                raise ValueError(f'asked value({new_value}) above maximum({self._scale(v.maximum_volt, "voltage")}) for {v.name}')
            else:
                if v._output is None:
                    raise Exception(f'{voltage_name} regulator is not defined')
                else:
                    self.pmic.SetVoltage(v._output, self._unscale(new_value, "voltage"))

    def _set_boot_voltage(self, voltage_name, boot_value):
        self.logger.info(f"SetBootVoltage({voltage_name}, {boot_value})")
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            if boot_value < self._scale(v.minimum_volt, "voltage"):
                raise ValueError(f'asked value({boot_value}) below minimum({self._scale(v.minimum_volt, "voltage")}) for {v.name}')
            elif boot_value > self._scale(v.maximum_volt, "voltage"):
                raise ValueError(f'asked value({boot_value}) above maximum({self._scale(v.maximum_volt, "voltage")}) for {v.name}')
            else:
                if v._output is None:
                    raise Exception(f'{voltage_name} regulator is not defined')

        directory = os.path.dirname(RAFT_DIR + '.raft/')
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        bootvoltage_path = os.path.join(directory, 'bootvoltage')

        try:
            with dbm.dumb.open(bootvoltage_path, 'c') as db:
                db[voltage_name] = "{:.3f}".format(round(self._unscale(boot_value, "voltage"), 3))
        except Exception as err:
            raise Exception(f"Unknown error: {err}")
        finally:
            db.sync()
            db.close()

    def _restore_voltage(self, voltage_name):
        self.logger.info(f"RestoreVoltage({voltage_name})")
        v = self.__find_voltage(voltage_name)
        if v is None:
            raise ValueError(f'{voltage_name} does not exits')
        else:
            self._set_voltage(voltage_name, self._scale(v.typical_volt, "voltage"))
            directory = os.path.dirname(RAFT_DIR + '.raft/')
            bootvoltage_path = os.path.join(directory, 'bootvoltage')
            try:
                with dbm.dumb.open(bootvoltage_path, 'w') as db:
                    del db[voltage_name]
            except KeyError:
                raise Exception(f"{voltage_name} voltage is not in bootvoltage list")
            finally:
                db.sync()
                db.close()

    def _get_temperatures(self):
        data = {}
        if self.sysmon is None:
            raise ValueError(f'Sysmon is not available')
        else:
            temp, minimum, max_max, min_min = self.sysmon.ReadSysmonTemperatures()
            data['TEMP'] = self._scale(temp, "temperature")
            data['MIN'] = self._scale(minimum, "temperature")
            data['MAX_MAX'] = self._scale(max_max, "temperature")
            data['MIN_MIN'] = self._scale(min_min, "temperature")
        return data

    def __del__(self):
        self.logger.info("Inside PM Destructor")