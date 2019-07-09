""" Name: pgpm.py
    Author: Howl & Edgerton, llc 2019
    About: PowerWind alarm and status emailing program.
"""

import asyncio
import os
import logging

from statemachine import PGPmStatemachine
from targets import PowerWind
from emailer import Emailer
from poller import ModbusPoller

from datetime import datetime
from configparser import ConfigParser
from datetime import datetime
from collections import namedtuple


async def state_machine_loop(statemachine, target):
    """ The state machine tracks the current software state: NoAlarm and Alarm.
    """

    while True:
        print('Current State: {}'.format(statemachine.current_state))

        statemachine.run(target)

        await asyncio.sleep(statemachine.update_rate)


async def poll_target(poller, target):
    """ The update loop continiously polls configured objects
        and pipes new alarms to the email loop.
    """

    while True:
        print('Polling Target @ {}'.format(datetime.now().time()))

        response = poller.read(target.comm.registers)
        print("response: {}".format(response))
        target.update_from(response)

        await asyncio.sleep(poller.update_rate)


async def email_loop(emailer):
    """ The email loop reads alarm file and dispatches alarm emails
    """

    while True:
        emailer.check_events()
        await asyncio.sleep(emailer.update_rate)


def main(*args, **kwargs):
    """ Read configuration and launch three async loops: 
        polling, emailing, and state machine.
    """

    loop = asyncio.get_event_loop()
    boostrap_config = kwargs['bootstrap']
    turbine_list = [t.strip() for t in boostrap_config['TURBINES']['turbine_list'].split(',')]
    for turbine in turbine_list:
        emailer = Emailer(boostrap_config['EMAIL'])
        poller = ModbusPoller(boostrap_config[turbine + '_COMM'])
        statemachine = PGPmStatemachine(boostrap_config['STATEMACHINE'])

        """ target is shared between statemachine and poller.
            poller updates target, statemachine reads target.
        """
        target = PowerWind()
        loop.create_task(poll_target(poller, target))
        loop.create_task(email_loop(emailer))
        loop.create_task(state_machine_loop(statemachine, target))

    try:
        loop.run_forever()
    except:
        loop.close()
