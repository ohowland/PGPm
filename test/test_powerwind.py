import logging
import unittest

from PGPm.lib.targets import PowerWind

class TestPGPmPowerWind(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    def tearDown(self):
        pass

    def test_factory(self):
        pw = PowerWind()

if __name__ == '__main__':
    unittest.main()