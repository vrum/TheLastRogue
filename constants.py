import settings

FPS = 60

STATUS_BAR_WIDTH = 15

MONSTER_STATUS_BAR_WIDTH = 15
GAME_STATE_WIDTH = settings.WINDOW_WIDTH - (STATUS_BAR_WIDTH +
                                            MONSTER_STATUS_BAR_WIDTH)

MESSAGES_BAR_WIDTH = STATUS_BAR_WIDTH + GAME_STATE_WIDTH
MESSAGES_BAR_HEIGHT = 10

GAME_STATE_HEIGHT = settings.WINDOW_HEIGHT - MESSAGES_BAR_HEIGHT

STATUS_BAR_HEIGHT = GAME_STATE_HEIGHT
MONSTER_STATUS_BAR_HEIGHT = settings.WINDOW_HEIGHT + MESSAGES_BAR_HEIGHT

ITEMS_ALLOWED_PER_TILE = 1
ENTITIES_ALLOWED_PER_TILE = 1

DIRECTIONS = {
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
    "NW": (-1, 1),
    "NE": (1, 1),
    "SW": (-1, -1),
    "SE": (1, -1)
}

DIRECTIONS_LIST = DIRECTIONS.values()
