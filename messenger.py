EQUIP_MESSAGE = "%(source_entity)s equips %(item)s."
UNEQUIP_MESSAGE = "%(source_entity)s puts away %(item)s."
HEAL_MESSAGE = "%(source_entity)s heals %(target_entity)s for %(health)s health."
HEALTH_POTION_MESSAGE = "The health potion heals %(target_entity)s for %(health)s health."
DISSOLVE_MESSAGE = "%(source_entity)s dissolves %(target_entity)s for %(damage)s damage."
HIT_MESSAGE = "%(source_entity)s hits %(target_entity)s for %(damage)s damage."
MISS_MESSAGE = "%(source_entity)s misses %(target_entity)s."
CRIT_MESSAGE = "%(source_entity)s critically hits %(target_entity)s for %(damage)s damage."

HAUNT_MESSAGE = "%(source_entity)s haunts the %(target_entity)s!"

HEART_STOP_MESSAGE = "%(target_entity)s clutches its heart."
DARKNESS_MESSAGE = "An unnatural darkness fills the dungeon."
PICK_UP_MESSAGE = "You pick up %(item)s."
POISON_MESSAGE = "%(target_entity)s takes %(damage)s in poison damage."
BLEED_MESSAGE = "%(target_entity)s is bleeding out %(damage)s damage."

DOWN_STAIRS_HEAL_MESSAGE = "Your feel vitalized by your progress, you regain %(health)s health."
FALL_DOWN_MESSAGE = "You take a damage of %(damage)s from the fall."
DRINK_FOUNTAIN_MESSAGE = "You drink from the fountain, your max health increases by %(health)s."

HURT_BY_EXPLOSION = "The explosion blasts %(target_entity)s for %(damage)s damage."
HURT_BY_FIRE = "The fire burns %(target_entity)s for %(damage)s damage."

WONT_BREAK_OUT_OF_WEB_MESSAGE = "%(target_entity)s is stuck in the spider web."
BREAKS_OUT_OF_WEB_MESSAGE = "%(target_entity)s breaks free."

WANT_TO_JUMP_DOWN_CHASM = "Are you sure you want to drop down the chasm?"
PRESS_ENTER_TO_ACCEPT = "Press ENTER to accept, another key to reject."

PLAYER_TELEPORT_MESSAGE = "Your surroundings seem different."
PLAYER_SWITCH_MESSAGE = "Your surrounding is replaced."

PLAYER_MAP_MESSAGE = "You surroundings suddenly seem familiar."
PLAYER_PUSH_SCROLL_MESSAGE = "You as you form the words of the scroll your voice turns into a strong wind."

GLASS_TURNING_MESSAGE = "You surroundings suddenly seem more transparent."
SWAP_DEVICE_MESSAGE = "Your surroundings has changed."

ZAP_DEVICE_MESSAGE = "%(source_entity)s zaps %(target_entity)s for %(damage)s damage!"
HEALTH_DEVICE_MESSAGE = "%(target_entity)s is healed by the device for %(health)s health."

STARE_PARALYZE_MESSAGE = "%(source_entity)s stares at %(target_entity)s, it's paralyzed!."
NO_LONGER_PARALYZED_MESSAGE = "%(source_entity)s is no longer paralyzed."

FROST_POTION_DRINK_MESSAGE = "That potion was cold as ice! You feel yourself slow down."
FROST_POTION_BREAKS_MESSAGE = "The potion smashes to the ground and creates a freezing cloud of mist!"
POTION_SMASHES_AGAINST_FLOOR_MESSAGE = "The potion smashes to the ground and breaks into pieces."
FLAME_POTION_DRINK_MESSAGE = "As you drink the potion the liquid ignites!"
FLAME_POTION_BREAKS_MESSAGE = "The potion smashes to the ground and creates a roaring fire!"
POISON_POTION_DRINK_MESSAGE = "The potion tastes really nasty, you feel sick!"
POISON_POTION_BREAK_MESSAGE = "The potion smashes to the ground and creates a poisonous cloud of gas!"

POTION_SMASH_TO_GROUND = "The %(target_entity)s smashes to the ground and breaks into pieces."
ITEM_HITS_THE_GROUND_HEAVY = "The %(target_entity)s hits the ground with a thud."
ITEM_HITS_THE_GROUND_LIGHT = "The %(target_entity)s falls to the ground."
ITEM_FALLS_DOWN_CHASM = "The %(target_entity)s falls into the chasm and disappears."
ENTITY_EXPLODES = "%(target_entity)s explodes!"


class Messenger(object):
    def __init__(self):
        self._messages = []
        self._has_new_message = False
        self.player = None

    @property
    def has_new_message(self):
        return self._has_new_message

    @has_new_message.setter
    def has_new_message(self, value):
        self._has_new_message = value

    def send_visual_message(self, new_message, position):
        if self.player.dungeon_mask.can_see_point(position):
            self._message(new_message)

    def send_global_message(self, new_message):
        self._message(new_message)

    def _message(self, new_message):
        new_message = Message(new_message.capitalize())
        old_message = next((message for message in self._messages
                           if message.message == new_message.message and
                              message.ttl == new_message.ttl), None)
        if old_message:
            old_message.increase()
        else:
            self._messages.append(new_message)
        self.has_new_message = True

    def tail(self, length):
        self.has_new_message = False
        self._messages = [message for message in self._messages if message.ttl > 0]
        map(lambda m: m.tick(), self._messages)
        return self._messages[-length:]

    def clear(self):
        self._messages = []


class Message(object):
    def __init__(self, message):
        self.message = message
        self.count = 1
        self.ttl = 5

    def increase(self):
        self.count += 1

    def tick(self):
        self.ttl -= 1

    def __str__(self):
        if self.count > 1:
            return str(self.message) + " x" + str(self.count)
        return str(self.message)


msg = Messenger()
