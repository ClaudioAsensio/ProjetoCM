# Initialize the LoRa radio on Node B
from network import LoRa
import socket

lora = LoRa(mode=LoRa.LORA)


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
        print(message)
        s.send('Ack-cm2022')
        print("sended")
