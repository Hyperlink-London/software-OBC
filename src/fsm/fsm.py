from transitions import Machine

from fsm.states import acceleration, armed, braking, cruise, disarmed, emergency_stop, fullstop, idle, safe_abort, safe_to_arm, safety_checks, secondary_brake

class StateMachine(Machine):

    def __init__(self):
        
        # Todo: add data classes and comms classes
        self.current_state = None
        self.breaking_data = None
        self.propulsion_data = None
        self.breaking_coms = None
        self.propulsion_coms = None


        # Initialise the state machine
        # Define States
        self.state_classes = {
            'idle': idle.Idle(),
            'safety_checks': safety_checks.SafetyChecks(),
            'safe_to_arm': safe_to_arm.SafeToArm(),
            'disarmed': disarmed.Disarmed(),
            'armed': armed.Armed(),
            'acceleration': acceleration.Acceleration(),
            'cruise': cruise.Cruise(),
            'braking': braking.Braking(),
            'secondary_brake': secondary_brake.SecondaryBrake(),
            'full_stop': fullstop.FullStop(),
            'safe_abort': safe_abort.SafeAbort(),
            'emergency_stop': emergency_stop.EmergencyStop()
        }

        # Initialize the state machine with states and initial state, with strict transition checking
        super().__init__(
            model=self,
            states=list(self.state_classes.keys()),
            initial=self.state_classes['idle'].name,
            auto_transitions=False  # Disable automatic/undefined transitions
        )

        # Mark the final state
        self.add_state('full_stop', final=True)

        # Define transitions
        # Todo: Add transitions
        self.add_transition(trigger='to_acceleration', source='idle', dest='acceleration')
        self.add_transition(trigger='to_safe_abort', source='acceleration', dest='safe_abort')

    def run_current_state(self):
        # Call the run method of the current state
        current_state = self.state_classes[self.state]
        current_state.run()






    # Todo: implement these methods

    # getData: This method is used to get data from the propulsion and braking systems
    def get_data(self):
        pass
    
    # sendData: This method is used to send data to the propulsion and braking systems
    def send_data(self,breaking_data, propulsion_data):
        pass

    # receive_api_data: This method is used to receive data from the API
    def receive_api_data(self):
        pass

    # send_api_data: This method is used to send data to the API
    def send_api_data(self):
        pass

    # Run: This is the main loop of the state machine
    # Todo: check whether we can have run as async or methods inside run as async
    def run(self):
        self.get_data()                                          # async
        self.receive_api_data()                                 # async
        self.run_current_state()                                # async
        self.send_data(self.breaking_data, self.propulsion_data) # async
        self.send_api_data()                                    # async
