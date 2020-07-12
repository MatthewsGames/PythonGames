import pygame as p
import random
import math
p.init()
screenWidth = 800
screenHeight = 800
players = [[[20,20],[p.K_w,p.K_s],[20,60],False],[[screenWidth - 40,screenHeight/2],[p.K_UP,p.K_DOWN],[20,60],"v",True,1],[[screenWidth/2,20],[p.K_k,p.K_l],[60,20],"h",True,2]]
screen = p.display.set_mode((screenWidth, screenHeight))
while not done:
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True
    keys2 = p.key.get_pressed()
    keys = []
    for i in keys2:
        keys.append(i)
    for j in keys:
        for i in players:
            if keys[i[1][0]]:
                a = 0
            elif keys[i[1][1]]:

            if keys[i[1][0]]:

            elif keys[i[1][1]]:
    p.sleep(10)
    p.display.flip()