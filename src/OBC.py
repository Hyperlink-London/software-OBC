from fsm import fsm

controller = fsm.StateMachine()


# Testing transitioning between states
print(controller.state)
controller.run_current_state()
controller.to_acceleration()
controller.run_current_state()
#controller.to_safe_abort() # This should raise an exception
print(controller.state)

"""
# Main execution loop
if __name__ == "__main__":
    while True:
        controller.run()
"""

