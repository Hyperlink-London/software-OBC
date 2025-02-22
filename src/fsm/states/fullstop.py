from transitions import State
from enum import Enum
from src.constants import FSMConstants

class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_IDLE = 'to_idle'
    STAY = 'stay'

class FullStop(State):
    def __init__(self, name='fullstop'):
        self.top_speed = FSMConstants.MAX_SPEED
        self.waypoint_distance = FSMConstants.WAYPOINT_DISTANCE
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        self.max_speed = FSMConstants.MAX_SPEED
        super().__init__(name=name)

    def enter(self):
        print("Entering fullstop state")
        # logic for enter

    def run(self, input_data):
        print("Running fullstop state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)

        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')

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