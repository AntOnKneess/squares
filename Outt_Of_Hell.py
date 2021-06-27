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

Debug = False

def update_fps():

    fps = str(int(clock.get_fps()))
    GameSpeed = (61/(int(fps)+1))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    TilesSurface.fill((3, 3, 3))
    TilesSurface.blit(fps_text, (0,0))

    return TilesSurface




def renders():
    allsprites.update(CamX, CamY, collisions)
    allsprites.draw(screen)

player = player.Player(x= 90, y= 255)
allsprites.add(player)


floor = platform.Platform(x= 525, y =900, w= 1000, h=100)
floor2 = platform.Platform(x = 540, y= 580, w= 100, h = 400)
allsprites.add(floor)
allsprites.add(floor2)
collisions.add(floor2)
collisions.add(floor)

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
                if Debug:
                    Debug = False
                else:
                    Debug = True
        if event.type == pygame.QUIT:
            loop = 0
    renders()
   
    screen.blit(update_fps(), (10,screen.get_height() * 0.97))
    if(Debug):
        pygame.draw.rect(screen, (255,0,0) , player.rectBottom, 3)
        pygame.draw.rect(screen, (255,255,0) , player.rectLeft, 3)
        for i in collisions:
            pygame.draw.rect(screen, (0,255,0) , i.rect, 3)
    pygame.display.update()