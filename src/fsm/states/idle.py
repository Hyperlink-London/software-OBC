from transitions import State

class Idle(State):
    def __init__(self, name='idle'):
        super().__init__(name=name)

    def enter(self):
        print("Entering idle state")
        # logic for enter

    def run(self, input_data) -> bool:
        print("Running idle state")
        if(input_data.safety_button_pressed):
            return 'safety_button'
        
        

    def exit(self):
        print("Exiting idle state")
        # logic for exit