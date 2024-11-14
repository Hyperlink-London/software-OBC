from transitions import State

class EmergencyStop(State):
    def __init__(self, name='emergency_stop'):
        super().__init__(name=name)

    def enter(self):
        print("Entering emergency_stop state")
        # logic for enter

    def run(self):
        print("Running emergency_stop state")
        # logic for run

    def exit(self):
        print("Exiting emergency_stop state")
        # logic for exit