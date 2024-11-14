from transitions import State

class Idle(State):
    def __init__(self, name='idle'):
        super().__init__(name=name)

    def enter(self):
        print("Entering idle state")
        # logic for enter

    def run(self):
        print("Running idle state")
        # logic for run

    def exit(self):
        print("Exiting idle state")
        # logic for exit