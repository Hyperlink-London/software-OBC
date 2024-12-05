from transitions import State
from enum import Enum
from src.constants import FSMConstants

class ValidTransitions(Enum):
    ABORT = 'abort'
    SAFETY_PASS = 'safety_pass'
    SAFETY_FAIL = 'safety_fail'
    STAY = 'stay'


class SafetyChecks(State):
    def __init__(self, name='safety_checks'):
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering safety_checks state")
        # logic for enter

    def run(self, input_data):
        print("Running safety_checks state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.safety_checks_passed == None):
            return (ValidTransitions.STAY, False, False, False, 'safety_checks')
        if(input_data.safety_checks_passed == True):
            return (ValidTransitions.SAFETY_PASS, False, False, False, 'Transitioning to: safe_to_arm')
        if(input_data.safety_checks_passed == False):
            return (ValidTransitions.SAFETY_FAIL, False, False, False, 'Transitioning to: idle')
        

        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        

        return (ValidTransitions.STAY, False, False, False, 'safety_checks')


    def exit(self):
        print("Exiting safety_checks state")
        # logic for exit