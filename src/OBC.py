from fsm import fsm

controller = fsm.StateMachine()


# Testing transitioning between states
print(controller.state)
controller.run_current_state()
controller.to_acceleration()
controller.run_current_state()
#controller.to_safe_abort() # This should raise an exception
print(controller.state)



# To confirm: shouldn't we have the following code here?
"""
    def run(self):
        self.get_data()                                          # async
        self.receive_api_data()                                 # async
        self.run_current_state()                                # async
        self.send_data(self.breaking_data, self.propulsion_data) # async
        self.send_api_data()                                    # async
"""





"""
# Main execution loop
if __name__ == "__main__":
    while True:
        controller.run()
"""

