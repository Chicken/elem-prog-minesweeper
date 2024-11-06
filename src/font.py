from typing import Tuple
import pygame as pg

Font54 = pg.font.Font("./assets/Poppins-Regular.ttf", 54)
Font36 = pg.font.Font("./assets/Poppins-Regular.ttf", 36)
Font22 = pg.font.Font("./assets/Poppins-Regular.ttf", 22)
Font16 = pg.font.Font("./assets/Poppins-Regular.ttf", 16)

def draw_text_centered(surface: pg.Surface, font: pg.font.Font, color: Tuple[int, int, int], text: str) -> None:
    """
    Writes a text centered on a surface with a given font and color
    """
    parts = text.split("\n")
    sizes = [font.size(part) for part in parts]
    total_height = sum(size[1] for size in sizes)
    curr_height = 0
    for i, part in enumerate(parts):
        surface.blit(
            font.render(part, True, color),
            (
                int(surface.get_width() / 2 - sizes[i][0] / 2),
                int(surface.get_height() / 2 - total_height / 2 + curr_height)
            )
        )
        curr_height += sizes[i][1]
