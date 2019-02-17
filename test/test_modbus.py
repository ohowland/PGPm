import logging
import unittest

from PGPm import config
from PGPm.poller import ModbusPoller
from PGPm.targets import PowerWind

from pathlib import Path
from configparser import ConfigParser

class TestPGPmModbus(unittest.TestCase):

    

    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.REMOTE_TARGET = True # Set this flag for live testing

        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        logging.debug('Loading bootstrap configuration: {}'.format(bootstrap_path.as_posix()))
        bootstrap_parser = ConfigParser()
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        pass

    def test_read(self):
        if self.REMOTE_TARGET:
            logging.debug('bootstrap.ini sections: {}'.format(self.bootstrap.sections()))
            poller = ModbusPoller(self.bootstrap['COMM'])
            target = PowerWind()
            logging.debug('target registers: {}'.format(target.comm.registers))

            response = poller.read(target.comm.registers)
            self.assertEqual(response, {'alarm_word': 2, 'status_word': 4})


        else:
            pass

if __name__ == '__main__':
    unittest.main()