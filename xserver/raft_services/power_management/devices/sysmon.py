# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import os
import sys
import logging
import subprocess
from periphery import I2C

RAFT_DIR = '/usr/share/raft/'
sys.path.append(RAFT_DIR + 'xserver/utils')
sys.path.append(RAFT_DIR + 'xserver/raft_services/power_management/devices')
from pm_types import *

logging.basicConfig(level=logging.ERROR)

class Sysmon(object):
    def __init__(self, address, devicepath, devicetype):
        logging.info("Inside SysmonI2C Constructor")
        self._address = None
        self._bus = None
        self._min = 0
        self._min_min = 0
        self._max_max = 0
        self._temp = 0
        self._device_type = devicetype
        self._device_path = devicepath

        if self._device_type is Sysmon_Device_Type.I2C:
            self._address = int(address, 0)
            self._bus = I2C(self._device_path)
            try:
                msgs = [I2C.Message([0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00])]
                self._bus.transfer(self._address, msgs)
            except IOError:
                logging.error("Sysmon I2C device init failed.")
                raise Exception("Sysmon I2C device init failed")

        elif self._device_type is Sysmon_Device_Type.PMBUS:
            self._address = int(address, 0)
            self._bus = I2C(self._device_path)
            try:
                msgs = [I2C.Message([0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00])]
                self._bus.transfer(self._address, msgs)
            except IOError:
                logging.error("Sysmon Pmbus device init failed.")
                raise Exception("Sysmon Pmbus device init failed")

        elif self._device_type is Sysmon_Device_Type.SYSFS:
            for root, subdirs, files in os.walk("/sys/bus/iio/devices/"):
                for subdir in subdirs:
                    filepath = os.path.join(root, subdir, "name")
                    if os.path.isfile(filepath):
                        with open(filepath, 'r') as f:
                            file_content = f.read()
                            if 'xlnx,versal-sysmon' in file_content:
                                temp_path = os.path.join(root, subdir)
                                device_path = os.path.abspath(temp_path)
                                self._device_path = device_path
            if self._device_path is None:
                logging.error("Sysmon Sysfs device init failed.")
                raise Exception("Sysmon Sysfs device init failed.")
        else:
            logging.error("Unknown Sysmon device type.")
            raise Exception("Unknown Sysmon device type.")

    @staticmethod
    def twos_comp(val, bits):
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val

    @staticmethod
    def ConvertRawtoProcessed(first_byte, second_byte):
        val1 = (second_byte << 8) + first_byte
        if (val1 & 0x8000) == 0x8000:
            val1 = Sysmon.twos_comp(val1, 16)
        val2 = 128
        return float(val1)/float(val2)

    def ReadSysmonTemperatures(self):
        """
        Read Processing System Temperature Values

        :return: values of temp, min, max_max and min_min
        """
        if self._device_type == Sysmon_Device_Type.SYSFS:
            if self._device_path is not None:
                cmd  = 'cat ' + os.path.join(self._device_path, 'in_temp160_temp_input')
                ret, val = subprocess.getstatusoutput(cmd)
                if ret == 0:
                    self._temp = round(int(val)/1000, 3)

                cmd  = 'cat ' + os.path.join(self._device_path, 'in_temp161_min_input')
                ret, val = subprocess.getstatusoutput(cmd)
                if ret == 0:
                    self._min = round(int(val)/1000, 3)

                cmd  = 'cat ' + os.path.join(self._device_path, 'in_temp162_max_max_input')
                ret, val = subprocess.getstatusoutput(cmd)
                if ret == 0:
                    self._max_max = round(int(val)/1000, 3)

                cmd  = 'cat ' + os.path.join(self._device_path, 'in_temp163_min_min_input')
                ret, val = subprocess.getstatusoutput(cmd)
                if ret == 0:
                    self._min_min = round(int(val)/1000, 3)
            else:
                logging.error("Sysmon device path is None.")

        elif self._device_type == Sysmon_Device_Type.I2C:
            try:
                msgs = [I2C.Message([0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00])]
                self._bus.transfer(self._address, msgs)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x0c, 0x04, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x0d, 0x04, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._temp = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0xe3, 0x07, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min_min = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0xe4, 0x07, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max_max = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

            except IOError:
                logging.error("Read Sysmon failed.")

        elif self._device_type == Sysmon_Device_Type.PMBUS:
            try:
                msgs = [I2C.Message([0xc6, 0xd7, 0xe8, 0xf9, 0x03, 0x00, 0x08, 0x00])]
                self._bus.transfer(self._address, msgs)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x0c, 0x04, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0x0d, 0x04, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._temp = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0xe3, 0x07, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._min_min = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

                msgs = [I2C.Message([0x00, 0x00, 0x00, 0x00, 0xe4, 0x07, 0x04, 0x00]), I2C.Message([0x00, 0x00, 0x00, 0x00], read=True)]
                self._bus.transfer(self._address, msgs)
                logging.debug("{0}: 0x{1:02x}{2:02x}{2:02x}{3:02x}".format(self._address, msgs[1].data[0], msgs[1].data[1], msgs[1].data[2], msgs[1].data[3]))

                self._max_max = round(self.ConvertRawtoProcessed(msgs[1].data[0], msgs[1].data[1]), 3)

            except IOError:
                logging.error("Read Sysmon failed.")
        else:
            ps_path  = os.path.join(self._device_path, self._address)
            ret, val = subprocess.getstatusoutput(["cat", ps_path])
            if ret == 0:
                self._temp = int(val)

        return self._temp, self._min, self._max_max, self._min_min

    def __del__(self):
        logging.info("Inside Sysmon Destructor")
