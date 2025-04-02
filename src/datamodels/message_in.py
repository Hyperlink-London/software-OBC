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
        self.demo = None #float

        #Initiailize timestamp as time generated
        self.timestamp = time.time()

    def has_enough_data(self):
        return all([self.temperature_celsius_brake, self.temperature_celsius_propulsion_1, self.temperature_celsius_propulsion_2, self.rpm, self.safety_checks_button_pressed, self.speed_m_per_s])

    #Process the data from the json string from ESP
    def add_data_from_json(self, json_string:str):
        json_data = json.loads(json_string)  
        if hasattr(self, json_data["sensor"]):
            setattr(self, json_data["sensor"], json_data["value"])

    def update_from_data(self, message):
        for key in message.__dict__:
            if hasattr(self, key):
                setattr(self, key, message.__dict__[key])
        pass

    def fillout_for_testing(self):
        if self.temperature_celsius_brake is None:
            self.temperature_celsius_brake = 0
        if self.temperature_celsius_propulsion_1 is None:
            self.temperature_celsius_propulsion_1 = 0
        if self.temperature_celsius_propulsion_2 is None:
            self.temperature_celsius_propulsion_2 = 0
        if self.rpm is None:
            self.rpm = 0
        if self.speed_m_per_s is None:
            self.speed_m_per_s = 0
        if self.safety_checks_button_pressed is None:
            self.safety_checks_button_pressed = False
        if self.safety_checks_passed is None:
            self.safety_checks_passed = False
        if self.arm_button_pressed is None:
            self.arm_button_pressed = False
        if self.abort_button_pressed is None:
            self.abort_button_pressed = False
        if self.launch_button_pressed is None:
            self.launch_button_pressed = False
        if self.fault_condition is None:
            self.fault_condition = False
        if self.disarm_button_pressed is None:
            self.disarm_button_pressed = False
        if self.distance is None:
            self.distance = 0
        if self.primary_brakes_on is None:
            self.primary_brakes_on = False
        if self.secondary_brakes_on is None:
            self.secondary_brakes_on = False
        if self.demo is None:
            self.demo = 0

    def __repr__(self):
        return str(self.__dict__)


