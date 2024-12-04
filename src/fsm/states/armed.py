from transitions import State
from enum import Enum
from src.constants import FSMConstants

class ValidTransitions(Enum):
    ABORT = 'abort'
    FAULT = 'fault'
    ARM_BUTTON_RELEASED = 'arm_button_released'
    LAUNCH_BUTTON = 'launch_button'


class Armed(State):
    def __init__(self, name='armed'):
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering armed state")
        # logic for enter

    def run(self, input_data):
        print("Running armed state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.fault_condition):
            return (ValidTransitions.FAULT, False, False, False, 'Transitioning to: idle')
        if(input_data.arm_button_released):
            return (ValidTransitions.ARM_BUTTON_RELEASED, False, False, False, 'Transitioning to: safe_to_arm')
        if(input_data.launch_button_pressed):
            return (ValidTransitions.LAUNCH_BUTTON, False, False, False, 'Transitioning to: acceleration')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        return ('', False, False, False, 'armed')
        

    def exit(self):
        print("Exiting armed state")
        # logic for exit