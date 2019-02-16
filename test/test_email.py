""" Name: test_email.py
    Author: Howl & Edgerton, llc 2019
    About: Unit tests for email fuctions
"""

import logging
import unittest

from pathlib import Path
from configparser import ConfigParser
from PGPm.lib import email, config
from collections import namedtuple

class TestPGPmEmail(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        logging.debug('Loading bootstrap configuration: {}'.format(bootstrap_path.as_posix()))
        bootstrap_parser = ConfigParser()
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        logging.debug('Bootstrap.ini sections: {}'.format(self.bootstrap.sections()))
        email_config = email.configure(self.bootstrap['EMAIL'])

        self.assertEqual(email_config.smtp_port, 465)
        self.assertEqual(email_config.smtp_server, 'smtp.gmail.com')
        self.assertEqual(email_config.username, 'support@howlandedgerton.com')
        self.assertEqual(email_config.password, 'gH417xd^t!K5')
        self.assertEqual(email_config.recipient_list, ['support@howlandedgerton.com', 'owen@howlandedgerton.com'])

if __name__ == '__main__':
    unittest.main()