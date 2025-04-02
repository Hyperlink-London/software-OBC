class MessageOut():
    def __init__(self,primary_brakes_on,secondary_brakes_on,propulsion_on,current_state):
        self.primary_brakes_on = primary_brakes_on #boolean
        self.secondary_brakes_on = secondary_brakes_on #boolean
        self.propulsion_on = propulsion_on #boolean
        self.current_state = current_state #string


    def add_data_from_json(self, json_data: dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])

    def __repr__(self):
        return f"MessageOut: PrimaryBrakesOn: {self.primary_brakes_on}, SecondaryBrakesOn: {self.secondary_brakes_on}, PropulsionOn: {self.propulsion_on}, CurrentState: {self.current_state}"

    def message_to_esp(self):
        #TODO: implement this function
        pass