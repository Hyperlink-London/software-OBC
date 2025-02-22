from transitions import State
from enum import Enum

class ValidTransitions(Enum):
    STOPPED_AND_ABORT_RELEASED = 'stopped_and_abort_released'
    STAY = 'stay'

class SafeAbort(State):
    def __init__(self, name='safe_abort'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safe_abort state")
        # logic for enter

    def run(self, input_data):
        print("Running safe_abort state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)

    


        if(input_data.speed_m_per_s == 0 and input_data.abort_button_pressed == False ):
            return (ValidTransitions.STOPPED_AND_ABORT_RELEASED, False, False, False, 'Transitioning to: full_stop')
        return (ValidTransitions.STAY, False, False, False, 'safe_abort')

    def exit(self):
        print("Exiting safe_abort state")
        # logic for exit