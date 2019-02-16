import logging

from PGPm.lib import comm

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

    def update_status(self):
        self.alarm = self.alarm_word > 0

class PowerWindComm(object):
    
    def __init__(self):
        self.registers = [
            comm.register('alarm_word', 1, 1, 0x03)
        ]

    def read(self, config):
        comm.read(config, self.registers)