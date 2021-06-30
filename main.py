import pygame, gui, player, platform, particles
from pygame.locals import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0))

w, h = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

TilesSurface = pygame.Surface((20, 20))

CamX, CamY = (0,0)
allsprites = pygame.sprite.Group()
allLevelsprites = pygame.sprite.Group()
collisions = pygame.sprite.Group()
fakeLevel = pygame.sprite.Group()
ticks = 0
deltaTime = 0
foward = True
floors = []
fakefloors = []
Debugs = False
particlesArr = []
level = 1
screentransition = False
screentransitionFrame = 0


def update_fps():
    global deltaTime, ticks
    fps = str(int(clock.get_fps()))
    if(ticks > 25):
        deltaTime = (61/(int(fps)+1))
    else:
        deltaTime = 1
    ticks += 1
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    TilesSurface.fill((3, 3, 3))
    TilesSurface.blit(fps_text, (0,0))

    return TilesSurface

def loadLevel(level):
    floors.clear()
    collisions.empty()
    allLevelsprites.empty()
    
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
                floors.append(platform.Platform(x=x*(w/(rowlen-1)), y=y*(h/(linecount - 1)), w= (w/(rowlen-1)) + 1, h = (h/(linecount - 1)) + 1))
    for i in floors:
        allLevelsprites.add(i)
        collisions.add(i)
        allLevelsprites.draw(screen)


def TestWorld():
    floor1 = platform.Platform(x=720, y =950, w=1250, h=125)
    collisions.add(floor1)
    allsprites.add(floor1)
    floor2 = platform.Platform(x=720, y =500, w=75, h=600)
    collisions.add(floor2)
    allsprites.add(floor2)
         
def loadFakeLevel(level):
    fakeLevel.empty()    
    fakefloors.clear()

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
                fakefloors.append(platform.Platform(x=x*(w/(rowlen-1)), y=y*(h/(linecount - 1)), w= (w/(rowlen-1)) + 1, h = (h/(linecount - 1)) + 1))
    for i in fakefloors:
        fakeLevel.add(i)



loadLevel(1)
#TestWorld()

def playerlogic():
    global screentransition, screentransitionFrame, CamX, level, foward
    if(screentransition and screentransitionFrame < 60):
        player.canmove = False
        if(foward):        
            if(screentransitionFrame == 0):
                loadFakeLevel(level + 1)
            CamX += w/60 * deltaTime
            screentransitionFrame += 1 * deltaTime
        else:
            if(screentransitionFrame == 0):
                loadFakeLevel(level - 1)
            CamX -= w/60 * deltaTime
            screentransitionFrame += 1 * deltaTime


    elif(screentransitionFrame >= 60):

        if(foward):
            level += 1
            player.x = 25
        else:
            level -=1
            player.x = w - 25
        player.canmove = True
        screentransitionFrame = 0
        screentransition = False
        loadLevel(level)
        fakeLevel.empty()
        CamX=0
        print("yes!")
    if(player.x > w - 10):
        foward = True
        screentransition = True
    if(player.x < 2 ):
        foward = False
        screentransition = True


def renders():

    playerlogic()
    allsprites.update(CamX, CamY, collisions, deltaTime)
    allsprites.draw(screen)
    allLevelsprites.draw(screen)
    allLevelsprites.update(CamX, CamY, collisions, deltaTime)
    if(foward):
        fakeLevel.update(CamX - w, 0, collisions, deltaTime)
    else:
        fakeLevel.update(CamX + w, 0, collisions, deltaTime) 
    fakeLevel.draw(screen)
    
    pos = 0
    for par in particlesArr:
        pos+=1
        screen.blit(par.update(deltaTime), (par.x, par.y))
        if(par.frame > par.lifetime):
            particlesArr.pop(pos-1)


player = player.Player(x= 90, y= 255 , screen=screen)
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
    screen.fill((237, 180, 235))

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