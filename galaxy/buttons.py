import pygame 
from .tools import get_colour

BUTTON = {"colour":"black",
         "highlight":"yellow",
         "font":"arial",
         "text size":30,
         "text colour":"white",
         "border colour":"black",
         "border size":0,
         "text pos":"center"}
                 
class Button:
    def __init__(self, rect, text, style=None, center=None):
        style_copy = BUTTON.copy()
        if style != None:
            style_copy.update(style)
        
        self.colour = get_colour(style_copy["colour"])
        self.highlight = get_colour(style_copy["highlight"])
        self.font = style_copy["font"]
        self.text_size = style_copy["text size"]
        self.text_colour = get_colour(style_copy["text colour"])
        self.border_colour = get_colour(style_copy["border colour"])
        self.border_size = style_copy["border size"]
        self.text_pos = style_copy["text pos"]
                
        self.rect = pygame.Rect(rect)
        if center != None:
            if center[3] != 0:
                self.rect.y = center[1] + center[3] / 2 - self.rect.h / 2
            if center[2] != 0:
                self.rect.x = center[0] + center[2] / 2 - self.rect.w / 2
        self.text = text
        
        self.click = False
        self.hover = False
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse):
            self.hover = True
            if events.click:
                self.click = True 
        else:
            self.hover = False
        
    def draw(self, graphics):
        if self.hover:
            colour = self.highlight
        else:
            colour = self.colour
        pygame.draw.rect(graphics.surface, colour, self.rect)
        if self.border_size > 0:
            pygame.draw.rect(graphics.surface, self.border_colour, self.rect, self.border_size)
        
        if self.text_pos == "center":
            pos = self.rect 
        else:
            pos = (self.rect.x + self.text_pos[0], self.rect.y + self.text_pos[1])
        graphics.write(self.text, pos, font=self.font, size=self.text_size, colour=self.text_colour)
