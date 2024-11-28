class message_model():
    def __init__(self):
        self.x:int = None
        self.y:int = None
        self.z = None


    def add_data_from_json(self, json_data:dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])
