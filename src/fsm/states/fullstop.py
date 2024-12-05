from transitions import State
from enum import Enum
class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_IDLE = 'to_idle'
    STAY = 'stay'

class FullStop(State):
    def __init__(self, name='fullstop'):
        super().__init__(name=name)

    def enter(self):
        print("Entering fullstop state")
        # logic for enter

    def run(self, input_data):
        print("Running fullstop state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.fault_condition):
            return (ValidTransitions.FAULT, False, False, False, 'Transitioning to: abort')
        if(input_data.disarm_button_pressed and input_data.primary_brakes_on == False and input_data.secondary_brakes_on == False):   
            return (ValidTransitions.TO_IDLE, False, False, False, 'Transitioning to: idle')
        return (ValidTransitions.STAY, False, False, False, 'fullstop')

    def exit(self):
        print("Exiting fullstop state")
        # logic for exit