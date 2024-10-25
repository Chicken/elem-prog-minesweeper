from enum import Enum

TILE_SIZE = 16
GAME_SCALE_FACTOR = 2
TOP_OFFSET = 0

class MouseButton(Enum):
    MOUSE_LEFT = 1
    MOUSE_RIGHT = 2

class TileState(Enum):
    UNKNOWN = 1
    FLAGGED = 2
    VISIBLE = 3
