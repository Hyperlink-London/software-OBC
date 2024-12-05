from transitions import State
from src.constants import FSMConstants
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_FULL_STOP = 'to_full_stop'
    STAY = 'stay'


class SecondaryBrake(State):
    def __init__(self, name='secondary_brake'):
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering secondary_brake state")
        # logic for enter

    def run(self, input_data):
        print("Running secondary_brake state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.fault_condition):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.speed_m_per_s == 0): # to consider: edge case speed < 0??  
            return (ValidTransitions.TO_FULL_STOP, False, False, False, 'Transitioning to: full_stop')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        return (ValidTransitions.STAY, False, True, False, 'secondary_brake')

    def exit(self):
        print("Exiting secondary_brake state")
        # logic for exit