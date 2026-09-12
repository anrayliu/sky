from typing import Union


class Location:
    def __init__(self, main) -> None:
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.cam = main.cam
        self.main = main

    # called on location startup
    def start(self, args_: Union[None, dict]) -> None:
        pass

    # called on transition to different location
    def stop(self) -> None:
        pass

    # called on window resize
    def scale(self) -> None:
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
        self.main.set_location(loc, args_)
