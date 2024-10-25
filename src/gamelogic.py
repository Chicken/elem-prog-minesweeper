import random
from threading import Thread
from time import sleep
from typing import List, Tuple

from constants import TileState

def populate_field(target_field: List[List[str]], mine_count: int, safe_position: Tuple[int, int]) -> None:
    h = len(target_field)
    w = len(target_field[0])
    candidates = []

    # list available positions
    for r in range(h):
        for c in range(w):
            # first click is always safe
            if (r, c) == safe_position:
                continue
            candidates.append((r, c))

    bombs = random.sample(candidates, k=mine_count)
    for r, c in bombs:
        target_field[r][c] = "bomb"

    # calculate numbers
    for r in range(h):
        for c in range(w):
            if target_field[r][c] == "bomb":
                continue
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if (dr, dc) == (0, 0):
                        continue
                    nr, nc = r + dr, c + dc
                    if nr < 0 or nr >= h or nc < 0 or nc >= w:
                        continue
                    if target_field[nr][nc] == "bomb":
                        count += 1
            target_field[r][c] = str(count)

def _reveal_internal(target_field: List[List[str]], tile_states: List[List[TileState]], pos: Tuple[int, int]) -> None:
    """
    Internal function, sleeps a thread, should not be called directly
    """
    h = len(target_field)
    w = len(target_field[0])
    q = [pos]
    v = set()
    to_reveal = []
    while len(q) > 0:
        (r,c) = q.pop(0)
        to_reveal.append((r, c))
        if target_field[r][c] != "0":
            continue
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr, dc) == (0, 0):
                    continue
                (nr, nc) = (r + dr, c + dc)
                if nr < 0 or nc < 0 or nr >= h or nc >= w:
                    continue
                if (nr, nc) in v:
                    continue
                v.add((nr, nc))
                q.append((nr, nc))

    total_tiles = len(to_reveal)
    for i, (r, c) in enumerate(to_reveal):
        tile_states[r][c] = TileState.VISIBLE
        # a smooth animation function
        t = (i / total_tiles)
        sleep(4 * t * (1 - t) * 0.002)

def reveal(target_field: List[List[str]], tile_states: List[List[TileState]], pos: Tuple[int, int]) -> None:
    Thread(target=_reveal_internal, args=(target_field, tile_states, pos)).start()
