import pygame,particles

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, speed = 10, screen = ""):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height =  50
        self.speed = speed
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((3, 206, 164))
        self.rect = self.surf.get_rect()
        self.rectBottom = pygame.Rect(x,y+(self.height / 2),30,1)
        self.rectLeft = pygame.Rect(x-(self.width/2),y,1,10)
        self.rectRight = pygame.Rect(x+(self.width/2),y,1,10)
        self.rectTop = pygame.Rect(x,y-(self.height / 2),30,1)
        self.image = self.surf
        self.grav = 0
        self.jump = 0
        self.isground = False
        self.LeftWall = False
        self.RightWall = False
        self.wallJoin = False
        self.momentumX = 0
        self.dash = True
        self.particlesArr = []
        self.trailArr = []
        self.screen = screen
        self.canslide = True
        self.level = 0
        self.canmove = True


    def UpdateRects(self, cX, cY):
        self.rect.center = (self.x - cX, self.y - cY)
        self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) - cY)
        self.rectLeft.center = (self.x - (self.width/2) - cX, self.y - cY)
        self.rectRight.center = (self.x + (self.width/2) - cX, self.y - cY)
        self.rectTop.center = (self.x - cX, self.y -(self.height / 2) - cY)

        
    def particles(self, delta):
        pos = 0
        for par in self.particlesArr:
            pos+=1
            self.screen.blit(par.update(delta), (par.x -250, par.y -250))
            if(par.frame > par.lifetime):
                self.particlesArr.pop(pos-1)
        pos = 0
        for tar in self.trailArr:
            pos+=1
            self.screen.blit(tar.update(delta,self.x-25,self.y-25), (0,0))
            if(tar.frame > tar.lifetime):
                self.trailArr.pop(pos-1)

    def Physics(self, cX, cY, collisions):
        for i in collisions:

            

            if(self.rectBottom.colliderect(i.rect)):
                while(self.rectBottom.colliderect(i.rect)):
                    self.y -= 0.1
                    self.UpdateRects(cX, cY)
                    self.momentumX = 0

            if(self.rectLeft.colliderect(i.rect)):
                self.jump = 0
                self.grav = 0
                self.momentumX = 0
                while(self.rectLeft.colliderect(i.rect)):
                    self.x += 0.1
                    self.UpdateRects(cX, cY)
                    self.wallJoin = True

            if(self.rectRight.colliderect(i.rect)):
                self.jump = 0
                self.grav = 0
                self.momentumX = 0
                while(self.rectRight.colliderect(i.rect)):
                    self.x -= 0.1
                    self.UpdateRects(cX, cY)
                    self.wallJoin = True

            if(self.rectTop.colliderect(i.rect)):
                self.jump = 0
                self.grav = 0
                self.momentumX = 0
                while(self.rectTop.colliderect(i.rect)):
                    self.y += 0.1
                    self.UpdateRects(cX, cY)


            self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) + 0.1 - cY)
            if(self.rectBottom.colliderect(i.rect)):
                self.grav = 0
                if(self.jump < 4):
                    self.isground = True
            self.UpdateRects(cX, cY)
            
            self.rectLeft.center = (self.x - cX - (self.width/2) - 0.1, self.y - cY)
            if(self.rectLeft.colliderect(i.rect) and self.wallJoin):
                self.LeftWall = True
            
            self.UpdateRects(cX, cY)

            self.rectRight.center = (self.x - cX + (self.width/2) + 0.1, self.y - cY)
            if(self.rectRight.colliderect(i.rect) and self.wallJoin):
                self.RightWall = True
            
            self.UpdateRects(cX, cY)
            

    def update(self, cX ,cY, collisions, delta):
        

        self.particles(delta)
        key = pygame.key.get_pressed()
        if(self.canmove):
            if(key[pygame.K_w]):
                if(self.isground or self.LeftWall or self.RightWall):
                    
                    pygame.mixer.Sound("SFX/Jump.wav").play()
                    self.grav = 0
                    self.wallJoin = False
                    self.canslide = False
                    if(self.LeftWall):
                        self.momentumX = 30 
                        self.jump = 4.5
                        self.particlesArr.append(particles.Particles(x=self.x - 27, y=self.y - 25, direction=(270, 450)))
                    elif(self.RightWall):
                        self.momentumX = -30
                        self.jump = 4.5
                        self.particlesArr.append(particles.Particles(x=self.x + 5 , y=self.y -25, direction=(90, 270)))
                    else:
                        self.jump = 5.5
                        self.isground = False
                        self.particlesArr.append(particles.Particles(x=self.x, y=self.y + 10, direction=(180, 360)))
           

            if(key[pygame.K_s]):
                self.y += 1 * self.speed * delta
            if(key[pygame.K_a]):
                if(self.LeftWall == False):
                    self.x -= 1 * self.speed * delta
            if(key[pygame.K_d]):
                if(self.RightWall == False):
                    self.x += 1 * self.speed * delta
            if(key[pygame.K_SPACE] and self.dash and self.isground == False):
                self.dash = False
                self.trailArr.append(particles.Trail(x=self.x, y=self.y, roundness=3,color=(237, 107, 134), w=50, h=50))
                if(key[pygame.K_d]):
                    self.momentumX += 50
                if(key[pygame.K_a]):
                    self.momentumX += -50
                if(key[pygame.K_w]):
                    self.grav = 0
                    self.jump = 6
            
        
        self.LeftWall = False
        self.RightWall = False
        self.isground = False
        
        
        self.Physics(cX,cY,collisions)
            
            
        if(self.isground != True):
            if(self.LeftWall != True and self.RightWall != True):
                self.grav += 0.75
            else:
                self.grav += 0.1
                if(self.canslide): 
                    if(self.LeftWall):
                        self.particlesArr.append(particles.Particles(x=self.x -27, y=self.y - 10, direction=(270, 360), density=10, lifetime=5, fade=20, color=(237, 107, 134), w=5,h=5))
                    else:
                        self.particlesArr.append(particles.Particles(x=self.x + 27, y=self.y - 10, direction=(180, 270), density=10, lifetime=5, fade=20, color=(237, 107, 134), w=5,h=5))
                self.canslide = True
        else:
            self.wallJoin = False
            self.dash = True
            
            
        
            
        if(self.jump > 0):
            self.grav -= self.jump
            self.jump -= 1
        if(self.momentumX < 0.001 and self.momentumX > -0.001):
            self.momentumX = 0
        if(self.momentumX != 0):
            print("Mo X" + str(self.momentumX))
            if(self.momentumX > 0):
                for i in range (round(self.momentumX * delta)):
                    self.x += 1                 
                    if(round(self.x) % 7 == 0):
                        self.Physics(cX,cY,collisions)
            if(self.momentumX < 0):
                for i in range (round(self.momentumX *-1 * delta)):
                    self.x -= 1
                    if(round(self.x) % 7 == 0):
                        self.Physics(cX,cY,collisions)
            self.momentumX /= 1.25
            
            
        if(self.grav * delta > 0):
            for i in range (round(self.grav * delta)):
                self.y += 1
                if(round(self.y) % 5 == 0):
                    self.Physics(cX,cY,collisions)
        else:
            for i in range (round(self.grav * delta * -1)):
                self.y -= 1
                if(round(self.y) % 5 == 0):
                    self.Physics(cX,cY,collisions)
         
        self.UpdateRects(cX, cY)



        

