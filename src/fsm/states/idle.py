from transitions import State
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    SAFETY_BUTTON = 'safety_button'


class Idle(State):
    def __init__(self, name='idle'):
        super().__init__(name=name)

    def enter(self):
        print("Entering idle state")
        # logic for enter

    def run(self, input_data):
        print("Running idle state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.safety_checks_button_pressed):
            return  ValidTransitions.SAFETY_BUTTON
        return ''
        
        

    def exit(self):
        print("Exiting idle state")
        # logic for exit