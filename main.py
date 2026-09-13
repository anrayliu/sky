import pygame
import sky

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

        self.sky = sky.Sky(self.win)
        self.sky.locations["game"] = Game(self.sky)
        self.sky.set_location("game")

    def run(self):
        running = True
        while running:
            self.sky.update(60, post_processing=sky.PostProcessing.vhs)
            if self.sky.events.quit:
                running = False

            pygame.display.update()

        self.sky.quit()
        pygame.quit()


Main().run()
