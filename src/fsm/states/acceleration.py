from transitions import State
from enum import Enum
from src.constants import FSMConstants


class ValidTransitions(Enum):
    ABORT = 'abort'
    FAULT = 'fault'
    TOP_SPEED_REACHED = 'top_speed_reached'
    WAYPOINT_REACHED = 'waypoint_reached'


class Acceleration(State):
    def __init__(self, name='acceleration'):
        super().__init__(name=name)

    def enter(self, input_data):
        print("Entering acceleration state")
        

    def run(self, input_data):
        print("Running acceleration state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.fault_condition):
            return ValidTransitions.ABORT # FAULT is the same as ABORT in this transition
        if(input_data.speed_m_per_s >= FSMConstants.MAX_SPEED):
            return ValidTransitions.TOP_SPEED_REACHED
        if(input_data.distance >= FSMConstants.WAYPOINT_DISTANCE): # not actually a constant right now
            return ValidTransitions.WAYPOINT_REACHED
        return ''


    def exit(self):
        print("Exiting acceleration state")
        # logic for exit
