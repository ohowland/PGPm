""" Name: pgpm.py
    Author: Howl & Edgerton, llc 2019
    About: PowerWind alarm and status emailing program.
"""

import asyncio
import os
import email
import logging

from comm import Modbus
from statemachine import PGPmStatemachine
from targets import PowerWind
from email import Email

from datetime import datetime
from configparser import ConfigParser
from datetime import datetime
from collections import namedtuple


async def state_machine_loop(statemachine, target):
    """ The state machine tracks the current software state: NoAlarm and Alarm.
    """
    
    while True:
        logging.debug('Current State: {}'.format(statemachine.current_state))

        statemachine.run(target)

        await asyncio.sleep(statemachine.update_rate)
        

async def poll_target(poller, target):
    """ The update loop continiously polls configured objects
        and pipes new alarms to the email loop.
    """

    while True:
        logging.debug('Polling Target @ {}'.format(datetime.now().time))

        response = poller.read(target.comm.registers)
        target.update_from(response)

        await asyncio.sleep(poller.update_rate)

async def email_loop(emailer):
    """ The email loop reads alarm file and dispatches alarm emails
    """

    while True:
        await asyncio.sleep(emailer.update_rate)

def main(*args, **kwargs):
    """ Read configuration and launch three async loops: 
        polling, emailing, and state machine.
    """

    boostrap_config = kwargs['bootstrap']
    emailer = Email(boostrap_config['EMAIL'])
    poller = Modbus(boostrap_config['COMM'])
    statemachine = PGPmStatemachine(boostrap_config['STATEMACHINE'])
    
    """ target is shared between statemachine and poller.
        poller updates target, statemachine reads target.
    """
    target = PowerWind()

    loop = asyncio.get_event_loop()
    loop.create_task(poll_target(poller, target))
    loop.create_task(email_loop(emailer))
    loop.create_task(state_machine_loop(statemachine, target))

    try:
        loop.run_forever()
    except:
        loop.close()