from transitions import State

class SafeAbort(State):
    def __init__(self, name='safe_abort'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safe_abort state")
        # logic for enter

    def run(self):
        print("Running safe_abort state")
        # logic for run

    def exit(self):
        print("Exiting safe_abort state")
        # logic for exit