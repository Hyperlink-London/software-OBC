class message_out():
    def __init__(self,primary_brakes_on,secondary_brakes_on,propulsion_on,current_state):
        self.primary_brakes_on = primary_brakes_on #boolean
        self.secondary_brakes_on = secondary_brakes_on #boolean
        self.propulsion_on = propulsion_on #boolean
        self.current_state = current_state #string

    def get_primary_brakes_on(self):
        return self.primary_brakes_on

    def get_secondary_brakes_on(self):
        return self.secondary_brakes_on

    def get_propulsion_on(self):
        return self.propulsion_on

    def get_current_state(self):
        return self.current_state

    def add_data_from_json(self, json_data: dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])
