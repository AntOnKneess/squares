import pygame

pygame.init()



class Panel():
    def __init__(self,x,y, Width, Height, screen, Border=True, BGColor=(5,5,5), BorderColor=(0,0,0), percentageScale=True, percentagePos=True, borderThickness=4, id=""):
        
        w, h = pygame.display.get_surface().get_size()
        self.screen = screen
        self.Border= Border
        self.BGColor= BGColor
        self.id = id
        self.Thickness = borderThickness
        self.BorderColoer = BorderColor
        if(percentageScale):
            self.width= w*(Width/100)
            self.height = h*(Height/100)
        else:
            self.width = w
            self.h = h
        
        if(percentagePos):
            self.x = w*(x/100)
            self.y = h*(y/100)
        else:
            self.x = x
            self.y = y
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, BGColor, self.rect)

    def update(self, events=""):  
        pygame.draw.rect(self.screen, self.BorderColoer, self.rect, self.Thickness)  
        pygame.draw.rect(self.screen, self.BGColor, self.rect)



class Text():
    def __init__(self,text, x,y, fontFamily, fontSize, screen,  BGColor=(5,5,5), percentageScale=True, percentagePos=True, id =""):
        
        w, h = pygame.display.get_surface().get_size()
        self.screen = screen
        self.BGColor= BGColor
        self.text = text
        self.font = fontFamily
        self.id = id
        if(percentageScale):
            self.fontsize = round(w*(fontSize/100))
        else:
            self.fontsize = fontSize

        if(percentagePos):
            self.x = w*(x/100)
            self.y = h*(y/100)
        else:
            self.x = x
            self.y = y
            
        self.fontRender = pygame.font.SysFont(fontFamily, self.fontsize)
        self.RenderedText = self.fontRender.render(self.text, 1, pygame.Color(BGColor))
        self.screen.blit(self.RenderedText, (self.x, self.y))
        

    def update(self, events=""):
        self.RenderedText = self.fontRender.render(self.text, 1, pygame.Color(self.BGColor))
        self.screen.blit(self.RenderedText, (self.x, self.y))


class Button():
    def __init__(self,x,y, scale, Image, screen, name, hoverchange=True, percentagePos=True, percentageScale=True, FitWidth = 0, tooltip = "" , TTW = 100, TTH= 20, TTX=15, TTY=0, id=""):
        self.tooltip = tooltip
        self.TTW = TTW
        self.TTH = TTH
        self.TTX = TTX
        self.TTY = TTY
        self.ActivTool = False
        w, h = pygame.display.get_surface().get_size()
        scale = scale/10
        self.mouse = pygame.mouse.get_pos() 
        self.screen = screen
        self.cageVal = None
        self.id = id
        self.name = name
        self.image= pygame.image.load(Image)
        self.hoverchange = hoverchange
        self.fontRender = pygame.font.SysFont("Arial", 15)
        if(percentagePos):
            self.x = w*(x/100)
            self.y = h*(y/100)
        else:
            self.x = x
            self.y = y

        if(percentageScale):
            self.scale = round(w*(scale/100))
        else:
            self.scale = scale
        if(FitWidth != 0):
            self.scale = (FitWidth/self.image.get_width())

        self.image = pygame.transform.rotozoom(self.image, 0, self.scale)
        self.imageBackup = self.image.copy()
        self.imageBlended = self.image.copy()
        colorImage = pygame.Surface(self.imageBlended.get_size()).convert_alpha()
        colorImage.fill((100,100,100))        
        self.imageBlended.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y 
        self.screen.blit(self.image, (self.rect.left, self.rect.top))

    def update(self, events=""):  
        self.cageVal = None
        self.screen.blit(self.image, (self.rect.left, self.rect.top))
        for event in events: 
            
            self.mouse = pygame.mouse.get_pos() 
      
            if self.rect.left <= self.mouse[0] <= self.rect.left+self.rect.width and self.rect.top <= self.mouse[1] <= self.rect.top+self.rect.height:
        
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    
                    return self.name
             
                if(self.hoverchange):
                    self.image= self.imageBlended
                if(self.tooltip != ""):
                    self.ActivTool = True
            else: 
                self.image = self.imageBackup
                self.ActivTool = False


    def DrawTooltip(self):
        if(self.ActivTool):
            self.RenderedText = self.fontRender.render(self.tooltip, 1, pygame.Color(0,0,0))
            self.rectTwo = pygame.Rect(self.mouse[0]+self.TTX, self.mouse[1]+self.TTY, self.TTW, self.TTH)
            pygame.draw.rect(self.screen, (255,255,255), self.rectTwo)
            self.screen.blit(self.RenderedText, (self.mouse[0] +self.TTX+1, self.mouse[1] + self.TTY + 1))
            


