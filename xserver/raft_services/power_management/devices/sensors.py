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
    MANUFACTURER_ID_VAL = 0x5449
    DIE_ID_VAL =    0x2260

    die_id = 0
    manu_id = 0

    def __init__(self, address, devicepath):
        logging.info("Inside INA226 Constructor")
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
        return self._readRegister(int(INA226.DIE_ID))

    def readRegisterValues(self):
        registers = []
        for reg_adr in range(8):
            registers.append(self._readRegister(reg_adr))
        registers.append(self.manu_id)
        registers.append(self.die_id)
        for index, reg_val in enumerate(registers):
            pm_print("register[0x{0:02x}] = 0x{1:04x}".format(index, reg_val))
        return registers

    def writeRegisterValues(self, list_registers):
        for reg in list_registers:
            for k, v in reg.items():
                pm_print(f"{k}:{v}")
                #self._writeRegister(reg, v)
        pass

    def _readRegister(self, register):
        val = None
        try:
            msgs = [I2C.Message([register]), I2C.Message([0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}: 0x{1:02x}{2:02x}".format(self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        except IOError:
                logging.error("INA226 _readRegister failed.")
        return val

    def _writeRegister(self, register, value):
        ret = False
        data = None
        try:
            data = bytearray(value.to_bytes(2, "big"))
            data.insert(0, register)
            msgs = [I2C.Message(data)]
            self.i2c.transfer(self.addr, msgs)
            ret = True
        except IOError:
            logging.error("INA226 _writeRegister failed.")
        return ret

    def __del__(self):
        logging.info("Inside INA226 Destructor")

class INA7XX(object):
    def __init__(self, address, devicepath):
        logging.info("Inside INA7XX Constructor")
        self.addr = int(address, 0)
        self.i2c = I2C(devicepath)
        pass

    def initSensor(self, mc, sr, pm):
        pass

    def getAddress(self):
        return self.addr

    def getShuntVoltage(self):
        pass
    def getBusVoltage(self):
        pass

    def getPower(self):
        pass

    def getCurrent(self):
        pass


    def SetCalibration(self, max_current, shunt_resistor, phase_multiplier):
        pass

    def getManufacturerID(self):
        pass

    def getDieID(self):
        pass

    def _readRegister(self, reg):
        val = None
        try:
            msgs = [I2C.Message([reg]), I2C.Message([0x00, 0x00], read=True)]
            self.i2c.transfer(self.addr, msgs)
            logging.debug("{0}: 0x{1:02x}{2:02x}".format(self.addr, msgs[1].data[0], msgs[1].data[1]))
            val = (msgs[1].data[0] << 8) + msgs[1].data[1]
        except IOError:
            logging.error("INA7XX _readRegister failed.")
        return val

    def _writeRegister(self, reg, val):
        ret = False
        data = None
        try:
            data = bytearray(val.to_bytes(2, "big"))
            data.insert(0, reg)
            msgs = [I2C.Message(data)]
            self.i2c.transfer(self.addr, msgs)
            ret = True
        except IOError:
            logging.error("INA7XX _writeRegister failed.")
        return ret

    def __del__(self):
        logging.info("Inside INA7XX Destructor")


