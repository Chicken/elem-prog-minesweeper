from entity import Entity
from game import Game
import pygame as pg
from typing import Callable, Tuple
from constants import MAX_HEIGHT, MAX_MINES_PERCENTAGE, MAX_WIDTH, MIN_HEIGHT, MIN_MINES, MIN_WIDTH, TILE_SIZE, MouseButton
from pygame import Surface
from scene import Scene
from assets import Assets
from sfx import Sfx

class Menu(Scene):
    def __init__(self) -> None:
        self.game_width = 10
        self.game_height = 10
        self.game_mines = 20
        pass

    def start(self, change_scene: Callable[['Scene'], None], resize_screen: Callable[[Tuple[int, int]], None]) -> None:
        resize_screen((320, 320))
        self.change_scene = change_scene
        self.entities = []

        # load different font sizes for different texts
        self.font50 = pg.font.Font("./assets/PixelifySans-Regular.ttf", 50)
        self.font30 = pg.font.Font("./assets/PixelifySans-Regular.ttf", 30)
        self.font25 = pg.font.Font("./assets/PixelifySans-Regular.ttf", 25)

        # menu buttons and settings displays 
        
        start_button = Entity(
            Surface((120, 30)),
            (100, 280),
            click_handler=lambda _btn, _pos: self.start_game()
        )
        start_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(start_button.surface, self.font30, (255, 255, 255), "Start")
        self.entities.append(start_button)

        exit_button = Entity(
            Surface((60, 30)),
            (10, 280),
            click_handler=lambda _btn, _pos: self.exit_game()
        )
        exit_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(exit_button.surface, self.font25, (255, 255, 255), "Exit")
        self.entities.append(exit_button)

        decrease_width_button = Entity(
            Surface((20, 20)),
            (20, 250),
            click_handler=lambda _btn, _pos: self.decrease_width()
        )
        decrease_width_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(decrease_width_button.surface, self.font25, (255, 255, 255), "-")
        self.entities.append(decrease_width_button)

        self.width_display = Entity(
            Surface((40, 20)),
            (40, 250),
            update_handler=lambda: self.update_width_display()
        )
        self.entities.append(self.width_display)

        increase_width_button = Entity(
            Surface((20, 20)),
            (80, 250),
            click_handler=lambda _btn, _pos: self.increase_width()
        )
        increase_width_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(increase_width_button.surface, self.font25, (255, 255, 255), "+")
        self.entities.append(increase_width_button)

        decrease_height_button = Entity(
            Surface((20, 20)),
            (120, 250),
            click_handler=lambda _btn, _pos: self.decrease_height()
        )
        decrease_height_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(decrease_height_button.surface, self.font25, (255, 255, 255), "-")
        self.entities.append(decrease_height_button)

        self.height_display = Entity(
            Surface((40, 20)),
            (140, 250),
            update_handler=lambda: self.update_height_display()
        )
        self.entities.append(self.height_display)

        increase_height_button = Entity(
            Surface((20, 20)),
            (180, 250),
            click_handler=lambda _btn, _pos: self.increase_height()
        )
        increase_height_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(increase_height_button.surface, self.font25, (255, 255, 255), "+")
        self.entities.append(increase_height_button)

        decrease_mines_button = Entity(
            Surface((20, 20)),
            (220, 250),
            click_handler=lambda _btn, _pos: self.decrease_mines()
        )
        decrease_mines_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(decrease_mines_button.surface, self.font25, (255, 255, 255), "-")
        self.entities.append(decrease_mines_button)

        self.mines_display = Entity(
            Surface((40, 20)),
            (240, 250),
            update_handler=lambda: self.update_mines_display()
        )
        self.entities.append(self.mines_display)

        increase_mines_button = Entity(
            Surface((20, 20)),
            (280, 250),
            click_handler=lambda _btn, _pos: self.increase_mines()
        )
        increase_mines_button.surface.fill((0x4b, 0x55, 0x63))
        self.draw_text_centered(increase_mines_button.surface, self.font25, (255, 255, 255), "+")
        self.entities.append(increase_mines_button)

        # TODO: implement scrollable history

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        # forward click to clicked button
        for button in self.entities:
            if button.rect.collidepoint(pos):
                if btn == MouseButton.MOUSE_LEFT:
                    button.handle_click(btn, pos)

    def draw_text_centered(self, surface: Surface, font: pg.font.Font, color: Tuple[int, int, int], text: str) -> None:
        surface.blit(
            font.render(text, False, color),
            (
                int(surface.get_width() / 2 - font.size(text)[0] / 2),
                int(surface.get_height() / 2 - font.size(text)[1] / 2)
            )
        )

    # button actions

    def start_game(self) -> None:
        self.change_scene(Game(self.game_width, self.game_height, self.game_mines))

    def exit_game(self) -> None:
        pg.event.post(pg.event.Event(pg.QUIT))

    def decrease_width(self) -> None:
        if self.game_width > MIN_WIDTH:
            self.game_width -= 1
            max_mines = self.game_width * self.game_height * MAX_MINES_PERCENTAGE
            if self.game_mines > max_mines:
                self.game_mines = int(max_mines)
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    def increase_width(self) -> None:
        if self.game_width < MAX_WIDTH:
            self.game_width += 1
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    def decrease_height(self) -> None:
        if self.game_height > MIN_HEIGHT:
            self.game_height -= 1
            max_mines = self.game_width * self.game_height * MAX_MINES_PERCENTAGE
            if self.game_mines > max_mines:
                self.game_mines = int(max_mines)
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    def increase_height(self) -> None:
        if self.game_height < MAX_HEIGHT:
            self.game_height += 1
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    def decrease_mines(self) -> None:
        if self.game_mines > MIN_MINES:
            self.game_mines -= 1
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    def increase_mines(self) -> None:
        max_mines = self.game_width * self.game_height * MAX_MINES_PERCENTAGE
        if self.game_mines < max_mines:
            self.game_mines += 1
            Sfx["positive_btn"].play()
        else:
            Sfx["negative_btn"].play()

    # settings display updater functions

    def update_width_display(self) -> None:
        self.width_display.surface.fill((0x6b, 0x72, 0x80))
        self.draw_text_centered(self.width_display.surface, self.font25, (255, 255, 255), str(self.game_width))

    def update_height_display(self) -> None:
        self.height_display.surface.fill((0x6b, 0x72, 0x80))
        self.draw_text_centered(self.height_display.surface, self.font25, (255, 255, 255), str(self.game_height))

    def update_mines_display(self) -> None:
        self.mines_display.surface.fill((0x6b, 0x72, 0x80))
        self.draw_text_centered(self.mines_display.surface, self.font25, (255, 255, 255), str(self.game_mines))

    def draw(self, screen: Surface) -> None:
        # background

        for r in range(20):
            for c in range(20):
                screen.blit(Assets["unknown"], (c * TILE_SIZE, r * TILE_SIZE))

        # on screen texts

        screen.blit(
            self.font50.render(
                "Minesweeper",
                False,
                (255, 255, 255)
            ),
            (int(screen.get_width() / 2 - self.font50.size("Minesweeper")[0] / 2),0)
        )

        screen.blit(
            self.font25.render(
                "Width",
                False,
                (255, 255, 255)
            ),
            (25,220)
        )

        screen.blit(
            self.font25.render(
                "Height",
                False,
                (255, 255, 255)
            ),
            (120,220)
        )

        screen.blit(
            self.font25.render(
                "Mines",
                False,
                (255, 255, 255)
            ),
            (227,220)
        )
        
        # buttons and displays

        for ent in self.entities:
            ent.update()
            ent.draw(screen)

