# Copyright (C) 2024 - 2026 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2024 - 2026, Advanced Micro Devices, Inc."

from enum import IntEnum
from periphery import I2C, GPIO
import threading

PM_LOWLEVEL_DEBUG = False

class PMBUS(IntEnum):
    PAGE =          0x00
    OPERATION =     0x01
    ON_OFF_CONFIG = 0x02
    CLEAR_FAULTS =  0x03
    PHASE =         0x04
    VOUT_MODE =     0x20
    VOUT_COMMAND =  0x21
    VOUT_MAX =      0X24
    VOUT_MIN =      0x2B
    VOUT_SCALE_LOOP = 0x29
    STATUS_BYTE =   0x79
    STATUS_WORD =   0x79
    STATUS_VOUT =   0x7A
    STATUS_IOUT =   0x7B
    STATUS_INPUT =  0x7C
    STATUS_TEMP =   0x7D
    STATUS_CML =    0x7E
    STATUS_OTHER =  0x7F
    READ_VOUT =     0x8B
    READ_IOUT =     0x8C
    READ_TEMP_1 =   0x8D
    IC_DEVICE_ID =  0xAD
    IC_DEVICE_REV = 0xAE

class ScalingType(IntEnum):
    VID = 1
    LINEAR16 = 2
    LINEAR11 = 3
    DIRECT = 4

PMBUS_IEEE754_VOUT_MODE = 0x60
PMBUS_IEEE754_EXP_OFFSET = 25
PMBUS_IEEE754_MIN_MANTISSA = 0x400
PMBUS_IEEE754_MAX_MANTISSA = 0x7FF
PMBUS_IEEE754_VOUT_SCALE = 1000

# Decode PMBus VOUT IEEE754 half-precision register data to volts.
def _pmbus_ieee754_reg_to_volts(reg):
    # 16-bit word: [15]=sign, [14:10]=exponent, [9:0]=mantissa.
    sign = (reg >> 15) & 1
    exponent = (reg >> 10) & 0x1F
    val = reg & 0x3FF
    scale = PMBUS_IEEE754_VOUT_SCALE

    if exponent == 0:
        # Subnormal: effective exponent is -24.
        exponent = -(14 + 10)
    elif exponent == 0x1F:
        # Saturated value.
        exponent = 0
        val = 65504
    else:
        # Normal: remove IEEE754 bias (15+10) and restore implicit mantissa bit.
        exponent -= PMBUS_IEEE754_EXP_OFFSET
        val |= PMBUS_IEEE754_MIN_MANTISSA

    # Scale to millivolts, apply exponent, then convert back to volts.
    val *= scale
    if exponent >= 0:
        val <<= exponent
    else:
        val >>= -exponent

    if sign:
        val = -val

    return val / scale

# Encode volts as PMBus VOUT IEEE754 half-precision register data.
def _pmbus_volts_to_ieee754_reg(value):
    scale = PMBUS_IEEE754_VOUT_SCALE
    if value == 0:
        return 0

    sign = 0
    # Work in millivolts to keep the mantissa in integer form.
    data = round(value * scale)
    if data < 0:
        sign = 1
        data = -data

    # Start at the IEEE754 half-precision bias and normalize mantissa into range.
    exponent = PMBUS_IEEE754_EXP_OFFSET
    while data > PMBUS_IEEE754_MAX_MANTISSA * scale and exponent < 30:
        exponent += 1
        data >>= 1
    while data < PMBUS_IEEE754_MIN_MANTISSA * scale and exponent > 1:
        exponent -= 1
        data <<= 1

    mantissa = round(data / scale)

    # Clamp mantissa to the 10-bit IEEE754 half-precision range.
    mantissa = max(PMBUS_IEEE754_MIN_MANTISSA, min(mantissa, PMBUS_IEEE754_MAX_MANTISSA))

    # Pack sign, biased exponent, and 10-bit mantissa into one 16-bit register.
    return (sign << 15) | ((exponent & 0x1F) << 10) | (mantissa & 0x3FF)

def pm_print(printstr):
    if(PM_LOWLEVEL_DEBUG):
        print(printstr)

