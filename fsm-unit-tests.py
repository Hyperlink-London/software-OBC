from src.fsm.fsm import StateMachine
from src.logger import logger
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut
from src.constants import FSMConstants

import copy

# Unit Tests for Transitions
def full_journey_test_without_cruise():
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

def full_journey_test_with_cruise():
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

    print("TEST: Transitioning to cruise")
    #print("### Before State: ", controller.state)
    messageIn.speed_m_per_s = FSMConstants.MAX_SPEED
    print("###", controller.run_current_state(messageIn))
    #print("### After State: ", controller.state)
    assert controller.state == 'cruise', f"Valid Transitions: Expected cruise but got {controller.state}"
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
    event_dictionary = controller.event_dictionary



    for i in state_classes:
        print("\n\n\n")
        controller.state = i
        print(f"Current state: {controller.state}")
        #print(f"Testing invalid transitions for {i}")

        valid_transitions = []
        invalid_transitions = []

        for key in event_dictionary:
            testController = copy.deepcopy(controller)
            try:
                testController.event_dictionary[key]()
                valid_transitions.append(key)
            except Exception as e:
                invalid_transitions.append(key)
        print("\n")
        print(f"Valid Transitions: {valid_transitions}")
        print("\n")
        print(f"Invalid Transitions: {invalid_transitions}")

def abort_fault_test():
    controller = StateMachine()
    state_classes = controller.state_classes


    successMessageIn = MessageIn()
    successMessageIn.temperature_celsius_brake = 20 # abort condition
    successMessageIn.temperature_celsius_propulsion_1 = 20 # abort condition
    successMessageIn.temperature_celsius_propulsion_2 = 20 #abort condition
    successMessageIn.rpm = 0 # abort condition
    successMessageIn.speed_m_per_s = 0
    successMessageIn.safety_checks_button_pressed = False
    successMessageIn.safety_checks_passed = None # abort condition
    successMessageIn.arm_button_pressed = False
    successMessageIn.abort_button_pressed = False # abort condition
    successMessageIn.launch_button_pressed = False
    successMessageIn.fault_condition = False # fault condition
    successMessageIn.disarm_button_pressed = False
    successMessageIn.distance = 0
    successMessageIn.primary_brakes_on = False
    successMessageIn.secondary_brakes_on = False

    abortMessages = []

    tempCelciusBrakeAbort = copy.deepcopy(successMessageIn)
    tempCelciusBrakeAbort.temperature_celsius_brake = FSMConstants.MAX_TEMP_BRAKING
    abortMessages.append(tempCelciusBrakeAbort)

    tempCelciusPropulsionAbort1 = copy.deepcopy(successMessageIn)
    tempCelciusPropulsionAbort1.temperature_celsius_propulsion_1 = FSMConstants.MAX_TEMP_PROPULSION
    abortMessages.append(tempCelciusPropulsionAbort1)

    tempCelciusPropulsionAbort2 = copy.deepcopy(successMessageIn)
    tempCelciusPropulsionAbort2.temperature_celsius_propulsion_2 = FSMConstants.MAX_TEMP_PROPULSION
    abortMessages.append(tempCelciusPropulsionAbort2)

    rpmAbort = copy.deepcopy(successMessageIn)
    rpmAbort.rpm = FSMConstants.MAX_RPM
    abortMessages.append(rpmAbort)

    abortButtonAbort = copy.deepcopy(successMessageIn)
    abortButtonAbort.abort_button_pressed = True
    abortMessages.append(abortButtonAbort)




    for i in state_classes:
        print("\n\n\n")

        for j in abortMessages:
            controller.state = i
            if(controller.state == 'safe_abort'):
                continue
            print(f"Current state: {controller.state}")
            print(f"Testing abort condition for {i}")
            print(f"MessageIn: {j}")
            print("\n")
            print(f"MessageOut: {controller.run_current_state(j)}")
            print("\n\n\n")
            assert controller.state == 'safe_abort', f"Abort Transitions: Expected safe_abort but got {controller.state} for {state_classes[i]}"

    # test safety checks failed
    safetyChecksAbort = copy.deepcopy(successMessageIn)
    safetyChecksAbort.safety_checks_passed = False
    # does not append because it is a fault condition only for this state

    controller.state = 'safety_checks'
    print("\n\n\n")
    print(f"Current state: {controller.state}")
    print(f"Testing safety checks failed condition for {state_classes['safety_checks']}")
    print(f"MessageIn: {safetyChecksAbort}")
    print("\n")
    messageOut = controller.run_current_state(safetyChecksAbort)
    #print(f"MessageOut: {controller.run_current_state(safetyChecksAbort)}")
    print("\n\n\n")
    assert controller.state == 'idle', f"Valid Transitions: Expected idle but got {controller.state}"


# Main execution loop
if __name__ == "__main__":
    #full_journey_test_without_cruise()
    #full_journey_test_with_cruise()
    #invalid_transition_test()
    abort_fault_test()
