# Copyright (C) 2023 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Salih Erim"
__copyright__ = "Copyright 2023, Advanced Micro Devices, Inc."

import os
import platform
import sys
import json
import subprocess

print(platform.machine())

if platform.machine() == 'x86_64':
    RAFT_DIR = '/usr/share/raft/'
else:
    RAFT_DIR = os.environ['RAFT_DIR']

sys.path.append(RAFT_DIR + 'xserver/utils')
#sys.path.append(os.environ['RAFT_DIR'] + 'xserver/utils')
import logging
from pmic import PMIC
from utils import get_python_log_levels


class Supply:
    def __init__(self, name, device, device_type, shunt_resistor, addr, domain_tag):
        self.name = name
        self.device = device
        self.device_type = device_type
        self.addr = addr
        self.domain_tag = domain_tag
        self.shunt_resistor = shunt_resistor

    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['device', 'addr', 'shunt_resistor', 'device_type','domain_tag'] and v
        }
        return str(str_info)
    pass
class Domain:
    def __init__(self, name, description, tag):
        self.name = name
        self.description = description
        self.tag = tag
        self.supplies = []
        self.temperatures = []

   # def __str__(self):
    #    return "{0} {1} {2}".format(self.name, self.description, self.tag)
    
    def __str__(self):
        str_info = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ['supplies', 'temperatures'] and v
        }
        return str(str_info)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    #def __repr__(self):
    #    return f'Domain(\'{self.name}\', {self.description})'

    #def AddSupply(self, supply):
    #   self.supplies.append(supply)

    #def GetSupplies(self):
    #    return self.suplies
        
class PM(object):
    device_id = 0
    logger = None
    domain_list = []
    pmic = None
    

    def __init__(self, json_data):
        self.logger = self.GetLogger()

        #json_formatted_str = json.dumps(json_data, indent=2)
        #self.logger.info(json_formatted_str)
        
        domains = json_data['domains']
        #print(domains)
        for d in domains:
            self.domain_list.append(Domain(**d)) 
            #print(d)

        supplies = json_data['supplies']
        print(supplies)
        for s in supplies:
            supply = Supply(**s)
            for index, domain in enumerate(self.domain_list):
                if supply.domain_tag == domain.tag:
                    self.domain_list[index].supplies.append(supply)
                    print(self.domain_list[index])
                    for p in self.domain_list[index].supplies:
                        print(p)

        ret, self.pmic = self.InitPMIC(supplies)
        if ret != True:
            self.logger.error(f"PM: InitBoardInfo failed. ret = {ret}")
        self.logger.info("Inside PM Constructor")
        pass
    
    @staticmethod
    def InitPMIC(supplies):
        ret = True
        pmic = PMIC(supplies)

        #logger = logging.getLogger(__name__)
        #try:
        #    handler_set_check = getattr(logger, 'handler_set')
        #except AttributeError:
        #    handler_set_check = False
        #if not handler_set_check:
        #    logger.setLevel(log_level)
        #    logger.handler_set = True
        #    logger.disabled = False
        return ret, pmic

    @staticmethod
    def GetLogger():
        """
        Static method to get the logger for the class.
        Default loglevel is set inside this class

        :return: logger

        """
        log_level = logging.INFO
        logging.basicConfig(format="%(levelname)s:%(message)s")
        logger = logging.getLogger(__name__)
        try:
            handler_set_check = getattr(logger, 'handler_set')
        except AttributeError:
            handler_set_check = False
        if not handler_set_check:
            logger.setLevel(log_level)
            logger.handler_set = True
            logger.disabled = False
        return logger

    # Log level
    def GetPythonLogLevels(self):
        """
        Return the logging levels supported by logging library in python

        :param : None
        :return: Dictionary showing the log levels supported by logging library
        """
        return get_python_log_levels()

    def SetServerLogLevel(self, PythonLogLevel):
        """
        Set the python log level to the given level

        :param : Log level to set
        :return: None
        """
        self.logger.debug(f"PythonLogLevel = {PythonLogLevel}")
        LogLevelsDict = get_python_log_levels()
        if PythonLogLevel == LogLevelsDict["DEBUG"]:
            self.logger.setLevel(logging.DEBUG)
        elif PythonLogLevel == LogLevelsDict["INFO"]:
            self.logger.setLevel(logging.INFO)
        elif PythonLogLevel == LogLevelsDict["WARNING"]:
            self.logger.setLevel(logging.WARNING)
        elif PythonLogLevel == LogLevelsDict["ERROR"]:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.CRITICAL)
        return

    def GetBoardInfo(self):
        return 
    
    def GetPowerDomains(self):
        powerdomains = []
        for d in self.domain_list:
            #print(str(d))
            powerdomains.append(str(d))
        #jsonStr = json.dumps(self.domain_list.__dict__)
        #json_string = json.dumps([domain.__dict__ for domain in self.domain_list])
        return powerdomains

    def GetSuppliesOfDomain(self, tag):
        print(tag)
        lst = []
        for d in self.domain_list:
            if d.tag == tag:
               for s in d.supplies:
                lst.append(str(s))
        #jsonStr = json.dumps(self.domain_list.__dict__)
        #json_string = json.dumps([domain.__dict__ for domain in self.domain_list])
        return lst
    
    def GetSupplyDetails(self, supplyname):
        lst = []
        for d in self.domain_list:
            for s in d.supplies:
                if supplyname == s.name:
                   lst.append(str(s))
        return lst
    
    @staticmethod
    def ReadSupplyValues(supply):
        val = None
        if (sensor := self.pmic.GetSensor(supply.tag, supply.name)) is not None:
            val = self.pmic.GetSensorValues(sensor)
        return val

    def GetValuesofSuply(self, tag, supplyname):
        val = None
        for s in self.domain_list:
            if s.tag == tag and s.name == supplyname:
                val = ReadSupplyValues(s)
        return val

    def GetValuesAll(self):
        val = []
        for s in self.domain_list:
            val.append(self.ReadSupplyValues(supply))
        print(vars(val))
        return val
    """
    def RaftConsole(self, str_cmd):
        
        API console command.

        :param : string as a "cat" command argument 
        :return: outStr output from cat command
        
        self.logger.debug(f"execute: " + str_cmd)
        ret = subprocess.getstatusoutput(str_cmd)
        status = ret[0]
        str_cmd_ret = ret[1]
        self.logger.debug(f"return: status: {status}, command output: {str_cmd_ret}")
        return status, str_cmd_ret
    """
    def __del__(self):
        self.logger.info("Inside PM Destructor")
