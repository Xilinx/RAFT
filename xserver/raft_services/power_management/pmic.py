# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import os
import sys
import datetime
import logging
import dbm.dumb
from periphery import I2C
from utils import get_python_log_levels

RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
sys.path.append(RAFT_DIR + 'xserver/raft_services/power_management/devices')

from pm_types import *
from devices.sensors import *
from devices.regulators import *
class PMIC(object):
    logger = None
    domains = []
    voltages = []
    power_sensors = []

    def __init__(self, pm_domains, pm_powersensor, pm_voltages):
        self.logger = self.GetLogger()
        self.domains = pm_domains

        for ps in pm_powersensor:
            match ps.part_name:
                case 'INA226':
                    ps._sensor = INA226(ps.i2c_address, ps.i2c_bus)
                case 'INA700':
                    ps._sensor = INA700(ps.i2c_address, ps.i2c_bus)
                case 'INA745A' | 'INA745B':
                    ps._sensor = INA745x(ps.i2c_address, ps.i2c_bus)
                case _:
                    ps._sensor = None

            if ps._sensor is None:
                self.logger.error(f"Sensor({ps.name}) device initialization is Failed.")
            else:
                if ps._sensor.initSensor(ps.maximum_current, ps.shunt_resistor, ps.phase_multiplier):
                    self.power_sensors.append(ps)
                    self.logger.debug(f"Sensor({ps.name}) device initialization Successfully.")
                else:
                    self.logger.error(f"Sensor({ps.name}) device is not found !")

        directory = os.path.dirname(RAFT_DIR + '.raft/')
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        bootvoltage_path = os.path.join(directory, 'bootvoltage')

        db = dbm.dumb.open(bootvoltage_path, 'c')
        for v in pm_voltages:
            v._output = None
            match v.part_name:
                case 'IR35215'| 'IRPS5401' | 'IR38164' | 'IR38064' | 'IR38060'\
                    | 'TPS53681' | 'TPS546B24A' | 'TPS546D24A' | 'TPS544B25'\
                    | 'MPQ2283' | 'MPQ2285' | 'MPQ72963':
                    v._output = PMBusRegulator(device_name=v.part_name, device_path=v.i2c_bus, device_address=v.i2c_address, page=v.page_select, pmbus_vout_mode=v.pmbus_vout_mode, phase=v.phase)
                case 'MPM54322' | 'MPM54522':
                    v._output = MPSRegulator(device_path=v.i2c_bus, device_address=v.i2c_address, page=v.page_select, phase=v.phase, fb_ratio=v.fb_ratio)
                case _:
                    v._output = None #DefaultRegulator(device_path=v.i2c_bus, device_address=v.i2c_address)
            if v._output is None:
                self.logger.error(f"Voltage regulator for {v.name} is not defined.")
            else:
                self.voltages.append(v)
                self.logger.debug(f"Regulator Output({v.name}) device initialization Successfully.")
                for key, value in db.items():
                    voltage_name = key.decode('utf-8')
                    if voltage_name == v.name:
                        self.SetVoltage(v._output, float(value))
        db.close()
        self.logger.info("Inside PMIC Constructor")

    @staticmethod
    def GetLogger():
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

    def GetPythonLogLevels(self):
        return get_python_log_levels()

    def SetServerLogLevel(self, PythonLogLevel):
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

    def GetBoardInfo(self, eeprom, has_pdi):
        boardinfo = {}
        i2c = I2C(eeprom.I2C_Bus)
        bytes = bytearray(256)
        try:
            msgs = [I2C.Message([0x0, 0x0]), I2C.Message(bytes, read=True)]
            i2c.transfer(eeprom.I2C_Addr, msgs)
            eeprom_data = msgs[1].data
            #print(''.join('{:02x} '.format(x) for x in eeprom_data))
            offset = 0xA
            boardinfo["Language"] = eeprom_data[offset]

            if has_pdi is not None:
                boardinfo["Silicon Revision"] = "PROD"
            else:
                boardinfo["Silicon Revision"] = ""

            build_date = datetime.datetime(1996, 1, 1)
            minutes  = (eeprom_data[0xd] << 16 | eeprom_data[0xc] << 8 | eeprom_data[0xb])
            time_delta = datetime.timedelta(minutes=minutes)
            build_date += time_delta
            time_string = build_date.strftime('%c')
            boardinfo['Manufacturing Date'] = time_string

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
            #/* Skip FRU File ID */
            offset = offset + length + 1
            length = int.from_bytes(eeprom_data[offset:offset+1], "big")
            length &= 0x3f
            boardinfo["Board Revision"] = eeprom_data[(offset+1):((offset+1) + length)].decode("utf-8").strip('\x00')
        except IOError:
            logging.error(f"Onboard {eeprom.Name} Eeprom read failed!")
        finally:
            i2c.close()
        return boardinfo

    def EnableVoltage(self, o):
        self.logger.debug(f"EnableVoltage({o.addr}@{o.i2c.devpath})")
        o.enable_output()

    def DisableVoltage(self, o):
        self.logger.debug(f"DisableVoltage({o.addr}@{o.i2c.devpath})")
        o.shutdown_output()

    def GetRegulator(self, o):
        self.logger.debug(f"GetRegulator({o.addr}@{o.i2c.devpath})")
        return o.read_telemetry_all()

    def GetVoltage(self, o):
        self.logger.debug("GetVoltage(0x{0:02x}@{1})".format(o.addr, o.i2c.devpath))
        return o.read_voltage()

    def SetVoltage(self, o, val):
        self.logger.debug("SetVoltage(0x{0:02x}@{1}, {2})".format(o.addr, o.i2c.devpath, val))
        o.set_voltage(val)

    def GetPowerSensorConf(self, s):
        self.logger.debug("GetPowerSensorConf(0x{0:02x}@{1})".format(s.addr, s.i2c.devpath))
        data = {}
        registers = s.readRegisterValues()
        data['Configuration'] = '0x{0:04x}'.format(registers[INA226.CONFIGURATION])
        data['Shunt_Voltage'] = '0x{0:04x}'.format(registers[INA226.SHUNT_VOLTAGE])
        data['Bus_Voltage'] =   '0x{0:04x}'.format(registers[INA226.BUS_VOLTAGE])
        data['Power'] = '0x{0:04x}'.format(registers[INA226.POWER])
        data['Current'] = '0x{0:04x}'.format(registers[INA226.CURRENT])
        data['Calibration'] = '0x{0:04x}'.format(registers[INA226.CALIBRATION])
        data['Mask_Enable'] = '0x{0:04x}'.format(registers[INA226.MASK_ENABLE])
        data['Alert_Limit'] = '0x{0:04x}'.format(registers[INA226.ALERT_LIMIT])
        return data

    def SetPowerSensorConf(self, s, data):
        self.logger.debug("SetPowerSensorConf(0x{0:02x}@{1})".format(s.addr, s.i2c.devpath))
        s.writeRegisterValues(data)

    def GetSensorValues(self, s):
        self.logger.debug("GetSensorValues(0x{0:02x}@{1})".format(s.addr, s.i2c.devpath))
        vbus = round(s.getBusVoltage(), 4)
        current = round(s.getCurrent(), 4)
        power = round(s.getPower(), 4)
        return vbus, current, power

    def __del__(self):
        self.logger.info("Inside PMIC Destructor")
