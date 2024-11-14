# Define a sample Message class (assuming it’s needed for message passing)
class Message:
    def __init__(self, recipient: str, data: str):
        self.recipient = recipient
        self.data = data

    def is_valid(self) -> bool:
        # Placeholder validation logic
        return bool(self.data)

    def message_to_esp(self):
        #takes stuff inside a message and from esp readable string
        pass

#TODO: Implement the validation logic after Ivet confirms the requirements