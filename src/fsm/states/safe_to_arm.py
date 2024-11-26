from transitions import State
from enum import Enum

class ValidTransitions(Enum):
    ABORT = 'abort'
    ARM_BUTTON_PRESSED = 'arm_button_pressed'
    FAULT = 'fault'


class SafeToArm(State):
    def __init__(self, name='safe_to_arm'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safe_to_arm state")
        # logic for enter

    def run(self, input_data):
        print("Running safe_to_arm state")
        if(input_data.abort_button_pressed):
            return ValidTransitions.ABORT
        if(input_data.arm_button_pressed):
            return ValidTransitions.ARM_BUTTON_PRESSED
        if(input_data.fault_condition):
            return ValidTransitions.FAULT
        return ''

    def exit(self):
        print("Exiting safe_to_arm state")
        # logic for exit