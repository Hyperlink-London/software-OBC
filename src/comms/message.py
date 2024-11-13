# Define a sample Message class (assuming it’s needed for message passing)
class Message:
    def __init__(self, recipient: str, data: str):
        self.recipient = recipient
        self.data = data

    def is_valid(self) -> bool:
        # Placeholder validation logic
        return bool(self.data)

#TODO: Implement the validation logic after Ivet confirms the requirements