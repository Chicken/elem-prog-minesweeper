from time import time
from typing import Tuple
from constants import MINE, TILE_SIZE, TOP_OFFSET, TileState, MouseButton
from entity import Entity
from gamelogic import populate_field, reveal
from history import History, HistoryEntry
from pygame import Surface
from scene import Scene
from assets import Assets
from sfx import Sfx
from font import Font22, draw_text_centered

def translate_tile_to_world(pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    r,c -> x,y+offset
    """
    return pos[1] * TILE_SIZE, pos[0] * TILE_SIZE + TOP_OFFSET

class Game(Scene):
    def __init__(self, width: int, height: int, mines: int) -> None:
        self.width = width
        self.height = height
        self.mines = mines
        self.generated = False
        self.field = [["0" for _ in range(width)] for _ in range(height)]
        self.tile_states = [[TileState.UNKNOWN for _ in range(width)] for _ in range(height)]
        self.start_time = 0
        self.moves = 0

    def start(self, change_scene, resize_screen) -> None:
        resize_screen((self.width * TILE_SIZE, TOP_OFFSET + self.height * TILE_SIZE))
        self.change_scene = change_scene
        self.entities = []

        # top bar entities

        restart_button = Entity(
            Surface((60, 60)),
            (int(self.width * TILE_SIZE / 2 - 30), 0),
            click_handler=lambda _btn, _pos: self.restart_game()
        )
        restart_button.surface.fill((0x6b, 0x72, 0x80))
        draw_text_centered(restart_button.surface, Font22, (255, 255, 255), ":D")
        self.entities.append(restart_button)

        self.mines_display = Entity(
            Surface((90, 60)),
            (0, 0),
            update_handler=lambda: self.update_mines_display()
        )
        self.entities.append(self.mines_display)

        self.timer_display = Entity(
            Surface((90, 60)),
            (int(self.width * TILE_SIZE - 90), 0),
            update_handler=lambda: self.update_timer_display()
        )
        self.entities.append(self.timer_display)

    def handle_click(self, btn, pos) -> None:
        if pos[1] < TOP_OFFSET:
            for entity in self.entities:
                if entity.rect.collidepoint(pos):
                    if btn == MouseButton.MOUSE_LEFT:
                        entity.handle_click(btn, pos)
            return
        
        # x,y+offset -> r,c
        c, r = pos[0] // TILE_SIZE, (pos[1] - TOP_OFFSET) // TILE_SIZE
        # sanity check
        if r < 0 or r >= self.height or c < 0 or c >= self.width:
            return

        if btn == MouseButton.MOUSE_LEFT:
            # reveal tile clicks
            if self.tile_states[r][c] == TileState.UNKNOWN:
                # generate field on first click
                if not self.generated:
                    populate_field(self.field, self.mines, (r, c))
                    self.generated = True
                    self.start_time = time()
                
                self.moves += 1

                # reveal single tiles
                if self.field[r][c] != "0":
                    self.tile_states[r][c] = TileState.VISIBLE
                    if self.field[r][c] == MINE:
                        # end game as a loss
                        Sfx["explosion"].play()
                        duration = int(time() - self.start_time)
                        remaining_mines = self.mines - sum([row.count(TileState.FLAGGED) for row in self.tile_states])
                        hist = History.get_instance()
                        entry = HistoryEntry(
                            int(self.start_time),
                            duration,
                            self.moves,
                            False,
                            self.width,
                            self.height,
                            self.mines,
                            remaining_mines
                        )
                        hist.add_entry(entry)
                        # prevent circular import
                        from end import End
                        self.change_scene(End(False, duration, self.moves, self.field, self.tile_states))
                        return
                # floodfill zeros
                else:
                    reveal(self.field, self.tile_states, (r, c))

                # check for win
                unrevealed = sum([sum([tile == TileState.UNKNOWN or tile == TileState.FLAGGED for tile in row]) for row in self.tile_states])
                if unrevealed == self.mines:
                    # end game a a win
                    duration = int(time() - self.start_time)
                    hist = History.get_instance()
                    entry = HistoryEntry(
                        int(self.start_time),
                        duration,
                        self.moves,
                        True,
                        self.width,
                        self.height,
                        self.mines,
                        0
                    )
                    hist.add_entry(entry)
                    # prevent circular import
                    from end import End
                    self.change_scene(End(True, duration, self.moves, self.field, self.tile_states))
            # click on a number tile to reveal surrounding tiles
            elif self.tile_states[r][c] == TileState.VISIBLE and self.field[r][c] != "0" and self.field[r][c] != MINE:
                # count surround flags
                surrounding_flags = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (dr, dc) == (0, 0):
                            continue
                        nr, nc = r + dr, c + dc
                        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
                            continue
                        if self.tile_states[nr][nc] == TileState.FLAGGED:
                            surrounding_flags += 1
                # reveal surrounding tiles if flag count matches number on tile
                if surrounding_flags == int(self.field[r][c]):
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if (dr, dc) == (0, 0):
                                continue
                            nr, nc = r + dr, c + dc
                            if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
                                continue
                            if self.tile_states[nr][nc] == TileState.UNKNOWN:
                                # emulate a click (handles floodfill and lose/win condition)
                                self.handle_click(MouseButton.MOUSE_LEFT, translate_tile_to_world((nr, nc)))
        # toggle flag on an unrevealed tile
        elif btn == MouseButton.MOUSE_RIGHT:
            if self.tile_states[r][c] == TileState.UNKNOWN:
                self.tile_states[r][c] = TileState.FLAGGED
            elif self.tile_states[r][c] == TileState.FLAGGED:
                self.tile_states[r][c] = TileState.UNKNOWN

    # top bar buttons and display updaters

    def restart_game(self) -> None:
        self.generated = False
        self.field = [["0" for _ in range(self.width)] for _ in range(self.height)]
        self.tile_states = [[TileState.UNKNOWN for _ in range(self.width)] for _ in range(self.height)]
        self.start_time = 0
        self.moves = 0

    def update_mines_display(self):
        self.mines_display.surface.fill((0x6b, 0x72, 0x80))
        remaining_mines = self.mines - sum([row.count(TileState.FLAGGED) for row in self.tile_states])
        draw_text_centered(self.mines_display.surface, Font22, (255, 255, 255), str(remaining_mines))

    def update_timer_display(self):
        self.timer_display.surface.fill((0x6b, 0x72, 0x80))
        timer = min(999, int(time() - self.start_time)) if self.generated else 0
        draw_text_centered(self.timer_display.surface, Font22, (255, 255, 255), str(timer))

    def draw(self, screen) -> None:
        # draw field
        for r in range(self.height):
            for c in range(self.width):
                state = self.tile_states[r][c]
                if state == TileState.UNKNOWN:
                    screen.blit(Assets["unknown"], translate_tile_to_world((r, c)))
                elif state == TileState.FLAGGED:
                    screen.blit(Assets["flag"], translate_tile_to_world((r, c)))
                elif state == TileState.VISIBLE:
                    screen.blit(Assets[self.field[r][c]], translate_tile_to_world((r, c)))

        # top bar
        screen.fill((0x4b, 0x55, 0x63), (0,0, self.width * TILE_SIZE, TOP_OFFSET))

        for ent in self.entities:
            ent.update()
            ent.draw(screen)
