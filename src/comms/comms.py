# Comms Class
from typing import Optional
from src.datamodels.message import Message
from ESPHandler import ESPHandler
import asyncio
import json
from WebsocketClient import WebSocketClient
from src.fsm.fsm import StateMachine
from src.constants import network_constants, ESPConstants, CommsConstants


#TODO: Add Logger logic



class Comms:
    def __init__(self, braking_coms:ESPHandler, propulsion_coms:ESPHandler):
        self.state_machine = StateMachine()
        self.braking_coms = braking_coms
        self.propulsion_coms = propulsion_coms
        self.message_queue = asyncio.Queue()
        self.websocket_client = WebSocketClient(network_constants.WEBSOCKET_IP)
        self.running = True
        
    async def process_messages(self, p_message: Message, b_message: Message):
        """Process messages from both ESPs concurrently"""
        tasks = []
        
        if p_message or b_message:
            # Create API tasks
            if p_message:
                tasks.append(self.send_data_to_api(p_message))
            if b_message:
                tasks.append(self.send_data_to_api(b_message))
                
            # Update FSM
            tasks.append(self.update_fsm(p_message, b_message))
            
            # Send to WebSocket
            ws_data = json.dumps({
                "propulsion": p_message,
                "braking": b_message
            })
            tasks.append(self.websocket_client.send(ws_data))
            
            # Execute all tasks concurrently
            await asyncio.gather(*tasks)



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
        data = None
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
                if self.websocket_client and self.websocket_client.is_connected:
                    success = await self.websocket_client.send(message)
                    if not success:
                        print("Failed to send message to WebSocket server")
                else:
                    print("WebSocket not connected, skipping message send")
            except Exception as e:
                print(f"Error processing message: {e}")
            await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent tight loop

    async def serial_health_check(self):
        """Monitor ESP connections and attempt to reconnect if lost"""
        while True:
            if not self.braking_coms.serial_connection or not self.braking_coms.serial_connection.is_open:
                await self.braking_coms.reconnect()
            if not self.propulsion_coms.serial_connection or not self.propulsion_coms.serial_connection.is_open:
                await self.propulsion_coms.reconnect()
            await asyncio.sleep(ESPConstants.ESP_HEALTHCHECK_INTERVAL)  # Check connection status every second

    #Interface with Websockets
    async def websocket_health_check(self):
        while True:
            try:
                if not self.websocket_client.is_connected:
                    print("WebSocket not connected, attempting to connect...")
                    await self.attempt_websocket_connection()
                else:
                    # Only send health check if already connected
                    try:
                        await self.websocket_client.send("health_check")
                    except Exception as e:
                        print(f"Health check failed: {e}")
                        self.websocket_client.is_connected = False  # Mark as disconnected
            except Exception as e:
                print(f"Error in websocket health check: {e}")
                self.websocket_client.is_connected = False  # Mark as disconnected
            await asyncio.sleep(network_constants.WEBSOCKET_HEALTHCHECK_INTERVAL)  # Wait before next health check

    async def attempt_websocket_connection(self):
        if self.websocket_client.is_connected:
            return True  # Already connected, no need to reconnect
        
        retry_delay = network_constants.WEBSOCKET_RETRY_DELAY  # seconds
        try:
            print(f"Attempting WebSocket connection...")
            websocket_client = await self.websocket_client.start()
            if websocket_client:
                print("Successfully connected to WebSocket server!")
                return True
        except Exception as e:
            print(f"Connection attempt failed: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
        return False

    #Main execution
    async def start(self):
        # Start background tasks
        background_tasks = [
            asyncio.create_task(self.process_queue_messages()),
            asyncio.create_task(self.websocket_health_check()),
            asyncio.create_task(self.serial_health_check())
        ]
        
        try:
            # Initial connections
            brake_connected, prop_connected = await asyncio.gather(
                self.braking_coms.connect(),
                self.propulsion_coms.connect()
            )
            
            while self.running:
                try:
                    # Get messages from both ESPs concurrently
                    p_message, b_message = await asyncio.gather(
                        self.receive_message_from_esp("propulsion"),
                        self.receive_message_from_esp("braking")
                    )
                    
                    # Process messages if any
                    await self.process_messages(p_message, b_message)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error in main loop: {e}")
                    await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent tight loop on error
                
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent CPU overload
                
        except Exception as e:
            print(f"Critical error: {e}")
        finally:
            # Cleanup
            self.running = False
            for task in background_tasks:
                task.cancel()
            await self.cleanup()
            
    async def cleanup(self):
        await self.websocket_client.close()
        self.braking_coms.close_connection()
        self.propulsion_coms.close_connection()




#Test comms
if __name__ == "__main__":
    testcomms = Comms(ESPHandler(port=ESPConstants.BRAKING_ESP_PORT), ESPHandler(port=ESPConstants.PROPULSION_ESP_PORT))
    asyncio.run(testcomms.start())