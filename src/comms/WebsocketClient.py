import asyncio
import websockets

class WebSocketClient:
    def __init__(self, server_uri: str):
        self.server_uri = server_uri

    async def connect(self):
        """Connect to the WebSocket server."""
        print(f"Connecting to WebSocket server at {self.server_uri}...")
        self.connection = await websockets.connect(self.server_uri)
        print("Connected to WebSocket server.")

    async def send_and_receive(self, message: str):
        """Send a single message to the server and process the response."""
        try:
            print(f"Sending: {message}")
            await self.connection.send(message)

            # Wait for a response
            response = await self.connection.recv()
            print(f"Received from server: {response}")
            return response
            
        except websockets.ConnectionClosed:
            print("Connection to the server was closed.")
        except KeyboardInterrupt:
            print("Client interrupted. Closing connection...")

    async def run(self):
        """Main logic to handle connection and messaging."""
        await self.connect()
        await self.send_and_receive("Hello from client")

    async def close(self):
        """Close the WebSocket connection."""
        if self.connection:
            await self.connection.close()
            print("Disconnected from WebSocket server.")

# Example usage
async def main():
    # Replace with the URI of your WebSocket server
    client = WebSocketClient("ws://localhost:8000/hyperlink/api/v1/ws/data")
    try:
        await client.run()
    except KeyboardInterrupt:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())