""" Name: target.py
    Author: Howl & Edgerton, llc 2019
    About: targets for alarming program
"""

import logging

from poller import Modbus

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
        super().__init__()
        self._comm = PowerWindComm()
        self._active_alarm_level = 0
        self._active_brake_level = 0

    @property
    def comm(self):
        return self._comm

    @property
    def active_alarm_level(self):
        return self._active_alarm_level

    @active_alarm_level.setter
    def active_alarm_level(self, value):
        self._active_alarm_level = value

    @property
    def active_brake_level(self):
        return self._active_brake_level

    @active_brake_level.setter
    def active_brake_level(self, value):
        self._active_brake_level = value

    def update_from(self, polled_data):
        for key, val in polled_data.items():
            setattr(self, "_" + key, val)

        self._alarm = self.active_alarm_level > 0 or self.active_brake_level > 40


class PowerWindComm(object):

    def __init__(self):
        #register = namedtuple('modbus_register', 'name, address, type, function_code')
        self.registers = [
            Modbus.register('active_alarm_level', 0, 'U16', 0x03),
            Modbus.register('active_brake_level', 1, 'U16', 0x03),
        ]
