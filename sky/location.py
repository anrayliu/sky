from typing import Tuple, Union
from .sky import Sky


class Location:
    def __init__(self, sky: Sky) -> None:
        self.graphics = sky.graphics
        self.events = sky.events
        self.win = sky.win
        self.cam = sky.cam

        self._switch_func = sky.set_location

    # called on location startup
    def start(self, args_: Union[None, dict]) -> None:
        pass

    # called on transition to different location
    def stop(self) -> None:
        pass

    # called on window resize
    def scale(self, new_size: Tuple[int, int]) -> None:
        pass

    # called on app close
    def cleanup(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self.draw()

    def draw(self) -> None:
        pass

    # wrapper for convenience
    def set_location(self, loc: str, args_: Union[None, dict] = None) -> None:
        self._switch_func(loc, args_)
