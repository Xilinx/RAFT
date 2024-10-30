# Copyright (C) 2023-2024 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023-2024, Advanced Micro Devices, Inc."

import os
import psutil
import subprocess

SYSMON_IIO_DIR = '/sys/bus/iio/devices/iio:device0/'

class Stats(object):

    @staticmethod
    def path2channel(channel_name):
        return SYSMON_IIO_DIR + channel_name
        #return os.path.join(SYSMON_IIO_DIR, '/'.join(channel_name))

    def getCpuUtilization(self):
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_utilization = {"CPU Utilization": {}}
        for i, cpu_percent in enumerate(cpu_percent_per_core):
            cpu_utilization["CPU Utilization"][f"CPU Core {i + 1}"] = cpu_percent
        return cpu_utilization

    def getCpuFrequencies(self):
        cpu_frequencies = {"CPU Frequencies": {}}
        for i, freq in enumerate(psutil.cpu_freq(percpu=True)):
            cpu_frequencies["CPU Frequencies"][f"CPU Core {i + 1}"] = {
                "Current Frequency": freq.current,
                "Max Frequency": freq.max,
                "Min Frequency": freq.min
            }
        return cpu_frequencies

    def getMemoryUsage(self):
        memory = psutil.virtual_memory()
        used_memory = memory.used
        free_memory = memory.free
        total_memory = memory.total

        with open('/proc/meminfo') as meminfo_file:
            meminfo_data = meminfo_file.read()

        cma_total_line = next(line for line in meminfo_data.split('\n') if 'CmaTotal' in line)
        cma_free_line = next(line for line in meminfo_data.split('\n') if 'CmaFree' in line)

        cma_total = int(cma_total_line.split()[1])
        cma_free = int(cma_free_line.split()[1])

        swap = psutil.swap_memory()
        swap_free = swap.free
        swap_total = swap.total
        swap_percent = swap.percent

        memory_usage = {
            "Memory Usage": {
                "Used Memory": used_memory / (1024 ** 2),
                "Free Memory": free_memory / (1024 ** 2),
                "Total Memory": total_memory / (1024 ** 2)
            },
            "CMA Mem Utilization": {
                "Cma Total" : cma_total,
                "Cma Free" : cma_free
            },
            "Swap Mem Utilization": {
                "Swap Free": swap_free / (1024 ** 2),
                "Swap Total": swap_total / (1024 ** 2),
                "Swap Usage": swap_percent
            }
        }
        return memory_usage

    def getVoltages(self):
        voltages = {"Voltage Info": {
            "PS Sysmon": {},
            "PL Sysmon": {},
            "AMS CTRL": {}
        }}
        voltages
        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage9_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage9_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCC PS LPD": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage10_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage10_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCC PS FPD": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage11_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage11_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"PS AUX": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage12_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage12_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"DDR IO VCC": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage13_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage13_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"PS IO BANK 503": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage14_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage14_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"PS IO BANK 500": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage15_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage15_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCCO_PSIO1": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage16_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage16_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCCO_PSIO2": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage17_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage17_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCC_PS_GTR": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage18_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage18_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VTT_PS_GTR": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage19_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage19_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PS Sysmon"].update({"VCC_PSADC": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage21_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage21_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCCINT": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage22_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage22_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCCAUX": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage23_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage23_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"ADC Ref P+": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage24_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage24_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"ADC Ref N-": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage25_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage25_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCCBRAM": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage26_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage26_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCC_PSINTLP": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage27_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage27_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCC_PSINTFP": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage28_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage28_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"PS AUX": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage29_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage29_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["PL Sysmon"].update({"VCCAMS": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage0_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage0_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCC_PSPLL": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage1_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage1_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCC_PSBATT": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage2_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage2_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCCINT": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage3_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage3_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCCBRAM": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage4_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage4_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCCAUX": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage5_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage5_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCC_PSDDR_PLL": val})

        ret1, raw = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage6_raw'))
        ret2, scale = subprocess.getstatusoutput('cat ' + self.path2channel('in_voltage6_scale'))
        if  (ret1 | ret2) == 0:
            val = round((int(raw) * float(scale))/1000, 3)
            voltages["Voltage Info"]["AMS CTRL"].update({"VCC_PSINTFP_DDR": val})
        return voltages

    def getTemperatures(self):
        temps = {"Temperature Info": {}}
        ret1, pl_temp = subprocess.getstatusoutput('cat ' + self.path2channel("in_temp20_input"))
        ret2, lpd_temp = subprocess.getstatusoutput('cat ' + self.path2channel('in_temp7_input'))
        ret3, fpd_temp = subprocess.getstatusoutput('cat ' + self.path2channel('in_temp8_input'))
        if (ret1 | ret2 | ret3) == 0:
            temps["Temperature Info"]["FPD Temp"] = float(int(fpd_temp)/1000)
            temps["Temperature Info"]["LPD Temp"] = float(int(lpd_temp)/1000)
            temps["Temperature Info"]["PL Temp"] = float(int(pl_temp)/1000)
        return temps

    def getLastStatus(self):
        status = {}
        status.update(self.getCpuUtilization())
        status.update(self.getCpuFrequencies())
        status.update(self.getMemoryUsage())
        status.update(self.getTemperatures())
        status.update(self.getVoltages())
        return status