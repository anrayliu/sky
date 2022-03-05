import pygame
import os
from .tools import get_colour


class Graphics:
    def __init__(self, surface):
        self.surface = surface
        
        self.images = {}
        self.fonts = {"arial":{"30":pygame.font.SysFont("arial", 30)}}
        self.font_paths = {}
        
    def load_folder(self, dir):
        for file in os.listdir(dir):
            if file.endswith(".ttf") or file.endswith(".otf"):
                self.load_font(os.path.join(dir, file))
            elif file.endswith(".png") or file.endswith(".jpg"):
                self.load_image(os.path.join(dir, file))
    
    def load_font(self, path):
        head, tail = os.path.split(path[:-4])
        self.font_paths[tail] = path
        self.fonts[tail] = {"30":pygame.font.Font(path, 30)}
        
    def load_image(self, path):
        head, tail = os.path.split(path[:-4])
        self.images[tail] = pygame.image.load(path).convert_alpha()
                
    def load_sysfont(self, font):
        self.fonts[font] = {"30":pygame.font.SysFont(font, 30)}
                
    def draw(self, img, pos, angle=None, size=None, transparency=None):
        x, y = pos[0], pos[1]
        if size == None:
            surf = self.images[img].copy()
        else:
            surf = pygame.transform.scale(self.images[img], size)
        if angle != None:
            surf = pygame.transform.rotate(surf, angle)
            x, y = surf.get_rect(center=(x, y)).topleft
        if len(pos) == 4:
            if pos[3] != 0:
                y += pos[3]/2 - surf.get_height()/2
            if pos[2] != 0:
                x += pos[2]/2 - surf.get_width()/2
        if transparency != None:
            surf.set_alpha(transparency)
        self.surface.blit(surf, (x, y))

    def write(self, text, pos, size=30, colour="white", transparency=None, font="arial"):
        colour = get_colour(colour)
        if not font in self.fonts:
            self.fonts[font] = {}
        if str(size) in self.fonts[font]:
            obj = self.fonts[font][str(size)]
        else:
            if font in pygame.font.get_fonts():
                obj = pygame.font.SysFont(font, size)
            else:
                obj = pygame.font.Font(self.font_paths[font], size)
            self.fonts[font][str(size)] = obj
        text = obj.render(str(text), True, colour)
        x, y = pos[0], pos[1]
        if len(pos) == 4:
            if pos[3] != 0:
                y += pos[3]/2 - text.get_height()/2
            if pos[2] != 0:
                x += pos[2]/2 - text.get_width()/2
        if transparency != None:
            text.set_alpha(transparency)
        self.surface.blit(text, (x, y))
