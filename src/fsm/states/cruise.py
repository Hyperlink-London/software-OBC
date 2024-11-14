from transitions import State

class Cruise(State):
    def __init__(self, name='cruise'):
        super().__init__(name=name)

    def enter(self):
        print("Entering cruise state")
        # logic for enter

    def run(self):
        print("Running cruise state")
        # logic for run

    def exit(self):
        print("Exiting cruise state")
        # logic for exit