from typing import Any, Callable, Optional, Tuple
from constants import MouseButton
from pygame import Surface, Rect

class Entity:
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
        if self.click_handler is not None:
            self.click_handler(btn, pos)

    def update(self) -> None:
        if self.update_handler is not None:
            self.update_handler()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.surface, self.pos)
