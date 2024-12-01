class message_in():
    def __init__(self,temperature_celsius_brake,temperature_celsius_propulsion_1,temperature_celsius_propulsion_2,rpm,speed_m_per_s,safety_checks_button_pressed,safety_checks_passed,arm_button_pressed,abort_button_pressed,launch_button_pressed,fault_condition,disarm_button_pressed,distance):
        self.temperature_celsius_brake = temperature_celsius_brake #optional float
        self.temperature_celsius_propulsion_1 = temperature_celsius_propulsion_1 #optional float
        self.temperature_celsius_propulsion_2 = temperature_celsius_propulsion_2 #optional float
        self.rpm = rpm  #optional float
        self.speed_m_per_s = speed_m_per_s #boolean
        self.safety_checks_button_pressed = safety_checks_button_pressed #boolean
        self.safety_checks_passed = safety_checks_passed #boolean
        self.arm_button_pressed = arm_button_pressed #boolean
        self.abort_button_pressed = abort_button_pressed #boolean
        self.launch_button_pressed = launch_button_pressed #boolean
        self.fault_condition = fault_condition #boolean
        self.disarm_button_pressed = disarm_button_pressed #boolean
        self.distance = distance #int

    def get_temperature_celsius_brake(self):
        return self.temperature_celsius_brake

    def get_temperature_celsius_propulsion_1(self):
        return self.temperature_celsius_propulsion_1

    def get_temperature_celsius_propulsion_2(self):
        return self.temperature_celsius_propulsion_2

    def get_rpm(self):
        return self.rpm

    def get_speed_m_per_s(self):
        return self.speed_m_per_s

    def get_safety_checks_button_pressed(self):
        return self.safety_checks_button_pressed

    def get_safety_checks_passed(self):
        return self.safety_checks_passed

    def get_arm_button_pressed(self):
        return self.arm_button_pressed

    def get_abort_button_pressed(self):
        return self.abort_button_pressed

    def get_launch_button_pressed(self):
        return self.launch_button_pressed

    def get_fault_condition(self):
        return self.fault_condition

    def get_disarm_button_pressed(self):
        return self.disarm_button_pressed

    def get_distance(self):
        return self.distance

    def add_data_from_json(self, json_data:dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])
