""" Name: statemachine.py
    Author: Howl & Edgerton, llc 2019
    About: Statemachine for alarming program
"""

import logging

from datetime import datetime


class State(object):
    def __init__(self, new_state):
        self.new_state = new_state

    def check_transitions(self, state, target):
        pass

    def actions(self, state, target):
        pass


class NoAlarmState(State):
    def __init__(self, new_state=False):
        super().__init__(new_state)

    def __repr__(self):
        return "No Alarm State"

    def check_transitions(self, target):
        if target.alarm == True:
            return AlarmState(new_state=True)
        else:
            return NoAlarmState()

    def actions(self, target):
        pass


class AlarmState(State):
    def __init__(self, new_state=False):
        super().__init__(new_state)

    def __repr__(self):
        return "Alarm State"

    def check_transitions(self, target):
        if target.alarm == False:
            return NoAlarmState(new_state=True)
        else:
            return AlarmState()

    def actions(self, target):
        if self.new_state is True:
            record_alarm(target.active_alarm_level)


class Statemachine(object):
    def __init__(self, config):
        self.current_state = None
        self.update_rate = int(config['update_rate'])

    def run(self, target):
        self.current_state = self.state_transitions(target)
        self.state_actions(target)

    def state_transitions(self, target):
        return self.current_state.check_transitions(target)

    def state_actions(self, target):
        self.current_state.actions(target)


class PGPmStatemachine(Statemachine):
    def __init__(self, config):
        super().__init__(config)
        self.current_state = NoAlarmState()


def record_alarm(active_alarm_level):
    try:
        timestamp = datetime.utcnow()
        with open('events/alarms.txt', 'a+') as file:
            file.write("[{}] Active Alarm Level: {}\n".format(timestamp, active_alarm_level))

    except Exception as e:
        logging.warning(e)
