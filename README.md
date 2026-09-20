# sky

This mini-framework is designed to abstract away some tediums I frequently encounter with Pygame.
The main abstractions are `Camera`, `Events`, and `Graphics`. To make things even easier, 
the `Sky` class groups and initializes all of them at once.

Look at this initialization code in `main.py`:
```
pygame.init()

self.win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("sky demo")

try:
    pygame.display.set_icon(pygame.image.load("assets\\icon.png"))
except FileNotFoundError:
    pass

self.sky = sky.Sky(self.win)
self.sky.locations["game"] = Game(self.sky)
self.sky.set_location("game")
```
Notice how the first half still consists of core Pygame operations like `init()` and `display.set_mode()`.
Sky is designed to work _with_ Pygame, not to replace it. It provides abstractions for helpers I found myself
repeatedly writing, but it doesn't hide the lower-level control that Pygame provides.

## features

- generic button class with css-esque customization
- game world camera
- sinusoidal screen shake
- flat state machine
- automatic delta time
- event handler
- asset manager (images and fonts)
- image caching for transformations
- post processing
- keep full control over game loop

# Documentation

Still a WIP, and some parts may not be fully clear, but in this AI-era, it shouldn't be too hard to probe an agent about it.

# *class* Button(rect: pygame.Rect | (int, int, int, int), text: str, style: dict = None, center: pygame.Rect = None, cam: sky.Camera = None)

If several buttons are overlapping, the first one to be processed will be the only one updating `click` and `hover` properties.

## Parameters

- `rect: pygame.Rect | (int, int, int, int)` - Rect representing button in global space. If a tuple is provided instead, a `pygame.Rect` will be automatically created.
- `text: str` - Text to display on button.
- `style: dict` - Dictionary containing button style properties. If not provided, a default style will be used.
    - `colour` - Default button colour. Default is `"black"`.
    - `highlight` - Button colour when being hovered over. Default is `"yellow"`.
    - `border colour` - Colour of button edges. Default is `"white"`.
    - `border size` - Thickness of button edges. Default is `0`.
    - `rounding` - Button corner rounding. Default is `0`.
    - `offset x` - Horizontal text offset in button. Default is `0`.
    - `offset y` - Vertical text offset in button. Default is `0`.
    - `text only` - Whether to draw only the text and not the button rect. Default is `False`.
    - `font` - Text font. Default is `"arial"`.
    - `font size` - Text size. Default is `30`.
    - `font colour` - Text colour. Default is `"white"`.
- `center: pygame.Rect` - If a rect is provided here, the button will be centered inside. The positional values provided in `rect`  will then be treated as offsets, applied after centering.
- `cam: sky.Camera` - If provided, button will be rendered in game space instead of global space.

## Properties

- `rect: pygame.Rect` - Same as given argument.
- `style: dict` - Same as given argument.
- `text: str` - Same as given argument. Can be set.
- `click: bool` - `True` if button was pressed when `update()` was last called.
- `hover: bool` - `True` if button was moused over when `update()` was last called.

## Methods

- `update(events: sky.Events)` - Updates `hover` and `click` properties.
- `draw(graphics: sky.Graphics)` - Renders the button.

# *class* Camera(size: (int, int), restriction: pygame.Rect = None)

Responsible for converting global space coordinates to game space coordinates. Global space coordinates are absolute positions on the screen, while game space coordinates include the camera offset. The camera offset will change based on which position the camera is tracking and screen shake.

## Parameters

- `size: (int, int)` - Width and height of camera. Usually just the window size.
- `restriction: pygame.Rect` - If provided, camera will never move outside this rect.

## Properties

- `rect: pygame.Rect` - Rect representing camera in global space.
- `restriction: pygame.Rect` - Same as given argument.
- `x: int` - Offset to be added to global space coordinates to convert them to game space coordinates.
- `y: int` - Offset to be added to global space coordinates to convert them to game space coordinates.

## Methods

