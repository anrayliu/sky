import pygame 
from .colours import *


def get_colour(value):
    try:
        colour = globals()[value.upper().replace(" ", "_")]
    except (KeyError, AttributeError):
        colour = value
    return colour