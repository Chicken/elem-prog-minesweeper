from typing import Callable, Tuple
from constants import TILE_SIZE, TOP_OFFSET, TileState, MouseButton
from gamelogic import populate_field, reveal
from pygame import Surface
from scene import Scene
from assets import Assets

def translate_tile_to_world(pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    r,c -> x,y+offset
    """
    return pos[1] * TILE_SIZE, pos[0] * TILE_SIZE + TOP_OFFSET

class Game(Scene):
    def __init__(self, width: int, height: int, bombs: int) -> None:
        self.width = width
        self.height = height
        self.bombs = bombs
        self.generated = False
        self.field = [["0" for _ in range(width)] for _ in range(height)]
        self.tile_states = [[TileState.UNKNOWN for _ in range(width)] for _ in range(height)]

    def start(self, change_scene: Callable[['Scene'], None], resize_screen: Callable[[Tuple[int, int]], None]) -> None:
        resize_screen((self.width * TILE_SIZE, self.height * TILE_SIZE))
        self.change_scene = change_scene

    def handle_click(self, btn: MouseButton, pos: Tuple[int, int]) -> None:
        if pos[1] < TOP_OFFSET:
            # TODO: handle top bar clicks
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
                    populate_field(self.field, self.bombs, (r, c))
                    self.generated = True
                
                # reveal single tiles
                if self.field[r][c] != "0":
                    self.tile_states[r][c] = TileState.VISIBLE
                    if self.field[r][c] == "bomb":
                        print("Lose!")
                        # TODO: end game
                # floodfill zeros
                else:
                    reveal(self.field, self.tile_states, (r, c))

                # check for win
                unrevealed = sum([sum([tile == TileState.UNKNOWN or tile == TileState.FLAGGED for tile in row]) for row in self.tile_states])
                if unrevealed == self.bombs:
                    print("Win!")
                    # TODO: end game
            # click on a number tile to reveal surrounding tiles
            elif self.tile_states[r][c] == TileState.VISIBLE and self.field[r][c] != "0" and self.field[r][c] != "bomb":
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

    def draw(self, screen: Surface) -> None:
        # TODO: restart button
        # TODO: return to menu button
        # TODO: bomb counter
        # TODO: timer

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
