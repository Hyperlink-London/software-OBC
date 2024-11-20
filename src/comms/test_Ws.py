import asyncio
import websockets
import json


async def websocket_client():
    # Simplified URI - let's test basic connection first
    uri = "ws://localhost:8000/ws"  # Removed path for initial testing

    try:
        print(f"Attempting to connect to {uri}")
        async with websockets.connect(uri) as websocket:
            print("Connection established!")
            # Simple ping message
            await websocket.send(json.dumps({
                "temperature_celsius_brake": 9999,
                "temperature_celsius_propulsion_1": 0,
                "temperature_celsius_propulsion_2": 0,
                "rpm": 0,
                "speed_m_per_s": 0,
                "brake_version": "string",
                "propulsion_version": "string",
                "pod_version": "string"
            }))
            response = await websocket.recv()
            print(f"Received: {response}")

    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {str(e)}")
    except Exception as e:
        print(f"General error: {e}")


if __name__ == "__main__":
    # Fix for deprecation warning - use asyncio.run instead
    asyncio.run(websocket_client())
