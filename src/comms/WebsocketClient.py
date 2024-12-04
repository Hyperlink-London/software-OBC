import asyncio
import json

import websockets
from src.constants import network_constants, CommsConstants
from src.datamodels.message_in import MessageIn
from src.logger import logger


class WebSocketClient:
    def __init__(self, server_uri: str):
        self.server_uri = server_uri
        self.connection = None
        self.is_connected = False
        # self.message_queue = asyncio.Queue() #Queue for messages when connection is down

    async def start(self):
        """Start the WebSocket client and queue processor"""
        await self.connect()
        # self.queue_processor_task = asyncio.create_task(self.process_queue())

    async def connect(self):
        """Connect to the WebSocket server."""
        if self.connection:
            await self.connection.close()

        self.connection = await websockets.connect(
            self.server_uri,
            close_timeout=network_constants.WEBSOCKET_CLOSE_TIMEOUT
        )
        self.is_connected = True
        logger.info("Successfully connected to WebSocket server")
        return True

    async def send(self, message: str):
        if not self.is_connected:
            logger.info("Not connected to server. Discarding message...")
            return False

        try:
            #logger.debug(f"Sending: {message}")
            await self.connection.send(message)
            return True
        except websockets.ConnectionClosed:
            logger.info("Connection closed normally")
            self.is_connected = False
            return False
        except Exception as e:
            logger.error(f"Send error: {e}")
            # Don't immediately set is_connected to False
            # Let the health check handle reconnection
            return False

    async def receive(self):
        """Receive a message from the server."""
        if not self.is_connected:
            logger.info("Not connected to server. Attempting to reconnect...")
            await self.connect()
            if not self.is_connected:
                return None

        try:
            response = await self.connection.recv()
            logger.debug(f"Received from server: {response}")
            return response
        except websockets.ConnectionClosed:
            logger.info("Connection to the server was closed.")
            self.is_connected = False
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            self.is_connected = False
            return None

    async def close(self):
        """Close the WebSocket connection."""
        if self.connection:
            try:
                await self.connection.close()
                logger.info("Disconnected from WebSocket server.")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
            finally:
                self.is_connected = False

    async def send_message(self, message: MessageIn, run_id):
        temp = message.__dict__
        temp["run_id"] = str(run_id)
        await self.send(json.dumps(temp))

    # async def queue_message(self, message: str):
    #     """Queue messages when connection is down"""
    #     await self.message_queue.put(message)

    # async def process_queue(self):
    #     """Process queued messages"""
    #     while True:
    #         if self.is_connected and not self.message_queue.empty():
    #             message = await self.message_queue.get()
    #             success = await self.send(message)
    #         await asyncio.sleep(CommsConstants.ASYNCIO_SLEEP)

# Example usage
# async def main():
#     # Replace with the URI of your WebSocket server
#     client = WebSocketClient("ws://localhost:8000/hyperlink/api/v1/ws/data")
#     try:
#         await client.run()
#     except KeyboardInterrupt:
#         await client.close()
#
# if __name__ == "__main__":
#     asyncio.run(main())
