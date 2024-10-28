from typing import Tuple
from typing import List
from assets import Assets
from constants import END_MENU_WIDTH, MINE, TILE_SIZE, MouseButton, TileState
from entity import Entity
from font import draw_text_centered
from pygame import Surface
from scene import Scene
from font import Font22, Font36

def translate_tile_to_world(pos: Tuple[int, int]) -> Tuple[int, int]:
    return pos[1] * TILE_SIZE, pos[0] * TILE_SIZE

class End(Scene):
    def __init__(self, win: bool, time: int, moves: int, field: List[List[str]], tile_states: List[List[TileState]]) -> None:
        self.win = win
        self.time = time
        self.moves = moves
        self.field = field
        self.height = len(field)
        self.width = len(field[0])
        self.tile_states = tile_states

    def start(self, change_scene, resize_screen) -> None:
        resize_screen((self.width * TILE_SIZE + END_MENU_WIDTH, self.height * TILE_SIZE))
        self.change_scene = change_scene
        self.entities = []
        self.offset_x = self.width * TILE_SIZE
        self.screen_height = self.height * TILE_SIZE

        menu_button = Entity(
            Surface((150, 40)),
            (int(self.offset_x + END_MENU_WIDTH / 2 - 150 / 2), self.screen_height - 50),
            click_handler=lambda _btn, _pos: self.back_to_menu()
        )
        menu_button.surface.fill((0x6b, 0x72, 0x80))
        draw_text_centered(menu_button.surface, Font22, (255, 255, 255), "Menu")
        self.entities.append(menu_button)

        restart_button = Entity(
            Surface((150, 40)),
            (int(self.offset_x + END_MENU_WIDTH / 2 - 150 / 2), self.screen_height - 100),
            click_handler=lambda _btn, _pos: self.restart()
        )
        restart_button.surface.fill((0x6b, 0x72, 0x80))
        draw_text_centered(restart_button.surface, Font22, (255, 255, 255), "Restart")
        self.entities.append(restart_button)

    def handle_click(self, btn, pos) -> None:
        # forward click to clicked button
        for entity in self.entities:
            if entity.rect.collidepoint(pos):
                if btn == MouseButton.MOUSE_LEFT:
                    entity.handle_click(btn, pos)

    def back_to_menu(self) -> None:
        # prevent circular import
        from menu import Menu
        self.change_scene(Menu())

    def restart(self) -> None:
        # prevent circular import
        from game import Game
        mines = sum([row.count(MINE) for row in self.field])
        self.change_scene(Game(self.width, self.height, mines))

    def draw(self, screen) -> None:
        # draw field
        for r in range(self.height):
            for c in range(self.width):
                state = self.tile_states[r][c]
                if state == TileState.UNKNOWN:
                    if self.field[r][c] == MINE:
                        if self.win:
                            # flag unflagged mines if won
                            screen.blit(Assets["flag"], translate_tile_to_world((r, c)))
                        else:
                            # reveal unfound mines if lost
                            screen.blit(Assets["mine"], translate_tile_to_world((r, c)))
                    else:
                        screen.blit(Assets["unknown"], translate_tile_to_world((r, c)))
                elif state == TileState.FLAGGED:
                    screen.blit(Assets["flag"], translate_tile_to_world((r, c)))
                elif state == TileState.VISIBLE:
                    screen.blit(Assets[self.field[r][c]], translate_tile_to_world((r, c)))

        # side bar
        screen.fill((0x4b, 0x55, 0x63), (self.width * TILE_SIZE, 0, END_MENU_WIDTH, self.height * TILE_SIZE))

        # all the text

        title = "You win!" if self.win else "You lost..."
        screen.blit(
            Font36.render(
                title,
                True,
                (255, 255, 255)
            ),
            (self.offset_x + 10, 0)
        )

        screen.blit(
            Font22.render(
                f"{self.time} seconds",
                True,
                (255, 255, 255)
            ),
            (self.offset_x + 10, 50)
        )

        screen.blit(
            Font22.render(
                f"{self.moves} moves",
                True,
                (255, 255, 255)
            ),
            (self.offset_x + 10, 80)
        )

        if not self.win:
            remaining_mines = sum([row.count(MINE) for row in self.field]) - sum([row.count(TileState.FLAGGED) for row in self.tile_states])
            screen.blit(
                Font22.render(
                    f"{remaining_mines} mine{"s" if remaining_mines > 1 else ""} left",
                    True,
                    (255, 255, 255)
                ),
                (self.offset_x + 10, 110)
            )

        for ent in self.entities:
            ent.update()
            ent.draw(screen)
