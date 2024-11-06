from typing import Any, Callable, Optional, Tuple
from pygame import Surface, Rect
from constants import MouseButton

class Entity:
    """
    Represents a generic game entity.
    An entity has a position and a surface (and therefore a size/rect).
    An entity can have something to update what it looks like and something to handle clicks on it.
    """

    def __init__(
            self,
            surface: Surface,
            pos: Tuple[int, int],
            click_handler: Optional[Callable[[MouseButton, Tuple[int, int]], Any]] = None,
            update_handler: Optional[Callable[[], Any]] = None
            ) -> None:
        self.surface = surface
        self.pos = pos
        self.rect = Rect(pos, surface.get_size())
        self.click_handler = click_handler
        self.update_handler = update_handler

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        """
        Passes a click event to a defined click handler
        """
        if self.click_handler is not None:
            self.click_handler(btn, pos)

    def update(self) -> None:
        """
        Runs a defined updater function to redraw the entity
        """
        if self.update_handler is not None:
            self.update_handler()

    def draw(self, screen: Surface) -> None:
        """
        Draws the entity on a surface at its position
        """
        screen.blit(self.surface, self.pos)
