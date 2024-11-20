import serial
import asyncio

from src.datamodels.message import Message


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

    async def connect(self):
        """
        Attempt to establish a serial connection with retry logic.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
                print(f"Successfully connected to {self.port}")
                return True
            except serial.SerialException as e:
                print(f"Connection failed: {e}")
                retries += 1
                print(f"Retrying in {self.retry_interval} seconds... ({retries}/{self.max_retries})")
                await asyncio.sleep(self.retry_interval)
        print("Maximum connection retries exceeded.")
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
                    print(f"Received data: {decoded_data}")
                    #Create message object and verify validity
                    #return message object
                    return decoded_data
            except serial.SerialException:
                print("Error reading data; attempting to reconnect.")
                self.reconnect()
        return ""

    def send_data(self, message:Message) -> None:
        """
        Send data to the ESP device.
        """
        message.message_to_esp()
        data = "PLACEHOLDER"
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(data.encode('utf-8'))
                print(f"Sent data: {data}")
            except serial.SerialException:
                print("Error sending data; attempting to reconnect.")
                self.reconnect()

    def reconnect(self) -> bool:
        """
        Attempt to reconnect to the ESP device if the connection is lost.
        """
        if self.serial_connection:
            self.serial_connection.close()
        return self.connect()

    def close_connection(self) -> None:
        """
        Close the serial connection if it's open.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Connection to {self.port} closed.")

    async def handle_serial(self, data: Message = None):
        """
        Asynchronously handle reading and sending data.
        If data is provided, it will be sent; otherwise, data will be read.
        """
        if data:
            self.send_data(data)
        else:
            print("Reading data...")
            received_data = self.read_data()
            await asyncio.sleep(0.2)  # Short delay to avoid overwhelming the loop
            return received_data
