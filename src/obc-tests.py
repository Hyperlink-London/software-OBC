from src.fsm.fsm import StateMachine
from src.logger import logger
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut

controller = StateMachine()




# Unit Tests for Transitions
# (Currently on checks the valid states -> need to unit test invalid transitions)

import time

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



print("------------------------")
print("### Before State: ", controller.state)
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'idle', f"Expected idle but got {controller.state}"
print("------------------------")

# change to safety_checks
print("TEST: Transitioning to safety checks")
print("### Before State: ", controller.state)
messageIn.safety_checks_button_pressed = True
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'safety_checks', f"Expected safety_checks but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to safety pass")
print("### Before State: ", controller.state)
messageIn.safety_checks_passed = True
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'safe_to_arm', f"Expected safe_to_arm but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to armed")
print("### Before State: ", controller.state)
messageIn.arm_button_pressed = True
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'armed', f"Expected armed but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to acceleration")
print("### Before State: ", controller.state)
messageIn.launch_button_pressed = True
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'acceleration', f"Expected acceleration but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to primary_braking")
print("### Before State: ", controller.state)
messageIn.distance = 200
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'primary_braking', f"Expected primary_braking but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to secondary_braking")
print("### Before State: ", controller.state)
messageIn.speed_m_per_s = 50
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'secondary_brake', f"Expected secondary_braking but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to full_stop")
print("### Before State: ", controller.state)
messageIn.speed_m_per_s = 0
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'full_stop', f"Expected full_stop but got {controller.state}"
print("------------------------")

print("TEST: Transitioning to idle")
print("### Before State: ", controller.state)
messageIn.disarm_button_pressed = True
messageIn.primary_brakes_on = False
messageIn.secondary_brakes_on = False
print("###", controller.run_current_state(messageIn))
print("### After State: ", controller.state)
assert controller.state == 'idle', f"idle but got {controller.state}"
print("------------------------")





"""
# Main execution loop
if __name__ == "__main__":
    while True:
        controller.run()
"""

