import json
import time

from src.logger import logger


class MessageIn():

    def __init__(self,data:str = None):
        self.temperature_celsius_brake:float = None
        self.temperature_celsius_propulsion_1:float = None
        self.temperature_celsius_propulsion_2:float = None
        self.rpm:float = None 
        self.speed_m_per_s:bool = None
        self.safety_checks_button_pressed:bool = None
        self.safety_checks_passed:bool = None
        self.arm_button_pressed:bool = None
        self.abort_button_pressed:bool = None
        self.launch_button_pressed:bool = None
        self.fault_condition:bool = None
        self.disarm_button_pressed:bool = None
        self.distance:int = None
        self.primary_brakes_on:bool = None
        self.secondary_brakes_on:bool = None
        self.demo:float = None

        #Initiailize timestamp as time generated
        self.timestamp = time.time()
        
        #If data is not None, parse the json string
        if data:
            self.add_data_from_json(data)

    def has_enough_data(self):
        return all([self.temperature_celsius_brake, self.temperature_celsius_propulsion_1, self.temperature_celsius_propulsion_2, self.rpm, self.safety_checks_button_pressed, self.speed_m_per_s])

    def add_data_from_json(self, json_string:str):
        """
        Parse the JSON string and update the attributes of the class.

        The JSON string should be in the format:
        {
            "espId": "esp-propulsion",
            "sensor": "demo",
            "value": 4.90
        }
        """
        json_data = json.loads(json_string)  
        if hasattr(self, json_data["sensor"]):
            setattr(self, json_data["sensor"], json_data["value"])
        else:
            logger.error(f"Invalid sensor type: {json_data['sensor']}(value: {json_data['value']}) from {json_data['espId']} ")

    def fill_from_data(self, message):
        """
        Update the attributes of the class with the values from the message object.
        Used for FSM caching due to nature of the sending logic
        """
        for key in message.__dict__:
            if hasattr(self, key):
                setattr(self, key, message.__dict__[key])
        pass

    def fillout_for_testing(self):
        """
        Fill out the attributes with default values for testing purposes.
        """
        defaults = {
            "temperature_celsius_brake": 0.0,
            "temperature_celsius_propulsion_1": 0.0,
            "temperature_celsius_propulsion_2": 0.0,
            "rpm": 0.0,
            "speed_m_per_s": 0.0,
            "safety_checks_button_pressed": False,
            "safety_checks_passed": False,
            "arm_button_pressed": False,
            "abort_button_pressed": False,
            "launch_button_pressed": False,
            "fault_condition": False,
            "disarm_button_pressed": False,
            "distance": 0.0,
            "primary_brakes_on": False,
            "secondary_brakes_on": False,
            "demo": 0.0
        }

        for attr, default in defaults.items():
            if getattr(self, attr, None) is None:
                setattr(self, attr, default)

    def __repr__(self):
        return str(self.__dict__)


