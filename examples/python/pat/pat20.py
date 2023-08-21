# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-3-Clause

from enum import Enum
from i2c_client import i2c
import threading

class P_TYPE(Enum):
     PD_PROGRAMMABLE_LOGIC = 1
     PD_FULL = 2
     PD_LOW = 3
     PD_TEMP = 4

class Ina226Data:
    def __init__(self, addr0, name0, description0, domain0, mOhms0, uALsb0):
        self.addr = addr0
        self.name = name0
        self.description = description0,
        self.domain = domain0
        self.mOhms = mOhms0
        self.uAlsb = uALsb0
        self.cal = cal = 5120000 / mOhms0 / uALsb0
        self.vAdc = 0
        self.vShuntAdc = 0
        self.iAdc = 0
        v = 0
        i = 0
        p = 0
        pass

class SysmonData:
    def __init__(self, idStr0, name0, description0, domain0):
        self.idStr = idStr0
        self.name = name0
        self.description = description0,
        self.domain = domain0
        self.vAdc = 0
        self.vShuntAdc = 0
        self.iAdc = 0
        v = 0
        i = 0
        p = 0
        pass

class PAT20:
    def __init__(self):
        self.chip_list = []
        self.sysmon = []
        self.fpdReport = ""
        self.lpdReport = ""
        self.pldReport = ""
        self.fpdPower = 0.0
        self.ldpPower = 0.0
        self.pldPower = 0.0
        self.TotalPower = 0.0
        self.psTemp = 0.0
        self.chip_list.append(Ina226Data(0x40, "VCCINT", "PL Core Rail", P_TYPE.PD_PROGRAMMABLE_LOGIC, 0.5, 2000))  # 0.85V
        self.chip_list.append(Ina226Data(0x45, "VADJ_FMC", "Main FMC Rail", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 200))  # 1.8V
        self.chip_list.append(Ina226Data(0x46, "MGTAVCC", "Receiver and Transmitter Internal", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 200))  # 0.9V
        self.chip_list.append(Ina226Data(0x49, "VCCINT_AMS", "ADC and DAC Digital Logic", P_TYPE.PD_PROGRAMMABLE_LOGIC, 0.5, 500))  # 0.85V
        self.chip_list.append(Ina226Data(0x4a, "DAC_AVTT", "DAC Termination", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 40))   # 2.5V
        self.chip_list.append(Ina226Data(0x4b, "DAC_AVCCAUX", "Analog for the custom DAC block", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 40))   # 1.8V
        self.chip_list.append(Ina226Data(0x4c, "ADC_AVCC", "Digital for the custom ADC block", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 200))  # 0.925V
        self.chip_list.append(Ina226Data(0x4d, "ADC_AVCCAUX", "Analog for the custom ADC block", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 200))  # 1.8V
        self.chip_list.append(Ina226Data(0x4e, "DAC_AVCC", "Digital for the custom DAC block", P_TYPE.PD_PROGRAMMABLE_LOGIC, 5, 100))  # 0.925V
        """
         PS FPD
        """
        self.chip_list.append(Ina226Data(0x43, "VCC1V2", "DDR Termination", P_TYPE.PD_FULL, 5, 500))  # 1.2V
        self.chip_list.append(Ina226Data(0x47, "MGT1V2", "GTH Termination Power", P_TYPE.PD_FULL, 5, 500))  # 1.2V
        self.chip_list.append(Ina226Data(0x48, "MGT1V8", "GTH Power", P_TYPE.PD_FULL, 5, 40))   # 1.8V

        """
         PS LPD
        """
        self.chip_list.append(Ina226Data(0x41, "VCCPSINT", "PS Core Rail", P_TYPE.PD_LOW, 0.5, 1000))  # 0.85V
        self.chip_list.append(Ina226Data(0x42, "VCC1V8",   "Auxiliary Circuits", P_TYPE.PD_LOW, 2, 200))   # 1.8V

        """
         SYSMON
        """
        self.sysmon.append(SysmonData("in_temp0_ps_temp", "PS Temperature", "", P_TYPE.PD_TEMP))

        self.sysmon.append(SysmonData("in_voltage8_vccpsintfp", "VCCPSINTFP", "", P_TYPE.PD_FULL))
        self.sysmon.append(SysmonData("in_voltage6_vccpsintfpddr", "VCCO_PSDDR_504", "", P_TYPE.PD_FULL))
        self.sysmon.append(SysmonData("in_voltage7_vccpsintlp", "VCCPSINTLP", "", P_TYPE.PD_LOW))
        self.sysmon.append(SysmonData("in_voltage9_vccpsaux", "VCCPSAUX", "", P_TYPE.PD_LOW))
        self.sysmon.append(SysmonData("in_voltage11_vccpsio3", "VCCOPS3", "", P_TYPE.PD_LOW))
        self.sysmon.append(SysmonData("in_voltage12_vccpsio0", "VCCOPS0", "", P_TYPE.PD_LOW))
        self.sysmon.append(SysmonData("in_voltage13_vccpsio1", "VCCOPS1", "", P_TYPE.PD_LOW))
        self.sysmon.append(SysmonData("in_voltage14_vccpsio2", "VCCOPS2", "", P_TYPE.PD_LOW))

    def PullINA226Data(self, i2c):
        for chip in self.chip_list:
            #read the I2C data
            #global i2c
            ret, value = i2c.XI2c_ReadINA226Reg(chip.addr, 0x2)
            chip.vAdc = value;
            ret, value = i2c.XI2c_ReadINA226Reg(chip.addr, 0x1)
            if value >= 0x8000:
                """
                Handle negative current values.
                """
                value = 0 # Set a negative current to 0
            elif value < 0x0000:
                """
                Handle negative current values.
                """
                value = 0 # Set a negative current to 0
            chip.vShuntAdc = value;
            chip.v = chip.vAdc * 5 / 4;
            chip.i = chip.vShuntAdc * 2500 / chip.mOhms;
            chip.p = chip.i / 200 * chip.vAdc / 4;

    def generateReport(self):
        str = ""
        for chip in self.chip_list:
            str = str + '<tr><td></td><td>{}</td><td align="right">{: f}</td><td align="right">{: f}</td><td align="right">{: f}</td></tr>\n'.format(chip.name, float(chip.v/1000), float(chip.i/1000), float(chip.p/1000))
        return(str)

    def generateFullReport(self):
        self.fpdPower = 0.0
        self.lpdPower = 0.0
        self.pldPower = 0.0
        self.totalPower = 0.0
        self.pldReport = ""
        self.lpdReport = ""
        self.fpdReport = ""
        for chip in self.chip_list:
            str = '<tr><td></td><td>{}</td><td align="right">{:1.3f}</td><td align="right">{:3.1f}</td><td align="right">{:3.1f}</td></tr>\n'.format(chip.name, float(chip.v/1000), float(chip.i/1000), float(chip.p/1000))
            if chip.domain == P_TYPE.PD_FULL:
                 self.fpdReport = self.fpdReport + str
                 self.fpdPower = self.fpdPower + chip.p
            elif chip.domain == P_TYPE.PD_LOW:
                 self.lpdReport = self.lpdReport + str
                 self.lpdPower = self.lpdPower + chip.p
            elif chip.domain == P_TYPE.PD_PROGRAMMABLE_LOGIC:
                 if chip.name == "DAC_AVTT":
                      self.pldReport = self.pldReport + "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Analog Rails</FONT></td>"
                 self.pldPower = self.pldPower + chip.p
                 self.pldReport = self.pldReport + str
            self.totalPower = self.totalPower + chip.p


        t = "<FONT color=\"#33ff33\">\n"
        t = t + "<table align=\"center\">\n"
        t = t + "<tr>\n"
        #t = t + "<td width=\"140\"></td>\n"
        #t = t + "<td width=\"200\"></td>\n"
        #t = t + "<td width=\"150\"></td>\n"
        #t = t + "<td width=\"150\"></td>\n"
        #t = t + "<td width=\"150\"></td>\n"
        #t = t + "<td width=\"250\"></td>\n"

        t = t + "<td width=\"140\"></td>\n"
        t = t + "<td width=\"200\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"250\"></td>\n"

        #t = t + "<td width=\"70\"></td>\n"
        #t = t + "<td width=\"100\"></td>\n"
        #t = t + "<td width=\"75\"></td>\n"
        #t = t + "<td width=\"75\"></td>\n"
        #t = t + "<td width=\"75\"></td>\n"
        #t = t + "<td width=\"125\"></td>\n"
        t = t + "</tr>\n"

        units = "<td align=\"right\" valign=\"bottom\">Voltage (V)</td><td align=\"right\" valign=\"bottom\">Current (mA)</td><td align=\"right\" valign=\"bottom\">Power (mW)</td>";

        t = t + "<FONT color=\"#0000ff\">\n"
        s = "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">PS Temperature {0:3.1f}°</FONT></td>".format(float(self.psTemp))
        t = t + s;
        s = "</tr>\n"
        s = "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Full Power Domain</FONT></td>"
        t = t + s;
        t = t + units
        s = "<td align=\"right\"><H3><FONT color=\"#0080ff\" size=\"5\">{0:3.1f} mW</FONT></H3></td></tr>\n".format(self.fpdPower / 1000)
        t = t + s;
        t = t + self.fpdReport
        t = t + "<tr></tr>"
        s = "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Low Power Domain</FONT></td>"
        t = t + s
        t = t +units
        s = "<td align=\"right\"><H3><FONT color=\"#0080ff\" size=\"5\">{0:03.1f} mW</FONT></H3></td></tr>\n".format(self.lpdPower / 1000)
        t = t + s
