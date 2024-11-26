from transitions import State
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    SAFETY_PASS = 'safety_pass'
    SAFETY_FAIL = 'safety_fail'


class SafetyChecks(State):
    def __init__(self, name='safety_checks'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safety_checks state")
        # logic for enter

    def run(self, input_data):
        print("Running safety_checks state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.safety_checks_passed == None):
            return ''
        if(input_data.safety_checks_passed == True):
            return ValidTransitions.SAFETY_PASS
        if(input_data.safety_checks_passed == False):
            return ValidTransitions.SAFETY_FAIL


    def exit(self):
        print("Exiting safety_checks state")
        # logic for exit