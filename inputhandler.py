import libtcodpy as libtcod
import vector2d as v2d

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3
NORTHWEST = 4
NORTHEAST = 5
SOUTHWEST = 6
SOUTHEAST = 7
ENTER = 104
REST = 105
HEAL = 106
HURT = 107
TELEPORT = 108
SPAWN = 109
INVISIBILITY = 110
ESCAPE = 111
PICKUP = 112
INVENTORY = 113
EXAMINE = 114
SHIFT = 115

#Dungeon creator
RESET = 116
DRUNKWALK = 117
CELLULAR = 118
EXPLOSION = 119

#Aliases:
UP = NORTH
DOWN = SOUTH
LEFT = WEST
RIGHT = EAST

KEY_SHIFT = libtcod.KEY_SHIFT

# TODO move to settings.
move_controls = {
    NORTH: v2d.Vector2D(0, -1),
    SOUTH: v2d.Vector2D(0, 1),
    WEST: v2d.Vector2D(-1, 0),
    EAST: v2d.Vector2D(1, 0),
    NORTHWEST: v2d.Vector2D(-1, -1),
    NORTHEAST: v2d.Vector2D(1, -1),
    SOUTHWEST: v2d.Vector2D(-1, 1),
    SOUTHEAST: v2d.Vector2D(1, 1)
}

controls = {
    't': NORTH,  # up
    libtcod.KEY_UP: NORTH,  # up
    libtcod.KEY_KP8: NORTH,  # up

    'h': SOUTH,   # down
    libtcod.KEY_DOWN: SOUTH,  # up
    libtcod.KEY_KP2: SOUTH,  # up

    'd': WEST,  # left
    libtcod.KEY_LEFT: WEST,  # left
    libtcod.KEY_KP4: WEST,  # up

    'n': EAST,   # right
    libtcod.KEY_RIGHT: EAST,  # right
    libtcod.KEY_KP6: EAST,  # up

    'g': NORTHWEST,   # up, left
    libtcod.KEY_KP7: NORTHWEST,  # up, left

    'c': NORTHEAST,   # up, right
    libtcod.KEY_KP9: NORTHEAST,  # up, right

    'm': SOUTHWEST,   # down, left
    libtcod.KEY_KP1: SOUTHWEST,  # down, left

    'w': SOUTHEAST,   # down, right
    libtcod.KEY_KP3: SOUTHEAST,  # down, right

    libtcod.KEY_ENTER: ENTER,
    libtcod.KEY_ESCAPE: ESCAPE,
    libtcod.KEY_SHIFT: SHIFT,  # shift

    "r": REST,
    "p": PICKUP,
    "i": INVENTORY,
    "x": EXAMINE,
    libtcod.KEY_0: RESET,
    libtcod.KEY_1: HEAL,
    libtcod.KEY_1: DRUNKWALK,
    libtcod.KEY_2: HURT,
    libtcod.KEY_2: CELLULAR,
    libtcod.KEY_3: TELEPORT,
    libtcod.KEY_3: EXPLOSION,
    libtcod.KEY_4: SPAWN,
    libtcod.KEY_5: INVISIBILITY,
}


def wait_for_keypress():
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS,
                               key, mouse, False)
    key_char = get_key_char(key)
    return key_char


def get_keypress():
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS,
                                key, mouse)
    key_char = get_key_char(key)
    if key_char in controls.keys():
        return controls[key_char]
    return None


def get_key_char(key):
    if key.vk == libtcod.KEY_CHAR:
        return chr(key.c).lower()  # Case insensetive
    else:
        return key.vk


def is_special_key_pressed(special_key):
    if special_key in controls.keys():
        return libtcod.console_is_key_pressed(special_key)
    return False
