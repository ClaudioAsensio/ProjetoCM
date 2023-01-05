from network import LoRa
from machine import Timer
from os import urandom
import socket
import time
import pycom

results = []

sf = 8

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, sf=sf)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print("Node A initiated")

s.setblocking(False)
pycom.heartbeat(False)
pycom.rgbled(0xFF0000)  #Red

chrono = Timer.Chrono()
#n_sent = 0
#n_recv = 0
n_messages = 5
#rtt = []
#rssi = []
distance = '250'
sizes = [50, 100, 150, 200, 250]
#sizes = [250]
#rnd_size = size - 6 # ter em conta o size de 'cm2022'


for size in sizes:
    i = 0
    rtt = []
    rssi = []
    n_sent = 0
    n_recv = 0
    print("Distance = %s" % distance)
    print("Size = %d bytes" % size)
    while i < n_messages:
    #for i in range(n_messages):
        data = None
        rnd = 'cm2022' + urandom(size-6).decode('latin1')
        s.send(rnd)
        n_sent += 1
        print("Msg # %d" % i)
        print(str(rnd))
        chrono.reset()
        chrono.start()
        data = s.recv(64)
        while chrono.read() <= 5:   # Timeout = 5 seg
            if data[:10] == b'Ack-cm2022':
                print("Signal strength (dBm):", lora.stats())
                n_recv += 1
                lap = chrono.read_ms()
                chrono.stop()
                pycom.rgbled(0x00FF00)  #Green
                time.sleep(0.5)
                pycom.rgbled(0xFF0000)  #Red
                rtt.append(lap)
                print("Ack")
                print("Round Trip Time = %f ms \n" % lap)
                rssi.append(data[16:].decode('latin1'))
                print(rssi)
                i += 1
                break
            #elif int(chrono.read())==25:
                #rtt.append(None)
                #print("Timeout msg %d" % i)
            data = s.recv(64)
        #time.sleep(2)

    pl = 1 - (n_recv/n_sent)
    print("Packet loss = %f " % pl)

    data_write = 'distance= ' + str(distance) + ', size= ' + str(size) + ', rtt1= ' + str(rtt[0]) + ', rtt2= ' + str(rtt[1]) + ', rtt3= ' + str(rtt[2]) + ', rtt4= ' + str(rtt[3]) + ', rtt5= ' + str(rtt[4]) + ', pl= ' + str(pl) + ', rssi1= ' + str(rssi[0]) + ', rss2= ' + str(rssi[1])+ ', rssi3= ' + str(rssi[2])+ ', rssi4= ' + str(rssi[3])+ ', rssi5= ' + str(rssi[4]) + ', sf= ' + str(sf)
    results.append(data_write)
    print('------------------------')
    print(data_write)
    print('------------------------')

print('------------------------')
print(results)
print('------------------------')
