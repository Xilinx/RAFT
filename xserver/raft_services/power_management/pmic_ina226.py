# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import logging
from enum import IntEnum
from periphery import I2C


class INA226_REGS(IntEnum):
    CONFIGURATION = 0x00
    SHUNT_VOLTAGE = 0x01
    BUS_VOLTAGE = 0x02
    POWER = 0x03
    CURRENT = 0x04
    CALIBRATION = 0x05
    MASK_ENABLE = 0x06
    ALERT_LIMIT = 0x07
    MANUFACTURER = 0XFE
    DIE_ID = 0XFF


BUS_MILLIVOLTS_LSB = 1.25
SHUNT_MILLIVOLTS_LSB = 0.0025


logging.basicConfig(level=logging.ERROR)
class INA226(object):
	def __init__(self, address, devicepath):
		logging.info("Inside INA226 Constructor")
		self._address = int(address, 0)
		self._bus = I2C(devicepath)
		self._currentLSB = 0
		self._maxCurrent = 0
		self._shunt = 0
		self._phase_multiplier = 0
		pass

	def initSensor(self, mc, sr, pm):
		if 0x2260 == self.getDieID():
			if self.SetCalibration(mc, sr, pm):
				return True
			else:
				logging.error("INA226 Calibration Failed.")
				return False
		else:
			logging.error("INA226 init failed.") 
			return False


	def getAddress(self):
		return _address

	def getShuntVoltage(self):
		voltage = self._readRegister(INA226_REGS.SHUNT_VOLTAGE)
		voltage *= 2.5.e-6
		return voltage 

	def getBusVoltage(self):
		voltage = self._readRegister(INA226_REGS.BUS_VOLTAGE)
		voltage *= 1.25e-3
		return voltage
	
	def getPower(self):
		power = self._readRegister(INA226_REGS.POWER)
		power *= (self._currentLSB * 25)
		power *= self._phase_multiplier
		return power

	def getCurrent(self):
		value = self._readRegister(INA226_REGS.CURRENT)
		
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

		self._writeRegister(INA226_REGS.CALIBRATION, int(calibration))

		calibration = self._readRegister(INA226_REGS.CALIBRATION)

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
		return self._readRegister(INA226_REGS.MANUFACTURER)

	def getDieID(self):
		return self._readRegister(int(INA226_REGS.DIE_ID))

	def _readRegister(self, reg):
		val = None
		try:
			msgs = [I2C.Message([reg]), I2C.Message([0x00, 0x00], read=True)]
			self._bus.transfer(self._address, msgs)
			logging.debug("{0}: 0x{1:02x}{2:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1]))
			val = (msgs[1].data[0] << 8) + msgs[1].data[1]
		except IOError:
			logging.error("INA226 _readRegister failed.")
		return val
	

	def _writeRegister(self, reg, val):
		ret = False
		data = None
		try:
			data = bytearray(val.to_bytes(2, "big"))
			data.insert(0, reg)
			msgs = [I2C.Message(data)]
			self._bus.transfer(self._address, msgs)
			ret = True
		except IOError:
			logging.error("INA226 _writeRegister failed.")
		return ret

	def __del__(self):
		logging.info("Inside INA226 Destructor")