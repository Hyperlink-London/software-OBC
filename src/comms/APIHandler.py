from typing import Optional

import aiohttp
import asyncio
from aiohttp import web
from message import Message
import json


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
        self.message:Message = None
        self.queue = None

        # Define route for processing requests
        self.app.router.add_post('/api/process', self.process_request_from_api)

    def set_queue(self, queue: asyncio.Queue):
        """Set the queue for inter-process communication."""
        self.queue = queue

    async def _send_post_request(self, endpoint: str, payload: dict) -> bool:
        """
        Helper method to send HTTP POST requests.

        Args:
            endpoint (str): The endpoint to send the POST request.
            payload (dict): The payload data to send.

        Returns:
            bool: True if the request is successful, False otherwise.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        print(f"POST request to {endpoint} succeeded.")
                        return True
                    else:
                        print(f"POST request to {endpoint} failed with status: {response.status}")
                        return False
        except aiohttp.ClientError as e:
            print(f"Error in POST request to {endpoint}: {e}")
            return False

    async def send_data_to_api(self, message:Message):
        #process the message into a payload here
        return await self._send_post_request("PLACEHOLDER",payload=None)

    async def process_request_from_api(self, request: web.Request) -> web.Response:
        """
        Process incoming API requests to route data to either the FSM or ESPHandler.

        Args:
            request (web.Request): The HTTP request from the client.

        Returns:
            web.Response: A response confirming the processing result.
        """
        try:
            data = await request.json()
            print(f"Processing data from API: {data}")
            message = None # Placeholder
           #TODO: parse json into message object
            if self.queue:
                await self.queue.put(message)
            return web.Response(status=200, text="Request processed successfully.")
        except Exception as e:
            print(f"Error processing request: {e}")
            return web.Response(status=500, text="Error processing request.")

    async def start_server(self):
        # """Start the HTTP server to listen for requests on the specified port."""
        # runner = web.AppRunner(self.app)
        # await runner.setup()
        # site = web.TCPSite(runner, '127.0.0.1', self.port)
        # await site.start()
        # print(f"Server started, listening on port {self.port}")
        # Set up WebSocket endpoint
        self.app.router.add_get('/ws', self.websocket_handler)
        print("WebSocket endpoint configured at /ws")

    async def websocket_handler(self, request):
        """Handle WebSocket connections and messages."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print("WebSocket connection established")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        print(f"Received WebSocket message: {data}")
                        message = None  # TODO: parse json into message object similar to HTTP endpoint
                        if self.queue:
                            await self.queue.put(message)
                        await ws.send_str(json.dumps({"status": "success"}))
                    except json.JSONDecodeError:
                        await ws.send_str(json.dumps({"status": "error", "message": "Invalid JSON"}))
                elif msg.type == web.WSMsgType.ERROR:
                    print(f"WebSocket connection closed with exception {ws.exception()}")
        finally:
            print("WebSocket connection closed")
            return ws
