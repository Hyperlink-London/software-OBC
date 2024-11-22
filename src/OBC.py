from fsm.fsm import StateMachine
from src.logger import logger

controller = StateMachine()


# Testing transitioning between states
import time
print(controller.state)
logger.debug(controller.state)
controller.safety_button()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.safety_pass()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.arm_button_pressed()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.launch_button()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.top_speed_reached()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.braking_waypoint_reached()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.to_secondary_brake()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.to_full_stop()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)
controller.to_idle()
time.sleep(1)
print(controller.state)
logger.debug(controller.state)


"""
# Main execution loop
if __name__ == "__main__":
    while True:
        controller.run()
"""

