from transitions import State
from enum import Enum
from src.constants import FSMConstants


class ValidTransitions(Enum):
    ABORT = 'abort'
    FAULT = 'fault'
    TOP_SPEED_REACHED = 'top_speed_reached'
    WAYPOINT_REACHED = 'waypoint_reached'
    STAY = 'stay'


class Acceleration(State):
    def __init__(self, name='acceleration'):
        self.top_speed = FSMConstants.MAX_SPEED
        self.waypoint_distance = FSMConstants.WAYPOINT_DISTANCE
        self.max_temp_propulsion = FSMConstants.MAX_TEMP_PROPULSION
        self.max_temp_braking = FSMConstants.MAX_TEMP_BRAKING
        self.max_rpm = FSMConstants.MAX_RPM
        self.max_speed = FSMConstants.MAX_SPEED
        super().__init__(name=name)

    def enter(self, input_data):
        print("Entering acceleration state")
        

    def run(self, input_data):
        print("Running acceleration state")
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        if(input_data.abort_button_pressed):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort') # Todo: do we brake or just abort everything?
        if(input_data.fault_condition):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort') # FAULT is the same as ABORT in this transition
        if(input_data.speed_m_per_s >= self.max_speed):
            return (ValidTransitions.TOP_SPEED_REACHED, False, False, True, 'Transitioning to: primary_braking')
        if(input_data.distance >= self.waypoint_distance): # not actually a constant right now
            return (ValidTransitions.WAYPOINT_REACHED, False, False, True, 'Transitioning to: primary_braking')
        
        # Constant Temperature + RPM Checks
        if(input_data.temperature_celsius_propulsion_1 >= self.max_temp_propulsion or input_data.temperature_celsius_propulsion_2 >= self.max_temp_propulsion):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.temperature_celsius_brake >= self.max_temp_braking):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')
        if(input_data.rpm >= self.max_rpm):
            return (ValidTransitions.ABORT, False, False, False, 'Transitioning to: abort')


        return (ValidTransitions.STAY, False, False, True, 'acceleration')

    def exit(self):
        print("Exiting acceleration state")
        # logic for exit
