# Copyright (C) 2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2024, Advanced Micro Devices, Inc."

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
    VID = 0
    LINEAR16 = 1
    LINEAR11 = 2
    DIRECT = 3

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
            case 'MPQ2283' | 'MPQ2285':
                self.vout_scaling = ScalingType.DIRECT
                self.iout_scaling = None
                self.temp_scaling = None
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
        if self.page > 0:
            self._select_page()
        config = self._read_byte(PMBUS.ON_OFF_CONFIG)
        if config:
            config |= 0x08
            self._write_byte(PMBUS.ON_OFF_CONFIG, config)
            pm_print("ON_OFF_CONFIG = 0x{0:02x}".format(config))
        self._write_byte(PMBUS.OPERATION, 0x80)

    def shutdown_output(self):
        """Disable output via OPERATION command."""
        if self.page > 0:
            self._select_page()
        config = self._read_byte(PMBUS.ON_OFF_CONFIG)
        if config:
            config |= 0x08
            self._write_byte(PMBUS.ON_OFF_CONFIG, config)
            pm_print("ON_OFF_CONFIG = 0x{0:02x}".format(config))
        self._write_byte(PMBUS.OPERATION, 0x00)

    def set_voltage(self, value):
        pm_print(f"set_voltage({value})")
        if self.name in ("MPQ2283", "MPQ2285"):
            raw_value = self._value_2_rawvalue(value, self.vout_scaling)
            pm_print("raw_value 0x{0:02x}".format(raw_value))
            self._write_byte(PMBUS.VOUT_COMMAND, raw_value)
        else:
            self.shutdown_output()
            if self.page > 0:
                self._select_page()
            self._get_vout_mode()
            raw_value = self._value_2_rawvalue(value, self.vout_scaling)
            self._write_word(PMBUS.VOUT_COMMAND, raw_value)
            pm_print("raw_value 0x{0:04x}".format(raw_value))
            self.enable_output()

    def read_voltage(self):
        """Read and scale output voltage using READ_VOUT command."""
        pm_print(f"read_voltage()")
        if not self.vout_scaling:
            return None
        if self.page >= 0:
            self._select_page()
        self._get_vout_mode()
        if self.name in ("MPQ2283", "MPQ2285"):
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
        if self.name in ("MPQ2283", "MPQ2285"):
            VOUT_SL = self._read_byte(PMBUS.VOUT_SCALE_LOOP) + 1
            value = ((raw_value * 6.25e-3) + 206.25e-3) * VOUT_SL
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
        if self.name in ("MPQ2283", "MPQ2285"):
            VOUT_SL = self._read_byte(PMBUS.VOUT_SCALE_LOOP) + 1
            raw_value = ((value / VOUT_SL) - 206.25e-3) / 6.25e-3
            #value = ((raw_value * 6.25e-3) + 206.25e-3) * VOUT_SL
        else:
            raw_value = 0 # implement !
        return round(raw_value)

    def _value_2_rawvalue(self, value, scaling):
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
        self.vout_mode = self._read_byte(PMBUS.VOUT_MODE)
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
    def __init__(self, device_path, device_address, page=-1, phase=-1, fb_ratio=1, alert_gpio_pin=None):
        """
        Initialize a MPS(MPM54) device with a specific page (output).

        :param device_path: I2C bus number (e.g., 1 for /dev/i2c-1)
        :param device_address: I2C address of the PMIC
        :param page: Page number corresponding to the output
        :param phase: Phase number corresponding to the output
        :param fb_ratio: Feedback Ratio corresponding to the output
        :param alert_gpio_pin: Optional GPIO pin for ALERT (None if not used)
        """
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
        """Clean up resources."""
        self.i2c.close()
        if self.alert_gpio:
            self.alert_gpio.close()

    def enable_output(self):
        pm_print("enable_output")
        """Enable output via OPERATION command."""
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
        pm_print("set_voltage")
        #self.shutdown_output()
        #VOUT_COMMAND = 0x21
        #raw_value = self._unscaled_value(value, self.vout_scaling)
        #self._write_word(raw_value)
        #self.enable_output()

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
        voltage = ((raw_voltage * 16) / 1000) / self.fb_ratio # 16mV per LSB and mV to V
        return round(voltage, 4)

    def read_current(self):
        READ_IOUT = 0x13
        if self.page >= 0:
            READ_IOUT += self.page * 2
        raw_current = self._read_byte(READ_IOUT)
        pm_print("raw_current(0x{0:02x}) 0x{1:02x}".format(READ_IOUT, raw_current))
        return ((raw_current * 50) / 1000) # 50mA per LSB and mV to V

    def read_temperature(self):
        """Read and scale output temperature using TEMPERATURE command."""
        """     000: < 80°C
                001: 85°C
                010: 95°C
                011: 105°C
                100: 115°C
                101: 125°C
                110: 135°C
                111: ≥ 140°C """
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

    def _read_byte(self, command):
        byte = None
        try:
            write_msg = I2C.Message([command])
            read_msg = I2C.Message([0x00], read=True)
            self.i2c.transfer(self.addr, [write_msg, read_msg])
            byte = read_msg.data[0]
        except:
            pm_print("IOError: {0}@0x{1:02x}".format(self.i2c.devpath, self.addr))
        return byte