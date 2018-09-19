# Citation: Box Of Hats (https://github.com/Box-Of-Hats )
# Einar Barkved from Sentdex

import win32api as wapi
import time
import socket

HOST = '158.37.74.84'
PORT1 = 12345  #port til å sende meldinger
ss =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((HOST, PORT1))
ss.send(str.encode("w"))
print("koblet til styring")
PORT = 12346 #port til å motta Lidardata

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("koblet til lidar")


def Styr(datainn):
    if (datainn == [1,0,0,0,0,0,0,0,0]):
        ss.send(str.encode("w"))
        print("Sender w")
        return datainn
        time.sleep(1)
    elif (datainn == [0,1,0,0,0,0,0,0,0]):
        ss.send(str.encode("s"))
        print("Sender s")
        return datainn
        time.sleep(1)
    elif (datainn == [0,0,1,0,0,0,0,0,0]):
        ss.send(str.encode("a"))
        print("Sender a")
        return datainn
        time.sleep(1)
    elif (datainn == [0,0,0,1,0,0,0,0,0]):
        ss.send(str.encode("d"))
        print("Sender d")
        return datainn
        time.sleep(1)
    else:
        ss.send(str.encode("q"))
        return [0,0,0,0,0,0,0,0,1]
        time.sleep(1)




keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys

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

# def main():
#     while(True):
#         keys = key_check()
#         Styr(keys_to_output(keys))
#         #print(keys_to_output(keys))
        

# main()