
class FSM:
    def __init__(self):
        self.current_state = Breaking()
        self.breaking_data = breaking_data
        self.propulsion_data = propulsion_data
        self.breaking_coms = coms.COMS_ESP()
        self.propulsion_coms = coms.COMS_ESP()

    def run(self):
        getdata()  # async
        self.current_state.run()  # async
        senddata(self.breaking_data, self.propulsion_data)  # async
        # test to make sure that the functions work asynchronously
        receive_api_data()  # async
