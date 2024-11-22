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
    """
    Example import from .env file:
    API_IP = os.getenv("API_IP")
    """
    WEBSOCKET_IP = os.getenv("WEBSOCKET_IP")

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
