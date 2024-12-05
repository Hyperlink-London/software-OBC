from src.fsm.fsm import StateMachine
from src.logger import logger
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut

controller = StateMachine()




# Testing transitioning between states

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




print(controller.state)
logger.debug(controller.state)
# idle state
print(controller.run_current_state(messageIn))


# change to safety_checks
time.sleep(2)
print("Transitioning to safety")
messageIn.safety_checks_button_pressed = True
print(controller.run_current_state(messageIn))


"""
# Main execution loop
if __name__ == "__main__":
    while True:
        controller.run()
"""

