# Initialize the LoRa radio on Node B
from network import LoRa
import socket
import pycom
import time

lora = LoRa(mode=LoRa.LORA, sf=12)

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)  #Red


# Create a socket for the LoRa communication on Node B
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the socket to blocking mode
s.setblocking(False)
print("Node B initiated")
while True:
    # Receive the message
    message = s.recv(64)
    if message[:6] == b'cm2022':
        print("received")
        pycom.rgbled(0x00FF00)  #Green
        time.sleep(0.1)
        pycom.rgbled(0xFF0000)  #Red
        print(lora.stats())
        print(message)
        rssi = lora.stats().rssi
        s.send('Ack-cm2022/rssi='+str(rssi))
        print("sended")
