import pygame 
from .colours import *


def get_colour(value):
    try:
        colour = globals()[value.upper().replace(" ", "_")]
    except (KeyError, AttributeError):
        colour = value
    return colour
    
    
def draw_round_rect(surface, colour, rect, r):
    x, y, w, h = rect
    colour = get_colour(colour)

    pygame.draw.ellipse(surface, colour,(x,y,r,r))
    pygame.draw.ellipse(surface, colour,(x+w-r,y,r,r))
    pygame.draw.ellipse(surface, colour,(x,y+h-r,r,r))
    pygame.draw.ellipse(surface, colour,(x+w-r,y+h-r,r,r))

    pygame.draw.rect(surface, colour,(x+r/2,y,w-r,r))
    pygame.draw.rect(surface, colour,(x+r/2,y+h-r/2-r/2,w-r,r))
    pygame.draw.rect(surface, colour,(x,y+r/2,r,h-r))
    pygame.draw.rect(surface, colour,(x+w-r,y+r/2,r,h-r))

    pygame.draw.rect(surface, colour,(x+r,y+r,w-r*2,h-r*2))