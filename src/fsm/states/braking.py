from transitions import State

class Braking(State):
    def __init__(self, name='braking'):
        super().__init__(name=name)

    def enter(self):
        print("Entering braking state")
        # logic for enter

    def run(self):
        print("Running braking state")
        # logic for run

    def exit(self):
        print("Exiting braking state")
        # logic for exit