#          textBuffer.append("<FONT color=\"#33ff33\">\n");
        t = t + self.lpdReport
        t = t + "<tr></tr>"
        t = t + "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Prog Logic Domain</FONT></td>"
        t = t + units
        s = "<td align=\"right\"><H3><FONT color=\"#0080ff\" size=\"5\">{0:03.1f} mW</FONT></H3></td></tr>\n".format(self.pldPower / 1000)
        t = t + s
        t = t + self.pldReport
        t = t + "<tr></tr>"
        s = "<tr><td colspan=\"5\"><H3><FONT color=\"#0080ff\" size=\"5\">Total</FONT></H3></td><td align=\"right\"><H3><FONT color=\"#0080ff\" size=\"5\">{0:03.1f} mW</FONT></H3></td></tr>\n".format(self.totalPower / 1000)
        t = t + s
        t = t + "<FONT color=\"#0080ff\">\n"
        t = t + "</table>"
        return (t)

    def PullSysmonData(self, sysmon):
        for sm in self.sysmon:
            ret, value = sysmon.XSysmon_ReadValue(sm.idStr)
            sm.vAdc = value;
            if sm.name == "PS Temperature":
                 self.psTemp = value

    def PullData(self, i2c, sysmon):
         thread1 = threading.Thread(target=self.PullINA226Data, args=(i2c,))
         thread2 = threading.Thread(target=self.PullSysmonData, args=(sysmon,))
         thread1.start()
         thread2.start()
         thread1.join()
         thread2.join()



    def generateFullSysmonReport(self):
        self.fpdReport = ""
        self.lpdReport = ""
        t = ""
        for sm in self.sysmon:
            str = "<tr><td></td><td>{}</td><td align=\"right\">{:1.3f}</td></tr>\n".format(sm.name, sm.vAdc)
            if sm.domain == P_TYPE.PD_FULL:
                 self.fpdReport = self.fpdReport + str
            elif sm.domain == P_TYPE.PD_LOW:
                 self.lpdReport = self.lpdReport + str

        t = t + "<FONT color=\"#33ff33\">\n"
        t = t + "<table align=\"center\">\n"
        t = t + "<tr>\n"
