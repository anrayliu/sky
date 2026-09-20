import random
import math
from typing import Tuple, Union

import pygame


class Camera:
    def __init__(self, size: Tuple[int, int], restriction: Union[None, pygame.Rect] = None) -> None:
        self._rect = pygame.Rect((0, 0, *size))
        self._x, self._y = (0, 0)

        self._timerx, self._timery = (0, 0)
        self._shakex, self._shakey = (0, 0)

        self._initial_force = 0
        self._x_mult = 0
        self._y_mult = 0

        # prevents division by 0
        self._shake_duration = 1

        self._restriction = restriction

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def restriction(self) -> pygame.Rect:
        return self._restriction

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

            self._shakey = math.sin(self._timery) * self._initial_force * self._y_mult
            self._shakex = math.sin(self._timerx) * self._initial_force * self._x_mult

            self._initial_force += (0 - self._initial_force) / self._shake_duration * dt

    def update(self, pos: Tuple[int, int], dt: float, steps: int = 15) -> None:
        self._x += (pos[0] - self._x) / steps * dt
        self._y += (pos[1] - self._y) / steps * dt

        self._rect.centerx = self._x
        self._rect.centery = self._y

        if self._restriction is not None:
            self._rect.clamp_ip(self._restriction)

        self._handle_shake(dt)

    def shake(self, initial_force: int = 10, x_multiplier: int = 5, y_multiplier: int = 5, steps: int = 10) -> None:
        self._timerx = random.uniform(0, 6.28)
        self._timery = random.uniform(0, 6.28)

        self._initial_force = initial_force
        self._x_mult = x_multiplier
        self._y_mult = y_multiplier
        self._shake_duration = steps

    def reset(self, size: Union[None, Tuple[int, int]] = None, restriction: Union[None, pygame.Rect] = None, 
              stop_shake: bool = False, pos: Union[None, Tuple[int, int]] = None):
        if size is not None:
            self._rect.w = size[0]
            self._rect.h = size[1]

        if restriction is not None:
            self._restriction = restriction

        if pos is not None:
            self.update(pos, 1, 1)

        if stop_shake:
            self._initial_force = 0
            self._x_mult = 0
            self._y_mult = 0

            # prevents division by 0
            self._shake_duration = 1

            self._shakex = 0
            self._shakey = 0

        if self._restriction is not None:
            self._rect.clamp_ip(self._restriction)

    # debug method
    def show_borders(self, win: pygame.Surface) -> None:
        # we love python :)
        for rect, colour in zip(([self._restriction.copy()] if self._restriction is not None else []) + [self._rect.copy()], 
                                [(0, 0, 0 if self._restriction is None else 255), (0, 0, 0)]):
            # render debug lines in game space
            rect.x += self.x
            rect.y += self.y

            pygame.draw.rect(win, colour, rect, 5)
            pygame.draw.line(win, colour, rect.topleft, rect.bottomright, 5)
            pygame.draw.line(win, colour, rect.topright, rect.bottomleft, 5)
