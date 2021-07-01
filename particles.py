import pygame, random, math

from pygame.display import set_allow_screensaver

class Particles():
    def __init__(self, x=40, y=40, speed = 3.25, w = 25, h=25, roundness = 10, color=(255,255,255), lifetime = 20, fade=5, direction = (0,180), density = 10):
        super().__init__()
        self.x =x
        self.y = y
        self.speed = speed
        self.w = w
        self.h = h
        self.roundness = roundness
        self.color = color
        self.lifetime = lifetime
        self.fade = fade
        self.directionmin, self.directionmax = direction
        self.density = density
        self.surf = pygame.Surface((500, 500), pygame.SRCALPHA)
        self.surfClean = pygame.Surface((500, 500), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.rect.center = (x,y)
        self.frame = 0
        self.particlesROT = []





    def update(self, delta):
      
      
        self.surf.fill((255,255,255,0))
        self.surf.set_alpha(255-((2.55*self.fade)*self.frame))
        if(self.frame == 0):
            for i in range(self.density):
                self.particlesROT.append(random.randint(self.directionmin,self.directionmax))
        for i in range(self.density):
            rect = (250+ math.cos(math.radians(self.particlesROT[i]))*self.speed*self.frame * delta, 250 + math.sin(math.radians(self.particlesROT[i]))*self.speed*self.frame * delta, self.w, self.h)
            pygame.draw.rect(self.surf, self.color, rect, border_radius = self.roundness)
        self.frame +=1 * delta
        return self.surf
        
class Trail():
    def __init__(self, x=40, y=40, speed = 3.25, w = 25, h=25, roundness = 10, color=(255,255,255), lifetime = 40, fade=5, direction = (0,180), density = 10, fadedel = 20, scw = 1920, sch = 1080):
        super().__init__()
        self.x =x
        self.y = y
        self.speed = speed
        self.w = w
        self.h = h
        self.roundness = roundness
        self.color = color
        self.lifetime = lifetime
        self.fade = fade
        self.directionmin, self.directionmax = direction
        self.density = density
        self.surf = pygame.Surface((scw, sch), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.rect.center = (x,y)
        self.frame = 0
        self.particlesROT = []
        self.fadedel = fadedel
        self.scw = scw
        self.sch = sch




    def update(self, delta, X, Y):
        self.frame += 1/delta        
        if(self.frame >= self.fadedel):
            self.surf.set_alpha(255-((2.55*self.fade)* (self.frame-self.fadedel)))
        rect = (X, Y , self.w, self.h)
        pygame.draw.rect(self.surf, self.color, rect, border_radius = self.roundness)
        return self.surf
