import pygame 

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, speed = 10):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height =  50
        self.speed = speed
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((50, 50, 50))
        self.rect = self.surf.get_rect()
        self.rectBottom = pygame.Rect(x,y+(self.height / 2),25,3)
        self.rectLeft = pygame.Rect(x-(self.width/2),y+(self.height / 2),25,3)
        self.image = self.surf
        self.grav = 0
        self.jump = 0
        self.isground = False

        
    def UpdateRects(self, cX, cY):
        self.rect.center = (self.x - cX, self.y - cY)
        self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) - cY)


    def update(self, cX ,cY, collisions):
        
        
     
        key = pygame.key.get_pressed()
        if(key[pygame.K_w]):
            if(self.isground):
                self.jump = 4.5
        if(key[pygame.K_s]):
            self.y += 1 * self.speed
        if(key[pygame.K_a]):
            self.x -= 1 * self.speed
        if(key[pygame.K_d]):
            self.x += 1 * self.speed

        for i in collisions:

            if(self.rectBottom.colliderect(i.rect)):
                while(self.rectBottom.colliderect(i.rect)):
                    self.y -= 1
                    self.rect.center = (self.x - cX, self.y - cY)
                    self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) - cY)


            self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) + 1 - cY)
            if(self.rectBottom.colliderect(i.rect)):
                self.grav = 0
                self.isground = True
            else:
                self.isground = False
            self.UpdateRects(cX, cY)
        if(self.isground != True):
            self.grav += 0.75
        if(self.jump > 0):
            self.grav -= self.jump
            self.jump -= 1
        self.y += self.grav
        self.UpdateRects(cX, cY)



        

