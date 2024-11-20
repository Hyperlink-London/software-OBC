# Comms Class
from typing import Optional
from src.datamodels.message import Message
from ESPHandler import ESPHandler
import asyncio
import json
from WebsocketClient import WebSocketClient
from src.fsm.fsm import StateMachine

#TODO: Add Logger logic

class Comms:
    def __init__(self, braking_coms:ESPHandler, propulsion_coms:ESPHandler):
        self.state_machine = StateMachine()
        self.braking_coms = braking_coms
        self.propulsion_coms = propulsion_coms
        # self.http_handler = HTTPHandler(self, "8080")
        self.message_queue = asyncio.Queue()
        self.websocket_client = WebSocketClient("ws://localhost:8000/ws")
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
    async def update_fsm(self, p_message:Message,b_message:Message) -> Message:
        # Logic to send data to FSM
        #Deal with two messages and pass it to the fsm at once
        fsm_data = self.state_machine.receive_data(data)
        pass


    async def send_command_to_fsm(self, command: str) -> Message:
        # Logic to send a command to FSM. this is only used when api command received from fsm and is a change state command
        fsm_command = self.state_machine.receive_command(command)
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


        return False

    async def process_queue_messages(self):
        """Dedicated consumer for processing queue messages"""
        while True:
            try:
                message = await self.message_queue.get()
                await self.process_request_from_api(message)
                self.message_queue.task_done()
            except Exception as e:
                print(f"Error processing queue message: {e}")

    #Interface with Websockets
    async def websocket_health_check(self):
        while True:
            try:
                await self.websocket_client.send("health_check")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error in websocket health check: {e}")
                #Potentially block the main loop until the websocket is reconnected
                await self.websocket_client.close()
                await self.websocket_client.connect()

#TODO: Pass data to State Machine as it comes in
#TODO: Figure out a way to retrieve commands from the FSM
    async def start(self):
        # Start the message consumer as a separate task
        consumer_task = asyncio.create_task(self.process_queue_messages())
        
        # Run both connections simultaneously
        brake_connected, prop_connected = await asyncio.gather(
            self.braking_coms.connect(),
            self.propulsion_coms.connect()
        )
        
        websocket_client = await self.websocket_client.connect()
        
        try:
            while True:
                print('Running')
                # Run ESP message handling concurrently
                p_message, b_message = await asyncio.gather(
                    self.receive_message_from_esp("propulsion"),
                    self.receive_message_from_esp("braking")
                )

                # Handle messages concurrently if they exist
                tasks = []
                if p_message:
                    print('Propulsion message')
                    tasks.extend([
                        asyncio.create_task(self.send_data_to_api(p_message)),
                    ])

                if b_message:
                    print('Braking message')
                    tasks.extend([
                        asyncio.create_task(self.send_data_to_api(b_message)),
                    ])

                if p_message or b_message:
                    tasks.extend([
                        asyncio.create_task(self.update_fsm(p_message, b_message)),
                    ])
                    await self.websocket_client.send_and_receive(
                        json.dumps({
                            "propulsion": p_message,
                            "braking": b_message
                        })
                    )
                await asyncio.sleep(0.1)

                if tasks:
                    await asyncio.gather(*tasks)

                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            consumer_task.cancel()
            websocket_client.close()
            await websocket_client.wait_closed()
            try:
                await consumer_task
            except asyncio.CancelledError:
                pass




#Test comms
if __name__ == "__main__":
    testcomms = Comms(ESPHandler(port="/dev/cu.usbserial-0001"), ESPHandler(port="/dev/cu.usbserial-0001"))
    asyncio.run(testcomms.start())