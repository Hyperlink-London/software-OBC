from transitions import State

class SecondaryBrake(State):
    def __init__(self, name='secondary_brake'):
        super().__init__(name=name)

    def enter(self):
        print("Entering secondary_brake state")
        # logic for enter

    def run(self):
        print("Running secondary_brake state")
        # logic for run

    def exit(self):
        print("Exiting secondary_brake state")
        # logic for exit