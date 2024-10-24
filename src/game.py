from typing import Callable, Tuple
from constants import MouseButton
from pygame import Surface
from scene import Scene
from assets import Assets

class Game(Scene):
    def __init__(self, width: int, height: int, bombs: int) -> None:
        self.width = width
        self.height = height
        self.bombs = bombs

    def start(self, change_scene: Callable[['Scene'], None], resize_screen: Callable[[Tuple[int, int]], None]) -> None:
        resize_screen((self.height * 16, self.width * 16))
        self.change_scene = change_scene

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        print("game", btn, pos)
        # TODO: implement actual game logic
        # TODO: generate bombs
        # TODO: floodfill clicks
        # TODO: check ending conditions

    def draw(self, screen: Surface) -> None:
        # TODO: restart button
        # TODO: return to menu buton
        # TODO: bomb counter
        # TODO: timer
        # TODO: draw actual game state
        for r in range(self.height):
            for c in range(self.width):
                screen.blit(Assets["unknown"], (r * 16, c * 16))
