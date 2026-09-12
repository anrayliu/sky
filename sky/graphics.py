import math
import os
from typing import Tuple, Union, Dict

import pygame

from .camera import Camera


class Graphics:
    def __init__(self, surf: pygame.Surface, cam: Camera = None) -> None:
        self._target_surf = surf

        self._images = {}

        self._font_objs = {}
        self._font_paths = []

        self._cam = cam

    @property
    def surf(self) -> pygame.Surface:
        return self._target_surf

    @surf.setter
    def surf(self, new_surf: pygame.Surface) -> None:
        if not isinstance(new_surf, pygame.Surface):
            raise ValueError("must be a surface")

        self._target_surf = new_surf

    def load_folder(self, path: str, sizes: Union[None, Dict[str, Tuple[int, int]]] = None) -> int:
        loaded = 0

        for file in os.listdir(path):
            if file.endswith(".ttf") or file.endswith(".otf"):
                self._font_paths.append(os.path.join(path, file))
                loaded += 1

            elif file.endswith(".png") or file.endswith(".jpg"):
                name = os.path.splitext(file)[0]

                img = pygame.image.load(os.path.join(path, file)).convert_alpha()

                if sizes is not None and name in sizes:
                    img = pygame.transform.smoothscale(img, sizes[name])

                self._images[name] = img

                loaded += 1

        return loaded

    def draw(self, image: str, pos: Union[int, int], angle: Union[None, int, float] = None,
             size: Union[None, Tuple[int, int]] = None, transparency: Union[None, int] = None, radians: bool = False,
             center: Union[None, pygame.Rect] = None, use_cam: bool = True) -> pygame.Rect:
        image_ = self._images[image].copy()

        if size != None:
            image_ = pygame.transform.scale(image_, size)

        if angle != None:
            if radians:
                angle = math.degrees(angle)
            image_ = pygame.transform.rotate(image_, angle)
            pos = image_.get_rect(center=pos).topleft

        if transparency != None:
            image_.set_alpha(transparency)

        if center != None:
            pos = image_.get_rect(center=pygame.Rect(center).center).topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(image_, pos)

    def write(self, text: str, pos: Union[int, int], size: int = 30, colour: Union[pygame.Color, str] = "white",
              transparency: Union[None, int] = None, font: str = "arial", center: Union[None, pygame.Rect] = None,
              use_cam: bool = True) -> pygame.Rect:
        try:
            font_ = self._font_objs[font + str(size)]
        except KeyError:
            if font in pygame.font.get_fonts():
                font_ = pygame.font.SysFont(font, size)
            else:
                for path in self._font_paths:
                    if os.path.splitext(os.path.basename(path))[0] == font:
                        font_ = pygame.font.Font(path, size)
                        break
                else:
                    raise RuntimeError("no font file found")

            self._font_objs[font + str(size)] = font_

        text_ = font_.render(text, True, colour)

        if transparency != None:
            text_.set_alpha(transparency)

        if center != None:
            pos = text_.get_rect(center=pygame.Rect(center).center).topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(text_, pos)
