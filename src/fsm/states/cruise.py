from transitions import State
from src.constants import FSMConstants
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    WAYPOINT_REACHED = 'waypoint_reached'

class Cruise(State):
    def __init__(self, name='cruise'):
        super().__init__(name=name)

    def enter(self):
        print("Entering cruise state")
        # logic for enter

    def run(self, input_data):
        print("Running cruise state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.fault_condition):
            return ValidTransitions.FAULT
        if(input_data.distance >= input_data.waypoint_distance):
            return ValidTransitions.WAYPOINT_REACHED
        return ''

    def exit(self):
        print("Exiting cruise state")
        # logic for exit