from transitions import State
from src.constants import FSMConstants
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_FULL_STOP = 'to_full_stop'


class SecondaryBrake(State):
    def __init__(self, name='secondary_brake'):
        super().__init__(name=name)

    def enter(self):
        print("Entering secondary_brake state")
        # logic for enter

    def run(self, input_data):
        print("Running secondary_brake state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.fault_condition):
            return ValidTransitions.ABORT
        if(input_data.speed_m_per_s == 0): # to consider: edge case speed < 0??  
            return ValidTransitions.TO_FULL_STOP
        return ''

    def exit(self):
        print("Exiting secondary_brake state")
        # logic for exit