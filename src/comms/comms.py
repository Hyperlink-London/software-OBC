# Comms Class
import copy
from typing import Optional, Dict
import asyncio
import json
import time
import uuid

from src.comms.WebsocketClient import WebSocketClient
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut
from src.fsm.fsm import StateMachine
from src.constants import network_constants, ESPConstants, CommsConstants
from src.logger import logger
from src.comms.espHandler import espHandler


class Comms:
    def __init__(self, esp_configs: Dict[str, str]):
        """
        Initialize Comms with a dictionary of ESP configurations.
        
        Args:
            esp_configs: Dictionary mapping ESP names to their port strings
                       e.g., {"braking": "/dev/ttyUSB0", "propulsion": "/dev/ttyUSB1"}
        """
        # Initialize FSM and Websocket
        self.state_machine = StateMachine()
        self.websocket_client = WebSocketClient(network_constants.WEBSOCKET_IP)

        # Initialize ESP handlers
        self.esp_handlers: Dict[str, espHandler] = {
            name: espHandler(name, port)
            for name, port in esp_configs.items()
        }

        # Internal state variables
        self.abort_flag = False
        self.running = True

        self.current_data = MessageIn()

        # Generate unique run ID
        self.run_id = uuid.uuid4()

    async def send_message_to_esp(self, message: MessageOut) -> bool:
        """Send message to all ESPs by default."""
        if self.abort_flag:
            return False
        tasks = [handler.send_data(message) for handler in self.esp_handlers.values()]
        results = await asyncio.gather(*tasks)
        return all(results)

        # if message.recipient and message.recipient in self.esp_handlers:
        #     return await self.esp_handlers[message.recipient].send_data(message)
        # else:
        #     # Send to all ESPs if no specific recipient
        #     tasks = [handler.send_data(message) for handler in self.esp_handlers.values()]
        #     results = await asyncio.gather(*tasks)
        #     return all(results)

    async def receive_message_from_esp(self, device: str) -> Optional[MessageIn]:
        #should this just poll all esp handlers?
        """Receive message from specified ESP."""
        if device in self.esp_handlers:
            return await self.esp_handlers[device].read_data()
        return None

    async def update_current_data(self, messages: list[MessageIn]):
        """Update current data object with messages from ESPs."""
        for message in messages:
            self.current_data.fill_from_data(message)

    async def update_fsm(self) -> MessageOut:
        """Update FSM with current data."""
        logger.debug("Updating FSM")
        self.current_data.fillout_for_testing()#TODO: Remove this for PROD
        fsm_reply = self.state_machine.run_current_state(copy.copy(self.current_data))
        return fsm_reply

    async def process_messages(self, messages: Dict[str, Optional[MessageIn]]):
        """Process messages from all ESPs concurrently."""
        tasks = []
        new_data = []

        async def update_current_data(messages_list: list[MessageIn]):
            """Update current data with messages from ESPs."""
            for message in messages_list:
                self.current_data.fill_from_data(message)

        async def update_fsm() -> MessageOut:
            """Update FSM with current data."""
            logger.debug("Updating FSM")
            self.current_data.fillout_for_testing()#TODO: Remove this for PROD
            fsm_data = self.state_machine.run_current_state(copy.copy(self.current_data))
            return fsm_data
        
        for device, message in messages.items():
            if message:
                tasks.append(self.websocket_client.send_message(message, self.run_id))
                new_data.append(message)

        if tasks:
            await asyncio.gather(*tasks)
            await update_current_data(new_data)
            fsm_return_data = await update_fsm()
            await self.send_message_to_esp(fsm_return_data)
            await self.websocket_client.send_output_message(fsm_return_data,self.run_id)


    # Interface with API

    async def send_data_to_api(self, message: MessageIn) -> bool:
        await self.websocket_client.send_message(message,self.run_id)
        return False

    async def serial_health_check(self):
        """Monitor ESP connections and attempt to reconnect if lost."""
        while True:
            for handler in self.esp_handlers.values():
                if not handler.interface.serial_connection or not handler.interface.serial_connection.is_open:
                    await handler.connect()
            await asyncio.sleep(ESPConstants.ESP_HEALTHCHECK_INTERVAL)

    async def message_timeout_check(self):
        """Monitor ESP message timeouts."""
        while True:
            try:
                # Check timeouts for all ESPs
                timeout_tasks = [handler.check_timeout() for handler in self.esp_handlers.values()]
                responsive_states = await asyncio.gather(*timeout_tasks)

                # Set abort flag if any ESP is unresponsive
                if not all(responsive_states) and not self.abort_flag:
                    logger.error("Setting abort flag due to unresponsive ESP(s)")
                    self.abort_flag = True
                    logger.error(f"Abort flag status: {self.abort_flag}")

                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in message timeout check: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    async def abort_handler(self):
        """Handle sending abort messages while abort flag is set."""
        logger.debug("Starting abort handler")
        while True:
            try:
                if self.abort_flag:
                    logger.warning("Abort flag active - sending abort messages")

                    #TODO: Create abort message
                    abort_message = MessageOut()
                    
                    # Send abort message to all ESPs
                    tasks = [handler.send_data(abort_message) for handler in self.esp_handlers.values()]
                    await asyncio.gather(*tasks)
                    
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in abort handler: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    # Interface with Websockets
    async def websocket_health_check(self):
        """Monitor WebSocket connection health."""
        while True:
            # logger.debug("Running WebSocket health check")
            try:
                if not self.websocket_client.is_connected:
                    logger.debug("WebSocket not connected, attempting to connect...")
                    await self.attempt_websocket_connection()
                else:
                    try:
                        await self.websocket_client.send("health_check")
                        logger.debug("OK: WebSocket is connected")
                    except Exception as e:
                        logger.error(f"Health check failed: {e}")
                        self.websocket_client.is_connected = False  # Mark as disconnected
            except Exception as e:
                logger.error(f"Error in websocket health check: {e}")
                self.websocket_client.is_connected = False  # Mark as disconnected
            await asyncio.sleep(network_constants.WEBSOCKET_HEALTHCHECK_INTERVAL)  # Wait before next health check

    async def attempt_websocket_connection(self):
        """Attempt to establish WebSocket connection."""
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
        """Handle incoming WebSocket messages."""

        async def process_request_from_api(request: dict) -> bool:
            # IF its abort, turn the flag to abort
            # TODO: Logic to process API request and route to FSM or ESPHandler
            pass

        while True:
            try:
                if self.websocket_client and self.websocket_client.is_connected:
                    message = await self.websocket_client.receive()
                    if message:
                        logger.info(f"Received from server: {message}")
                        try:
                            data = json.loads(message)
                            # Process the message
                            await process_request_from_api(data)
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse WebSocket message: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)
            except Exception as e:
                logger.error(f"Error in WebSocket message handler: {e}")
                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

    # Main execution
    async def start(self):
        """Main execution loop."""
        logger.info(f"Running comms with run_id: {self.run_id}")
        # Start background tasks
        background_tasks = [
            asyncio.create_task(self.websocket_health_check()),
            asyncio.create_task(self.serial_health_check()),
            asyncio.create_task(self.message_timeout_check()),
            asyncio.create_task(self.abort_handler()),
            asyncio.create_task(self.handle_websocket_messages())
        ]

        try:
            # Connect to all ESPs
            await asyncio.gather(*[handler.connect() for handler in self.esp_handlers.values()])

            while self.running:
                try:
                    # Get messages from all ESPs concurrently
                    messages = await asyncio.gather(*[
                        self.receive_message_from_esp(name)
                        for name in self.esp_handlers.keys()
                    ])
                    
                    # Process messages if any
                    await self.process_messages(dict(zip(self.esp_handlers.keys(), messages)))

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

                await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

        except Exception as e:
            logger.critical(f"Critical error: {e}")
        finally:
            self.running = False
            for task in background_tasks:
                task.cancel()
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        await self.websocket_client.close()
        for handler in self.esp_handlers.values():
            handler.close()
