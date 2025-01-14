# Copyright (C) 2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2024, Advanced Micro Devices, Inc."

import json
from enum import IntEnum

class Sysmon_Device_Type(IntEnum):
    I2C = 0
    PMBUS = 1
    SYSFS = 2

class Rails:
    def __init__(self, Name, Part_Name, I2C_Bus, I2C_Address,
                 Shunt_Resistor=None, Maximum_Current=None, Phase_Multiplier=None,
                 Maximum_Volt=None, Typical_Volt=None, Minimum_Volt=None,
                 PMBus_VOUT_MODE=-1, Page_Select=-1, Phase=-1, FB_Ratio=1.0, Voltage_Multiplier=-1):
        self.name = Name
        self.part_name = Part_Name
        self.i2c_bus = I2C_Bus
        self.i2c_address = I2C_Address
        self.shunt_resistor = Shunt_Resistor
        self.maximum_current = Maximum_Current
        self.phase_multiplier = Phase_Multiplier
        self.maximum_volt = Maximum_Volt
        self.typical_volt = Typical_Volt
        self.minimum_volt = Minimum_Volt
        self.pmbus_vout_mode = int(PMBus_VOUT_MODE)
        self.page_select = int(Page_Select)
        self.phase = int(Phase)
        self.fb_ratio = float(FB_Ratio)
        self.voltage_multiplier = int(Voltage_Multiplier)

        self._sensor = None
        self._output = None

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k and v is not None
        }
        return str(str_info)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Domain:
    def __init__(self, Name, Rails):
        self.name = Name
        self.railnames = Rails

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k and v
        }
        return str(str_info)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Unit:
    def __init__(self, base_unit, available_scales):
        self.base_unit = base_unit
        self.available_scales = available_scales
        self.current_unit = None
        self.quantity = None

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k and v
        }
        return str(str_info)