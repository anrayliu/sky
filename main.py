import sys

import pygame
import sky
from sky.colours import *

from game import Game


class Main:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("test")

        try:
            pygame.display.set_icon(pygame.image.load("assets\\icon.png"))
        except FileNotFoundError:
            pass

        self.cam = sky.Camera(self.win.get_size())
        self.graphics = sky.Graphics(self.win, cam=self.cam)
        self.events = sky.Events()

        try:
            self.graphics.load_folder("assets", sizes={
                "apple": (200, 100)
            })
        except FileNotFoundError:
            pass

        self.locations = {"game": Game(self)}
        self.location = None

        self._scale()

    def set_location(self, loc, args_=None):
        if self.location is not None:
            self.locations[self.location].stop()

        self.location = loc
        self.locations[self.location].start(args_)

    def _scale(self):
        for loc in self.locations.values():
            loc.scale()

    def _quit(self):
        if self.location is not None:
            self.locations[self.location].stop()

        for loc in self.locations.values():
            loc.cleanup()

        pygame.quit()
        sys.exit()

    def run(self):
        self.set_location("game")

        running = True
        while running:
            dt = self.events.update(60)
            if self.events.quit:
                running = False
            if self.events.resized:
                self._scale()

            self.win.fill(BLACK)

            loc = self.locations[self.location]

            # each location is responsible for calling draw()
            loc.update(dt)

            if SHOW_FPS := True:
                self.graphics.write(f"FPS: {self.events.get_fps()}", pos=(0, 0), colour=WHITE, size=15, use_cam=False)

            # self.win.blit(pygame.image.frombuffer(pyvidplayer2.PostProcessing.vhs(pygame.surfarray.pixels3d(pygame.display.get_surface()).swapaxes(0, 1)).tobytes(), self.win.get_size(), "RGB"), (0, 0))

            pygame.display.update()

        self._quit()


Main().run()
