from network import LoRa
import socket
import pycom

lora = LoRa(mode=LoRa.LORA)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
print("Node B initiated")

pycom.heartbeat(False)
while True:
    message = s.recv(64)
    if message[:6] == b'cm2022':
        print("received")
        message=message.decode('utf-8')
        print(int(message[6:]))
        pycom.rgbled(int(message[6:]))
        s.send('Ack-cm2022')
        print("Sent")