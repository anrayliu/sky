import random
import math
from typing import Tuple, Union

import pygame


class Camera:
    def __init__(self, size: Tuple[int, int], restriction: Union[None, pygame.Rect] = None) -> None:
        self._rect = pygame.Rect((0, 0, *size))

        self._timerx, self._timery = (0, 0)
        self._shakex, self._shakey = (0, 0)

        self._initial_force = 0
        self._force_multiplier = 0
        self._shake_duration = 1

        self._restriction = restriction

    @property
    def x(self) -> int:
        return -self._rect.x + self._shakex

    @property
    def y(self) -> int:
        return -self._rect.y + self._shakey

    def _handle_shake(self, dt: float) -> None:
        if 0 < self._initial_force < 0.1:
            self._initial_force = 0
        else:
            self._timerx += dt
            self._timery += dt

            self._shakey = math.sin(self._timery) * self._initial_force * self._force_multiplier
            self._shakex = math.sin(self._timerx) * self._initial_force * self._force_multiplier

            self._initial_force += (0 - self._initial_force) / self._shake_duration * dt

    def update(self, pos: Tuple[int, int], dt: float, speed: int = 20) -> None:
        self._rect.centerx += (pos[0] - self._rect.centerx) / speed * dt
        self._rect.centery += (pos[1] - self._rect.centery) / speed * dt

        if self._restriction is not None:
            self._rect.clamp_ip(self._restriction)

        self._handle_shake(dt)

    def shake(self, initial_force: int = 10, force_multiplier: int = 5, shake_duration: int = 10) -> None:
        self._timerx = random.uniform(0, 6.28)
        self._timery = random.uniform(0, 6.28)

        self._initial_force = initial_force
        self._force_multiplier = force_multiplier
        self._shake_duration = shake_duration

    # debug method
    #
    # def draw_borders(self, win: pygame.Surface) -> None:
    #     if self._restriction is not None:
    #         rect = self._restriction.copy()
    #         rect.x += self.x
    #         rect.y += self.y

    #         pygame.draw.rect(win, (0, 0, 255), rect, 5)
    #         pygame.draw.line(win, (0, 0, 255), rect.topleft, rect.bottomright, 5)
    #         pygame.draw.line(win, (0, 0, 255), rect.topright, rect.bottomleft, 5)

    #     rect = self._rect.copy()
    #     rect.x += self.x
    #     rect.y += self.y

    #     pygame.draw.rect(win, (0, 0, 0), rect, 5)
    #     pygame.draw.line(win, (0, 0, 0), rect.topleft, rect.bottomright, 5)
    #     pygame.draw.line(win, (0, 0, 0), rect.topright, rect.bottomleft, 5)