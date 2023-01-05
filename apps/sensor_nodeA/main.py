from network import LoRa
from machine import Timer
from os import urandom
import socket
import time
import pycom
from machine import Pin
import time
from machine import ADC
adc = ADC(0)
adc_c = adc.channel(pin='G6')
adc_c()
adc_c.value()
# led = Pin('P9', mode = Pin.OUT)
# sensor = Pin('G6', mode = Pin.IN)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print("Node A initiated")

s.setblocking(False)
pycom.heartbeat(False)
pycom.rgbled(0xFF0000)  #Red

while True:
    data = None
    # rnd = 'cm2022' + urandom(rnd_size).decode('latin1')
    rnd= 'cm2022' + str(adc_c.value())
    s.send(rnd)

    data = s.recv(64)
    time.sleep(1)