- `update(pos: (int, int), dt: float, speed: int = 15)` - Moves camera to focus onto `pos` (global space coordinates). Speed can be adjusted with `steps` (lower is faster). Pass a delta time (see `sky.Events`) to maintain consistent camera speed across various frame rates.
- `shake(initial_force: int = 10, x_multiplier: int = 5, y_multiplier: int = 5, steps: int = 10)` - Adds sinusoidal screen shake. Baseline intensity depends on `initial_force` while additional control on each axis can be controlled with `x_multiplier` and `y_multiplier`. Shake duration can be adjusted with `steps` (lower is shorter).
- `reset(size: (int, int) = None, restriction: pygame.Rect = None, stop_shake: bool = False, pos: (int, int) = None)` - Resets camera properties if provided.
- `apply(x: int, y: int) -> (int, int)` - Converts a global space coordinate to a game space coordinate.

# *class* Events

Event and frame rate manager.

## Properties

- `quit: bool` - `True` if the window 'X' button was clicked.
- `click: bool` - `True` if left mouse button was clicked.
- `resized: bool` - `True` if window was resized.
- `input: (any, str, any)` - `(None, "", None)` if no keyboard input, otherwise this tuple will hold the keystroke unicode, name, and Pygame constant.
- `key_down: pygame.key.ScancodeWrapper` - Equivalent to `pygame.key.get_pressed()`.
- `mouse_down: (bool, bool, bool)` - Equivalent to `pygame.mouse.get_pressed()`.
- `mouse: (int, int)` - Mouse coordinates (in global space).

## Methods

- `get_fps() -> int` - Returns current frames per second.
- `add_event_handler(event: int, handler: func(pygame.Event) -> None)` - Used to add custom event handling. Pass a Pygame event constant (e.g. `pygame.MOUSEMOTION`) and function to be called when the event is occurs. The function will be passed the `pygame.Event` object.
- `update(target_fps: int) -> float` - Updates properties and maintains desired frame rate. Returns the delta time between frames, which can be multiplied against hardcoded values to decouple them from frame rate. The delta time assumes a baseline of 60 fps. In other words, during development, hardcoded values designed for 60 fps, when multiplied with the returned delta time, will retain their speed across all frame rates.

# *class* Graphics(surf: pygame.Surface, cam: sky.Camera = None)

Resource manager for images and fonts.

## Parameters

- `surf: pygame.Surface` - Surface to draw to.
- `cam: sky.Camera` - If a camera object is passed, renders will automatically convert global space coordinates to game space coordinates, by default.

## Properties

- `surf: pygame.Surface` - Same as given argument. Can be set.

## Methods

- `load_folder(path: str, sizes: {str: (int, int)}) -> int` - Recursively walks down `path` and loads all `.ttf`, `.otf`, `.png` and `.jpg` files. Loaded resource names do not include extensions (e.g. reference `"apple.png"` simply as `"apple"`). Images can also be resized if their name and desired size is found in `sizes`. Returns number of resources loaded.
- `render_image(name: str, angle: int | float = None, size: (int, int) = None, transparency: int = None, radians: bool = False, update_cache: bool = False) -> pygame.Surface` - Returns an image surface with the desired transformations applied. `Graphics` keeps an internal cache for surface transformations, so further renders with the same transformations will be very efficient. Set `update_cache` to `True` to enable caching for this transformation (if some images are changing frequently, it will not benefit from caching and will only inflate memory usage). If `radians` is `True`, the given `angle` value will be treated as radians, otherwise degrees. `transparency` wants an alpha value `0-255`.
- `draw(name: str, pos: (int, int), angle: int | float = None, size: (int, int) = None, transparency: int = None, radians: bool = False, center: pygame.Rect = None, use_cam: bool = True, update_cache: bool = False) -> pygame.Rect` - Draws an image onto `surf`. Uses `render_image` for transformations and caching. If a rect is passed in `center`, the image will be rendered in the middle of it. In such cases, `pos` will then become a positional offset applied after centering. Otherwise, `pos` uses global space coordinates. If a camera object was configured, the image will be drawn using game space coordinates unless `use_cam` is set to `False`. Returns a rect representing the changed area on `surf`.
- `render_text(text: str, size: int = 30, colour: str | pygame.Color = "white", transparency: int = None, font: str = "arial", update_cache: bool = False) -> pygame.Surface` - Returns a text surface with the desired transformations applied. `Graphics` keeps an internal cache for surface transformations, so further renders with the same transformations will be very efficient. Set `update_cache` to `True` to enable caching for this transformation (if certain text are changing frequently, it will not benefit from caching and will only inflate memory usage). If `font` is a valid system font, it will automatically be loaded. `transparency` wants an alpha value `0-255`.
- `write(text: str, pos: (int, int), size: int = 30, colour: str | pygame.Color = "white", transparency: int = None, font: str = "arial", center: pygame.Rect = None, use_cam: bool = True, update_cache: bool = False) -> pygame.Rect` - Draws text onto `surf`. Uses `render_text` for transformations and caching. If a rect is passed in `center`, the text will be rendered in the middle of it. In such cases, `pos` will then become a positional offset applied after centering. Otherwise, `pos` uses global space coordinates. If a camera object was configured, the text will be drawn using game space coordinates unless `use_cam` is set to `False`. Returns a rect representing the changed area on `surf`.
- `get_image(name: str) -> pygame.Surface` - Returns original loaded image surface with no transformations.
- `clear_cache() -> None` - Clears internal cache.

