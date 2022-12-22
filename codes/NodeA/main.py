from network import LoRa
from machine import Timer
from os import urandom
import socket
import time
import pycom

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print("Node A initiated")

s.setblocking(False)
pycom.heartbeat(False)
pycom.rgbled(0xFF0000)  #Red

chrono = Timer.Chrono()
n_sent = 0
n_recv = 0
n_messages = 5
rtt = []
distance = '0'
size = 250
rnd_size = size - 6 # ter em conta o size de 'cm2022'
print("Distance = %s" % distance)
print("Size = %d bytes" % size)
for i in range(n_messages):
    data = None
    rnd = 'cm2022' + urandom(rnd_size).decode('latin1')
    s.send(rnd)
    n_sent += 1
    print("Msg # %d" % i)
    print(str(rnd))
    chrono.reset()
    chrono.start()
    data = s.recv(64)
    while chrono.read() <= 5:   # Timeout = 5 seg
        if data == b'Ack-cm2022':
            n_recv += 1
            lap = chrono.read_ms()
            chrono.stop()
            pycom.rgbled(0x00FF00)  #Green
            time.sleep(0.5)
            pycom.rgbled(0xFF0000)  #Red
            rtt.append(lap)
            print("Ack")
            print("Round Trip Time = %f ms \n" % lap)
            break
        elif int(chrono.read())==5:
            rtt.append(None)
            print("Timeout msg %d" % i)
        data = s.recv(64)
    time.sleep(2)

pl = 1 - (n_recv/n_sent)
print("Packet loss = %f " % pl)
