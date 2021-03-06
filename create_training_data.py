# create_training_data.py
# Einar Barkved from Sentdex

import os
import socket
import struct
import time
from datetime import datetime, timedelta
from statistics import mean
import win32api as wapi
import getkeys

import numpy as np

#from getkeys import key_check

HOST = '158.37.74.84'
PORT1 = 12345  #port til å sende meldinger
ss =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((HOST, PORT1))
print("koblet til styring")
PORT = 12346 #port til å motta Lidardata

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("koblet til lidar")

minsteFrem = 100
lengdePaLister = 10

punkter = []

def samleData():
    global punkter
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

                    #Legge til liste 0-180 for å systematisere tallene.
                    if (vinkel < 90.0 or vinkel > 180.0):
                        punkter.append(round(vinkel,0))
                        punkter.append(round(lengde,3))
                        #print(punkter)
                i+=1
    except: ('Feil i lesing')
            
            
  



file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():
    global punkter
    # for i in list(range(4))[::-1]:
    #     print(i+1)
    #     time.sleep(1)


    paused = False
    while(True):
        if not paused:
            keys = getkeys.key_check()
            npyOutput = getkeys.Styr(getkeys.keys_to_output(keys))
            
            if npyOutput != [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                for rr in range(1,100,1):
                    samleData()
                training_data.append([punkter,npyOutput])  #Legge inn LIDAR data
                punkter = []
            
        if len(training_data) % 100 == 0:
            #print(len(training_data))
            np.save(file_name,training_data)



        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
