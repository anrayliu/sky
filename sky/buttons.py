from typing import Tuple, Union

import pygame

from .events import Events
from .graphics import Graphics
from .camera import Camera

DEFAULT_STYLE = {"colour": "black",
                 "highlight": "yellow",
                 "border colour": "white",
                 "border size": 0,
                 "rounding": 0,
                 "offset x": 0,
                 "offset y": 0,
                 "text only": False,
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

        if center is not None:
            self._rect.center = pygame.Rect(*center).center

        self._text = text
        self._cam = cam

        self._hover = False
        self._click = False

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def style(self) -> dict:
        return self._style

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        self._text  = new_text

    @property
    def hover(self) -> bool:
        return self._hover

    @property
    def click(self) -> bool:
        return self._click

    def _get_rect(self) -> pygame.Rect:
        if self._cam is not None:
            rect = self._rect.copy()
            rect.x += self._cam.x
            rect.y += self._cam.y
        else:
            rect = self._rect

        return rect

    def update(self, events: Events) -> None:
        rect = self._get_rect()

        self._click = False
        self._hover = False

        if rect.collidepoint(events.mouse):
            self._hover = True
            if events.click:
                self._click = True

    def draw(self, graphics: Graphics) -> None:
        rect = self._get_rect()

        if not self._style["text only"]:
            pygame.draw.rect(graphics.surf, self._style["highlight"] if self._hover else self._style["colour"], rect, 0,
                            self._style["rounding"], self._style["rounding"], self._style["rounding"],
                            self._style["rounding"])
            if self._style["border size"] > 0:
                pygame.draw.rect(graphics.surf, self._style["border colour"], rect, self._style["border size"])

        # don't apply cam offset because rect already has it applied
        graphics.write(self._text, (self._style["offset x"], self._style["offset y"]), font=self._style["font"], size=self._style["font size"],
                       colour=self._style["font colour"], center=rect, use_cam=False)
