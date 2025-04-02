from typing import Optional
import time
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut
from src.logger import logger
from src.constants import ESPConstants
from espInterface import espInterface

class espHandler:
    def __init__(self, name: str, port: str):
        """
        Initialize ESPHandler with specified connection parameters.
        
        Args:
            name: Unique identifier for this ESP (e.g., "braking", "propulsion")
            port: Serial port to connect to
        """
        self.name = name
        self.port = port
        self.interface = espInterface(port=port)
        self.last_message = None
        self.responsive = True

    async def connect(self) -> bool:
        """Attempt to establish a serial connection with retry logic."""
        return await self.interface.connect()

    async def read_data(self) -> Optional[MessageIn]:
        """Read data from the ESP device."""
        message = await self.interface.read_data()
        if message:
            self.last_message = message.timestamp
        return message

    async def send_data(self, message: MessageOut) -> bool:
        """Send data to the ESP device."""
        if not self.interface.serial_connection or not self.interface.serial_connection.is_open:
            return await self.interface.reconnect()
        await self.interface.send_data(message)
        return True

    async def check_timeout(self) -> bool:
        """Check if the ESP has timed out based on last message timestamp."""
        if self.last_message is None:
            return True  # Consider as responsive if no messages yet

        current_time = time.time()
        delta = current_time - self.last_message
        
        if delta > ESPConstants.ESP_TIMEOUT:
            if self.responsive:
                logger.warning(f"{self.name} ESP timeout after {delta:.2f}s")
                self.responsive = False
            return False
        else:
            if not self.responsive:
                logger.info(f"{self.name} ESP responsive again")
            self.responsive = True
            return True

    def close(self):
        """Close the serial connection."""
        self.interface.close_connection() 