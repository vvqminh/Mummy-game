from bfs_mummy import Graph
import json

import pygame
import sys
from pygame.locals import *

with open('./map.json', 'r') as file:
    dataMap = json.load(file)

grap = Graph(6, 6)
grap.addRectangleEdges()


def getKey(X, Y):
    for item in dataMap:
        if item['X'] == X and item['Y'] == Y:
            return item["key"]


def getLocate(key):
    return {"X": dataMap[key]["X"], "Y": dataMap[key]["Y"]}


pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mummy maze !")

surfaceMap = pygame.transform.scale(
    pygame.image.load("./image/floor.jpg"), (600, 600))

# (0,0) (60, 0) (120,0) (180,0) (240,0)

playerUp = pygame.image.load("./image/player/move_up.png")
playerDown = pygame.image.load("./image/player/move_down.png")
playerLeft = pygame.image.load("./image/player/move_left.png")
playerRight = pygame.image.load("./image/player/move_right.png")

TIME = 5

mummyUp = pygame.image.load("./image/mummy/redup.png")
mummyDown = pygame.image.load("./image/mummy/reddown.png")
mummyLeft = pygame.image.load("./image/mummy/redleft.png")
mummyRight = pygame.image.load("./image/mummy/redright.png")

try_again_img = pygame.image.load("./image/tryagain_red.png")
try_again_img = pygame.transform.scale(try_again_img, (300, 100))  # Resize as needed
try_again = False

wallX1, wallY1, wallW1, wallH1 = 400, 200, 10, 100
wallX2, wallY2, wallW2, wallH2 = 200, 400, 100, 10
wallX3, wallY3, wallW3, wallH3 = 200, 300, 10, 100

class Player:
    mummyGo = 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surface.blit(playerDown, (20, 20), (0, 0, 60, 60))

        self.timeSkip = 0
        self.option = 0

        self.go = 0

    def update(self, up, down, left, right):

        if Player.mummyGo == 0:
            if self.go < 100:

                if self.timeSkip <= TIME:  # 0-5
                    self.option = 0
                elif self.timeSkip <= TIME*2:  # 6-10
                    self.option = 1
                elif self.timeSkip <= TIME*3:  # 11-15
                    self.option = 2
                elif self.timeSkip <= TIME*4:
                    self.option = 3
                elif self.timeSkip <= TIME*5:
                    self.option = 4
                elif self.timeSkip > TIME*5:
                    self.timeSkip = 0

                if up or down or left or right:
                    self.go += 5
                    self.timeSkip += 1
                    self.surface.fill((0, 0, 0, 0))
                    self.animate(up, down, left, right)

                if up:
                    self.y -= 5
                elif down:
                    self.y += 5
                elif left:
                    self.x -= 5
                elif right:
                    self.x += 5
            else:
                self.go = 0
                Player.mummyGo = 1

    def animate(self, up, down, left, right):
        img = ""
        if up:
            img = playerUp
        elif down:
            img = playerDown
        elif left:
            img = playerLeft
        elif right:
            img = playerRight

        if self.option == 0:
            self.surface.blit(img, (20, 20), (0, 0, 60, 60))
        if self.option == 1:
            self.surface.blit(img, (20, 20), (60, 0, 60, 60))
        if self.option == 2:
            self.surface.blit(img, (20, 20), (120, 0, 60, 60))
        if self.option == 3:
            self.surface.blit(img, (20, 20), (180, 0, 60, 60))
        if self.option == 4:
            self.surface.blit(img, (20, 20), (240, 0, 60, 60))

    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))


