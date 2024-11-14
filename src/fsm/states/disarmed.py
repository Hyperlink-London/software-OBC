from transitions import State

class Disarmed(State):
    def __init__(self, name='disarmed'):
        super().__init__(name=name)
    
    def enter(self):
        print("Entering disarmed state")
        # logic for enter
    
    def run(self):
        print("Running disarmed state")
        # logic for run
    
    def exit(self):
        print("Exiting disarmed state")
        # logic for exit
    
    