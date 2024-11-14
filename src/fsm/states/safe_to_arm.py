from transitions import State

class SafeToArm(State):
    def __init__(self, name='safe_to_arm'):
        super().__init__(name=name)

    def enter(self):
        print("Entering safe_to_arm state")
        # logic for enter

    def run(self):
        print("Running safe_to_arm state")
        # logic for run

    def exit(self):
        print("Exiting safe_to_arm state")
        # logic for exit