from typing import Callable, Optional, Tuple
from constants import MouseButton
from pygame import Surface, Rect

class Entity:
    def __init__(
            self,
            surface: Surface,
            pos: Tuple[int, int],
            click_handler: Optional[Callable[[MouseButton, Tuple[int, int]], None]] = None
            ) -> None:
        self.surface = surface
        self.pos = pos
        self.rect = Rect(pos, surface.get_size())
        self.click_handler = click_handler

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        if self.click_handler is not None:
            self.click_handler(btn, pos)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.surface, self.pos)
