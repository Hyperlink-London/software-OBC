# Comms Class
from typing import Optional
from message import Message
from APIHandler import APIHandler
from ESPHandler import ESPHandler
import logging
import asyncio


class Comms:
    def __init__(self, braking_coms:ESPHandler, propulsion_coms:ESPHandler):

        self.braking_coms = braking_coms
        self.propulsion_coms = propulsion_coms
        self.api = APIHandler(self, "http://localhost:8000")
        self.logger = logging.getLogger(__name__)


    #ESP Comms

    async def send_message_to_esp(self, message: Message) -> bool:
        """
        Send message to ESP
        :param message:
        :return:
        """
        if message.recipient == "braking":
            return await self.braking_coms.handle_serial(message)
        elif message.recipient == "propulsion":
            return await self.propulsion_coms.handle_serial(message)
        return False

    async def receive_message_from_esp(self, device:str) -> Optional[Message]:
        if device in ["braking","propulsion"]:
            if device == "braking":
                return await self.braking_coms.handle_serial()
            elif device == "propulsion":
                return await self.propulsion_coms.handle_serial()
        else:
            return -1

    #Interface with FSM
    async def send_command_to_fsm(self, command: str) -> bool:
        # Logic to send a command to FSM. this is only used when api command received from fsm and is a change state command
        #TODO: Add logic to interface with FSM
        pass

    # TODO: Refine Method Signature
    async def receive_data_from_fsm(self):
        # Receive commands or new states from the FSM and
        pass

    async def update_data_objects(self, message:Message)-> bool:
        #Update the braking and propulsion data objects for the FSM to make new decisions if needed
        pass

    #Interface with API
    async def process_request_from_api(self, request: dict) -> bool:
        #TODO: Logic to process API request and route to FSM or ESPHandler
        pass

    async def send_data_to_api(self, message:Message) -> bool:
        #TODO: Logic to send data to API everytime theres new data from ESP or FSM has new state
        """
        I was thinking, when FSM changes states have it async run a send command to comms so we have update the state on the dashboard
        :param message:
        :return:
        """
        pass

    async def start(self):
        """
        Continuously receive data from the ESP and send it to FSM and API.
        Logs outputs from each handler asynchronously.
        """
        while True:
            p_message = await self.receive_message_from_esp("propulsion")
            b_message = await self.receive_message_from_esp("braking")

            if p_message:
                # Create async tasks to send data to FSM and API simultaneously
                tasks = [
                    asyncio.create_task(self.send_data_to_api(p_message)),
                    asyncio.create_task(self.update_data_objects(p_message))
                ]

                # Log outputs from FSM and API
                for task in tasks:
                    try:
                        result = await task
                        self.logger.info(f"Task completed with result: {result}")
                    except Exception as e:
                        self.logger.error(f"Task failed with error: {e}")

            if b_message:
                # Create async tasks to send data to FSM and API simultaneously
                tasks = [
                    asyncio.create_task(self.send_data_to_api(b_message)),
                    asyncio.create_task(self.update_data_objects(b_message))
                ]

                # Log outputs from FSM and API
                for task in tasks:
                    try:
                        result = await task
                        self.logger.info(f"Task completed with result: {result}")
                    except Exception as e:
                        self.logger.error(f"Task failed with error: {e}")
            # Small delay to avoid overwhelming the loop
            await asyncio.sleep(0.1)