import aiohttp
import asyncio
from aiohttp import web
from src.comms.message import Message


class APIHandler:
    def __init__(self, base_url: str, port: int):
        """
        Initialize APIHandler to handle incoming HTTP requests and send data from ESP/FSM to the dashboard.

        Args:
            base_url (str): The base URL of the dashboard API to which data will be sent.
            port (int): The port on which the HTTP server will listen for incoming requests.
        """
        self.base_url = base_url
        self.port = port
        self.app = web.Application()

        # Define the routes for incoming API requests
        self.app.router.add_post('/api/process', self.process_request_from_api)

    async def send_data_to_dashboard(self, data: str) -> bool:
        """
        Send data from ESP or FSM to the dashboard via HTTP POST request.

        Args:
            data (str): The data to send to the dashboard.

        Returns:
            bool: True if the data is successfully sent, False otherwise.
        """
        url = f"{self.base_url}/dashboard/data"
        payload = {'data': data}  # You can adjust the payload format as needed

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print(f"Data sent successfully to dashboard.")
                        return True
                    else:
                        print(f"Failed to send data, status: {response.status}")
                        return False
        except aiohttp.ClientError as e:
            print(f"Error sending data to dashboard: {e}")
            return False

    async def send_message_to_dashboard(self, message: Message) -> bool:
        """
        Send a Message object from ESP/FSM to the dashboard via HTTP request.

        Args:
            message (Message): The Message object containing the data to send.

        Returns:
            bool: True if the message is successfully sent, False otherwise.
        """
        url = f"{self.base_url}/dashboard/message"
        payload = {'message': message.content}  # Assuming Message has a 'content' attribute

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print(f"Message sent successfully to dashboard.")
                        return True
                    else:
                        print(f"Failed to send message, status: {response.status}")
                        return False
        except aiohttp.ClientError as e:
            print(f"Error sending message to dashboard: {e}")
            return False

    async def send_command_status(self, command: str, status: str) -> bool:
        """
        Send the status of a command (e.g., success or failure) to the dashboard.

        Args:
            command (str): The command that was sent.
            status (str): The status of the command (e.g., 'success' or 'failure').

        Returns:
            bool: True if the command status is successfully sent, False otherwise.
        """
        url = f"{self.base_url}/dashboard/command_status"
        payload = {'message': f"Command: {command}, Status: {status}"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print(f"Command status sent successfully to dashboard.")
                        return True
                    else:
                        print(f"Failed to send command status, status: {response.status}")
                        return False
        except aiohttp.ClientError as e:
            print(f"Error sending command status to dashboard: {e}")
            return False

    async def process_request_from_api(self, request: web.Request) -> web.Response:
        """
        Process incoming API requests to route data to either the FSM or ESPHandler.

        Args:
            request (web.Request): The HTTP request from the client.

        Returns:
            web.Response: A response to the client confirming the processing result.
        """
        try:
            data = await request.json()  # Expecting JSON request body
            print(f"Processing data from API: {data}")

            # Route data to the FSM or ESPHandler, depending on your business logic
            # Example: you could check the type of data and route it to the appropriate handler
            if 'command' in data:
                command = data['command']
                # Send the command to FSM or ESPHandler
                print(f"Received command: {command}")
                await self.send_command_status(command, 'received')  # Example of sending command status
            elif 'message' in data:
                message = Message(data['message'])
                await self.send_message_to_dashboard(message)

            return web.Response(status=200, text="Request processed successfully.")
        except Exception as e:
            print(f"Error processing request: {e}")
            return web.Response(status=500, text="Error processing request.")

    async def start_server(self):
        """Start the HTTP server to listen for requests on the specified port."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)  # Listen on all interfaces
        await site.start()
        print(f"Server started, listening on port {self.port}")

    def stop_server(self):
        """Stop the HTTP server."""
        pass  # Implement if you need to shut down the server


# Example usage:
async def main():
    api_handler = APIHandler(base_url="http://example.com", port=8080)
    await api_handler.start_server()

# Run the asyncio event loop to start the server
if __name__ == "__main__":
    asyncio.run(main())