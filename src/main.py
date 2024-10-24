import pygame as pg
from typing import Optional, Tuple, Union
from constants import GAME_SCALE_FACTOR, MouseButton

# init pygame before importing scenes so that assets can be loaded
pg.init()
game_surface = pg.Surface((320, 320))
screen = pg.display.set_mode((640, 640))
pg.display.set_caption("Minesweeper")

from scene import Scene
from menu import Menu

clock = pg.time.Clock()
running = True

prev_mouse = (False,) * 3
current_scene: Scene = Menu()

def resize_screen(size: Tuple[int, int]) -> None:
    global screen, game_surface
    game_surface = pg.Surface(size)
    screen = pg.display.set_mode((size[0] * GAME_SCALE_FACTOR, size[1] * GAME_SCALE_FACTOR))

def change_scene(scene: Scene) -> None:
    global current_scene
    current_scene = scene
    scene.start(change_scene, resize_screen)

current_scene.start(change_scene, resize_screen)

def translate_mouse_pos(pos: Tuple[int, int]) -> Tuple[int, int]:
    return pos[0] // GAME_SCALE_FACTOR, pos[1] // GAME_SCALE_FACTOR

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if not running:
        break

    mouse = pg.mouse.get_pressed()
    if mouse[0] and not prev_mouse[0]:
        current_scene.handle_click(MouseButton.MOUSE_LEFT, translate_mouse_pos(pg.mouse.get_pos()))
    if mouse[2] and not prev_mouse[2]:
        current_scene.handle_click(MouseButton.MOUSE_RIGHT, translate_mouse_pos(pg.mouse.get_pos()))
    prev_mouse = mouse

    game_surface.fill((0, 0, 0))
    current_scene.draw(game_surface)

    scaled_surface = pg.transform.scale(game_surface, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_surface, (0, 0))

    pg.display.flip()
    clock.tick(60)

pg.quit()
