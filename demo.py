import pygame
import sky
from sky.colours import *


class Game(sky.Location):
    def __init__(self, sky_obj):
        super().__init__(sky_obj)

        self.button1 = sky.Button((200, 0, 200, 100), "WASD to move", cam=self._cam)

        self.button2 = sky.Button((300, 300, 150, 80), "hello", cam=self._cam,
                                  style={
                                      "font": "cool-font",
                                      "rounding": 10,
                                  })

    def start(self, passed_data):
        print("starting location...")

    def stop(self):
        print("stopping location...")

    def scale(self, new_size):
        self._cam.reset(size=new_size)

    def cleanup(self):
        self.graphics.clear_cache()

    def update(self, dt):
        self._cam.update(self.button1.rect.center, dt)

        self.button1.update(self._events)
        if self.button1.click:
            print("button clicked!")

        self.button2.update(self._events)
        if self.button2.click:
            print("world!")

        if self._events.input[1] == "space":
            self._cam.shake(8)

        self.button1.rect.y += (self._events.key_down[pygame.K_s] - self._events.key_down[pygame.K_w]) * dt * 10
        self.button1.rect.x += (self._events.key_down[pygame.K_d] - self._events.key_down[pygame.K_a]) * dt * 10

        self.draw()

    def draw(self):
        self._win.fill(GREEN)

        pygame.draw.line(self._win, BLACK, self._cam.apply(-20, 0), self._cam.apply(20, 0), 5)
        pygame.draw.line(self._win, BLACK, self._cam.apply(0, -20), self._cam.apply(0, 20), 5)

        self.graphics.draw("apple", (0, 200))

        self.graphics.write("(0, 0)", (12, 12), font="cool-font", colour=BLACK, size=30)
        self.graphics.write("press space for screen shake", (150, 150), font="cool-font", colour=BLUE, size=50)

        self.button2.draw(self.graphics)
        self.button1.draw(self.graphics)


class Main:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("sky demo")

        try:
            pygame.display.set_icon(pygame.image.load("assets\\icon.png"))
        except FileNotFoundError:
            pass

        self.sky = sky.Sky(self.win)
        self.sky.add_location("game", Game(self.sky))
        self.sky.set_location("game")

    def run(self):
        running = True
        while running:
            self.sky.update(60, show_fps=True, post_processing=sky.PostProcessing.none)
            if self.sky.events.quit:
                running = False

            pygame.display.update()

        self.sky.quit()
        pygame.quit()


Main().run()
