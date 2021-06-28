import pygame, gui, player, platform
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((0, 0))

w, h = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

TilesSurface = pygame.Surface((20, 20))

CamX, CamY = (0,0)
allsprites = pygame.sprite.Group()
collisions = pygame.sprite.Group()


floors = []
Debugs = False

def update_fps():

    fps = str(int(clock.get_fps()))
    GameSpeed = (61/(int(fps)+1))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    TilesSurface.fill((3, 3, 3))
    TilesSurface.blit(fps_text, (0,0))

    return TilesSurface

def loadLevel(level):
    f = open("Levels/" + str(level) +".txt", "r")
    row = []
    col = []
    linecount = 0
    rowlen = 0
    for line in f:
        if line != "\n":
            linecount += 1
            row = line.split(",")
            for i in row:
                rowlen = len(row)
            col.append(row)
    print(col)
    print (len(col))
    for y in range(linecount):
        for x in range(rowlen):
            if(col[y][x] == "1" or col[y][x] == "1\n"):
                floors.append(platform.Platform(x=x*(w/(rowlen-1)), y=y*(h/(linecount - 1)), w= (w/(rowlen-1)), h = (h/(linecount - 1))))
    for i in floors:
        allsprites.add(i)
        collisions.add(i)


def TestWorld():
    floor1 = platform.Platform(x=720, y =950, w=1250, h=125)
    collisions.add(floor1)
    allsprites.add(floor1)
    floor2 = platform.Platform(x=720, y =500, w=75, h=600)
    collisions.add(floor2)
    allsprites.add(floor2)
         
    
loadLevel(1)
#TestWorld()


def renders():
    allsprites.update(CamX, CamY, collisions)
    allsprites.draw(screen)

player = player.Player(x= 90, y= 255)
allsprites.add(player)




def Debug():
    if(player.isground):
        pygame.draw.rect(screen, (255,255,255) , player.rectBottom, 3)
    else: 
        pygame.draw.rect(screen, (255,0,0) , player.rectBottom, 3)
    if(player.LeftWall):
        pygame.draw.rect(screen, (255,255,255) , player.rectLeft, 3)
    else:
        pygame.draw.rect(screen, (255,255,0) , player.rectLeft, 3)
    if(player.RightWall):
        pygame.draw.rect(screen, (255,255,255) , player.rectRight, 3)
    else:
        pygame.draw.rect(screen, (255,0,255) , player.rectRight, 3)
    pygame.draw.rect(screen, (0,255,255) , player.rectTop, 3)
    for i in collisions:
        pygame.draw.rect(screen, (0,255,0) , i.rect, 3)


loop = 1
while loop:
    
    clock.tick(60)
    screen.fill((255, 255, 255))

    pressed_keys = pygame.event.get()
    for event in pressed_keys:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = 0  
            if event.key == pygame.K_F1:
                if Debugs:
                    Debugs = False
                else:
                    Debugs = True
        if event.type == pygame.QUIT:
            loop = 0
    renders()
   
    screen.blit(update_fps(), (10,screen.get_height() * 0.97))
    if(Debugs == True):
        Debug()
    pygame.display.update()