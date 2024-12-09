from serial import Serial
from comms.ESPHandler import ESPHandler

esp = ESPHandler(port='/dev/cu.usbserial-0001', baudrate=115200, timeout=1)

# while True:
#     line = esp.readline().decode('ascii', errors='ignore')
#     print(line)

esp.connect()