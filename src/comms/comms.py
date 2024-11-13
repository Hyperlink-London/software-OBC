# Comms Class
from typing import Optional
from message import Message
from APIHandler import APIHandler
from ESPHandler import ESPHandler


class Comms:
    def __init__(self, breaking_coms:ESPHandler, propulsion_coms:ESPHandler):
        self.breaking_coms = breaking_coms
        self.propulsion_coms = propulsion_coms
        self.api = APIHandler(self, "http://localhost:8000")

    async def send_message_to_esp(self, message: Message) -> bool:
        """
        Send message to ESP
        :param message:
        :return:
        """
        if message.is_valid():
            if message.recipient == "braking":
                self.breaking_coms.send_data(message.data)
            elif message.recipient == "propulsion":
                self.propulsion_coms.send_data(message.data)
            return True
        return False

    async def receive_message_from_esp(self) -> Optional[Message]:
        # Logic to receive message from ESP and validate it
        message = Message("Braking","sample data")  # Placeholder message
        #TODO: Add logic to interface with saving data so FSM can access it
        return message if message.is_valid() else None

    async def send_command_to_fsm(self, command: str) -> bool:
        # Logic to send a command to FSM
        #TODO: Add logic to interface with FSM
        return True

    async def process_request_from_api(self, request: dict) -> bool:
        #TODO: Logic to process API request and route to FSM or ESPHandler

        return True

    async def start(self):
        # Background process to handle receiving messages from ESP
        pass