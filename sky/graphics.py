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
    
    def render_image(self, name: str, angle: Union[None, int, float] = None,
             size: Union[None, Tuple[int, int]] = None, transparency: Union[None, int] = None, radians: bool = False,
             update_cache: bool = True) -> pygame.Surface:
        
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

            if transparency is not None:
                img.set_alpha(transparency)

            if update_cache:
                self._image_cache[cache_key] = img

        return img

    def draw(self, name: str, pos: Tuple[int, int], angle: Union[None, int, float] = None,
             size: Union[None, Tuple[int, int]] = None, transparency: Union[None, int] = None, radians: bool = False,
             center: Union[None, pygame.Rect] = None, use_cam: bool = True, update_cache: bool = True) -> pygame.Rect:
        
        img = self.render_image(name, angle=angle, size=size, transparency=transparency, radians=radians, update_cache=update_cache)

        if center is not None:
            rect = img.get_rect(center=pygame.Rect(center).center)
            # pos will act as offsets
            rect.x += pos[0]
            rect.y += pos[1]
            pos = rect.topleft

            if angle is not None:
                pos = img.get_rect(center=rect.center).topleft

        elif angle is not None:
            pos = img.get_rect(center=pos).topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(img, pos)

    def render_text(self, text: str, size: int = 30, colour: Union[pygame.Color, str] = "white",
              transparency: Union[None, int] = None, font: str = "arial", update_cache: bool = True) -> pygame.Surface:
        text = str(text)

        cache_key = text + str(size) + str(colour) + str(transparency) + font

        if cache_key in self._image_cache:
            text_surf = self._image_cache[cache_key]
        else:
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

            text_surf = font_.render(text, True, colour)

            if transparency is not None:
                text_surf.set_alpha(transparency)

            if update_cache:
                self._image_cache[cache_key] = text_surf

        return text_surf

    def write(self, text: str, pos: Tuple[int, int], size: int = 30, colour: Union[pygame.Color, str] = "white",
              transparency: Union[None, int] = None, font: str = "arial", center: Union[None, pygame.Rect] = None,
              use_cam: bool = True, update_cache: bool = True) -> pygame.Rect:
        text = str(text)

        text_surf = self.render_text(text, size=size, colour=colour, transparency=transparency, font=font, update_cache=update_cache)

        if center is not None:
            rect = text_surf.get_rect(center=pygame.Rect(center).center)
            # pos will act as offsets
            rect.x += pos[0]
            rect.y += pos[1]
            pos = rect.topleft

        if use_cam and self._cam is not None:
            pos = (pos[0] + self._cam.x, pos[1] + self._cam.y)

        return self._target_surf.blit(text_surf, pos)

    def get_image(self, name: str) -> pygame.Surface:
        return self._original_images[name]

    def clear_cache(self) -> None:
        self._image_cache.clear()