class TextInput():
    def __init__(self,x,y, fontFamily, fontsize, Width, Height, screen, id, fontColor=(255,255,255), text="",Border=True, BGColor=(5,5,5), BorderColor=(0,0,0), percentageScale=True, percentagePos=True, borderThickness=4):
        
        w, h = pygame.display.get_surface().get_size()
        self.screen = screen
        self.Border= Border
        self.BGColor= BGColor
        self.Thickness = borderThickness
        self.BorderColoer = BorderColor
        self.text = text
        self.fontColor = fontColor
        self.id = id
        self.font = fontFamily
        
        if(percentageScale):
            self.fontsize = round(w*(fontsize/100))
        else:
            self.fontsize = fontsize


        if(percentageScale):
            self.width= w*(Width/100)
            self.height = h*(Height/100)
        else:
            self.width = w
            self.h = h
        
        if(percentagePos):
            self.x = w*(x/100)
            self.y = h*(y/100)
        else:
            self.x = x
            self.y = y
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fontRender = pygame.font.SysFont(fontFamily, self.fontsize)
        pygame.draw.rect(screen, BGColor, self.rect)
        self.RenderedText = self.fontRender.render(self.text, 1, pygame.Color(self.fontColor))
        self.screen.blit(self.RenderedText, (self.x, self.y))

    def update(self, selected=True, events=""):  
        for event in events:
            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_RETURN:
                    return(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text =  self.text[:-1]
                else:
                    self.text += event.unicode

        pygame.draw.rect(self.screen, self.BorderColoer, self.rect, self.Thickness)  
        pygame.draw.rect(self.screen, self.BGColor, self.rect)
        self.RenderedText = self.fontRender.render(self.text, 1, pygame.Color(self.fontColor))
        if(self.text == ""):
            self.RenderedText = self.fontRender.render("Enter Text:", 1, (self.BGColor[0] + 20, self.BGColor[1] + 20, self.BGColor[2] + 20))
        
        self.screen.blit(self.RenderedText, (self.x, self.y))

class Cage():
    def __init__(self,x,y, Width, Height, screen, id,percentageScale=True, percentagePos=True, columns =1, Space=10, spaceCol = 100, topPad = 0):
        
        w, h = pygame.display.get_surface().get_size()
        self.screen = screen
        self.items = []
        self.id = id
        self.paddingTop = topPad
        self.columns = columns
        self.rSpace = Space
        self.cSpace = spaceCol
        self.passinfo = ""
        if(percentageScale):
            self.width= w*(Width/100)
            self.height = h*(Height/100)
        else:
            self.width = w
            self.h = h
        
        if(percentagePos):
            self.x = w*(x/100)
            self.y = h*(y/100)
        else:
            self.x = x
            self.y = y
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
 

    def update(self, events=""):  
        
        #pygame.draw.rect(self.screen, (0,0,0), self.rect)  
        a=[]
        for i in range(len(self.items)):
            a.append(self.items[i].update(events=events))
        for i in range(len(self.items)):
            if(isinstance(self.items[i], Button)):
                self.items[i].DrawTooltip()
    
        return a  

         
                  
     
            
        
    
    def FreshTiles(self):
        self.group = 0
        self.row = 1
        self.Space = (self.width - (self.cSpace * (self.columns + 1))) / self.columns 
        print(self.Space)
        print(self.items)
        for i in range(len(self.items)):
            
            self.col = i % self.columns
            self.items[i].rect.x = (self.Space * self.col) + (self.cSpace*(self.col+1)) + self.x
            self.items[i].rect.y = (self.row * self.rSpace) + (self.y + self.paddingTop)
            if(self.group + 1 < self.columns):
                self.group += 1
            else:
                self.group = 0
                self.row += 1

