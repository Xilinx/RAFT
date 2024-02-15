# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import logging
import subprocess
from enum import IntEnum
from periphery import I2C 

class Sysmon_Device_Type(IntEnum):
    iic = 0
    pmbus = 1
    sysfs = 2
 

logging.basicConfig(level=logging.ERROR)

class Sysmon(object):
    def __init__(self, address, devicepath, devicetype):
        logging.info("Inside SysmonI2C Constructor")
        self._address = None
        self._bus = None
        self._min = 0
        self._max = 0
        self._min_min = 0
        self._max_max = 0
        self._temp = 0
        self._device_type = devicetype

        if self._device_type is Sysmon_Device_Type.iic:
            self._address = int(address, 0)
            self._bus = I2C(devicepath)
            try:
                msgs = [I2C.Message(0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00)]
                self._bus.transfer(self._address, msgs)
            except IOError:
                logging.error("Create Sysmon iic device failed.")

        elif self._device_type is Sysmon_Device_Type.pmbus:
            self._address = int(address, 0)
            self._bus = I2C(devicepath)
            try:
                msgs = [I2C.Message(0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00)]
                self._bus.transfer(self._address, msgs)
            except IOError:
                logging.error("Create Sysmon pmbus device failed.")
        else:
            self._devicepath = devicepath
            self._address = address
            pass

    @staticmethod
    def twos_comp(val, bits):
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val 
    
    @staticmethod
    def ConvertRawtoProcessed(self, first_byte, second_byte):
        value = None
        val1 = (second_byte << 8) + first_byte
        if (val1 & 0x8000) == 0x8000:
            val1 = twos_comp(val1, 16)
        val2 = 128
       
        return float(val1)/float(val2)

    def ReadSysmonTemperatures(self):
        """
        Read Processing System Temp Value

        :return: values of min, max, min_min and max_max
        """
        if self._type == Sysmon_Device_Type.iic:
            try:
                msgs = [I2C.Message(0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00)]
                self._bus.transfer(self._address, msgs)

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x0c, 0x04, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])
                
                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x0d, 0x04, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0xe3, 0x07, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))
                
                self._min_min = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0xe4, 0x07, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max_max = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

            except IOError:
                logging.error("Read Sysmon failed.")
       
        elif self._type == Sysmon_Device_Type.pmbus:
            try:
                msgs = [I2C.Message(0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00)]
                self._bus.transfer(self._address, msgs)

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))
            
                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x0c, 0x04, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])
                
                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0x0d, 0x04, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0xe3, 0x07, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))
                
                self._min_min = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

                msgs = [I2C.Message(0x00, 0x00, 0x00, 0x00, 0xe4, 0x07, 0x04, 0x00), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max_max = ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1])

            except IOError:
                logging.error("Read Sysmon failed.")        
        else:
            ps_path  = os.path.join(self._devicepath, self._address)
            ret, val = subprocess.getstatusoutput(["cat", ps_path])
            if ret == 0:
                self._temp = int(val)        
        return self._min, self._max, self._min_min, self._max_max

    def __del__(self):
        logging.info("Inside Sysmon Destructor")
