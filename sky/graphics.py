import pygame
import math
import os


class Graphics:
    def __init__(self, surface):
        self.surface = surface
        
        self.images = {}
        self.fonts = {}
        
        self.font_paths = []
        
    def load_folder(self, dir, size=None):
        for file in os.listdir(dir):
            if file.endswith(".ttf") or file.endswith(".otf"):
                self.font_paths.append(os.path.join(dir, file))
                
            elif file.endswith(".png") or file.endswith(".jpg"):
                img = pygame.image.load(os.path.join(dir, file)).convert_alpha()
                if size != None:
                    img = pygame.transform.scale(img, size)
                    
                self.images[file[:-4]] = img
                
    def draw(self, image, pos, angle=None, size=None, transparency=None, radians=False, center=None):
        image_ = self.images[image].copy()
        
        if size != None:
            image_ = pygame.transform.scale(image_, size)
            
        if angle != None:
            if radians:
                angle = math.degrees(angle)
            image_ = pygame.transform.rotate(image_, angle)
            pos = image_.get_rect(center=pos).topleft
            
        if transparency != None:
            image_.set_alpha(transparency)
            
        if center != None:
            pos = image_.get_rect(center=pygame.Rect(center).center).topleft
            
        self.surface.blit(image_, pos)

    def write(self, text, pos, size=30, colour="white", transparency=None, font="arial", center=None):
        try:
            font_ = self.fonts[font + str(size)]
        except KeyError:
            if font in pygame.font.get_fonts():
                font_ = pygame.font.SysFont(font, size)
            else:
                for p in self.font_paths:
                    if os.path.split(p)[1][:-4] == font:
                        font_ = pygame.font.Font(p, size)
                        break
                
            self.fonts[font + str(size)] = font_
            
        text_ = font_.render(str(text), True, colour)
        
        if transparency != None:
            text_.set_alpha(transparency)
            
        if center != None:
            pos = text_.get_rect(center=pygame.Rect(center).center).topleft
        
        self.surface.blit(text_, pos)