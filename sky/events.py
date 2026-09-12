from typing import Tuple

import pygame


class Events:
    def __init__(self, target_fps: int) -> None:
        self._quit = False
        self._click = False
        self._input = (None, None, None)

        self._keys_down = None
        self._mouse_down = None
        self._mouse = (0, 0)

        self._target_fps = target_fps
        self._clock = pygame.time.Clock()

        pygame.event.pump()

    @property
    def fps(self) -> int:
        return round(self._clock.get_fps())

    @property
    def quit(self) -> bool:
        return self._quit

    @property
    def click(self) -> bool:
        return self._click

    @property
    def input(self) -> Tuple[any, str, any]:
        return self._input

    @property
    def key_down(self) -> pygame.key.ScancodeWrapper:
        return pygame.key.get_pressed()

    @property
    def mouse_down(self) -> Tuple[bool, bool, bool]:
        return pygame.mouse.get_pressed()

    @property
    def mouse(self) -> Tuple[int, int]:
        return pygame.mouse.get_pos()

    def update(self) -> None:
        self._quit = False
        self._click = False
        self._input = (None, None, None)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._click = True
            elif event.type == pygame.KEYDOWN:
                self._input = (event.unicode, pygame.key.name(event.key), event.key)

        return self._clock.tick(self._target_fps) / 1000 * 60