class PMBusRegulator:
    vout_scaling = ScalingType.LINEAR16
    iout_scaling = ScalingType.LINEAR11
    temp_scaling = None
    def __init__(self, device_name, device_path, device_address, page=-1, pmbus_vout_mode=-1, phase=-1, alert_gpio_pin=None):
        """
        Initialize a PMBus device with a specific page (output).

        :param bus_number: I2C bus number (e.g., 1 for /dev/i2c-1)
        :param device_address: I2C address of the PMIC
        :param page: PMBus page number corresponding to the output
        :param alert_gpio_pin: Optional GPIO pin for PMBus ALERT (None if not used)
        """
        self.name = device_name
        self.i2c = I2C(device_path)
        self.addr = int(device_address, 0)
        self.page = page
        self.pmbus_vout_mode = pmbus_vout_mode
        self.phase = phase
        self.vout_mode = 0

        match self.name:
            case 'TPS53681':
                self.vout_scaling = ScalingType.VID
                self.temp_scaling = ScalingType.LINEAR11
            case 'MPQ2283' | 'MPQ2285' | 'MPQ2287' | 'MPQ72963':
                self.vout_scaling = ScalingType.DIRECT
                self.iout_scaling = None
                self.temp_scaling = None
            case 'LT7182S':
                self.vout_scaling = ScalingType.LINEAR16
            case _:
                self.vout_scaling = ScalingType.LINEAR16

        if self.pmbus_vout_mode <= 0:
            self.vout_mode = 0x18 # 0x18 - 0x20 = -8

        # Initialize ALERT pin if provided
        self.alert_gpio = GPIO(alert_gpio_pin, "in") if alert_gpio_pin is not None else None
        if self.alert_gpio:
            self.alert_gpio.edge = "falling"
            self.alert_thread = threading.Thread(target=self._alert_monitor)
            self.alert_thread.daemon = True
            self.alert_thread.start()

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['i2c'] and v
        }
        return str(str_info)

    def close(self):
        """Clean up resources."""
        self.i2c.close()
        if self.alert_gpio:
            self.alert_gpio.close()

    def enable_output(self):
        """Enable output via OPERATION command."""
        if self.page >= 0:
            self._select_page()
        config = self._read_byte(PMBUS.ON_OFF_CONFIG)
        if config:
            config |= 0x08
            self._write_byte(PMBUS.ON_OFF_CONFIG, config)
            pm_print("ON_OFF_CONFIG = 0x{0:02x}".format(config))
        self._write_byte(PMBUS.OPERATION, 0x80)

    def shutdown_output(self):
        """Disable output via OPERATION command."""
        if self.page >= 0:
            self._select_page()
        config = self._read_byte(PMBUS.ON_OFF_CONFIG)
        if config:
            config |= 0x08
            self._write_byte(PMBUS.ON_OFF_CONFIG, config)
            pm_print("ON_OFF_CONFIG = 0x{0:02x}".format(config))
        self._write_byte(PMBUS.OPERATION, 0x00)

    def set_voltage(self, value):
        pm_print(f"set_voltage({value})")
        if self.name in ("MPQ2283", "MPQ2285", "MPQ2287"):
            raw_value = self._value_2_rawvalue(value, self.vout_scaling)
            pm_print("raw_value 0x{0:02x}".format(raw_value))
            self._write_byte(PMBUS.VOUT_COMMAND, raw_value)
        else:
            #self.shutdown_output()
            if self.page >= 0:
                self._select_page()
            self._get_vout_mode()
            raw_value = self._value_2_rawvalue(value, self.vout_scaling)
            self._write_word(PMBUS.VOUT_COMMAND, raw_value)
            pm_print("raw_value 0x{0:04x}".format(raw_value))
            #self.enable_output()

    def read_voltage(self):
        """Read and scale output voltage using READ_VOUT command."""
        pm_print(f"read_voltage()")
        if not self.vout_scaling:
            return None
        if self.page >= 0:
            self._select_page()
        self._get_vout_mode()
        if self.name in ("MPQ2283", "MPQ2285", "MPQ2287"):
            raw_voltage = self._read_byte(PMBUS.VOUT_COMMAND)
        else:
            raw_voltage = self._read_word(PMBUS.READ_VOUT)
        if not raw_voltage:
            return None
        else:
            pm_print("raw_voltage 0x{0:04x}".format(raw_voltage))
            return round(self._rawvalue_2_value(raw_voltage, self.vout_scaling), 4)

    def read_current(self):
        """Read and scale output current using READ_IOUT command."""
        if not self.iout_scaling:
            return None
        if self.page >= 0:
            self._select_page()
        if self.phase > 0:
            self._write_byte(PMBUS.PHASE, 0x80) # 0x80 to read whole phases as total
        raw_current = self._read_word(PMBUS.READ_IOUT)
        if not raw_current:
            return None
        else:
            pm_print("raw_current 0x{0:04x}".format(raw_current))
            return self._rawvalue_2_value(raw_current, self.iout_scaling)

    def read_temperature(self):
        """Read and scale output temperature using READ_TEMPERATURE_1 command."""
        if not self.temp_scaling:
            return None
        if self.page >= 0:
            self._select_page()
        raw_temp = self._read_word(PMBUS.READ_TEMP_1)
        if not raw_temp:
            return None
        else:
            pm_print("raw_temp 0x{0:04x}".format(raw_temp))
            return self._rawvalue_2_value(raw_temp, self.temp_scaling)

    def read_vin(self):
        return None

    def read_iin(self):
        return None

    def read_pout(self):
        return None

    def read_pin(self):
        return None

    def read_telemetry_all(self):
        telemetry = []
        telemetry.append(self.read_vin())
        telemetry.append(self.read_iin())
        telemetry.append(self.read_voltage())
        telemetry.append(self.read_current())
        telemetry.append(self.read_temperature())
        telemetry.append(self.read_pout())
        telemetry.append(self.read_pin())
        return telemetry

    def clear_faults(self):
        """Clear all recorded faults."""
        self._write_byte(PMBUS.CLEAR_FAULTS, 0x00)

    def _linear11_to_float(self, linear11):
        """ Convert a Linear11 formatted value to a float. """
        exponent = (linear11 >> 11) & 0x1F
        if exponent & 0x10:
            exponent -= 0x20
        mantissa = linear11 & 0x07FF
        if mantissa & 0x0400:
            mantissa -= 0x0800
        return mantissa * (2 ** exponent)

    def _linear16_to_float(self, linear16):
        """ Convert a Linear16 formatted value to a float. """
        exponent = self.vout_mode & 0x1F
        if exponent >= 0x10:
            exponent -= 0x20
        return linear16 * (2 ** exponent)

    def _vid_mode_to_float(self, raw_value):
        vid_mode = self.vout_mode & 0x0F
        if vid_mode == 0x04:
            value = 0.5 + (raw_value - 1) * 0.01 # 10mV
        elif vid_mode == 0x07:
            value = 0.25 + (raw_value - 1) * 0.005  # 5mV
        else:
            value = 0.25 + (raw_value - 1) * 0.005  # XmV, fix this !
        return value

    def _direct_to_float(self, raw_value):
        if self.name in ("MPQ2283", "MPQ2285", "MPQ2287"):
            VOUT_SL = self._read_byte(PMBUS.VOUT_SCALE_LOOP) + 1
            value = ((raw_value * 6.25e-3) + 206.25e-3) * VOUT_SL
        elif self.name == "MPQ72963":
            value = raw_value * 1.5625e-3
        else:
            value = 0 # implement !
        return value

    def _float_to_vid_mode(self, value):
        vid_mode = self.vout_mode & 0x0F
        value *= 1000
        if vid_mode == 0x04:
            raw_value = (((value - 500) / 10) + 1)
        elif vid_mode == 0x07:
            raw_value = (((value - 250) / 5) + 1)
        else:
            raw_value = (((value - 250) / 5) + 1)
        return round(raw_value)

    def _float_to_linear11(value):
        # Initialize the exponent
        exponent = 0
        # Scale the mantissa so that it fits in 11 bits
        mantissa = value
        while mantissa < -1024 or mantissa > 1023:
            mantissa /= 2
            exponent += 1
        
        # If the mantissa is too small, adjust by decreasing the exponent
        while mantissa > -1024 and mantissa < 1024 and exponent > -16:
            mantissa *= 2
            exponent -= 1
        # Round mantissa to the nearest integer
        mantissa = round(mantissa)
        # Handle cases where the mantissa still doesn't fit after rounding
        if mantissa < -1024 or mantissa > 1023:
            raise ValueError("Value cannot be represented in Linear11 format")
        # Encode exponent (5 bits, two's complement)
        encoded_exponent = exponent & 0x1F
        # Encode mantissa (11 bits, two's complement)
        encoded_mantissa = mantissa & 0x07FF
        
        # Combine into a 16-bit value
        linear11_value = (encoded_exponent << 11) | encoded_mantissa
        return linear11_value

    def _float_to_linear16(self, value):
        exponent = self.vout_mode & 0x1F
        if exponent >= 0x10:
            exponent -= 0x20
        return round((value / (2 ** exponent)))

    def _float_to_direct(self, value):
        if self.name in ("MPQ2283", "MPQ2285", "MPQ2287"):
            VOUT_SL = self._read_byte(PMBUS.VOUT_SCALE_LOOP) + 1
            raw_value = ((value / VOUT_SL) - 206.25e-3) / 6.25e-3
            #value = ((raw_value * 6.25e-3) + 206.25e-3) * VOUT_SL
        elif self.name == "MPQ72963":
            raw_value = value / 5e-3
        else:
            raw_value = 0 # implement !
        return round(raw_value)

    def _uses_ieee754_vout(self):
        return (self.vout_mode & 0x60) == PMBUS_IEEE754_VOUT_MODE

    def _value_2_rawvalue(self, value, scaling):
        if self._uses_ieee754_vout() and scaling == ScalingType.LINEAR16:
            return int(_pmbus_volts_to_ieee754_reg(value))
        match scaling:
            case ScalingType.VID:
                return int(self._float_to_vid_mode(value))
            case ScalingType.LINEAR16:
                return int(self._float_to_linear16(value))
            case ScalingType.LINEAR11:
                return int(self._float_to_linear11(value))
            case ScalingType.DIRECT:
                return int(self._float_to_direct(value))
            case _:
                return value / (2 ** self.vout_mode)

    def _rawvalue_2_value(self, raw_value, scaling):
        """Apply scaling to raw PMBus data based on scaling type."""
        if self._uses_ieee754_vout() and scaling == ScalingType.LINEAR16:
            return _pmbus_ieee754_reg_to_volts(raw_value)
        match scaling:
            case ScalingType.VID:
                return self._vid_mode_to_float(raw_value)
            case ScalingType.LINEAR16:
                return self._linear16_to_float(raw_value)
            case ScalingType.LINEAR11:
                return self._linear11_to_float(raw_value)
            case ScalingType.DIRECT:
                return self._direct_to_float(raw_value)
            case _:
                return raw_value * (2 ** self.vout_mode)

    def _alert_monitor(self):
        """Monitor ALERT GPIO and handle interrupts."""
        while True:
            self.alert_gpio.poll(timeout=None)
            status_word = self.handle_alert()
            if status_word is not None:
                pm_print(f"Alert! STATUS_WORD: 0x{status_word:04X}")

    def handle_alert(self):
        """Handle PMBus ALERT by checking STATUS_WORD."""
        ara_msg = I2C.Message([0x00], read=True)
        self.i2c.transfer(0x0C, [ara_msg])
        if ara_msg.data[0] == self.addr:
            return self.read_status_word()
        return None

    def read_status_word(self):
        """Read STATUS_WORD for fault info."""
        return self._read_word(PMBUS.STATUS_WORD)

    def _select_page(self):
        """Set the PMBus page for output control."""
        pm_print("set page to 0x{0:02x}".format(self.page))
        self._write_byte(PMBUS.PAGE, self.page)

    def _get_vout_mode(self):
        """Retrieve VOUT_MODE scaling exponent."""
        if self.pmbus_vout_mode <= 0:
            return
        mode = self._read_byte(PMBUS.VOUT_MODE)
        if mode is None:
            return
        self.vout_mode = mode
        pm_print("raw_vout_mode 0x{0:02x}".format(self.vout_mode))

    def _write_word(self, command, value):
        try:
            write_msg = I2C.Message([command, value & 0xFF, (value >> 8) & 0xFF])
            self.i2c.transfer(self.addr, [write_msg])
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))

    def _read_word(self, command):
        word = None
        try:
            write_msg = I2C.Message([command])
            read_msg = I2C.Message([0x00, 0x00], read=True)
            self.i2c.transfer(self.addr, [write_msg, read_msg])
            word = read_msg.data[0] | (read_msg.data[1] << 8)
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
        return word

    def _write_byte(self, command, value):
        try:
            write_msg = I2C.Message([command, value])
            self.i2c.transfer(self.addr, [write_msg])
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))

    def _read_byte(self, command):
        byte = None
        try:
            write_msg = I2C.Message([command])
            read_msg = I2C.Message([0x00], read=True)
            self.i2c.transfer(self.addr, [write_msg, read_msg])
            byte = read_msg.data[0]
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
        return byte

