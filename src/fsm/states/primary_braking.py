from transitions import State
from src.constants import FSMConstants
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    TO_SECONDARY_BRAKING = 'to_secondary_braking'


class PrimaryBraking(State):
    def __init__(self, name='braking'):
        super().__init__(name=name)

    def enter(self):
        print("Entering braking state")
        # logic for enter

    def run(self, input_data):
        print("Running braking state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.fault_condition):
            return ValidTransitions.FAULT
        if(input_data.speed_m_per_s <= FSMConstants.SECONDARY_BRAKING_SPEED):
            return ValidTransitions.TO_SECONDARY_BRAKING
        return ''

    def exit(self):
        print("Exiting braking state")
        # logic for exit