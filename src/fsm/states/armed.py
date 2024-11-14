from transitions import State

class Armed(State):
    def __init__(self, name='armed'):
        super().__init__(name=name)

    def enter(self):
        print("Entering armed state")
        # logic for enter

    def run(self):
        print("Running armed state")
        # logic for run

    def exit(self):
        print("Exiting armed state")
        # logic for exit