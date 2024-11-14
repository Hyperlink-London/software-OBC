from transitions import State

class Acceleration(State):
    def __init__(self, name='acceleration'):
        super().__init__(name=name)

    def enter(self):
        print("Entering acceleration state")
        # logic for enter

    def run(self):
        print("Running acceleration state")
        # logic for run

    def exit(self):
        print("Exiting acceleration state")
        # logic for exit
