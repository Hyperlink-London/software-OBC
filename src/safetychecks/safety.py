from serial import Serial
from comms.ESPHandler import ESPHandler
from src.logger import logger

# Do not have the port or baudrate information currently, will change once I do.
propulsion = ESPHandler(port='/dev/cu.usbserial-0001',
                        baudrate=115200, timeout=1)
braking = ESPHandler()
failsafe = ESPHandler()

# while True:
#     line = esp.readline().decode('ascii', errors='ignore')
#     print(line)


class ESPException(Exception):
    def __init__(self, message):
        super().__init__(message)


def safetychecks():
    # Checks if connected with all ESPs
    try:
        if not failsafe.connect():
            raise ESPException("Fail safe connection failed")
        logger.info("Fail safe connected successfully")

        if not braking.connect():
            raise ESPException("Braking connection failed")
        logger.info("Brake connected successfully")

        if not propulsion.connect():
            raise ESPException("Propulsion connection failed")
        logger.info("Propulsion connected successfully")

    except ESPException as e:
        logger.error(f"Safety checks failed: {e}")
        return
    # Checking of the data being recieved will go in the else block.
    else:
