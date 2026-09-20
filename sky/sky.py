from __future__ import annotations
from typing import Dict, TYPE_CHECKING, Callable

import pygame

from .camera import Camera
from .events import Events
from .graphics import Graphics

# gets around circular import for type hint
if TYPE_CHECKING:
    from .location import Location


# manager object for all sky abstractions

class Sky:
    def __init__(self, win: pygame.Surface) -> None:
        self._cam = Camera(win.get_size())
        self._graphics = Graphics(win, cam=self._cam)
        self._events = Events()
        self._win = win

        try:
            self._graphics.load_folder("assets")
        except FileNotFoundError:
            pass

        self._locations = {}
        self._location = None

        self._scale()

    @property
    def cam(self) -> Camera:
        return self._cam

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def events(self) -> Events:
        return self._events

    @property
    def win(self) -> pygame.Surface:
        return self._win

    @property
    def locations(self) -> Dict[str, Location]:
        return self._locations

    @property
    def location(self) -> str:
        return self._location

    def _scale(self):
        for loc in self._locations.values():
            loc.scale(self.win.get_size())

    def set_location(self, loc: str, args_: Dict[any, any] = None) -> None:
        if self._location is not None:
            self._locations[self._location].stop()

        self._location = loc
        self._locations[self._location].start(args_)

    def quit(self) -> None:
        if self._location is not None:
            self._locations[self._location].stop()

        for loc in self._locations.values():
            loc.cleanup()

    def update(self, target_fps: int, show_fps: bool = False, debug: bool = False, post_processing: Callable = None) -> None:
        dt = self._events.update(target_fps)
        if self._events.resized:
            self._scale()

        # each location is responsible for calling draw() by themselves
        # main is responsible for calling window methods
        self._locations[self._location].update(dt)

        if post_processing is not None:
            self.win.blit(pygame.image.frombuffer(post_processing(pygame.surfarray.pixels3d(pygame.display.get_surface()).swapaxes(0, 1)).tobytes(), self.win.get_size(), "RGB"), (0, 0))

        if debug:
            self._cam.show_borders(self.win)

        if show_fps:
            self._graphics.write(f"FPS: {self._events.get_fps()}", pos=(0, 0), colour=(255, 255, 255), size=15, use_cam=False)
