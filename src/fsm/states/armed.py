from transitions import State
from enum import Enum

class ValidTransition(Enum):
    ABORT = 'abort'
    FAULT = 'fault'
    ARM_BUTTON_RELEASED = 'arm_button_released'
    LAUNCH_BUTTON = 'launch_button'


class Armed(State):
    def __init__(self, name='armed'):
        super().__init__(name=name)

    def enter(self):
        print("Entering armed state")
        # logic for enter

    def run(self, input_data):
        print("Running armed state")
        if(input_data.abort_button_pressed):
            return ValidTransition.ABORT
        if(input_data.fault_condition):
            return ValidTransition.FAULT
        if(input_data.arm_button_released):
            return ValidTransition.ARM_BUTTON_RELEASED
        if(input_data.launch_button_pressed):
            return ValidTransition.LAUNCH_BUTTON
        return ''
        

    def exit(self):
        print("Exiting armed state")
        # logic for exit