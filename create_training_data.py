# create_training_data.py
# Einar Barkved from Sentdex

import socket
import time
from datetime import datetime, timedelta
import struct
from statistics import mean
import numpy as np
import time
from getkeys import key_check
import os

HOST = '158.37.74.84'
PORT = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("koblet til lidar")

PORT1 = 12345  #port til å sende meldinger
ss =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((HOST, PORT1))
print("koblet til styring")

minsteFrem = 100
lengdePaLister = 10

punkter = []

def samleData():
    try:
        reply = s.recv(2000)

        v = bytearray(reply)
        i = 0

        for value in v:
            try:
                if (v[i] == 255 and v[i+1] == 238):
                    vinkel = int.from_bytes(struct.pack("B",v[i+2])+ struct.pack("B",v[i+3]), byteorder='little') #reverserer bytsene, setter de sammen og finner vinkelen. PS en må dele vinkelen på 100 for å få den i grader
                    
                    lengde = int.from_bytes(struct.pack("B",v[i+7])+ struct.pack("B",v[i+8]), byteorder='little') #reverserer bytsene, setter de sammen og finner lengden til avstanden som er 1 grad oppver, dette er for å fjerne pungter som ikke er nødvendige må gange med 0.002 for å få meter

                    vinkel = vinkel/100 #HER ER VINKELEN TIL PUNTET SOM BLE LEST
                    lengde = lengde*0.002 #HER ER LENGDEN TIL PUNGTET SOM BLE LEST

                    punkter = [vinkel, lengde]
            
            
            except:
                print('Feil i lesing', end='')
    except:
        print('Feil i samling', end='')   

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
    [A,W,D] boolean values.
    '''
    output = [0,0,0,0,0,0,0,0,0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output


file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)


    paused = False
    while(True):

        if not paused:
            # 800x600 windowed mode
            # resize to something a bit more acceptable for a CNN
            samleData()
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([punkter,output])  #Legge inn LIDAR data
            
            if len(training_data) % 1000 == 0:
                print(len(training_data))
                np.save(file_name,training_data)

        keys = key_check()
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