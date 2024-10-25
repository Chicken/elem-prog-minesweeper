from entity import Entity
from game import Game
import pygame as pg
from typing import Callable, Tuple
from constants import TILE_SIZE, MouseButton
from pygame import Surface
from scene import Scene
from assets import Assets

class Menu(Scene):
    def __init__(self) -> None:
        pass

    def start(self, change_scene: Callable[['Scene'], None], resize_screen: Callable[[Tuple[int, int]], None]) -> None:
        resize_screen((320, 320))
        self.change_scene = change_scene
        self.buttons = []

        self.font = pg.font.Font(None, 40)

        # TODO: abstract Button class maybe ?
        start_button = Entity(
            Surface((120, 40)),
            (100, 240),
            click_handler=lambda _btn, _pos: self.start_game()
        )
        start_button.surface.fill((0x4b, 0x55, 0x63))
        start_button.surface.blit(
            self.font.render("Start", True, (255, 255, 255)),
            (60 - self.font.size("Start")[0] / 2, 20 - self.font.size("Start")[1] / 2)
        )
        self.buttons.append(start_button)

        # TODO: implement changing field size and mine count
        # TODO: implement scrollable history
        # TODO: implement quit button

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        # forward click to clicked button
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                if btn == MouseButton.MOUSE_LEFT:
                    button.handle_click(btn, pos)

    def start_game(self) -> None:
        self.change_scene(Game(10, 10, 20))

    def draw(self, screen: Surface) -> None:
        # TODO: draw a title

        for r in range(20):
            for c in range(20):
                screen.blit(Assets["unknown"], (c * TILE_SIZE, r * TILE_SIZE))
        
        for btn in self.buttons:
            btn.draw(screen)