class Mummy:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surface.blit(mummyDown, (20, 20), (0, 0, 60, 60))
        self.timeSkip = 0
        self.option = 0
        self.go = 0

        self.locat = []
        self.keyRun = {"X": self.x, "Y": self.y}

    def update(self, up, down, left, right):

        if self.go < 100:

            if self.timeSkip <= TIME:  # 0-5
                self.option = 0
            elif self.timeSkip <= TIME*2:  # 6-10
                self.option = 1
            elif self.timeSkip <= TIME*3:  # 11-15
                self.option = 2
            elif self.timeSkip <= TIME*4:
                self.option = 3
            elif self.timeSkip <= TIME*5:
                self.option = 4
            elif self.timeSkip > TIME*5:
                self.timeSkip = 0

            if up or down or left or right:
                self.go += 5
                self.timeSkip += 1
                self.surface.fill((0, 0, 0, 0))
                self.animate(up, down, left, right)

            if up:
                self.y -= 5
            elif down:
                self.y += 5
            elif left:
                self.x -= 5
            elif right:
                self.x += 5
        else:
            self.go = 0

           
            Player.mummyGo += 1
            if Player.mummyGo == 3:
                Player.mummyGo = 0

    def animate(self, up, down, left, right):
        img = ""
        if up:
            img = mummyUp
        elif down:
            img = mummyDown
        elif left:
            img = mummyLeft
        elif right:
            img = mummyRight

        if self.option == 0:
            self.surface.blit(img, (20, 20), (0, 0, 60, 60))
        if self.option == 1:
            self.surface.blit(img, (20, 20), (60, 0, 60, 60))
        if self.option == 2:
            self.surface.blit(img, (20, 20), (120, 0, 60, 60))
        if self.option == 3:
            self.surface.blit(img, (20, 20), (180, 0, 60, 60))
        if self.option == 4:
            self.surface.blit(img, (20, 20), (240, 0, 60, 60))

    def check_collision(self, player):
        # Kiểm tra tọa độ của Mummy có trùng với Player
        if self.x == player.x and self.y == player.y:
            return True
        return False
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

    def run(self, keyPlayer, playerX, playerY):

        if self.x != self.keyRun['X']:
            if self.x > self.keyRun['X']:  # qua trái
                self.update(False, False, True, False)
            else:  # qua phải
                self.update(False, False, False, True)

        elif self.y != self.keyRun['Y']:
            if self.y > self.keyRun['Y']:  # lên trên
                self.update(True, False, False, False)
            else:  # xuống
                self.update(False, True, False, False)
        else:
            keyMummy = getKey(self.x, self.y)
            listFind = grap.findListPath(keyMummy, keyPlayer)

            keyWall_1 = getKey(wallX1, wallY1)  # 16
            keyWall_2 = getKey(wallX2, wallY2)  # 26
            keyWall_3 = getKey(wallX3, wallY3)  # 20
            # wall dọc xanh
            if keyMummy == keyWall_1:
                
                if playerY == wallY1:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_1 - 1: # chặn xuyên tường
                            self.keyRun = getLocate(item)

            elif keyMummy == keyWall_1 - 1: # 15
                if playerY == wallY1:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_1: # chặn xuyên tường
                            self.keyRun = getLocate(item)
            
            # wall dọc đỏ
            elif keyMummy == keyWall_3:               
                if playerY == wallY3:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_3 - 1: # chặn xuyên tường
                            self.keyRun = getLocate(item)

            elif keyMummy == keyWall_3 - 1: # 19
                if playerY == wallY3:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_3: # chặn xuyên tường
                            self.keyRun = getLocate(item)
                            
            # wall ngang đỏ
            elif keyMummy == keyWall_2:               
                if playerX == wallX2:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_2 - 6: # chặn xuyên tường
                            self.keyRun = getLocate(item)

            elif keyMummy == keyWall_2 - 6: # 20
                if playerX == wallX2:
                    Player.mummyGo = 0
                else:
                    for item in listFind:
                        if item != keyWall_2: # chặn xuyên tường
                            self.keyRun = getLocate(item)
            else:

            # xử lý tt đi
                self.keyRun = getLocate(listFind[0])

player = Player()
mummy = Mummy()

up, down, left, right = False, False, False, False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True

            # Reset game khi nhấn R hoặc Space
            if event.key == K_r or event.key == K_SPACE:
                player.x, player.y = 0, 0
                mummy.x, mummy.y = 500, 500
                player.timeSkip = 0
                mummy.timeSkip = 0
                try_again = False 

    if not try_again:
        DISPLAYSURF.blit(surfaceMap, (0, 0))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255), (wallX1, wallY1, wallW1, wallH1))
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (wallX2, wallY2, wallW2, wallH2))
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (wallX3, wallY3, wallW3, wallH3))

        player.draw()
        player.update(up, down, left, right)
        mummy.draw()

        # Reset hướng di chuyển khi Player đứng yên
        if player.go == 0:
            up, down, left, right = False, False, False, False

        # Mummy thực hiện di chuyển nếu đến lượt
        if Player.mummyGo > 0:
            keyPlayer = getKey(player.x, player.y)
            mummy.run(keyPlayer, player.x, player.y)

        # Kiểm tra khi Mummy đến đúng tọa độ Player
        if mummy.check_collision(player):
            try_again = True  # Kết thúc game khi va chạm thực sự
            DISPLAYSURF.blit(try_again_img, (150, 250))  # Hiển thị "Try Again"

    pygame.display.update()
    pygame.time.Clock().tick(60)