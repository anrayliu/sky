from typing import Tuple, Callable

import pygame


class Events:
    def __init__(self) -> None:
        self._quit = False
        self._click = False
        self._input = (None, "", None)
        self._resized = False

        self._keys_down = None
        self._mouse_down = None
        self._mouse = (0, 0)

        self._clock = pygame.time.Clock()

        self._event_handlers = {}

        # ensures overlapping buttons don't both trigger
        self._button_hovered = False
        self._button_clicked = False

        pygame.event.pump()

    @property
    def quit(self) -> bool:
        return self._quit

    @property
    def click(self) -> bool:
        return self._click

    @property
    def resized(self) -> bool:
        return self._resized

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

    # for internal use

    @property
    def button_clicked(self) -> bool:
        return self._button_clicked

    @button_clicked.setter
    def button_clicked(self, val: bool) -> None:
        self._button_clicked = val

    @property
    def button_hovered(self) -> bool:
        return self._button_hovered

    @button_hovered.setter
    def button_hovered(self, val: bool) -> None:
        self._button_hovered = val

    def get_fps(self) -> int:
        return round(self._clock.get_fps())

    def add_event_handler(self, event: int, handler: Callable[[pygame.Event], None]) -> None:
        self._event_handlers[event] = handler

    def update(self, target_fps: int) -> float:
        self._quit = False
        self._click = False
        self._input = (None, "", None)
        self._resized = False

        self._button_clicked = False
        self.button_hovered = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._click = True
            elif event.type == pygame.KEYDOWN:
                self._input = (event.unicode, pygame.key.name(event.key), event.key)
            elif event.type == pygame.WINDOWRESIZED:
                self._resized = True

            # for handling custom events
            if event.type in self._event_handlers:
                self._event_handlers[event.type](event)

        # hardcoded 60
        # develop app and test with 60 fps, but delta time
        # will adjust for any frame rate

        return self._clock.tick(target_fps) * 60 / 1000