#        t = t + "<td width=\"70\"></td>\n"
#        t = t + "<td width=\"100\"></td>\n"
#        t = t + "<td width=\"75\"></td>\n"
#        t = t + "<td width=\"75\"></td>\n"
#        t = t + "<td width=\"75\"></td>\n"
#        t = t + "<td width=\"125\"></td>\n"
#        t = t + "<td width=\"5\"></td>\n"

        t = t + "<td width=\"140\"></td>\n"
        t = t + "<td width=\"200\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"150\"></td>\n"
        t = t + "<td width=\"250\"></td>\n"

        t = t + "</tr>\n"
        units = "<td align=\"right\" valign=\"bottom\">Voltage (V)</td>"

        t = t + "<FONT color=\"#33ff33\">\n"
        s = "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">PS Temperature {:03.1f}°</FONT></td>".format(self.psTemp)
        t = t + s
        s = "</tr>\n"
        s = s + "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Full Power Domain</FONT></td>"
        t = t + s
        t = t + units
        s = "</tr>\n"
        t = t + s
        t = t + self.fpdReport
        t = t + "<tr></tr>"
        s = "<tr><td colspan=\"2\"><FONT color=\"#0080ff\" size=\"5\">Low Power Domain</FONT></td>"
        t = t + s
        t = t + units
        s = "</tr>\n"
        t = t + s
        t = t + self.lpdReport
        t = t + "<tr></tr>"
        t = t + "<FONT color=\"#33ff33\">\n"
        t = t + "</table>"
        return(t)

pat = PAT20()
if __name__ == "__main__" :
    i2c.SetIpAndPort("192.168.1.15", 9090)
    i2c.XI2c_Initialize(2)
    ina216.PullINA226Data(i2c)
    str = ina216.generateReport()