# *class* Location(sky: Sky)

Represents a single game state. Users are meant to create their own game state classes inheriting this.

## Parameters

- `sky: sky.Sky` - Global sky object.

## Methods

- `start(args_: {any: any})` - Automatically called when location starts. `args_` contains information passed from the previous location. `"sky.previous_location"` will always contain the name of the previous location or `None` if this location is the first.
- `stop()` - Automatically called when location stops (e.g. transition to a different location).
- `scale(new_size: (int, int))` - Automatically called when window is resized.
- `cleanup()` - Automatically called on app shutdown.
- `update(dt: float)` - Automatically called every frame. Game logic goes here. The delta time is also automatically passed.
- `draw()` - Conventional for drawing-related code to go in here. This is _not_ automatically called and is the responsibility of `update()`. This method exists mostly for organizational reasons (separating logic and drawing makes it easier to implement features like pausing), as there's nothing inherently special about this.
- `set_location(loc: str, args_: {any: any})` - Alias to `Sky.set_location`.

# *class* Sky(win: pygame.Surface)

Aggregate manager for `Graphics`, `Events`, `Camera`, and `Location` objects and state machine. This object tracks all of the possible locations and automatically updates the active one. Only one location can be active at any given time, but the active location can freely change. Callbacks for all locations, not just the active one, are automatically called if necessary.

## Parameter

- `win: pygame.Surface` - Window surface.

## Properties

- `cam: sky.Camera` - Auto-instantiated camera object.
- `graphics: sky.Graphics` - Auto-instantiated graphics object.
- `events: sky.Events` - Auto-instantiated events object.
- `win: pygame.Surface` - Same as given argument.
- `locations: {str: Location}` - Names of tracked location objects.
- `location: str` - Current active location.

## Methods

- `set_location(loc: str, args_: {any: any})` - Used to transition to a new location `loc`. `args_` can be used to pass information to the `start()` call of the new location.
- `quit()` - Calls `stop()` for current location and `cleanup()` for all locations. 
- `update(target_fps: int, show_fps: bool = False, debug: bool = False, post_processing: func(np.ndarray) -> ndarray = sky.PostProcessing.none) -> None` - Updates locations. Updates `events`, passing `target_fps`. `show_fps` enables an fps counter in the topleft corner, `debug` toggles some debug visuals, and `post_processing` accepts a NumPy transformation function. The post-processing is applied after all `update()` and `draw()` calls.

# *class* PostProcessing

Small collection of post processing functions to try. Requires `opencv-python` to be installed.

Example usage:
```
self.sky.update(60, post_processing=sky.PostProcessing.vhs)
```

## Static Methods

- `none`
- `blur`
- `greyscale`
- `noise`
- `letterbox`
- `cel_shading`
- `flipup`
- `fliplr`
- `rotate90`
- `rotate270`
- `vhs`
- `emboss`
- `sharpen`
- `bgr2rgb`