class MPSRegulator:
    # MPM54322/MPM54522 I2C register map (BUCKx_CTRL1/2/3, VOUT GO bit).
    BUCK1_CTRL1 = 0x01
    BUCK1_CTRL2 = 0x02
    BUCK1_CTRL3 = 0x03
    BUCK2_CTRL1 = 0x06
    BUCK2_CTRL2 = 0x07
    BUCK2_CTRL3 = 0x08
    VOUT_GO_BIT = 0x80

    def __init__(self, device_path, device_address, page=-1, phase=-1, fb_ratio=1, alert_gpio_pin=None):
        # Initialize an MPS (MPM54322/MPM54522) regulator for the given I2C
        # device and buck page.
        self.i2c = I2C(device_path)
        self.addr = int(device_address, 0)
        self.page = page
        self.phase = phase
        self.fb_ratio = fb_ratio

        # Initialize ALERT pin if provided
        self.alert_gpio = GPIO(alert_gpio_pin, "in") if alert_gpio_pin is not None else None
        if self.alert_gpio:
            self.alert_gpio.edge = "falling"
            self.alert_thread = threading.Thread(target=self._alert_monitor)
            self.alert_thread.daemon = True
            self.alert_thread.start()

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['i2c'] and v
        }
        return str(str_info)

    def close(self):
        # Clean up I2C and ALERT GPIO resources.
        self.i2c.close()
        if self.alert_gpio:
            self.alert_gpio.close()

    def enable_output(self):
        # Enable output via OPERATION register (0x0D).
        pm_print("enable_output")
        OPERATION = 0x0D
        temp = self._read_byte(OPERATION)
        mask = 0
        if self.page >= 0:
            if self.page == 0:
                mask = 0x40
            else:
                mask = 0x20
        else:
            mask = 0x80
        temp |= mask
        self._write_byte(OPERATION, temp)

    def shutdown_output(self):
        # Disable output via OPERATION register (0x0D).
        pm_print("shutdown_output")
        OPERATION = 0x0D
        temp = self._read_byte(OPERATION)
        mask = 0
        if self.page >= 0:
            if self.page == 0:
                mask = ~0x40
            else:
                mask = ~0x20
        else:
            mask = ~0x80
        temp &= mask
        self._write_byte(OPERATION, temp)

    def set_voltage(self, value):
        # Set output voltage on MPM54322/MPM54522 via VOUT_SETTING + GO.
        # Output range is enforced by board JSON Minimum/Maximum_Volt in
        # pm.py.
        pm_print(f"set_voltage({value})")

        # Step 1: Convert requested output voltage (V) to the PMIC target in mV
        # at the FB node.
        # read_voltage() does the inverse: Vout = (raw * 16mV) / fb_ratio, so we
        # multiply by fb_ratio here.
        setting_mv = round(value * self.fb_ratio * 1000)

        # Step 2: Split setting_mv (11 bits) into setting_low [2:0] (3 bits)
        # and setting_high [10:3] (8 bits).
        setting_low = setting_mv & 0x7
        setting_high = (setting_mv >> 3) & 0xFF

        # Step 3: Pick the buck-1 or buck-2 control register set from board
        # JSON Page_Select.
        if self.page >= 1:
            ctrl1, ctrl2, ctrl3 = self.BUCK2_CTRL1, self.BUCK2_CTRL2, self.BUCK2_CTRL3
        else:
            ctrl1, ctrl2, ctrl3 = self.BUCK1_CTRL1, self.BUCK1_CTRL2, self.BUCK1_CTRL3

        # Step 4: Read ctrl1 and ctrl2 before any writes so an I2C read
        # failure cannot leave a partially programmed voltage target.
        ctrl1_val = self._read_byte(ctrl1)
        ctrl2_val = self._read_byte(ctrl2)

        # Step 5: Merge VOUTx_SETTING_LOW into ctrl2 (bits 2:0), preserving
        # other ctrl2 fields.
        ctrl2_val = (ctrl2_val & ~0x07) | setting_low

        # Step 6: Write VOUTx_SETTING_LOW/HIGH, then assert VOUTx_GO.
        self._write_byte(ctrl2, ctrl2_val)
        self._write_byte(ctrl3, setting_high)
        self._write_byte(ctrl1, ctrl1_val | self.VOUT_GO_BIT)
        pm_print("setting_mv={0} ctrl=0x{1:02x}/0x{2:02x}/0x{3:02x}".format(
            setting_mv, ctrl1, ctrl2, ctrl3))

    def read_all(self):
        values = {}
        values['voltage'] = self.read_voltage()
        values['current'] = self.read_current()
        values['temperature'] = self.read_temperature()
        return values

    def read_voltage(self):
        READ_VOUT = 0x12
        if self.page >= 0:
            READ_VOUT += self.page * 2
        raw_voltage = self._read_byte(READ_VOUT)
        pm_print("raw_voltage(0x{0:02x}) 0x{1:02x}".format(READ_VOUT, raw_voltage))
        # 16mV per LSB and mV to V
        voltage = ((raw_voltage * 16) / 1000) / self.fb_ratio
        return round(voltage, 4)

    def read_current(self):
        READ_IOUT = 0x13
        if self.page >= 0:
            READ_IOUT += self.page * 2
        raw_current = self._read_byte(READ_IOUT)
        pm_print("raw_current(0x{0:02x}) 0x{1:02x}".format(READ_IOUT, raw_current))
        # 50mA per LSB and mA to A
        return ((raw_current * 50) / 1000)

    def read_temperature(self):
        # Read junction temperature from TEMPERATURE register (0x11).
        # Encoded in upper 3 bits: 000 < 80°C, 001 85°C, 010 95°C, 011 105°C,
        # 100 115°C, 101 125°C, 110 135°C, 111 ≥ 140°C.
        TEMPERATURE = 0x11
        raw_temp = self._read_byte(TEMPERATURE)
        return ((((raw_temp & 0xE0) >> 5) * 5) + 80)

    def _write_word(self, command, value):
        try:
            write_msg = I2C.Message([command, value & 0xFF, (value >> 8) & 0xFF])
            self.i2c.transfer(self.addr, [write_msg])
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))

    def _read_word(self, command):
        word = None
        try:
            write_msg = I2C.Message([command])
            read_msg = I2C.Message([0x00, 0x00], read=True)
            self.i2c.transfer(self.addr, [write_msg, read_msg])
            word = read_msg.data[0] | (read_msg.data[1] << 8)
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
        return word

    def _write_byte(self, command, value):
        try:
            write_msg = I2C.Message([0x00, 0x00])
            self.i2c.transfer(self.addr, [write_msg])
            
            write_msg = I2C.Message([command, value])
            self.i2c.transfer(self.addr, [write_msg])
            
            write_msg = I2C.Message([0x00, 0x01])
            self.i2c.transfer(self.addr, [write_msg])
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
            raise IOError(
                "Failed to write 0x{0:02x} to {1}@0x{2:02x}".format(
                    command, self.i2c.devpath, self.addr))

    def _read_byte(self, command):
        try:
            write_msg = I2C.Message([command])
            read_msg = I2C.Message([0x00], read=True)
            self.i2c.transfer(self.addr, [write_msg, read_msg])
            return read_msg.data[0]
        except IOError:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
            raise IOError(
                "Failed to read 0x{0:02x} from {1}@0x{2:02x}".format(
                    command, self.i2c.devpath, self.addr))