from entity import Entity
from history import History
import pygame as pg
from constants import HISTORY_ITEM_HEIGHT, MAX_HEIGHT, MAX_MINES_PERCENTAGE, MAX_WIDTH, MIN_HEIGHT, MIN_MINES, MIN_WIDTH, SCROLL_FACTOR, TILE_SIZE, MouseButton
from pygame import Surface
from scene import Scene
from assets import Assets
from sfx import Sfx
from font import Font54, Font36, Font22, Font16, draw_text_centered

class Menu(Scene):
    def __init__(self) -> None:
        self.game_width = 10
        self.game_height = 10
        self.game_mines = 12
        pass

    def start(self, change_scene, resize_screen) -> None:
        screen_surface = pg.display.get_surface()
        if screen_surface.get_width() != 640 and screen_surface.get_height() != 640:
            resize_screen((640, 640))
        self.change_scene = change_scene
        self.entities = []
        
        # history scroll stuff
        
        self.history_scroll = 0
        self.hist = History.get_instance().get_history()

        self.history_display = Entity(
            Surface((560, 360)),
            (40, 100),
            update_handler=lambda: self.update_history_display()
        )
        self.entities.append(self.history_display)

        # menu buttons and settings displays 
        
        start_button = Entity(
            Surface((180, 60)),
            (230, 560),
            click_handler=lambda _btn, _pos: self.start_game()
        )
        start_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(start_button.surface, Font36, (255, 255, 255), "Start")
        self.entities.append(start_button)

        exit_button = Entity(
            Surface((80, 40)),
            (40, 580),
            click_handler=lambda _btn, _pos: self.exit_game()
        )
        exit_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(exit_button.surface, Font22, (255, 255, 255), "Exit")
        self.entities.append(exit_button)

        decrease_width_button = Entity(
            Surface((40, 40)),
            (40, 500),
            click_handler=lambda _btn, _pos: self.decrease_width()
        )
        decrease_width_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(decrease_width_button.surface, Font22, (255, 255, 255), "-")
        self.entities.append(decrease_width_button)

        self.width_display = Entity(
            Surface((80, 40)),
            (80, 500),
            update_handler=lambda: self.update_width_display()
        )
        self.entities.append(self.width_display)

        increase_width_button = Entity(
            Surface((40, 40)),
            (160, 500),
            click_handler=lambda _btn, _pos: self.increase_width()
        )
        increase_width_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(increase_width_button.surface, Font22, (255, 255, 255), "+")
        self.entities.append(increase_width_button)

        decrease_height_button = Entity(
            Surface((40, 40)),
            (240, 500),
            click_handler=lambda _btn, _pos: self.decrease_height()
        )
        decrease_height_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(decrease_height_button.surface, Font22, (255, 255, 255), "-")
        self.entities.append(decrease_height_button)

        self.height_display = Entity(
            Surface((80, 40)),
            (280, 500),
            update_handler=lambda: self.update_height_display()
        )
        self.entities.append(self.height_display)

        increase_height_button = Entity(
            Surface((40, 40)),
            (360, 500),
            click_handler=lambda _btn, _pos: self.increase_height()
        )
        increase_height_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(increase_height_button.surface, Font22, (255, 255, 255), "+")
        self.entities.append(increase_height_button)

        decrease_mines_button = Entity(
            Surface((40, 40)),
            (440, 500),
            click_handler=lambda _btn, _pos: self.decrease_mines()
        )
        decrease_mines_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(decrease_mines_button.surface, Font22, (255, 255, 255), "-")
        self.entities.append(decrease_mines_button)

        self.mines_display = Entity(
            Surface((80, 40)),
            (480, 500),
            update_handler=lambda: self.update_mines_display()
        )
        self.entities.append(self.mines_display)

        increase_mines_button = Entity(
            Surface((40, 40)),
            (560, 500),
            click_handler=lambda _btn, _pos: self.increase_mines()
        )
        increase_mines_button.surface.fill((0x4b, 0x55, 0x63))
        draw_text_centered(increase_mines_button.surface, Font22, (255, 255, 255), "+")
        self.entities.append(increase_mines_button)

    def handle_click(self, btn, pos) -> None:
        # forward click to clicked button
        for entity in self.entities:
            if entity.rect.collidepoint(pos):
                if btn == MouseButton.MOUSE_LEFT:
                    entity.handle_click(btn, pos)
        
        # handle scroll
        if self.history_display.rect.collidepoint(pos):
            if btn == MouseButton.MOUSE_SCROLL_UP:
                self.history_scroll = max(0, self.history_scroll - SCROLL_FACTOR)
            elif btn == MouseButton.MOUSE_SCROLL_DOWN:
                max_height = len(self.hist) * HISTORY_ITEM_HEIGHT - self.history_display.rect.height + 5
                self.history_scroll = min(max_height, self.history_scroll + SCROLL_FACTOR)

    # button actions

    def start_game(self) -> None:
        # prevent circular import
        from game import Game
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
        draw_text_centered(self.width_display.surface, Font22, (255, 255, 255), str(self.game_width))

    def update_height_display(self) -> None:
        self.height_display.surface.fill((0x6b, 0x72, 0x80))
        draw_text_centered(self.height_display.surface, Font22, (255, 255, 255), str(self.game_height))

    def update_mines_display(self) -> None:
        self.mines_display.surface.fill((0x6b, 0x72, 0x80))
        draw_text_centered(self.mines_display.surface, Font22, (255, 255, 255), str(self.game_mines))

    # history

    def update_history_display(self) -> None:
        self.history_display.surface.fill((0x4b, 0x55, 0x63))
        if len(self.hist) == 0:
            draw_text_centered(
                self.history_display.surface,
                Font16,
                (255, 255, 255),
                "No history yet.\nPlay your first game to see it here.\nPlay enough games and you'll get the joy of scrolling this container!\n:D"   
            )
        for i, entry in enumerate(reversed(self.hist)):
            entry_str = f"{entry.date.strftime("%d.%m.%Y %H:%M")} | {'Win' if entry.win else 'Loss'} | {entry.duration}s ({entry.moves} moves) | {entry.width}x{entry.height} | {f"" if entry.win else f"{entry.mines - entry.remaining_mines}/"}{entry.mines} mines"
            self.history_display.surface.blit(
                Font16.render(
                    entry_str,
                    True,
                    (0x16,0xa3,0x4a) if entry.win else (0xef,0x44,0x44)
                ),
                (5, 5 + i * HISTORY_ITEM_HEIGHT - self.history_scroll)
            )

    def draw(self, screen) -> None:
        # background

        for r in range(20):
            for c in range(20):
                screen.blit(Assets["unknown"], (c * TILE_SIZE, r * TILE_SIZE))

        # on screen texts

        screen.blit(
            Font54.render(
                "Minesweeper",
                True,
                (255, 255, 255)
            ),
            (int(screen.get_width() / 2 - Font54.size("Minesweeper")[0] / 2),0)
        )

        screen.blit(
            Font22.render(
                "Width",
                True,
                (255, 255, 255)
            ),
            (85,470)
        )

        screen.blit(
            Font22.render(
                "Height",
                True,
                (255, 255, 255)
            ),
            (285,470)
        )

        screen.blit(
            Font22.render(
                "Mines",
                True,
                (255, 255, 255)
            ),
            (485,470)
        )
        
        # buttons and displays

        for ent in self.entities:
            ent.update()
            ent.draw(screen)

