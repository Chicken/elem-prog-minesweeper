from enum import Enum

TILE_SIZE = 16
GAME_SCALE_FACTOR = 2
TOP_OFFSET = 0

MIN_WIDTH = 8
MIN_HEIGHT = 8

MAX_WIDTH = 30
MAX_HEIGHT = 30

MIN_MINES = 8
MAX_MINES_PERCENTAGE = 0.4

class MouseButton(Enum):
    MOUSE_LEFT = 1
    MOUSE_RIGHT = 2

class TileState(Enum):
    UNKNOWN = 1
    FLAGGED = 2
    VISIBLE = 3
