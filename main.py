import pygame
import sky
from sky.colours import *


class Game(sky.Location):
    def __init__(self, sky_obj) -> None:
        super().__init__(sky_obj)

        self.button = sky.Button((200, 0, 200, 100), "text here", cam=self.cam)

    def update(self, dt: float) -> None:
        self.cam.update(self.button.rect.center, dt)

        self.button.update(self.events)
        if self.button.click:
            print("hi!")

        if self.events.input[1] == "space":
            self.cam.shake(10)

        self.button.rect.y += (self.events.key_down[pygame.K_s] - self.events.key_down[pygame.K_w]) * dt * 10
        self.button.rect.x += (self.events.key_down[pygame.K_d] - self.events.key_down[pygame.K_a]) * dt * 10

        self.draw()

    def draw(self) -> None:
        self.win.fill(GREEN)

        self.graphics.draw("apple", (0, 200))

        self.graphics.write("WASD to move", (0, 50), font="cool-font", colour=ORANGE, size=25)
        self.graphics.write("press space for screen shake", (150, 150), font="cool-font", colour=BLUE, size=50)

        self.button.draw(self.graphics)


class Main:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("sky demo")

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
            self.sky.update(60, post_processing=sky.PostProcessing.none)
            if self.sky.events.quit:
                running = False

            pygame.display.update()

        self.sky.quit()
        pygame.quit()


Main().run()
