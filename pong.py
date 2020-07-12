import pygame as p
import random
import math
p.init()
screenWidth = 800
screenHeight = 800
screen = p.display.set_mode((screenWidth, screenHeight))
done = False
pSpeed = .003
maxBallSpeed = .75
balls = [[[screenWidth/2,screenHeight/2],[20,20],[random.randint(20,30)/100,random.randint(20,30)/100]]]
players = [[[20,screenHeight/2],[p.K_w,p.K_s],[20,60],"v",False,0],[[screenWidth - 40,screenHeight/2],[p.K_UP,p.K_DOWN],[20,60],"v",False,1],[[screenWidth/2,20],[p.K_k,p.K_l],[60,20],"h",True,2],[[screenWidth/2,screenHeight - 40],[p.K_v,p.K_b],[60,20],"h",True,3]]
def collision2(x1,y1,w1,h1,x2,y2,w2,h2):
    if (y1 + h1 > y2 and y1 + h1 < y2 + h2 and x1 < x2 + w2 and x1 + w1 > x2):
        return "down"
    if (y1 < y2 + h2 and y1 > y2 and x1 < x2 + w2 and x1 + w1 > x2):
        return "up"
    if (x1 + w1 > x2 and x1 + w1 < x2 + w2 and y1 < y2 + h2 and y1 + h1 > y2):
        return "right"
    if(x1 < x2 + w2 and x1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        return "left"
def collision(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x1 <= x2 and x1 + w1 >= x2 and y1 >= y2 and y1 <= y2 + h2 or x1 <= x2 and x1 + w1 >= x2 and y1 + h1 >= y2 and y1 + h1 <= y2 + h2 ):
        print("o:")
        print(x1)
        print(y1)
        return "left"
    elif (x1 <= x2 + w2 and x1 + w1 >= x2 + w2 and y1 >= y2 and y1 <= y2 + h2 or x1 <= x2 and x1 + w1 >= x2 and y1 + h1 >= y2 and y1 + h1 <= y2 + h2):
        print("o:")
        print(x1)
        print(y1)
        return "right"
    if (y1 <= y2 and y1 + h1 >= y2 and x1 >= x2 and x1 <= x2 + w2 or y1 <= y2 and y1 + h1 >= y2 and x1 + w1 <= x2 + w2 and x1 + w1 >= x2):
        print("o:")
        print(x1)
        print(y1)
        return "up"
    elif (y1 <= y2 + h2 and y1 + h1 >= y2 + h2 and x1 >= x2 and x1 <= x2 + w2 or y1 <= y2 and y1 + h1 >= y2 and x1 + w1 <= x2 + w2 and x1 + w1 >= x2):
        print("o:")
        print(x1)
        print(y1)
        return "down"


while not done:
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True
    keys2 = p.key.get_pressed()
    keys = []
    for i in keys2:
        keys.append(i)
    for i in players:
        a = 0
        d = []
        for j in range(len(balls)):
            if(i[3] == "h"):
                d.append(abs(balls[j][0][1] - i[0][1]))
            else:
                d.append(abs(balls[j][0][0] - i[0][0]))
        low = min(d)
        for j in range(len(d)):
            if(d[j] == low):
                a = j
        py = balls[a][0][1] + (i[0][0] - balls[a][0][0])/balls[a][2][0]*balls[a][2][1]
        px = balls[a][0][0] + (i[0][1] - balls[a][0][1])/balls[a][2][1]*balls[a][2][0]
        if(i[3] == "v" and balls[a][2][1]/abs(balls[a][2][1]) == 1):
            py -= i[2][1]/2
        elif (i[3] == "v" and balls[a][2][1] / abs(balls[a][2][1]) == -1):
            py += i[2][1] / 2
        if (i[3] == "h" and balls[a][2][0] / abs(balls[a][2][0]) == -1):
            px += i[2][0] / 2
        if (i[3] == "h" and balls[a][2][0] / abs(balls[a][2][0]) == 1):
            px -= i[2][0] / 2

        print("stuff:")
        print(px)
        print(py)
        if(i[4] == True and py + balls[a][1][1]/2 > i[0][1] + i[2][1]/2 and i[3] == "v"):
            keys[i[1][1]] = True
        if (i[4] == True and py + balls[a][1][1]/2 < i[0][1] + i[2][1]/2 and i[3] == "v"):
            keys[i[1][0]] = True
        if (i[4] == True and px + balls[a][1][0]/2 > i[0][0] + i[2][0]/2 and i[3] == "h"):
            keys[i[1][1]] = True
        if (i[4] == True and px + balls[a][1][0]/2 < i[0][0] + i[2][0]/2 and i[3] == "h"):
            keys[i[1][0]] = True
    for j in keys:
        for i in players:
            if keys[i[1][0]] and i[0][1] > .0005 and i[3] == "v":
                i[0][1] -= pSpeed
            elif keys[i[1][1]] and i[0][1] < screenHeight - i[2][1] and i[3] == "v":
                i[0][1] += pSpeed
            if keys[i[1][0]] and i[0][0] > .0005 and i[3] == "h":
                i[0][0] -= pSpeed
            elif keys[i[1][1]] and i[0][0] < screenWidth - i[2][0] and i[3] == "h":
                i[0][0] += pSpeed
    p.draw.rect(screen, (0, 0, 0), p.Rect(0, 0, screenWidth, screenHeight))
    for i in players:
        p.draw.rect(screen, (0, 128, 255), p.Rect(i[0][0], i[0][1], i[2][0], i[2][1]))
    for i in balls:
        i[0][0] += i[2][0]
        i[0][1] += i[2][1]
        p.draw.ellipse(screen, (255, 255, 255), [i[0][0],i[0][1],i[1][0],i[1][1]])
        for j in players:
            if(collision(i[0][0],i[0][1],i[1][0],i[1][1],j[0][0],j[0][1],j[2][0],j[2][1]) == "left"):
                if(abs(i[2][0]) < maxBallSpeed):
                    i[2][0]*=-1.2
                else:
                    i[2][0]*=-1
                i[0][0] = j[0][0] - i[1][0]

            elif (collision(i[0][0],i[0][1],i[1][0],i[1][1],j[0][0],j[0][1],j[2][0],j[2][1]) == "right"):
                if (abs(i[2][0]) < maxBallSpeed):
                    i[2][0] *= -1.2
                else:
                    i[2][0] *= -1
                i[0][0] = j[0][0] + j[2][0]
            if (collision(i[0][0],i[0][1],i[1][0],i[1][1],j[0][0],j[0][1],j[2][0],j[2][1]) == "up"):
                if (abs(i[2][1]) < maxBallSpeed):
                    i[2][1] *= -1.2
                else:
                    i[2][1] *= -1
                i[0][1] = j[0][1] - i[1][1]
            if (collision(i[0][0],i[0][1],i[1][0],i[1][1],j[0][0],j[0][1],j[2][0],j[2][1]) == "down"):
                if (abs(i[2][1]) < maxBallSpeed):
                    i[2][1] *= -1.2
                else:
                    i[2][1] *= -1
                i[0][1] = j[0][1] + j[2][1]
    for i in range(len(balls)):
        if(balls[i][0][0] > screenWidth or balls[i][0][0] < 0 or balls[i][0][1] > screenHeight or balls[i][0][1] < 0):
            r = random.randint(0,1)
            r2 = random.randint(0,1)
            if(r == 0):
                r = -1
            if (r2 == 0):
                r2 = -1
            balls[i] = [[screenWidth/2,screenHeight/2],[20,20],[random.randint(20,30)/100 * r,random.randint(20,30)/100 * r2]]

    p.display.flip()