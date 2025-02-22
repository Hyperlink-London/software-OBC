from transitions import State
from enum import Enum
from src.constants import FSMConstants

class ValidTransitions(Enum):
    ABORT = 'abort'
    SAFETY_BUTTON = 'safety_button'
    STAY = 'stay'


class Idle(State):
    def __init__(self, name='idle'):
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering idle state")
        # logic for enter

    def run(self, input_data):
        print("Running idle state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        if(input_data.safety_checks_button_pressed):
            return  (ValidTransitions.SAFETY_BUTTON, False, False, False, 'Transitioning to: safety_checks')
        

        return (ValidTransitions.STAY, False, False, False, 'idle')
        
        

    def exit(self):
        print("Exiting idle state")
        # logic for exit