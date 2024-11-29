# Define a sample Message class (assuming it’s needed for message passing)

import time

class Message:
    def __init__(self, recipient:str, sender: str, data: str):
        self.recipient = recipient
        self.sender = sender
        self.data = data
        self.timestamp = time.time()

    def is_valid(self) -> bool:
        # Placeholder validation logic
        return bool(self.data)

    def message_to_esp(self):
        #takes stuff inside a message and from esp readable string
        return self.data

#TODO: Implement the validation logic after Ivet confirms the requirements