from transitions import Machine

from fsm.states.acceleration import Acceleration
from fsm.states.armed import Armed
from fsm.states.braking import Braking
from fsm.states.cruise import Cruise
from fsm.states.disarmed import Disarmed
from fsm.states.emergency_stop import EmergencyStop
from fsm.states.fullstop import FullStop
from fsm.states.idle import Idle
from fsm.states.safe_abort import SafeAbort
from fsm.states.safe_to_arm import SafeToArm
from fsm.states.safety_checks import SafetyChecks
from fsm.states.secondary_brake import SecondaryBrake

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
            'idle': Idle(),
            'safety_checks': SafetyChecks(),
            'safe_to_arm': SafeToArm(),
            'disarmed': Disarmed(),
            'armed': Armed(),
            'acceleration': Acceleration(),
            'cruise': Cruise(),
            'braking': Braking(),
            'secondary_brake': SecondaryBrake(),
            'full_stop': FullStop(),
            'safe_abort': SafeAbort(),
            'emergency_stop': EmergencyStop()
        }

        # Initialize the state machine with states and initial state, with strict transition checking
        super().__init__(
            model=self,  # Links the state machine to self
            states=list(self.state_classes.keys()),  # Inputs the states
            initial=self.state_classes['idle'].name,  # Set the initial state
            auto_transitions=False,  # Only allow defined transitions to be triggered 
            send_event=True,  # Enables detailed event data to be sent with each transition trigger, useful for debugging and providing context for each transition.
            queued=True,  # Ensures that transition triggers are queued, preventing overlapping transitions and enforcing sequential processing
            before_state_change=self.validate_before_transition,  # Calls `validate_before_transition` before every state change
            after_state_change=self.log_transition,  # Calls `log_transition` after each state change
            ignore_invalid_triggers=False,  # Raises an exception if an invalid trigger is called
            name="OBCStateMachine"  # Sets a name, easier for logging
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

    # Todo: Define the before-state-change callback
    def validate_before_transition(self, event):
        """Perform checks or validations before each transition."""
        print(f"Validating transition from {event.state.name} to {event.transition.dest}")
        # Add any checks you need, return True if valid, or raise an error otherwise.

    # Todo: Define the after-state-change callback
    def log_transition(self, event):
        """Log information after each transition."""
        print(f"Transitioned from {event.state.name} to {event.transition.dest}")
        # Additional logging or monitoring logic can be added here.






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
