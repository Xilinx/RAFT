# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

REG_CONFIG = 0x00
REG_SHUNTVOLTAGE = 0x01
REG_BUSVOLTAGE = 0x02
REG_POWER = 0x03
REG_CURRENT = 0x04
REG_CALI = 0x05
REG_MASK = 0x06
REG_LIMIT = 0x07
REG_MANUFACTURER_ID = 0XFE
REG_DIE_ID = 0XFF


BUS_MILLIVOLTS_LSB = 1.25
SHUNT_MILLIVOLTS_LSB = 0.0025