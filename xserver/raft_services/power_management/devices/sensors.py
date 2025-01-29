# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import logging
from periphery import I2C

PM_LOWLEVEL_DEBUG = False

def pm_print(printstr):
    if(PM_LOWLEVEL_DEBUG):
        print(printstr)

logging.basicConfig(level=logging.ERROR)

class INA226(object):
    CONFIGURATION = 0x00
    SHUNT_VOLTAGE = 0x01
    BUS_VOLTAGE =   0x02
    POWER =         0x03
    CURRENT =       0x04
    CALIBRATION =   0x05
    MASK_ENABLE =   0x06
    ALERT_LIMIT =   0x07
    MANUFACTURER =  0XFE
    DIE_ID =        0XFF
    # default values
    MANUFACTURER_ID_VAL = 0x5449
    DIE_ID_VAL =    0x2260

    def __init__(self, address, devicepath):
        logging.info("Inside INA226 Constructor")
        self.die_id = 0
        self.manu_id = 0
        self.addr = int(address, 0)
        self.i2c = I2C(devicepath)
        self._currentLSB = 0
        self._maxCurrent = 0
        self._shunt = 0
        self._phase_multiplier = 0
    
    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k in ['addr', 'i2c'] and v
        }
        return str(str_info)

    def initSensor(self, mc, sr, pm):
        self.die_id = self.getDieID()
        self.manu_id = self.getManufacturerID()
        if self.die_id == INA226.DIE_ID_VAL:
            if self.SetCalibration(mc, sr, pm):
                return True
            else:
                logging.error("INA226 Calibration Failed.")
                return False
        else:
            logging.error("INA226 init failed.")
            return False

    def getShuntVoltage(self):
        voltage = self._readRegister(INA226.SHUNT_VOLTAGE)
        voltage *= 2.5e-6
        return voltage

    def getBusVoltage(self):
        voltage = self._readRegister(INA226.BUS_VOLTAGE)
        voltage *= 1.25e-3
        return voltage

    def getPower(self):
        power = self._readRegister(INA226.POWER)
        power *= (self._currentLSB * 25)
        power *= self._phase_multiplier
        return power

    def getCurrent(self):
        value = self._readRegister(INA226.CURRENT)
        if value > 0x7fff:
            value -= 0x10000
            value = abs(value)

        current = self._currentLSB * value
        current *= self._phase_multiplier
        return current

    def SetCalibration(self, max_current, shunt_resistor, phase_multiplier):
        current_LSB = max_current / (32678 * 1000)
        calibration = (0.00512 * 1000000) / (current_LSB * shunt_resistor)

        if calibration > 32767:
            calibration = 32767

        self._writeRegister(INA226.CALIBRATION, int(calibration))
        calibration = self._readRegister(INA226.CALIBRATION)

        if calibration != 0:
            current_LSB = (0.00512 * 1000000) / (calibration * shunt_resistor)
        else:
            return False

        self._currentLSB = current_LSB
        self._maxCurrent = current_LSB * 32768
        self._shunt = shunt_resistor
        self._phase_multiplier = phase_multiplier
        return True

    def getManufacturerID(self):
        return self._readRegister(INA226.MANUFACTURER)

    def getDieID(self):
        return self._readRegister(INA226.DIE_ID)

    def readRegisterValues(self):
        registers = []
        for reg_adr in range(8):
            registers.append(self._readRegister(reg_adr))
        registers.append(self.manu_id)
        registers.append(self.die_id)
        for index, reg_val in enumerate(registers):
            pm_print("register[0x{0:02x}] = 0x{1:04x}".format(index, reg_val))
        return registers

    def writeRegisterValues(self, reg_val):
        pm_print("0x{0:04x}".format(reg_val[0]))
        pm_print("0x{0:04x}".format(reg_val[1]))
        pm_print("0x{0:04x}".format(reg_val[2]))
        pm_print("0x{0:04x}".format(reg_val[3]))
        self._writeRegister(INA226.CONFIGURATION, reg_val[0])
        self._writeRegister(INA226.CALIBRATION, reg_val[1])
        self._writeRegister(INA226.MASK_ENABLE, reg_val[2])
        self._writeRegister(INA226.ALERT_LIMIT, reg_val[3])

    def _readRegister(self, register):
        val = 0
        try:
            msgs = [I2C.Message([register]), I2C.Message([0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        except IOError:
                logging.error("INA226 _readRegister failed.")
        return val

    def _writeRegister(self, register, value):
        data = None
        try:
            data = bytearray(value.to_bytes(2, "big"))
            data.insert(0, register)
            msgs = [I2C.Message(data)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[0].data[1], msgs[0].data[2]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[0].data[1], msgs[0].data[2]))
        except IOError:
            logging.error("INA226 _writeRegister failed.")

    def __del__(self):
        logging.info("Inside INA226 Destructor")

class INA7XX(object):
    CONFIG      = 0x00
    ADC_CONFIG  = 0x01
    VBUS        = 0x05 # readonly
    DIETEMP     = 0x06 # readonly
    CURRENT     = 0x07 # readonly
    POWER       = 0x08 # readonly
    ENERGY      = 0x09 # readonly
    CHARGE      = 0x0A # readonly
    DIAG_ALERT  = 0x0B
    COL         = 0x0C
    CUL         = 0x0D
    BOVL        = 0x0E
    BUVL        = 0x0F
    TEMP_LIMIT  = 0x10
    PWR_LIMIT   = 0x11
    MANUFACTURER_ID = 0x3E # readonly
    # register count
    REGISTERS   = 16
    MAX_REGISTERS = 16
    # default values
    CONFIG_DEFAULT      = 0x10
    ADC_CONFIG_DEFAULT  = 0xFB68 # averages=1
    VBUS_DEFAULT        = 0x00
    DIETEMP_DEFAULT     = 0x00
    CURRENT_DEFAULT     = 0x00
    POWER_DEFAULT       = 0x00
    ENERGY_DEFAULT      = 0x00
    CHARGE_DEFAULT      = 0x00
    DIAG_ALERT_DEFAULT  = 0x01
    COL_DEFAULT         = 0x7FFF
    CUL_DEFAULT         = 0x8000
    BOVL_DEFAULT        = 0x7FFF
    BUVL_DEFAULT        = 0x00
    TEMP_LIMIT_DEFAULT  = 0x7FFF
    PWR_LIMIT_DEFAULT   = 0xFFFF
    MANUFACTURER_ID_DEFAULT = 0x5449
    
    current_lsb = 0
    voltage_lsb = 0
    temperature_lsb = 0
    power_lsb = 0
    energy_lsb = 0
    charge_lsb = 0

    def __init__(self, address, devicepath):
        logging.info("Inside INA7XX Constructor")
        self.addr = int(address, 0)
        self.i2c = I2C(devicepath)

    def initSensor(self, mc, sr, pm):
        _ = mc
        _ = sr
        _ = pm
        if INA7XX.MANUFACTURER_ID_DEFAULT == self.getManufacturerID():
            return True
        else:
            return False

    def getBusVoltage(self):
        voltage = self._readRegister(INA7XX.VBUS)
        voltage *= self.voltage_lsb
        return voltage

    def getPower(self):
        power = self._readRegister24bit(INA7XX.POWER)
        power *= self.power_lsb
        return power

    def getCurrent(self):
        current = self._readRegister(INA7XX.CURRENT)
        if current & 0x8000:
            current -= 0x10000
        current *= self.current_lsb
        return current

    def getManufacturerID(self):
        return self._readRegister(INA7XX.MANUFACTURER_ID)

    def _readRegister40bit(self, register):
        val = 0
        try:
            msgs = [I2C.Message([register]), I2C.Message([0x00, 0x00, 0x00, 0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 32) (msgs[1].data[1] << 24) (msgs[1].data[2] << 16) + (msgs[1].data[3] << 8) + msgs[1].data[4]
        except IOError:
                logging.error("INA7XX _readRegister failed.")
        return val

    def _readRegister24bit(self, register):
        val = 0
        try:
            msgs = [I2C.Message([register]), I2C.Message([0x00, 0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 16) + (msgs[1].data[1] << 8) + msgs[1].data[2]
        except IOError:
                logging.error("INA7XX _readRegister failed.")
        return val

    def _readRegister(self, register):
        val = 0
        try:
            msgs = [I2C.Message([register]), I2C.Message([0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        except IOError:
                logging.error("INA7XX _readRegister failed.")
        return val

    def _writeRegister(self, register, value):
        data = None
        try:
            data = bytearray(value.to_bytes(2, "big"))
            data.insert(0, register)
            msgs = [I2C.Message(data)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[0].data[1], msgs[0].data[2]))
            pm_print("{0}@0x{1:02x}: 0x{2:02x}{3:02x}".format(self.i2c.devpath, self.addr, msgs[0].data[1], msgs[0].data[2]))
        except IOError:
            logging.error("INA7XX _writeRegister failed.")

    def __del__(self):
        logging.info("Inside INA7XX Destructor")

class INA700(INA7XX):
    def __init__(self, address, devicepath):
        self.current_lsb = 480e-6
        self.voltage_lsb = 3.125e-3
        self.temperature_lsb = 125e-3
        self.power_lsb = 96e-6
        self.energy_lsb = 1.536e-3
        self.charge_lsb = 30e-6
        super().__init__(address, devicepath)


class INA745x(INA7XX):
    def __init__(self, address, devicepath):
        self.current_lsb = 1.2e-3
        self.voltage_lsb = 3.125e-3
        self.temperature_lsb = 125e-3
        self.power_lsb = 240e-6
        self.energy_lsb = 3.840e-3
        self.charge_lsb = 75e-6
        super().__init__(address, devicepath)
