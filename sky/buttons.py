import pygame 


class Button:
    def __init__(self, rect, text, style={}, center=None):
        self.style = {"colour":"black",
                 "highlight":"yellow",
                 "border colour":"black",
                 "border size":0,
                 "font":"arial",
                 "font size":30,
                 "font colour":"white"}
        self.style.update(style)
                
        self.rect = pygame.Rect(rect)
        if center != None:
            self.rect.center = pygame.Rect(*center).center
        
        self.text = text
        
        self.click = False
        self.hover = False
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse):
            self.hover = True
            if events.click:
                self.click = True 
                events.click = False
        else:
            self.hover = False
        
    def draw(self, graphics):
        pygame.draw.rect(graphics.surface, self.style["highlight"] if self.hover else self.style["colour"], self.rect)
        if self.style["border size"] > 0:
            pygame.draw.rect(graphics.surface, self.style["border colour"], self.rect, self.style["border size"])
            
        graphics.write(self.text, (0, 0), font=self.style["font"], size=self.style["font size"], colour=self.style["font colour"], center=self.rect)