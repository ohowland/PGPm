""" Name: comm.py
    Author: Howl & Edgerton, llc 2019
    About: Communications module
"""

from configparser import ConfigParser
from collections import namedtuple


class Modbus(object):
        register = namedtuple('modbus_register', 'name, address, size, function_code')

        def __init__(self, configparser):
                pass

        def read(self, registers):
                """ Returns a dict of register names to register values\
                """
                
                return {'register_name': 'register_value'}
