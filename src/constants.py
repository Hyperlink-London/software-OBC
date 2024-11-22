import os
from dotenv import load_dotenv

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(src_dir, '..'))
env_file_path = os.path.join(project_dir, '.env')

load_dotenv(dotenv_path=env_file_path)

# TODO: Update each to the correct version after the each release
OBC_VERSION = "V0.0.1"  # V0.0.1:  initial commit
FSM_VERSION = "V0.0.1"  # V0.0.1:  initial commit
DATAMODELS_VERSION = "V0.0.1"  # V0.0.1:  initial commit
COMMS_VERSION = "V0.0.1"  # V0.0.1:  initial commit


class NetworkConstants:
    WEBSOCKET_IP = os.getenv("WEBSOCKET_IP")
    WEBSOCKET_CLOSE_TIMEOUT = os.getenv("WEBSOCKET_CLOSE_TIMEOUT")
    WEBSOCKET_HEALTHCHECK_INTERVAL = os.getenv("WEBSOCKET_HEALTHCHECK_INTERVAL")
    WEBSOCKET_RETRY_DELAY = os.getenv("WEBSOCKET_RETRY_INTERVAL")

    pass

class ESPConstants:
    BRAKING_ESP_PORT = os.getenv("BRAKING_ESP_PORT")
    PROPULSION_ESP_PORT = os.getenv("PROPULSION_ESP_PORT")
    ESP_BAUDRATE = os.getenv("ESP_BAUDRATE")
    ESP_TIMEOUT = os.getenv("ESP_TIMEOUT")
    ESP_RETRY_INTERVAL = os.getenv("ESP_RETRY_INTERVAL")
    ESP_HEALTHCHECK_INTERVAL = os.getenv("ESP_HEALTHCHECK_INTERVAL")

    pass

class CommsConstants:
    ASYNCIO_SLEEP = os.getenv("ASYNCIO_SLEEP")
    pass


class FSMConstants:
    """
    Example import from .env file:
    MAX_SPEED = os.getenv("MAX_SPEED")
    """
    pass


class LoggingConstants:
    LOG_LEVEL = os.getenv("LOG_LEVEL")


network_constants = NetworkConstants()
fsm_constants = FSMConstants()
logging_constants = LoggingConstants()
