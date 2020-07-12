import pygame
import socket
import random
import math
width = 1800
height = 900
ai = False
global name
name = input("What is your name?: ")
ip = input("Server: ")
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
clientNumber = 0
def collision(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x1 < x2 and x1 + w1 > x2 and y1 > y2 and y1 < y2 + h2 or x1 < x2 and x1 + w1 > x2 and y1 + h1 > y2 and y1 + h1 < y2 + h2 ):
        return True
    if (x1 < x2 + w2 and x1 + w1 > x2 + w2 and y1 > y2 and y1 < y2 + h2 or x1 < x2 and x1 + w1 > x2 and y1 + h1 > y2 and y1 + h1 < y2 + h2):
        return True
    if (y1 < y2 and y1 + h1 > y2 and x1 > x2 and x1 < x2 + w2 or y1 < y2 and y1 + h1 > y2 and x1 + w1 < x2 + w2 and x1 + w1 > x2):
        return True
    if (y1 < y2 + h2 and y1 + h1 > y2 + h2 and x1 > x2 and x1 < x2 + w2 or y1 < y2 and y1 + h1 > y2 and x1 + w1 < x2 + w2 and x1 + w1 > x2):
        return True
    return False
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        try:
            self.addr = (self.server,self.port)
            self.pos = self.connect()
        except:
            print("hi")
            

    def getPos(self):
        return self.pos
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

class Player():
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.dir = 0
        self.sx = -1000
        self.sy = -1000
        self.size = 1
        self.sw = 90
        self.sh = 20
        self.srect = pygame.Rect(self.sx,self.sy,self.sw,self.sh)
        self.dead = False
        self.d = -1
        self.vel = 5
        self.name = name
        self.lk = ""
        self.c = 0
        self.h = False
        self.snap = False
        self.brave = random.randint(0,5)
        self.c2 = 0

    def draw(self, win):
        font = pygame.font.Font("freesansbold.ttf", 20)
        if(len(self.name) > 7):
            title = font.render(self.name[0:8], True, (0, 0, 0))
        else:
            title = font.render(self.name, True, (0,0,0))
        win.blit(title, (self.x,self.y - 25))
        pygame.draw.rect(win, self.color, self.rect)
        if(self.dir == 0 or self.dir == 1):
            pygame.draw.rect(win,(100,100,100),(self.sx,self.sy,self.sw,self.sh))
        else:
            pygame.draw.rect(win, (100,100,100), (self.sx, self.sy, self.sh, self.sw))

    def move(self,players):
        keys2 = pygame.key.get_pressed()
        keys = []
        for i in keys2:
            keys.append(i)
        dist = []
        q = 0
        for i in players:
            if(q != 0):
                dist.append(math.sqrt((i.x - self.x)**2 + (i.y - self.y)**2))
            q += 1
        high = 10000
        index = -1
        for i in range(len(dist)):
            if(dist[i] < high and players[i+1].x > 200 or players[i+1].y > 200):
                high = dist[i]
                index = i
        if(ai and len(players) > 1 and index != -1):
            closest = players[index + 1]
            if (self.brave < 5):
                if closest.y - self.y > 30:
                    keys[pygame.K_s] = True
                    self.dir = 3
                if closest.y - self.y < 30:
                    keys[pygame.K_w] = True
                    self.dir = 2
                if closest.x - self.x > 30:
                    keys[pygame.K_d] = True
                    self.dir = 1
                if closest.x - self.x < 30:
                    keys[pygame.K_a] = True
                    self.dir = 0
            else:
                if (closest.size >= self.size):
                    if closest.y - self.y > 30:
                        keys[pygame.K_w] = True
                        self.dir = 2
                    if closest.y - self.y < 30:
                        keys[pygame.K_s] = True
                        self.dir = 3
                    if closest.x - self.x > 30:
                        keys[pygame.K_a] = True
                        self.dir = 0
                    if closest.x - self.x < 30:
                        keys[pygame.K_d] = True
                        self.dir = 1
                else:
                    if closest.y - self.y > 30:
                        keys[pygame.K_s] = True
                        self.dir = 3
                    if closest.y - self.y < 30:
                        keys[pygame.K_w] = True
                        self.dir = 2
                    if closest.x - self.x > 30:
                        keys[pygame.K_d] = True
                        self.dir = 1
                    if closest.x - self.x < 30:
                        keys[pygame.K_a] = True
                        self.dir = 0



        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_LEFT]:
            self.dir = 0

        if keys[pygame.K_RIGHT]:
            self.dir = 1

        if keys[pygame.K_UP]:
            self.dir = 2

        if keys[pygame.K_DOWN]:
            self.dir = 3

        if keys[pygame.K_SPACE] and self.name == "Crockett":
            self.x = random.randint(0,1800)
            self.y = random.randint(0, 900)
        if(keys[pygame.K_g] and self.name == "Crockett"):
            self.size += 1
        if (keys[pygame.K_j] and self.name == "Admin" or keys[pygame.K_j] and self.name == "Crockett"):
            self.snap = True
        no = False
        if(keys[pygame.K_h] and self.name == "Admin" and self.h == False or keys[pygame.K_h] and self.name == "Crockett" and self.h == False):
            self.h = True
            no = True
        if (keys[pygame.K_h] and self.name == "Admin" and self.h == True and no == False  or keys[pygame.K_h] and self.name == "Crockett" and self.h == True and no == False):
            self.h = False
            self.dir = 0
        if(pygame.mouse.get_pressed()[0] and self.name == "Crockett"):
            self.x = pygame.mouse.get_pos()[0]
            self.y = pygame.mouse.get_pos()[1]
        if (keys[pygame.K_m] and self.name == "Crockett" and self.c2 == 0):
            self.c2 = 1
        elif (keys[pygame.K_m] and self.name == "Crockett" and self.c2 == 1):
            self.c2 = 0
        print(self.c2)
        if(self.c2 == 1):
            self.x = pygame.mouse.get_pos()[0]
            self.y = pygame.mouse.get_pos()[1]

        self.update()
    def update(self):
        if self.x + self.width > width:
            self.x -= self.vel
        if self.x < 0:
            self.x += self.vel
        if self.y + self.height > height:
            self.y -= self.vel
        if self.y < 0:
            self.y += self.vel
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.h == True:
            self.dir += 1
        if(self.dir > 4):
            self.dir = 0

        if (self.dir == 0 or self.dir == 1):
            self.srect = pygame.Rect(self.sx, self.sy, self.sw, self.sh)
        else:
            self.srect = pygame.Rect(self.sx, self.sy, self.sh, self.sw)
        self.sw = 70 + self.size*20
        if(self.dir == 0):
            self.sx = self.x - (self.sw)
            self.sy = self.y + self.height/2
        if (self.dir == 1):
            self.sx = self.x + self.width
            self.sy = self.y + self.height / 2
        if (self.dir == 2):
            self.sx = self.x + self.width / 2
            self.sy = self.y - self.sw
        if (self.dir == 3):
            self.sx = self.x + self.width / 2
            self.sy = self.y + self.height
        self.c += 1
        if(self.c >= 100):
            self.lk = ""
            self.c = 0


    def collide(self,players):
        a = 0
        for i in players:
            collision(self.x,self.y,self.width,self.height,i.sx,i.sy,i.sw,i.sh)
            if(collision(self.x,self.y,self.rect[2],self.rect[3],i.sx,i.sy,i.srect[2],i.srect[3]) and a != 0 and self.x > 200 or collision(self.x,self.y,self.rect[2],self.rect[3],i.sx,i.sy,i.srect[2],i.srect[3]) and a != 0 and self.y > 200):
                self.dead = True
                self.d = a
            a += 1
    def collide2(self,players):
        a = 0
        for i in players:
            if(collision(self.sx,self.sy,self.srect[2],self.srect[3],i.x,i.y,i.rect[2],i.rect[3]) and i.x > 200 and self.lk != a or collision(self.sx,self.sy,self.srect[2],self.srect[3],i.x,i.y,i.rect[2],i.rect[3]) and i.y > 200 and self.lk != a):
                self.size += 1
                self.lk = a
            a += 1

