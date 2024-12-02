class message_in():
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

    def add_data_from_json(self, json_data:dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])

    def __repr__(self):
        return str(self.__dict__)
