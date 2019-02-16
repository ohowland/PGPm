from configparser import ConfigParser
from collections import namedtuple

register = namedtuple('modbus_register', 'name, address, size, function_code')

class Modbus(object):
        def __init__(self, configparser):
                pass

        def read(self, registers):
                return {'register_name': 'register_value'}
