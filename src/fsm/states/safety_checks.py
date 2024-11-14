from transitions import State

class SafetyChecks(State):
    def __init__(self, name='safety_checks'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safety_checks state")
        # logic for enter

    def run(self):
        print("Running safety_checks state")
        # logic for run

    def exit(self):
        print("Exiting safety_checks state")
        # logic for exit