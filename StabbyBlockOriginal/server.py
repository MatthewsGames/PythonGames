import socket
import random
from _thread import *
import sys
global currentPlayer
currentPlayer = 0
server = "10.1.130.171"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server,port))
except socket.error as e:
    str(e)
s.listen()
print("Waiting for connection, Server Started")
def read_pos(str):
    str = str.split(",")
    tup = []
    a = 0
    for i in str:
        #print("i:",i)
        if(a != 4 and i != "password" and i != "snap"):
            tup.append(int(i))
        else:
            tup.append(i)
        a += 1
    return tup

def make_pos(tup):
    strin = ""
    for i in tup:
        strin += str(i) + ','
    return strin[0:-1]

pos = []
def take_input():
    while True:
        inp = input()
        if(inp[0:4] == "kill"):
            print("terminating player", inp[5])
            pos[int(inp[5])] = "die"

def threaded_client(conn, player):
    pos.append([0, 0, 0, 0,"Matthew"])
    #print(pos[player])
    conn.send(str.encode("password123"))
    print("Added player")
    while True:
        try:
            reply = []
            data = read_pos(conn.recv(4096).decode())
            password = ""
            #print(data)
            if not data:
                print("Disconnected")
                break
            #print(player)
            if(data[0] != "password" and data[0] != "snap"):
                pos[player] = data
            reply.append("0")
            reply.append("0")
            reply.append("0")
            reply.append("0")
            reply.append("0")
            for i in range(len(pos)):
                if(i != player):
                    if(i != len(pos)):
                        reply.append(str(pos[i][0]))
                        reply.append(str(pos[i][1]))
                        reply.append(str(pos[i][2]))
                        reply.append(str(pos[i][3]))
                        reply.append(str(pos[i][4]))
            #print("Received: ", data)
            #print("Sending: ", reply)
            if (data[0] == "password"):
                reply = "crockettrockett"
                conn.sendall(str.encode(reply))
            elif (data[0] == "snap" and pos[player][4] == "Admin"):
                for i in pos:
                    r = random.randint(0,1)
                    if(r == 0):
                        pos[0] = 0
                        pos[1] = 0
                        pos[3] = 1
            else:
                conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Lost connection")
    conn.close()
    global currentPlayer
    currentPlayer -= 1
    print(player)
    print(pos)
    try:
        pos.pop(player)
    except:
        print("failure")
while True:
    conn, addr = s.accept()
    print("Connected to:",addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    #start_new_thread(take_input())
