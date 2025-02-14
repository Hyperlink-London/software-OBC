from src.fsm.fsm import StateMachine
from src.logger import logger
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut
from src.constants import FSMConstants

# Unit Tests for Transitions
def full_journey_test():
    """ Full Journey Tests """
    controller = StateMachine()
    messageIn = MessageIn()
    messageIn.temperature_celsius_brake = 20
    messageIn.temperature_celsius_propulsion_1 = 20
    messageIn.temperature_celsius_propulsion_2 = 20
    messageIn.rpm = 0
    messageIn.speed_m_per_s = 0
    messageIn.safety_checks_button_pressed = False
    messageIn.safety_checks_passed = False
    messageIn.arm_button_pressed = False
    messageIn.abort_button_pressed = False
    messageIn.launch_button_pressed = False
    messageIn.fault_condition = False
    messageIn.disarm_button_pressed = False
    messageIn.distance = 0
    messageIn.primary_brakes_on = False
    messageIn.secondary_brakes_on = False


    

    print("### Before State: ", controller.state)
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'idle', f"Valid Transitions: Expected idle but got {controller.state}"
    print('\n'); print('\n')


    print("TEST: Transitioning to safety checks")
    #print("### Before State: ", controller.state)
    messageIn.safety_checks_button_pressed = True
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'safety_checks', f"Valid Transitions: Expected safety_checks but got {controller.state}"
    messageIn.safety_checks_button_pressed = False
    print('\n'); print('\n')

    print("TEST: Transitioning to safe_to_arm")
    #print("### Before State: ", controller.state)
    messageIn.safety_checks_passed = True
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'safe_to_arm', f"Valid Transitions: Expected safe_to_arm but got {controller.state}"
    print('\n'); print('\n')


    print("TEST: Transitioning to armed")
    #print("### Before State: ", controller.state)
    messageIn.arm_button_pressed = True
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'armed', f"Valid Transitions: Expected armed but got {controller.state}"
    print('\n'); print('\n')

    print("TEST: Transitioning to acceleration")
    #print("### Before State: ", controller.state)
    messageIn.launch_button_pressed = True
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'acceleration', f"Valid Transitions: Expected acceleration but got {controller.state}"
    messageIn.arm_button_pressed = False
    messageIn.launch_button_pressed = False
    print('\n'); print('\n')

    print("TEST: Transitioning to primary_braking")
    #print("### Before State: ", controller.state)
    messageIn.distance = FSMConstants.WAYPOINT_DISTANCE
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'primary_braking', f"Valid Transitions: Expected primary_braking but got {controller.state}"
    print('\n'); print('\n')


    print("TEST: Transitioning to secondary_braking")
    #print("### Before State: ", controller.state)
    messageIn.speed_m_per_s = FSMConstants.SECONDARY_BREAKING_SPEED
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'secondary_brake', f"Valid Transitions: Expected secondary_braking but got {controller.state}"
    print('\n'); print('\n')


    print("TEST: Transitioning to full_stop")
    #print("### Before State: ", controller.state)
    messageIn.speed_m_per_s = 0
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'full_stop', f"Valid Transitions: Expected full_stop but got {controller.state}"
    print('\n'); print('\n')


    print("TEST: Transitioning to idle")
    #print("### Before State: ", controller.state)
    messageIn.disarm_button_pressed = True
    messageIn.primary_brakes_on = False
    messageIn.secondary_brakes_on = False
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'idle', f"Valid Transitions: Expected idle but got {controller.state}"
    print('\n'); print('\n')
    print("All full journey tests passed!")

def invalid_transition_test():
    """ Tests for all possible invalid transitions """
    controller = StateMachine()
    state_classes = controller.state_classes
    messageIn = MessageIn()
    messageIn.temperature_celsius_brake = 20
    messageIn.temperature_celsius_propulsion_1 = 20
    messageIn.temperature_celsius_propulsion_2 = 20
    messageIn.rpm = 20
    messageIn.speed_m_per_s = 0
    messageIn.safety_checks_button_pressed = 0
    messageIn.safety_checks_passed = 0
    messageIn.arm_button_pressed = 0
    messageIn.abort_button_pressed = 0
    messageIn.launch_button_pressed = 0
    messageIn.fault_condition = 0
    messageIn.disarm_button_pressed = 0
    messageIn.distance = 0
    messageIn.primary_brakes_on = False
    messageIn.secondary_brakes_on = False

# Main execution loop
if __name__ == "__main__":
    full_journey_test()





