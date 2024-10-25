import os
import pygame as pg

Assets = {}

# load assets on import
for file in os.listdir("assets"):
    if file.endswith(".png"):
        name = file[:-4]
        Assets[name] = pg.image.load("assets/" + file).convert()
