""" Name: email.py
    Author: Howl & Edgerton, llc 2019
    About: Email configuration and sending routines
"""

import smtplib
import ssl
import logging
import os

from configparser import ConfigParser
from collections import namedtuple
from datetime import datetime

email_config = namedtuple(
    'email_config', 'smtp_port smtp_server recipient_list username password')


class Emailer(object):
    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.recipient_list = [x.strip()
                               for x in config['recipient_list'].split(',')]
        self.smtp_port = int(config['port'])
        self.smtp_server = config['smtp_server']
        self.update_rate = int(config['update_rate'])
        self.site = config['site_name']
        self.timeout = int(config['timeout'])
            
        self.sent_timestamp = datetime.fromordinal(1)
    

    def send(self, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, self.recipient_list, message)

    def build_message(self, alarms):
        message = 'Subject: Alarm: {}\n\n'.format(self.site)
        for alarm in alarms:
            message += alarm

        print('message: {}'.format(message))
        return message

    def check_events(self):
        if (datetime.now() - self.sent_timestamp).total_seconds() > self.timeout:
            self.get_new_events()
        else:
            pass

    def get_new_events(self):
        alarms = []

        try:
            with open('events/alarms.txt', 'r+') as file:
                alarms = file.readlines()
        except:
            logging.warning('failed to read events')
            if not os.path.exists('events/alarms.txt'):
                open('events/alarms.txt', 'w+').close()

        logging.debug("ALARMS: {}".format(alarms))
        if alarms:
            try:
                open('events/alarms.txt', 'w').close()
                message = self.build_message(alarms)
                logging.debug('Sending email:\n {}'.format(message))
                self.send(message)
                self.sent_timestamp = datetime.now()
            except Exception as e:
                logging.warning('failed to send email, {}'.format(e))
