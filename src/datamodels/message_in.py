import json
import time


class MessageIn():

    def __init__(self):
        self.temperature_celsius_brake = None #optional float
        self.temperature_celsius_propulsion_1 = None #optional float
        self.temperature_celsius_propulsion_2 = None #optional float
        self.rpm = None  #optional float
        self.speed_m_per_s = None #boolean
        self.safety_checks_button_pressed = None #boolean
        self.safety_checks_passed = None #boolean
        self.arm_button_pressed = None #boolean
        self.abort_button_pressed = None #boolean
        self.launch_button_pressed = None #boolean
        self.fault_condition = None #boolean
        self.disarm_button_pressed = None #boolean
        self.distance = None #int
        self.primary_brakes_on = None # boolean
        self.secondary_brakes_on = None # boolean

        #Initiailize timestamp as time generated
        self.timestamp = time.time()

    def has_enough_data(self):
        return all([self.temperature_celsius_brake, self.temperature_celsius_propulsion_1, self.temperature_celsius_propulsion_2, self.rpm, self.safety_checks_button_pressed, self.speed_m_per_s])

    #Process the data from the json string from ESP
    def add_data_from_json(self, json_string:str):
        json_data=json.loads(json_string)
        # print("DEBUG")
        # print(json_data)
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])

    def update_from_data(self, message):
        for key in message.__dict__:
            if hasattr(self, key):
                setattr(self, key, message.__dict__[key])
        pass

    def __repr__(self):
        return str(self.__dict__)


