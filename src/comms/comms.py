# Comms Class
from typing import Optional
from src.datamodels.message import Message
from ESPHandler import ESPHandler
import asyncio
import json
import time
from WebsocketClient import WebSocketClient
from src.fsm.fsm import StateMachine
from src.constants import network_constants, ESPConstants, CommsConstants
from src.logger import logger


class Comms:
    def __init__(self, braking_coms:ESPHandler, propulsion_coms:ESPHandler):
        self.state_machine = StateMachine()
        self.braking_coms = braking_coms
        self.propulsion_coms = propulsion_coms
        self.message_queue = asyncio.Queue()
        self.websocket_client = WebSocketClient(network_constants.WEBSOCKET_IP)
        self.braking_last_message = 0  # Timestamp of last message from braking ESP
        self.propulsion_last_message = 0  # Timestamp of last message from propulsion ESP
        self.braking_responsive = True
        self.propulsion_responsive = True
        self.abort_flag = False
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
        if not self.abort_flag:
            if message.recipient == "braking":
                return await self.braking_coms.handle_serial(message)
            elif message.recipient == "propulsion":
                return await self.propulsion_coms.handle_serial(message)
            return False
        else:
            return False

    async def receive_message_from_esp(self, device:str) -> Optional[Message]:
        message = None
        if device in ["braking","propulsion"]:
            if device == "braking":
                message = await self.braking_coms.handle_serial()
                if message:
                    self.braking_last_message = message.timestamp
            elif device == "propulsion":
                message = await self.propulsion_coms.handle_serial()
                if message:
                    self.propulsion_last_message = message.timestamp
            return message
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

         #IF its abort, turn the flag to abort
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
                       logger.warning("Failed to send message to WebSocket server")
                else:
                    logger.info("WebSocket not connected, skipping message send")
            except Exception as e:
                logger.error("Error processing message: {e}")
            await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent tight loop

    async def serial_health_check(self):
        """Monitor ESP connections and attempt to reconnect if lost"""
        while True:
            if not self.braking_coms.serial_connection or not self.braking_coms.serial_connection.is_open:
                await self.braking_coms.reconnect()
            if not self.propulsion_coms.serial_connection or not self.propulsion_coms.serial_connection.is_open:
                await self.propulsion_coms.reconnect()
            await asyncio.sleep(ESPConstants.ESP_HEALTHCHECK_INTERVAL)  # Check connection status every second

    async def message_timeout_check(self):
        """Monitor ESP message timeouts"""
        while True:
            current_time = time.time()
            # Check message timestamps
            if current_time - self.braking_last_message > ESPConstants.ESP_MESSAGE_TIMEOUT:
                if self.braking_responsive:
                    logger.warning("Braking ESP message timeout")
                    self.braking_responsive = False
                    # Trigger your callback or event here
            else:
                self.braking_responsive = True
                
            if current_time - self.propulsion_last_message > ESPConstants.ESP_MESSAGE_TIMEOUT:
                if self.propulsion_responsive:
                    logger.warning("Propulsion ESP message timeout")
                    self.propulsion_responsive = False
                    # Trigger your callback or event here
            else:
                self.propulsion_responsive = True

            if not self.braking_responsive or not self.propulsion_responsive:
                self.abort_flag = True
                
            await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    async def abort_handler(self):
        """Handle sending abort messages while abort flag is set"""
        while True:
            try:
                if self.abort_flag:
                    logger.warning("Abort flag active - sending abort messages")
                    abort_message = Message(
                        recipient="both",
                        message_type="command",
                        data={"command": "abort"},
                        timestamp=time.time()
                    )
                    
                    tasks = []
                    # Send to braking ESP
                    abort_message.recipient = "braking"
                    tasks.append(self.braking_coms.handle_serial(abort_message))
                    
                    # Send to propulsion ESP
                    abort_message.recipient = "propulsion"
                    tasks.append(self.propulsion_coms.handle_serial(abort_message))
                    
                    try:
                        await asyncio.gather(*tasks)
                    except Exception as e:
                        logger.error(f"Error sending abort messages: {e}")
                
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in abort handler: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    #Interface with Websockets
    async def websocket_health_check(self):
        while True:
            try:
                if not self.websocket_client.is_connected:
                    logger.debug("WebSocket not connected, attempting to connect...")
                    await self.attempt_websocket_connection()
                else:
                    # Only send health check if already connected
                    try:
                        await self.websocket_client.send("health_check")
                    except Exception as e:
                        logger.error("Health check failed: {e}")
                        self.websocket_client.is_connected = False  # Mark as disconnected
            except Exception as e:
                logger.error(f"Error in websocket health check: {e}")
                self.websocket_client.is_connected = False  # Mark as disconnected
            await asyncio.sleep(network_constants.WEBSOCKET_HEALTHCHECK_INTERVAL)  # Wait before next health check

    async def attempt_websocket_connection(self):
        if self.websocket_client.is_connected:
            return True  # Already connected, no need to reconnect
        
        retry_delay = network_constants.WEBSOCKET_RETRY_DELAY  # seconds
        try:
            logger.info("Attempting WebSocket connection...")
            websocket_client = await self.websocket_client.start()
            if websocket_client:
                logger.info("Successfully connected to WebSocket server!")
                return True
        except Exception as e:
            logger.error(f"Connection attempt failed: {e} Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
        return False

    #Main execution
    async def start(self):
        """Main execution"""

        # Start background tasks
        background_tasks = [
            asyncio.create_task(self.process_queue_messages()),
            asyncio.create_task(self.websocket_health_check()),
            asyncio.create_task(self.serial_health_check()),
            asyncio.create_task(self.message_timeout_check()),
            asyncio.create_task(self.abort_handler())
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
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent tight loop on error
                
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)  # Prevent CPU overload
                
        except Exception as e:
            logger.critical(f"Critical error: {e}")
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