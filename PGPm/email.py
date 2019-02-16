""" Name: email.py
    Author: Howl & Edgerton, llc 2019
    About: Email configuration and sending routines
"""

import smtplib, ssl, logging

from configparser import ConfigParser
from collections import namedtuple

email_config = namedtuple('email_config', 'smtp_port smtp_server recipient_list username password')

class Email(object):
        def __init__(self, config):
                self.username = config['username']
                self.password = config['password']
                self.recipient_list = [x.strip() for x in config['recipient_list'].split(',')]
                self.smtp_port = int(config['port'])
                self.smtp_server = config['smtp_server']
                self.update_rate = int(config['update_rate'])

        def send(self, message):   
                message = """\
                Subject: Hi there

                This message is sent from Python."""
        
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                        server.login(self.username, self.password)
                        for email in self.recipient_list:
                                server.sendmail(self.username, email, message)