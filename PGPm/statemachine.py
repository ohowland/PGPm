""" Name: statemachine.py
    Author: Howl & Edgerton, llc 2019
    About: Statemachine for alarming program
"""

class State(object):
    def __init__(self):
        pass

    def check_transitions(self, state, target):
        pass

    def actions(self, state, target):
        pass


class NoAlarmState(State):
    def __init__(self):
        super().__init__()

    def check_transitions(self, target):
        if target.alarm == True:
            return AlarmState()
        else: 
            self

    def actions(self, target):
        pass


class AlarmState(State):
    def __init__(self):
        super().__init__()

    def check_transitions(self, target):
        if target.alarm == False:
            return NoAlarmState()
        else: 
            self

    def actions(self, target):
        pass


class Statemachine(object):
    def __init__(self, config):
        self.current_state = None
        self.update_rate = int(config['update_rate'])

    def run(self, target):
        self.current_state.check_transitions(target)
        self.current_state.actions(target)


class PGPmStatemachine(Statemachine):
    def __init__(self, config):
        super().__init__(config)
        self.current_state = NoAlarmState()
