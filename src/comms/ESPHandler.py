import serial
import asyncio

from src.logger import logger
from src.datamodels.message import Message
from src.constants import ESPConstants

class ESPHandler:
    def __init__(self, port: str):
        """
        Initialize ESPHandler with specified connection parameters.
        """
        self.port = port
        self.baudrate:int = ESPConstants.ESP_BAUDRATE
        self.timeout:int = ESPConstants.ESP_TIMEOUT
        self.retry_interval:int = ESPConstants.ESP_RETRY_INTERVAL
        self.serial_connection = None

    async def connect(self):
        """
        Attempt to establish a serial connection with retry logic.
        """
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Successfully connected to {self.port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Connection failed: {e} Retrying in {self.retry_interval} seconds...")
            await asyncio.sleep(self.retry_interval)

    async def read_data(self) -> str:
        """
        Read data from the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            connected = await self.reconnect()
            if not connected:
                return ""

        try:
            data = self.serial_connection.readline()
            if data:
                decoded_data = data.decode('utf-8').strip()
                logger.debug(f"Received data: {decoded_data}")
                return decoded_data
        except serial.SerialException:
            logger.error("Error reading data; attempting to reconnect.")
            await self.reconnect()
        return ""

    async def send_data(self, message: Message) -> None:
        """
        Send data to the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            connected = await self.reconnect()
            if not connected:
                return

        message.message_to_esp()
        data = "PLACEHOLDER"
        try:
            self.serial_connection.write(data.encode('utf-8'))
            logger.debug(f"Sent data: {data}")
        except serial.SerialException:
            logger.error("Error sending data; attempting to reconnect.")
            await self.reconnect()

    async def reconnect(self) -> bool:
        """
        Attempt to reconnect to the ESP device if the connection is lost.
        """
        if self.serial_connection:
            self.serial_connection.close()
        return await self.connect()

    def close_connection(self) -> None:
        """
        Close the serial connection if it's open.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info(f"Connection to {self.port} closed.")

    async def handle_serial(self, data: Message = None):
        """
        Asynchronously handle reading and sending data.
        If data is provided, it will be sent; otherwise, data will be read.
        """
        try:
            if data:
                await self.send_data(data)
                return True
            else:
                logger.debug("Reading data...")
                received_data = await self.read_data()
                if received_data:
                    return received_data
                return None
                
        except serial.SerialException as e:
            logger.error(f"Serial error: {e}")
            await self.reconnect()
            return None
        except Exception as e:
            logger.critical(f"Unexpected error in handle_serial: {e}")
            return None