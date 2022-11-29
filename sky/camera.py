import pygame
import random


class Camera:
    def __init__(self, size, restriction=None):
        self.rect = pygame.Rect((0, 0, *size))
        self.x, self.y = self.shakex, self.shakey = (0, 0)
        self.restriction = restriction
        
    def update(self, pos, dt=1):
        #self.rect.centerx += (pos[0] - self.rect.centerx) / (100 / dt)
        #self.rect.centery += (pos[0] - self.rect.centery) / (100 / dt)
        self.rect.center = pos
        
        if self.restriction != None:
            self.rect.clamp_ip(self.restriction)
        
        self.x = -self.rect.x + self.shakex 
        self.y = -self.rect.y + self.shakey 
        
        self.shakex *= -0.8
        if self.shakex < 0.01:
            self.shakex = 0
        self.shakey *= -0.8
        if self.shakey < 0.01:
            self.shakey = 0
        
    def moved(self, pos, shake=True):
        x = self.x if shake else -self.rect.x
        y = self.y if shake else -self.rect.y
        return (pos[0] + x, pos[1] + y)
        
    def shake(self, value):
        self.shakex = value * random.choice([-1, 1])
        self.shakey = value * random.choice([-1, 1])