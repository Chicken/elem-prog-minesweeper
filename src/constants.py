from enum import Enum

# size constants
GAME_SCALE_FACTOR = 2
TILE_SIZE = 16 * GAME_SCALE_FACTOR
TOP_OFFSET = 60
END_MENU_WIDTH = 200

# history constants
HISTORY_ITEM_HEIGHT = 25
SCROLL_FACTOR = 20

# settings constants
MIN_WIDTH = 8
MIN_HEIGHT = 8
MAX_WIDTH = 30
MAX_HEIGHT = 30
MIN_MINES = 8
MAX_MINES_PERCENTAGE = 0.4

# handler constants
class MouseButton(Enum):
    MOUSE_LEFT = 1
    MOUSE_RIGHT = 2
    MOUSE_SCROLL_DOWN = 3
    MOUSE_SCROLL_UP = 4

# gamestate constants
MINE = "mine"
class TileState(Enum):
    UNKNOWN = 1
    FLAGGED = 2
    VISIBLE = 3

# color constants
GREY = (0x6b, 0x72, 0x80)
LIGHT_GREY = (0x4b, 0x55, 0x63)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
