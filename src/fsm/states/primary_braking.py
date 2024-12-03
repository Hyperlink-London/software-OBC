from transitions import State
from src.constants import FSMConstants
from enum import Enum
from src.constants import FSMConstants
class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_SECONDARY_BRAKING = 'to_secondary_braking'


class PrimaryBraking(State):
    def __init__(self, name='braking'):
        self.secondary_braking_speed = FSMConstants.SECONDARY_BREAKING_SPEED
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering braking state")
        # logic for enter

    def run(self, input_data):
        print("Running braking state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.fault_condition):
            return (ValidTransitions.FAULT, False, False, False, 'Transitioning to: abort')
        if(input_data.speed_m_per_s <= self.secondary_braking_speed):
            return (ValidTransitions.TO_SECONDARY_BRAKING, False, True, False, 'Transitioning to: secondary_braking')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        
        return ('', True, False, False, 'braking')

    def exit(self):
        print("Exiting braking state")
        # logic for exit