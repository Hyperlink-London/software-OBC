from transitions import State

class FullStop(State):
    def __init__(self, name='fullstop'):
        super().__init__(name=name)

    def enter(self):
        print("Entering fullstop state")
        # logic for enter

    def run(self):
        print("Running fullstop state")
        # logic for run

    def exit(self):
        print("Exiting fullstop state")
        # logic for exit