import asyncio

from src.comms.comms import Comms
from src.constants import ESPConstants



if __name__ == "__main__":
    esp_configs = {
        "braking": ESPConstants.BRAKING_ESP_PORT,
        "propulsion": ESPConstants.PROPULSION_ESP_PORT
    }
    Comms = Comms(esp_configs)
    asyncio.run(Comms.start())
