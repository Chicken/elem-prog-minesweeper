import pygame as pg
from typing import Tuple
from constants import GAME_SCALE_FACTOR, MouseButton

# init pygame before importing scenes so that assets can be loaded
pg.init()
pg.mixer.set_num_channels(16)
screen = pg.display.set_mode((640, 640))
pg.display.set_caption("Minesweeper")

from scene import Scene
from menu import Menu

clock = pg.time.Clock()
running = True

prev_mouse = (False,) * 3
current_scene: Scene = Menu()

# functions given to scenes

def resize_screen(size: Tuple[int, int]) -> None:
    global screen
    screen = pg.display.set_mode(size)

def change_scene(scene: Scene) -> None:
    global current_scene
    current_scene = scene
    scene.start(change_scene, resize_screen)

current_scene.start(change_scene, resize_screen)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                current_scene.handle_click(MouseButton.MOUSE_SCROLL_UP, pg.mouse.get_pos())
            if event.button == 5:
                current_scene.handle_click(MouseButton.MOUSE_SCROLL_DOWN, pg.mouse.get_pos())
    if not running:
        break

    # forward mouse presses to the current scene
    mouse = pg.mouse.get_pressed()
    if mouse[0] and not prev_mouse[0]:
        current_scene.handle_click(MouseButton.MOUSE_LEFT, pg.mouse.get_pos())
    if mouse[2] and not prev_mouse[2]:
        current_scene.handle_click(MouseButton.MOUSE_RIGHT, pg.mouse.get_pos())
    prev_mouse = mouse

    # call scene to draw a fram
    screen.fill((0, 0, 0))
    current_scene.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()
