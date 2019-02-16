""" Name: test_email.py
    Author: Howl & Edgerton, llc 2019
    About: Unit tests for email fuctions
"""

import logging
import unittest

from PGPm.lib import config
from PGPm.lib.email import Email

from pathlib import Path
from configparser import ConfigParser

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
        emailer = Email(self.bootstrap['EMAIL'])

        self.assertEqual(emailer.smtp_port, 465)
        self.assertEqual(emailer.smtp_server, 'smtp.gmail.com')
        self.assertEqual(emailer.username, 'support@howlandedgerton.com')
        self.assertEqual(emailer.password, 'gH417xd^t!K5')
        self.assertEqual(emailer.recipient_list, ['support@howlandedgerton.com', 'owen@howlandedgerton.com'])

if __name__ == '__main__':
    unittest.main()