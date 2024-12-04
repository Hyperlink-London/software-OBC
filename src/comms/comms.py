# Comms Class
import copy
from typing import Optional
from ESPHandler import ESPHandler
import asyncio
import json
import time
import uuid
from WebsocketClient import WebSocketClient
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut
from src.fsm.fsm import StateMachine
from src.constants import network_constants, ESPConstants, CommsConstants
from src.logger import logger


class Comms:
    def __init__(self, braking_coms: ESPHandler, propulsion_coms: ESPHandler):
        #Initialize FSM, ESPs, and Websocket
        self.state_machine = StateMachine()
        self.braking_coms = braking_coms
        self.propulsion_coms = propulsion_coms
        self.websocket_client = WebSocketClient(network_constants.WEBSOCKET_IP)

        #Internal state variables
        self.braking_last_message = None  # Initialize as None
        self.propulsion_last_message = None  # Initialize as None
        self.braking_responsive = True
        self.propulsion_responsive = True
        self.abort_flag = False
        self.running = True

        self.current_data = MessageIn()

        # Generate unique run ID
        self.run_id = uuid.uuid4()

    # Interface with ESP
    #TODO: Fix this to handle the message properly
    async def send_message_to_esp(self, message: MessageOut) -> MessageIn | None | bool:
        if not self.abort_flag:
            if message.recipient == "braking":
                return await self.braking_coms.handle_serial(message)
            elif message.recipient == "propulsion":
                return await self.propulsion_coms.handle_serial(message)
            return False
        else:
            return False

    async def receive_message_from_esp(self, device: str) -> Optional[MessageIn]:
        message = None
        if device in ["braking", "propulsion"]:
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
            return None

    async def process_messages(self, p_message: MessageIn, b_message: MessageIn):
        """Process messages from both ESPs concurrently"""
        # logger.debug("Processing messages...")
        tasks = []
        new_data=[]
        if p_message or b_message:
            if p_message:
                tasks.append(self.send_data_to_api(p_message))
                new_data.append(p_message)

            if b_message:
                tasks.append(self.send_data_to_api(b_message))
                new_data.append(b_message)

            await asyncio.gather(*tasks)
            await self.update_current_data(new_data)
            await self.update_fsm()

    async def update_current_data(self , messages: list[MessageIn]):
        for message in messages:
            self.current_data.update_from_data(message)
        pass

    # Interface with FSM
    async def update_fsm(self) -> MessageOut:
        fsm_data = self.state_machine.run_current_state(copy.copy(self.current_data))#passes a copy of the data to the fsm
        #Deal with returned data
        pass

    # Interface with API
    async def process_request_from_api(self, request: dict) -> bool:

        # IF its abort, turn the flag to abort
        # TODO: Logic to process API request and route to FSM or ESPHandler
        pass

    async def send_data_to_api(self, message: MessageIn) -> bool:
        await self.websocket_client.send_message(message,self.run_id)
        return False

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
            try:
                current_time = time.time()
                
                # Only check timeouts if we've received at least one message
                if self.braking_last_message is not None:
                    braking_delta = current_time - self.braking_last_message
                    logger.info(f"Braking delta: {braking_delta:.2f}s, Timeout threshold: {ESPConstants.ESP_TIMEOUT}s")
                    
                    if braking_delta > ESPConstants.ESP_TIMEOUT:
                        if self.braking_responsive:
                            #logger.warning(f"Braking ESP timeout after {braking_delta:.2f}s")
                            self.braking_responsive = False
                    else:
                        if not self.braking_responsive:
                            #logger.info("Braking ESP responsive again")
                            self.braking_responsive = True
                else:
                    pass
                    #logger.warning("No braking messages received yet")
                
                if self.propulsion_last_message is not None:
                    prop_delta = current_time - self.propulsion_last_message
                    logger.info(f"Propulsion delta: {prop_delta:.2f}s, Timeout threshold: {ESPConstants.ESP_TIMEOUT}s")
                    
                    if prop_delta > ESPConstants.ESP_TIMEOUT:
                        if self.propulsion_responsive:
                            logger.warning(f"Propulsion ESP timeout after {prop_delta:.2f}s")
                            self.propulsion_responsive = False
                    else:
                        if not self.propulsion_responsive:
                            logger.info("Propulsion ESP responsive again")
                        self.propulsion_responsive = True
                else:
                    pass
                    #logger.warning("No propulsion messages received yet")

                # Set abort flag if either ESP is unresponsive
                if not self.braking_responsive or not self.propulsion_responsive:
                    if not self.abort_flag:
                        logger.error("Setting abort flag due to unresponsive ESP(s)")
                        self.abort_flag = True
                        logger.error(f"Abort flag status: {self.abort_flag}")
                
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in message timeout check: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    async def abort_handler(self):
        """Handle sending abort messages while abort flag is set"""
        logger.debug("Starting abort handler")
        while True:
            try:
                if self.abort_flag:
                    logger.warning("Abort flag active - sending abort messages")
                    
                    # Create abort messages for each ESP
                    braking_abort = MessageOut()
                    propulsion_abort = MessageOut()
                    
                    # Send to both ESPs without awaiting response
                    asyncio.create_task(self.braking_coms.handle_serial(braking_abort))
                    asyncio.create_task(self.propulsion_coms.handle_serial(propulsion_abort))
                    
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in abort handler: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    # Interface with Websockets
    async def websocket_health_check(self):
        while True:
            logger.debug("Running WebSocket health check")
            try:
                if not self.websocket_client.is_connected:
                    logger.debug("WebSocket not connected, attempting to connect...")
                    await self.attempt_websocket_connection()
                else:
                    # Only send health check if already connected
                    try:
                        await self.websocket_client.send("health_check")
                    except Exception as e:
                        logger.error(f"Health check failed: {e}")
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

    async def handle_websocket_messages(self):
        """Handle incoming WebSocket messages"""
        while True:
            try:
                if self.websocket_client and self.websocket_client.is_connected:
                    message = await self.websocket_client.receive()
                    if message:
                        logger.info(f"Received WebSocket message: {message}")
                        try:
                            data = json.loads(message)
                            # Process the message
                            await self.process_request_from_api(data)
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse WebSocket message: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in WebSocket message handler: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    # Main execution
    async def start(self):
        """Main execution"""
        logger.info(f"Running Comms with run_id: {self.run_id}")
        # Start background tasks
        background_tasks = [
            asyncio.create_task(self.websocket_health_check()),
            asyncio.create_task(self.serial_health_check()),
            asyncio.create_task(self.message_timeout_check()),
            asyncio.create_task(self.abort_handler()),
            asyncio.create_task(self.handle_websocket_messages())
        ]

        try:
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


# Test comms
if __name__ == "__main__":
    testcomms = Comms(ESPHandler(port=ESPConstants.BRAKING_ESP_PORT), ESPHandler(port=ESPConstants.PROPULSION_ESP_PORT))
    asyncio.run(testcomms.start())
