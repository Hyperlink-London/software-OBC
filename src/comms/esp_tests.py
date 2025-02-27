import asyncio
from unittest.mock import patch, MagicMock
from src.comms.ESPHandler import ESPHandler
from src.datamodels.message_in import MessageIn
from src.datamodels.message_out import MessageOut

async def test_handle_data():
    a = esp_handler = ESPHandler("/dev/ttys011")

    while True:
        data = await esp_handler.handle_serial(None)
        if data:
            print(data)


# Run the test
asyncio.run(test_handle_data())