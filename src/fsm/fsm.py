from transitions import Machine

from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut

from src.fsm.states import (
    acceleration,
    armed,
    cruise,
    emergency_stop,
    fullstop,
    idle,
    primary_braking,
    safe_abort,
    safe_to_arm,
    safety_checks,
    secondary_brake
)


class StateMachine(Machine):

    def __init__(self):
        
        # Initialise the state machine
        # Define States
        self.state_classes = {
            'idle': idle.Idle(),
            'safety_checks': safety_checks.SafetyChecks(),
            'safe_to_arm': safe_to_arm.SafeToArm(),
            'armed': armed.Armed(),
            'acceleration': acceleration.Acceleration(),
            'cruise': cruise.Cruise(),
            'primary_braking': primary_braking.PrimaryBraking(),
            'secondary_brake': secondary_brake.SecondaryBrake(),
            'full_stop': fullstop.FullStop(),
            'safe_abort': safe_abort.SafeAbort(),
            'emergency_stop': emergency_stop.EmergencyStop()
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

        # Define transitions
        # Idle transitions
        self.add_transition(trigger='safety_button', source='idle', dest='safety_checks')
        self.add_transition(trigger='abort', source='idle', dest='safe_abort')

        # Safety Checks transitions
        self.add_transition(trigger='safety_pass', source='safety_checks', dest='safe_to_arm')
        self.add_transition(trigger='safety_fail', source='safety_checks', dest='idle')
        self.add_transition(trigger='abort', source='safety_checks', dest='safe_abort')

        # Safe to Arm transitions
        self.add_transition(trigger='arm_button_pressed', source='safe_to_arm', dest='armed')
        self.add_transition(trigger='fault', source='safe_to_arm', dest='idle')
        self.add_transition(trigger='abort', source='safe_to_arm', dest='safe_abort')

        # Armed transitions
        self.add_transition(trigger='arm_button_released', source='armed', dest='safe_to_arm')
        self.add_transition(trigger='launch_button', source='armed', dest='acceleration')
        self.add_transition(trigger='fault', source='armed', dest='idle')
        self.add_transition(trigger='abort', source='armed', dest='safe_abort')

        # Acceleration transitions
        self.add_transition(trigger='top_speed_reached', source='acceleration', dest='cruise')
        self.add_transition(trigger='abort_or_fault', source='acceleration', dest='safe_abort')
        self.add_transition(trigger='waypoint_reached', source='acceleration', dest='primary_braking')

        # Cruise transitions
        self.add_transition(trigger='braking_waypoint_reached', source='cruise', dest='primary_braking')
        self.add_transition(trigger='abort_or_fault', source='cruise', dest='safe_abort')

        # Primary Braking transitions
        self.add_transition(trigger='to_secondary_brake', source='primary_braking', dest='secondary_brake')
        self.add_transition(trigger='abort_or_fault', source='primary_braking', dest='safe_abort')

        # Secondary Braking transitions
        self.add_transition(trigger='to_full_stop', source='secondary_brake', dest='full_stop')
        self.add_transition(trigger='abort_or_fault', source='secondary_brake', dest='safe_abort')

        # Full Stop transitions
        self.add_transition(trigger='to_idle', source='full_stop', dest='idle')
        self.add_transition(trigger='abort_or_fault', source='full_stop', dest='safe_abort')

        # Safe Abort transitions
        self.add_transition(trigger='stopped_and_abort_released', source='safe_abort', dest='full_stop')
        

        self.event_dictionary = {
            'safety_button': 'self.safety_button()',
            'safety_pass': 'self.safety_pass()',
            'safety_fail': 'self.safety_fail()',
            'abort': 'self.abort()',
            'arm_button_pressed': 'self.arm_button_pressed()',
            'arm_button_released': 'self.arm_button_released()',
            'launch_button': 'self.launch_button()',
            'top_speed_reached': 'self.top_speed_reached()',
            'waypoint_reached': 'self.waypoint_reached()',
            'braking_waypoint_reached': 'self.braking_waypoint_reached()',
            'to_secondary_brake': 'self.to_secondary_brake()',
            'to_full_stop': 'self.to_full_stop()',
            'to_idle': 'self.to_idle()',
            'stopped_and_abort_released': 'self.stopped_and_abort_released()',
            'abort_or_fault': 'self.abort_or_fault()',
            'fault': 'self.fault()'
        }
        
    def run_current_state(self, input_data: MessageIn):
        # Call the run method of the current state
        current_state = self.state_classes[self.state]
        
        
        # DATA is a tuple of format: (event, primary_brakes_engaged, secondary_brakes_engaged, propulsion_engaged, current_state)
        data = current_state.run()

        # data[0] is to trigger a transition
        # Only run if the event is not empty
        if(data[0]):
            self.event_dictionary[data[0]]
        
        # return message out
        return MessageOut(data[1], data[2], data[3], data[4])

        

    # Todo: Define the before-state-change callback
    # The FSM already validates transitions by default, but we can add additional checks here
    def validate_before_transition(self, event):
        print(f"Validating transition from {event.state.name} to {event.transition.dest}")
        # Add any checks you need, return True if valid, or raise an error otherwise.

    # Todo: Define the after-state-change callback
    # Additional logging after each transition
    def log_transition(self, event):
        print(f"Transitioned to {event.transition.dest}")


