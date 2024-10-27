import os
import pygame as pg

Sfx = {}

# load assets on import
for file in os.listdir("assets"):
    if file.endswith(".wav"):
        name = file[:-4]
        Sfx[name] = pg.mixer.Sound("assets/" + file)
