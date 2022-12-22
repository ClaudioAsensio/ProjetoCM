from network import LoRa
import socket
import pycom

lora = LoRa(mode=LoRa.LORA)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
print("Node B initiated")

while True:
    message = s.recv(64)
    if message[:6] == b'cm2022':
        print("received")
        print(message)
        s.send('Ack-cm2022')
        print("Sent")
