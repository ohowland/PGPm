import logging
import unittest

from pathlib import Path
from configparser import ConfigParser
from PGPm.lib import modbus, config
from collections import namedtuple

class TestPGPmModbus(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        bootstrap_path = config.get('boostrap.ini')
        logging.debug('Loading bootstrap configuration: {}'.format(bootstrap_path.as_posix()))
        bootstrap_parser = ConfigParser()
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        pass


if __name__ == '__main__':
    unittest.main()