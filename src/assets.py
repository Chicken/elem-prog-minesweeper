import os
import pygame as pg
from constants import GAME_SCALE_FACTOR

Assets = {}

# load assets on import
for file in os.listdir("assets"):
    if file.endswith(".png"):
        name = file[:-4]
        asset = pg.image.load("assets/" + file).convert()
        Assets[name] = pg.transform.scale(asset, (asset.get_width() * GAME_SCALE_FACTOR, asset.get_height() * GAME_SCALE_FACTOR))
