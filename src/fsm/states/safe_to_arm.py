from transitions import State
from enum import Enum
from src.constants import FSMConstants

class ValidTransitions(Enum):
    ABORT = 'abort'
    ARM_BUTTON_PRESSED = 'arm_button_pressed'
    FAULT = 'fault'


class SafeToArm(State):
    def __init__(self, name='safe_to_arm'):
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering safe_to_arm state")
        # logic for enter

    def run(self, input_data):
        print("Running safe_to_arm state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.arm_button_pressed):
            return (ValidTransitions.ARM_BUTTON_PRESSED, False, False, False, 'Transitioning to: armed')
        if(input_data.fault_condition):
            return (ValidTransitions.FAULT, False, False, False, 'Transitioning to: idle')
        

        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        
        return ('', False, False, False, 'safe_to_arm')

    def exit(self):
        print("Exiting safe_to_arm state")
        # logic for exit