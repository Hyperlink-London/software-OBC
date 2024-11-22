import asyncio
import websockets

class WebSocketClient:
    def __init__(self, server_uri: str):
        self.server_uri = server_uri
        self.connection = None
        self.is_connected = False

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            # print(f"Connecting to WebSocket server at {self.server_uri}...")
            self.connection = await websockets.connect(self.server_uri)
            self.is_connected = True
            # print("Connected to WebSocket server.")
            return self.connection
        except websockets.exceptions.WebSocketException as e:
            print(f"Failed to connect to WebSocket server: {e}")
            self.is_connected = False
            return None

    async def send(self, message: str):
        """Send a single message to the server and process the response."""
        if not self.is_connected:
            print("Not connected to server. Message will be skipped.")
            return False

        try:
            print(f"Sending: {message}")
            await self.connection.send(message)
            return True
        except websockets.ConnectionClosed:
            print("Connection to the server was closed.")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    async def receive(self):
        """Receive a message from the server."""
        if not self.is_connected:
            print("Not connected to server. Attempting to reconnect...")
            await self.connect()
            if not self.is_connected:
                return None

        try:
            response = await self.connection.recv()
            print(f"Received from server: {response}")
            return response
        except websockets.ConnectionClosed:
            print("Connection to the server was closed.")
            self.is_connected = False
            return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            self.is_connected = False
            return None

    async def close(self):
        """Close the WebSocket connection."""
        if self.connection:
            try:
                await self.connection.close()
                print("Disconnected from WebSocket server.")
            except Exception as e:
                print(f"Error closing connection: {e}")
            finally:
                self.is_connected = False

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