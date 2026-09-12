from typing import Tuple, Union

import pygame

from .events import Events
from .graphics import Graphics
from .camera import Camera

DEFAULT_STYLE = {"colour": "black",
                 "highlight": "yellow",
                 "border colour": "black",
                 "border size": 0,
                 "font": "arial",
                 "font size": 30,
                 "font colour": "white"}


class Button:
    def __init__(self, rect: Union[pygame.Rect, Tuple[int, int, int, int]], text: str, style: Union[None, dict] = None,
                 center: Union[None, pygame.Rect] = None, cam: Camera = None) -> None:
        self._style = DEFAULT_STYLE.copy()
        if style is not None:
            self._style.update(style)

        if isinstance(rect, pygame.Rect):
            self._rect = rect
        else:
            self._rect = pygame.Rect(rect)

        if center != None:
            self._rect.center = pygame.Rect(*center).center

        self._text = text

        self._hover = False

        self._cam = cam

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def style(self) -> dict:
        return self._style

    @property
    def text(self) -> str:
        return self._text

    def update(self, events: Events) -> Tuple[bool, bool]:
        if self._cam is not None:
            rect = self._rect.copy()
            rect.x += self._cam.x
            rect.y += self._cam.y

        click = False
        self._hover = False

        if rect.collidepoint(events.mouse):
            self._hover = True
            if events.click:
                click = True

        return click, self._hover

    def draw(self, graphics: Graphics) -> None:
        if self._cam is not None:
            rect = self._rect.copy()
            rect.x += self._cam.x
            rect.y += self._cam.y

        pygame.draw.rect(graphics.surf, self._style["highlight"] if self._hover else self._style["colour"], rect)
        if self._style["border size"] > 0:
            pygame.draw.rect(graphics.surface, self._style["border colour"], rect, self._style["border size"])

        graphics.write(self._text, (0, 0), font=self._style["font"], size=self._style["font size"],
                       colour=self._style["font colour"], center=rect, use_cam=False)
