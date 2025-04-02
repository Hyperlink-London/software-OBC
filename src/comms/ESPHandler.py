from typing import Optional
import serial
import asyncio

from src.datamodels.message_out import MessageOut
from src.logger import logger
from src.datamodels.message_in import MessageIn
from src.constants import ESPConstants

import json


class ESPHandler:
    def __init__(self, port: str):
        """
        Initialize ESPHandler with specified connection parameters.
        """
        self.port = port
        self.baudrate: int = ESPConstants.ESP_BAUDRATE
        self.timeout: int = ESPConstants.ESP_TIMEOUT
        self.retry_interval: int = ESPConstants.ESP_RETRY_INTERVAL
        self.serial_connection = None

    async def connect(self):
        """
        Attempt to establish a serial connection with retry logic.
        """
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=None)
            logger.info(f"Successfully connected to {self.port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Connection failed for {self.port}: {e} Retrying in {self.retry_interval} seconds...")
            await asyncio.sleep(self.retry_interval)

    async def read_data(self) -> str:
        """
        Read data from the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            connected = await self.reconnect()
            if not connected:
                logger.debug("Failed to connect to serial device")
                return ""  # TODO: improve error handling

        try:
            data = self.serial_connection.readline()
            if data:
                filtered_data = data.replace(b'\x00', b'')
                decoded_data = filtered_data.decode('utf-8').strip()
                logger.debug(f"Received data: {decoded_data}")
                return decoded_data
        except serial.SerialException:
            logger.error("Error reading data; attempting to reconnect.")
            await self.reconnect()
        return ""

    async def send_data(self, message: MessageOut) -> None:
        """
        Send data to the ESP device.
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            connected = await self.reconnect()
            if not connected:
                return
        data = message.message_to_esp()
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

    async def handle_serial(self, message: MessageOut=None)-> Optional[MessageIn]:
        """
        Asynchronously handle reading and sending data.
        If data is provided, it will be sent; otherwise, data will be read.
        """
        try:
            if message:
                await self.send_data(message)
                return True
            else:
                # logger.debug("Attempting to read data from ESP.")
                received_data = await self.read_data()
                if received_data:
                    if received_data[0] == '{' and received_data[-1] == '}':
                        from_esp = MessageIn()
                        from_esp.add_data_from_json(received_data)
                        logger.debug(f"Received JSON: {from_esp}")
                        return from_esp
                    else:
                        return None
                else:
                    return None
        except serial.SerialException as e:
            logger.error(f"Serial error: {e}")
            await self.reconnect()
            return None
        except Exception as e:
            logger.critical(f"Unexpected error in handle_serial: {e}")
            return None
