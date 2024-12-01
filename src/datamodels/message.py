import time


#TODO: Implement the validation logic after Ivet confirms the requirements
class Message:
    def __init__(self, recipient:str, sender: str, data: str):
        self.recipient = recipient
        self.sender = sender
        self.data = data
        self.timestamp = time.time()


    def add_data_from_json(self, json_data:dict):
        for key in json_data:
            if hasattr(self, key):
                setattr(self, key, json_data[key])

    def message_to_esp(self):
        #takes stuff inside a message and from esp readable string
        return self.data
