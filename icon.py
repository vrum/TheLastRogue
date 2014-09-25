from argparse import _ActionsContainer

ROW_LENGTH = 16
WALL_PART = 16 * ROW_LENGTH
FEATURE_PART = WALL_PART + 8 * ROW_LENGTH

TEST_WALLS_ROW = WALL_PART
DUNGEON_WALLS_ROW = WALL_PART + ROW_LENGTH * 1
CAVE_WALLS_ROW = WALL_PART + ROW_LENGTH * 2
EGYPT_WALLS_ROW = WALL_PART + ROW_LENGTH * 3
BRICK_WALLS_ROW = WALL_PART + ROW_LENGTH * 4
CAVE_WALLS_ROW2 = WALL_PART + ROW_LENGTH * 5
CAVE_WALLS_ROW3 = WALL_PART + ROW_LENGTH * 6

DUNGEON_FEATURE_ROW = FEATURE_PART
EQUIPMENT_ITEMS_ROW = FEATURE_PART + ROW_LENGTH * 1
USABLE_ITEMS_ROW = FEATURE_PART + ROW_LENGTH * 2
DUNGEON_ENTITIES_ROW = FEATURE_PART + ROW_LENGTH * 3
TOMB_ENTITIES_ROW = FEATURE_PART + ROW_LENGTH * 4
BLOOD_ROW = FEATURE_PART + ROW_LENGTH * 5
ICON_ROW = FEATURE_PART + ROW_LENGTH * 6
GUI_ROW = FEATURE_PART + ROW_LENGTH * 7

CENTER_DOT = 15 * ROW_LENGTH + 10
BIG_CENTER_DOT = 15 * ROW_LENGTH + 9

################
#Dungeon Features
################

STAIRS_UP = DUNGEON_FEATURE_ROW
STAIRS_DOWN = DUNGEON_FEATURE_ROW + 1
PILLAR = DUNGEON_FEATURE_ROW + 2
DOOR = DUNGEON_FEATURE_ROW + 3
DOOR_LOCKED = DUNGEON_FEATURE_ROW + 4
DOOR_OPEN = DUNGEON_FEATURE_ROW + 5
FOUNTAIN_FULL = DUNGEON_FEATURE_ROW + 6
FOUNTAIN_EMPTY = DUNGEON_FEATURE_ROW + 7
CORPSE = DUNGEON_FEATURE_ROW + 8
WATER = DUNGEON_FEATURE_ROW + 9
WATER_RIPPLES = DUNGEON_FEATURE_ROW + 10
LAVA = DUNGEON_FEATURE_ROW + 11
FENCES = DUNGEON_FEATURE_ROW + 12
GLASS_WALL = DUNGEON_FEATURE_ROW + 13
CHASM = DUNGEON_FEATURE_ROW + 14
CHASM2 = DUNGEON_FEATURE_ROW + 15

################
#Equipment Items
################

SWORD = EQUIPMENT_ITEMS_ROW
GUN = EQUIPMENT_ITEMS_ROW + 1
HELM = EQUIPMENT_ITEMS_ROW + 2
ARMOR = EQUIPMENT_ITEMS_ROW + 3
BOOTS = EQUIPMENT_ITEMS_ROW + 4
AMULET = EQUIPMENT_ITEMS_ROW + 5
RING = EQUIPMENT_ITEMS_ROW + 6
SLING = EQUIPMENT_ITEMS_ROW + 7
STONE = EQUIPMENT_ITEMS_ROW + 8
CLOAK = EQUIPMENT_ITEMS_ROW + 9
KNIFE = EQUIPMENT_ITEMS_ROW + 10
SPEAR = EQUIPMENT_ITEMS_ROW + 11
MACE = EQUIPMENT_ITEMS_ROW + 12
AMMO1 = EQUIPMENT_ITEMS_ROW + 13
AMMO2 = EQUIPMENT_ITEMS_ROW + 14

################
#Usable Items
################

POTION = USABLE_ITEMS_ROW
SCROLL = USABLE_ITEMS_ROW + 1
MACHINE = USABLE_ITEMS_ROW + 2
ORB = USABLE_ITEMS_ROW + 3
BOMB = USABLE_ITEMS_ROW + 4
SKULL = USABLE_ITEMS_ROW + 14

##################
#Dungeon Entities
##################

GUNSLINGER = DUNGEON_ENTITIES_ROW
RATMAN = DUNGEON_ENTITIES_ROW + 1
SLIME = DUNGEON_ENTITIES_ROW + 2
GHOST = DUNGEON_ENTITIES_ROW + 3
GOLEM = DUNGEON_ENTITIES_ROW + 4
MAGICIAN = DUNGEON_ENTITIES_ROW + 5
AVATAR = DUNGEON_ENTITIES_ROW + 6
SKELETON_MAGE = DUNGEON_ENTITIES_ROW + 7
SKELETON_WARRIOR = DUNGEON_ENTITIES_ROW + 8
SAND_WORM = DUNGEON_ENTITIES_ROW + 9
SAND_WORM_SUBMERGED = DUNGEON_ENTITIES_ROW + 10
GUNSLINGER_THIN = DUNGEON_ENTITIES_ROW + 11
WITCH = DUNGEON_ENTITIES_ROW + 12
CYCLOPS = DUNGEON_ENTITIES_ROW + 13
CYCLOPS_HOLD_ROCK = DUNGEON_ENTITIES_ROW + 14
BANDIT = DUNGEON_ENTITIES_ROW + 15

##################
#Tomb Entities
##################

MUMMY = TOMB_ENTITIES_ROW
HORUS = TOMB_ENTITIES_ROW + 1
ANUBIS_SWORD = TOMB_ENTITIES_ROW + 2
ANUBIS_CLUB = TOMB_ENTITIES_ROW + 3
ANUBIS_STAFF = TOMB_ENTITIES_ROW + 4
SARCOPHAGUS = TOMB_ENTITIES_ROW + 5
SALAMANDER = TOMB_ENTITIES_ROW + 6
STAR_SPAWN = TOMB_ENTITIES_ROW + 7
STATUE = TOMB_ENTITIES_ROW + 8
PIXIE = TOMB_ENTITIES_ROW + 9
SPIDER = TOMB_ENTITIES_ROW + 10
FIRE = TOMB_ENTITIES_ROW + 11
DEMON = TOMB_ENTITIES_ROW + 13
GHOST2 = TOMB_ENTITIES_ROW + 14
BEETLE = TOMB_ENTITIES_ROW + 15

##################
#Icon
##################

SANITY_STAT = ICON_ROW
HEALTH_STAT = ICON_ROW + 1
ARMOR_STAT = ICON_ROW + 2
AMMO_ICON = ICON_ROW + 3
HEALTH_GAIN_ICON = ICON_ROW + 4
INVENTORY_ICON = ICON_ROW + 5

HEART = 3

##################
#Blood
##################

BLOOD1 = BLOOD_ROW
BLOOD2 = BLOOD_ROW + 1
BLOOD3 = BLOOD_ROW + 2
BLOOD4 = BLOOD_ROW + 3
BLOOD5 = BLOOD_ROW + 4
BLOOD6 = BLOOD_ROW + 5
BLOOD7 = BLOOD_ROW + 6

BLOOD_ICONS = [BLOOD1, BLOOD2, BLOOD3, BLOOD4, BLOOD5, BLOOD6, BLOOD7]

##################
#GUI
##################

FOOT_STEPS = GUI_ROW + 2

#Single Line
H_LINE = 196
V_LINE = 179
NE_LINE = 191
NW_LINE = 218
SE_LINE = 217
SW_LINE = 192