def redrawWindow(win,players):
    #win.fill((255,255,255))
    pygame.draw.rect(win,(0,0,255),(0,0,200,200))
    for i in players:
        i.draw(win)
    pygame.display.update()

def read_pos(str):
    str = str.split(",")
    tup = []
    a = 0
    for i in str:
        if(a%5 != 4 or a == 0):
            tup.append(int(i))
        else:
            tup.append(i)
        a += 1
    return tup

def make_pos(tup):
    stri = ""
    for i in tup:
        stri += str(i)
        stri += ","
    return stri[0:-1]

def main():
    win.fill((255,255,255))
    run = True
    n = Network()
    global name
    if(name == "Crockett"):
        name = "SuperFailure"
    if(name == "Admin"):
        password = input("Password: ")
        q = n.send("password")
        adm = q[0:8]
        c = q[8:len(q)]
        if(password != adm and password != c):
            name = "Failure"
        if(password == c):
            name = "Crockett"
    pygame.display.set_caption("Stabby Block - " + name)
    players = [Player(0,0,100,100,(255,0,0),name)]
    #p2 = Player(0,0,100,100,(255,0,0))
    for i in players:
        i.update()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        a = 0
        p2Pos = ""
        if(players[0].dead == False):
            p2Pos = read_pos(n.send(make_pos([players[0].x, players[0].y, players[0].dir, players[0].size, players[0].name])))
        else:
            print("You were stabbed by player " + str(players[players[0].d].name))
            players[0].x = 0
            players[0].y = 0
            players[0].size = 1
            players[0].brave = random.randint(0,5)
            players[0].dead = False
            p2Pos = read_pos(n.send(make_pos([players[0].x, players[0].y, players[0].dir, players[0].size,players[0].name])))
        if(len(p2Pos)/5 > len(players)):
            players.append(Player(0,0,100,100,(0,255,0),""))
        if (len(p2Pos) / 5 < len(players)):
            players.pop(len(players)-1)
        for i in players:
            if(a != 0 and a != "die"):
                i.x = p2Pos[a*5]
                i.y = p2Pos[a*5+1]
                i.dir = p2Pos[a*5 + 2]
                i.size = p2Pos[a*5 + 3]
                i.name = p2Pos[a * 5 + 4]
                i.update()
            if(a == "die"):
                i.dead = True
                #print(i.x)
            a += 1
        leaderboard = ["","","","",""]
        p = []
        for i in players:
            p.append(i)
        for i in range(5):
            if(len(p) == 0):
                break
            highest = 0
            index = 0
            for i3 in range(len(p)):
                if(p[i3].size > highest):
                    highest = p[i3].size
                    index = i3
            leaderboard[i] = str(i+1) + ". " + p[index].name
            p.remove(p[index])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        players[0].move(players)
        if(players[0].snap):
            n.send("snap")
        redrawWindow(win, players)
        win.fill((255,255,255))
        players[0].update()
        players[0].collide2(players)
        players[0].update()
        players[0].collide(players)
        players[0].update()
        font = pygame.font.Font("freesansbold.ttf", 20)
        title = font.render("Leaderboard:", True, (0,0,0))
        win.blit(title, (1650,10))
        for i in range(len(leaderboard)):
            title = font.render(leaderboard[i], True, (0,0,0))
            win.blit(title, (1650,i*25 + 35))
if __name__ == '__main__':
    main()
