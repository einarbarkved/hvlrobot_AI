import os
import socket
import struct
import time
from datetime import datetime, timedelta
from statistics import mean

import numpy as np


HOST = '158.37.74.84'
PORT1 = 12345  #port til å sende meldinger
ss =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((HOST, PORT1))
print("koblet til styring")
PORT = 12346 #port til å motta Lidardata

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("koblet til lidar")

punkter = []

def samleData():
    reply = s.recv(2000)

    v = bytearray(reply)
    i = 0
    try:
        for value in v:
            
                if (v[i] == 255 and v[i+1] == 238):
                    vinkel = int.from_bytes(struct.pack("B",v[i+2])+ struct.pack("B",v[i+3]), byteorder='little') #reverserer bytsene, setter de sammen og finner vinkelen. PS en må dele vinkelen på 100 for å få den i grader
                        
                    lengde = int.from_bytes(struct.pack("B",v[i+7])+ struct.pack("B",v[i+8]), byteorder='little') #reverserer bytsene, setter de sammen og finner lengden til avstanden som er 1 grad oppver, dette er for å fjerne pungter som ikke er nødvendige må gange med 0.002 for å få meter

                    vinkel = vinkel/100 #HER ER VINKELEN TIL PUNTET SOM BLE LEST
                    lengde = lengde*0.002 #HER ER LENGDEN TIL PUNGTET SOM BLE LEST

                    if (vinkel < 90.0 or vinkel > 180.0):
                        punkter.append(round(vinkel,0))
                        punkter.append(round(lengde,3))
                        #print(punkter)
                        
                i+=1
    except: ('Feil i lesing')
            
            


def main():
    global punkter
    for rr in range(0,100,1):
        samleData()

    print(punkter)
    punkter = []

main()