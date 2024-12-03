from transitions import State
from src.constants import FSMConstants
from enum import Enum
from src.constants import FSMConstants


class ValidTransitions(Enum):
    ABORT = 'abort'
    WAYPOINT_REACHED = 'waypoint_reached'

class Cruise(State):
    def __init__(self, name='cruise'):
        self.waypoint_distance = FSMConstants.WAYPOINT_DISTANCE
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        super().__init__(name=name)

    def enter(self):
        print("Entering cruise state")
        # logic for enter

    def run(self, input_data):
        print("Running cruise state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.fault_condition):
            return (ValidTransitions.FAULT, False, False, False, 'Transitioning to: abort')
        if(input_data.distance >= self.waypoint_distance):
            return (ValidTransitions.WAYPOINT_REACHED, True, False, False, 'Transitioning to: waypoint_reached')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')

        return ('', False, False, True, 'cruise') # Todo: implement to maintain cruise speed

    def exit(self):
        print("Exiting cruise state")
        # logic for exit