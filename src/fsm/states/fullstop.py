from transitions import State

from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_IDLE = 'to_idle'


class FullStop(State):
    def __init__(self, name='fullstop'):
        super().__init__(name=name)

    def enter(self):
        print("Entering fullstop state")
        # logic for enter

    def run(self, input_data):
        print("Running fullstop state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.fault_condition):
            return ValidTransitions.FAULT
        if(input_data.disarm_button_pressed and input_data.primary_brakes_disengaged and input_data.secondary_brakes_disengaged):   
            return ValidTransitions.TO_IDLE
        return ''

    def exit(self):
        print("Exiting fullstop state")
        # logic for exit