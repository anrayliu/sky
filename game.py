from typing import Union

import pygame
import sky
from sky.colours import *


class Game:
    def __init__(self, main) -> None:
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.cam = main.cam
        self.main = main

        self.button = sky.Button((200, 0, 200, 100), "hi", cam=self.cam)

    # called on location startup
    # args are passed in from main
    def start(self, args: Union[None, dict]) -> None:
        self.scale()

    # called when window is resized
    def scale(self) -> None:
        pass

    # called when main switches locations
    def end(self) -> None:
        pass

    # called when app closes
    def cleanup(self) -> None:
        pass

    def update(self, dt: int) -> None:
        self.cam.update(self.button.rect.center, dt)

        click, hover = self.button.update(self.events)
        if click:
            print("hi!")

        if self.events.input[1] == "space":
            self.cam.shake(10)

        self.button.rect.y += (self.events.key_down[pygame.K_s] - self.events.key_down[pygame.K_w]) * dt * 10
        self.button.rect.x += (self.events.key_down[pygame.K_d] - self.events.key_down[pygame.K_a]) * dt * 10

    def draw(self) -> None:
        self.win.fill(GREEN)

        self.graphics.draw("apple", (0, 200))

        self.graphics.write("WASD to move", (0, 50), font="cool-font", colour=ORANGE, size=25)
        self.graphics.write("press space for screen shake", (150, 150), font="cool-font", colour=BLUE, size=50)

        self.button.draw(self.graphics)
