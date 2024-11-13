import serial
import time
import logging
import asyncio
import threading

class ESPHandler:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1, max_retries: int = 5, retry_interval: int = 3):
        """
        Initialize ESPHandler with specified connection parameters.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.serial_connection = None

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """
        Attempt to establish a serial connection with retry logic.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
                self.logger.info(f"Successfully connected to {self.port}")
                return True
            except serial.SerialException as e:
                self.logger.error(f"Connection failed: {e}")
                retries += 1
                self.logger.info(f"Retrying in {self.retry_interval} seconds... ({retries}/{self.max_retries})")
                time.sleep(self.retry_interval)

        self.logger.error("Maximum connection retries exceeded.")
        return False

    def read_data(self) -> str:
        """
        Read data from the ESP device.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline()
                if data:
                    decoded_data = data.decode('utf-8').strip()
                    self.logger.info(f"Received data: {decoded_data}")
                    return decoded_data
                else:
                    self.logger.warning("No data received.")
                    return ""
            except serial.SerialException as e:
                self.logger.error(f"Error reading data: {e}")
                self.reconnect()
                return ""
        else:
            self.logger.warning("No active connection to read from.")
            return ""

    def send_data(self, data: str) -> None:
        """
        Send data to the ESP device.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(data.encode('utf-8'))
                self.logger.info(f"Sent data: {data}")
            except serial.SerialException as e:
                self.logger.error(f"Error sending data: {e}")
                self.reconnect()

    def reconnect(self) -> bool:
        """
        Attempt to reconnect to the ESP device if the connection is lost.
        """
        self.logger.info("Attempting to reconnect...")
        if self.serial_connection:
            self.serial_connection.close()
        return self.connect()

    def close_connection(self) -> None:
        """
        Close the serial connection if it's open.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.logger.info(f"Connection to {self.port} closed.")

    def _serial_thread(self, loop: asyncio.BaseEventLoop):
        """This function runs in a separate thread to handle serial communication."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_async(self):
        """
        Starts an async event loop in a separate thread for handling serial communication.
        """
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self._serial_thread, args=(loop,))
        thread.daemon = True
        thread.start()

    async def async_read(self):
        """Asynchronously read data."""
        while True:
            data = self.read_data()
            if data:
                await asyncio.sleep(1)

    async def async_send(self, data):
        """Asynchronously send data."""
        self.send_data(data)
        await asyncio.sleep(1)

# Test the ESPHandler class asynchronously
async def main():
    esp = ESPHandler(port='/dev/cu.usbserial-0001')
    if esp.connect():
        await esp.async_send("Hello, ESP!")
        await esp.async_read()

if __name__ == "__main__":
    asyncio.run(main())