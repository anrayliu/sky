import math
import os
from typing import Tuple, Union, Dict

import pygame

from .camera import Camera


class Graphics:
    def __init__(self, surf: pygame.Surface, cam: Camera = None) -> None:
        self._target_surf = surf

        self._original_images = {}
        self._image_cache = {}

        self._font_objs = {}
        self._font_paths = []

        self._cam = cam

    @property
    def surf(self) -> pygame.Surface:
        return self._target_surf

    @surf.setter
    def surf(self, new_surf: pygame.Surface) -> None:
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
                self._original_images[name] = img

                if sizes is not None and name in sizes:
                    # build a default cache key
                    self._image_cache[name + str(sizes[name]) + str(None) + str(None)] = pygame.transform.smoothscale(img, sizes[name])

                loaded += 1

        return loaded

    def draw(self, name: str, pos: Union[int, int], angle: Union[None, int, float] = None,
             size: Union[None, Tuple[int, int]] = None, transparency: Union[None, int] = None, radians: bool = False,
             center: Union[None, pygame.Rect] = None, use_cam: bool = True) -> pygame.Rect:
        
        cache_key = name + str(size) + str(angle) + str(transparency)

        if cache_key in self._image_cache:
            img = self._image_cache[cache_key]
        else:
            img = self._original_images[name].copy()

            if size is not None:
                img = pygame.transform.smoothscale(img, size)

            if angle is not None:
                if radians:
                    angle = math.degrees(angle)
                img = pygame.transform.rotate(img, angle)
                pos = img.get_rect(center=pos).topleft

            if transparency is not None:
                img.set_alpha(transparency)

            self._image_cache[cache_key] = img

        if center is not None:
            pos = img.get_rect(center=pygame.Rect(center).center).topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(img, pos)

    def write(self, text: str, pos: Tuple[int, int], size: int = 30, colour: Union[pygame.Color, str] = "white",
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

        text_ = font_.render(str(text), True, colour)

        if transparency is not None:
            text_.set_alpha(transparency)

        if center is not None:
            pos = text_.get_rect(center=pygame.Rect(center).center).topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(text_, pos)

    def get_image(self, name: str) -> pygame.Surface:
        return self._original_images[name]
