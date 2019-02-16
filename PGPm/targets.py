""" Name: target.py
    Author: Howl & Edgerton, llc 2019
    About: targets for alarming program
"""

import logging

from PGPm.comm import Modbus

class WindTurbine(object):
    def __init__(self):
        self._alarm = False

    @property
    def alarm(self):
        return self._alarm

    def update_status(self):
        pass

class PowerWind(WindTurbine):
    def __init__(self):
        self._comm = PowerWindComm()
        self._alarm_word = 0

    @property
    def comm(self):
        return self._comm

    @property
    def alarm_word(self):
        return self._alarm_word

    @alarm_word.setter
    def alarm_word(self, value):
        self._alarm_word = value

    def update_from(self, polled_data):
        for key, val in polled_data:
            setattr(self, "_" + key, val)

        self.alarm = self.alarm_word > 0

class PowerWindComm(object):
    
    def __init__(self):
        #register = namedtuple('modbus_register', 'name, address, type, function_code')
        self.registers = [
            Modbus.register('alarm_word' , 1, 'U16', 0x03),
            Modbus.register('status_word', 3, 'U16', 0x03),
        ]