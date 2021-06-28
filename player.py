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

    def UpdateRects(self, cX, cY):
        self.rect.center = (self.x - cX, self.y - cY)
        self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) - cY)
        self.rectLeft.center = (self.x - (self.width/2) - cX, self.y - cY)
        self.rectRight.center = (self.x + (self.width/2) - cX, self.y - cY)
        self.rectTop.center = (self.x - cX, self.y -(self.height / 2) - cY)

        


    def update(self, cX ,cY, collisions):
        
        
     
        key = pygame.key.get_pressed()
        if(key[pygame.K_w]):
            if(self.isground or self.LeftWall or self.RightWall):
                
               
                self.grav = 0
                self.wallJoin = False
                if(self.LeftWall):
                    self.momentumX = 30 
                    self.jump = 4.5
                elif(self.RightWall):
                    self.momentumX = -30
                    self.jump = 4.5
                else:
                     self.jump = 5.5
           

        if(key[pygame.K_s]):
            self.y += 1 * self.speed
        if(key[pygame.K_a]):
            if(self.LeftWall == False):
                self.x -= 1 * self.speed
        if(key[pygame.K_d]):
            if(self.RightWall == False):
                self.x += 1 * self.speed
        if(key[pygame.K_SPACE] and self.dash):
            self.dash = False
            if(key[pygame.K_d]):
                self.momentumX += 50
            if(key[pygame.K_a]):
                self.momentumX += -50
            if(key[pygame.K_w]):
                self.jump = 4
            
        self.LeftWall = False
        self.RightWall = False
        self.isground = False
        
        for i in collisions:

            

            if(self.rectBottom.colliderect(i.rect)):
                while(self.rectBottom.colliderect(i.rect)):
                    self.y -= 0.1
                    self.UpdateRects(cX, cY)

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
                while(self.rectTop.colliderect(i.rect)):
                    self.y += 0.1
                    self.UpdateRects(cX, cY)


            self.rectBottom.center = (self.x - cX, self.y +(self.height / 2) + 0.1 - cY)
            if(self.rectBottom.colliderect(i.rect)):
                self.grav = 0
                self.isground = True
            self.UpdateRects(cX, cY)
            
            self.rectLeft.center = (self.x - cX - (self.width/2) - 0.1, self.y - cY)
            if(self.rectLeft.colliderect(i.rect) and self.wallJoin):
                self.LeftWall = True
                self.dash = True
            self.UpdateRects(cX, cY)

            self.rectRight.center = (self.x - cX + (self.width/2) + 0.1, self.y - cY)
            if(self.rectRight.colliderect(i.rect) and self.wallJoin):
                self.RightWall = True
                self.dash = True
            self.UpdateRects(cX, cY)
            

                
            
            
        if(self.isground != True):
            if(self.LeftWall != True and self.RightWall != True):
                self.grav += 0.75
            else:
                self.grav += 0.1
        else:
            self.wallJoin = False
            self.dash = True
            
            
        
            
        if(self.jump > 0):
            self.grav -= self.jump
            self.jump -= 1
        if(self.momentumX != 0):
            self.x += self.momentumX
            self.momentumX /= 1.25   
        
        self.y += self.grav
        self.UpdateRects(cX, cY)



        

