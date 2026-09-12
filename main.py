import sys
from typing import Union

import pygame
import sky
from sky.colours import *

from game import Game


class Main:
    def __init__(self) -> None:
        pygame.init()

        self.win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("test")

        try:
            pygame.display.set_icon(pygame.image.load("assets\\icon.png"))
        except FileNotFoundError:
            pass

        self.cam = sky.Camera(self.win.get_size())
        self.graphics = sky.Graphics(self.win, cam=self.cam)
        self.events = sky.Events(60)

        try:
            self.graphics.load_folder("assets", sizes={
                "apple": (200, 100)
            })
        except FileNotFoundError:
            pass

        self.locations = {"game": Game(self)}
        self.location = None

        self.scale()

    def set_location(self, loc, args: Union[None, dict] = None) -> None:
        if self.location is not None:
            self.locations[self.location].end()

        self.location = loc
        self.locations[self.location].start(args)

    def scale(self) -> None:
        for loc in self.locations.values():
            loc.scale()

    def close(self) -> None:
        if self.location is not None:
            self.locations[self.location].end()

        for loc in self.locations.values():
            loc.cleanup()

        pygame.quit()
        sys.exit()

    def run(self) -> None:
        self.set_location("game")

        while True:
            dt = self.events.update()
            if self.events.resized:
                self.scale()

            loc = self.locations[self.location]
            loc.update(dt)

            if self.events.quit:
                self.close()

            loc.draw()

            if SHOW_FPS := True:
                self.graphics.write(f"FPS: {self.events.get_fps()}", pos=(0, 0), colour=WHITE, size=15, use_cam=False)

            # self.win.blit(pygame.image.frombuffer(pyvidplayer2.PostProcessing.vhs(pygame.surfarray.pixels3d(pygame.display.get_surface()).swapaxes(0, 1)).tobytes(), self.win.get_size(), "RGB"), (0, 0))

            pygame.display.update()


Main().run()
