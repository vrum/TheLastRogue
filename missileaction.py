import random

from action import Action, SOURCE_ENTITY, GAME_STATE
from actor import ParalyzedActor
from animation import animate_flight
from attacker import DamageTypes, UndodgeableAttack
from entityeffect import Heal, AddSpoofChild
import gametime
import geometry
from graphic import GraphicChar
from messenger import STARE_PARALYZE_MESSAGE
from monsteractor import MonsterWeightedAction
from mover import RandomStepper
from rng import coin_flip
import shoot
import colors
import icon
from util import get_path


class PlayerMissileAction(Action):
    def __init__(self, missile_graphic=None):
        super(PlayerMissileAction, self).__init__()
        self._missile_graphic = missile_graphic

    @property
    def missile_graphic(self):
        return self._missile_graphic

    def act(self, **kwargs):
        source_entity = kwargs[SOURCE_ENTITY]
        game_state = kwargs[GAME_STATE]
        max_missile_distance = \
            self.max_missile_distance(source_entity=source_entity)
        path = shoot.player_select_missile_path(source_entity,
                                                max_missile_distance,
                                                game_state)

        if path is None or path[-1] == source_entity.position.value:
            return False
        dungeon_level = source_entity.dungeon_level.value
        hit_detector = shoot.MissileHitDetection(False, False)
        path_taken = hit_detector.get_path_taken(path, dungeon_level)
        if path_taken is None or len(path_taken) < 1:
            return False
        animate_flight(game_state, path_taken, self.missile_graphic.icon, self.missile_graphic.color_fg)
        self.missile_hit_effect(dungeon_level, path_taken[-1], game_state, source_entity)
        self.add_energy_spent_to_entity(source_entity)

    def max_missile_distance(self, **kwargs):
        pass

    def missile_hit_effect(self, dungeon_level, path, game_state, source_entity):
        pass


class PlayerThrowItemAction(PlayerMissileAction):
    """
    This action will prompt the player to throw the parent item.
    """

    @property
    def missile_graphic(self):
        return self.parent.graphic_char

    def __init__(self):
        super(PlayerThrowItemAction, self).__init__()
        self.component_type = "player_throw_item_action"
        self.name = "Throw"
        self.display_order = 95

    # todo: will be handled properly by triggered effect. This whole file needs refactoring, ill deal with it then.
    def add_energy_spent_to_entity(self, entity):
        pass

    def max_missile_distance(self, **kwargs):
        """
        The distance the item can be thrown by the player.
        """
        source_entity = kwargs[SOURCE_ENTITY]
        return source_entity.strength.value * 4 - self.parent.weight.value

    def remove_from_inventory(self, source_entity):
        """
        Removes the parent item from the inventory.
        """
        source_entity.inventory.remove_item(self.parent)

    def handle_hit_ground(self, game_state, position, source_entity):
        self.handle_item_hit("hit_floor_action_tag", game_state, position, source_entity)

    def handle_hit_chasm(self, game_state, position, source_entity):
        self.handle_item_hit("hit_chasm_action_tag", game_state, position, source_entity)

    def handle_item_hit(self, tag, game_state, position, source_entity):
        for c in self.parent.get_children_with_tag(tag):
            if c.can_trigger(source_entity=source_entity, target_entity=self.parent,
                             game_state=game_state, target_position=position):
                c.trigger(source_entity=source_entity, target_entity=self.parent,
                          game_state=game_state, target_position=position)

    def missile_hit_effect(self, dungeon_level, position, game_state, source_entity):
        if is_hitting_ground(dungeon_level, position):
            self.handle_hit_ground(game_state, position, source_entity)
        else:
            self.handle_hit_chasm(game_state, position, source_entity)


def is_hitting_ground(dungeon_level, position):
    return not dungeon_level.get_tile_or_unknown(position).get_terrain().has("is_chasm")


class PlayerThrowStoneAction(PlayerMissileAction):
    def __init__(self):
        super(PlayerThrowStoneAction, self).__init__(GraphicChar(None, colors.GRAY, icon.STONE))
        self.component_type = "throw_stone_action"
        self.name = "Throw Stone"
        self.display_order = 95

    def add_energy_spent_to_entity(self, entity):
        entity.actor.newly_spent_energy += entity.throw_speed.value

    def missile_hit_effect(self, dungeon_level, position, game_state, source_entity):
        rock_hit_position(dungeon_level, position, source_entity)

    def max_missile_distance(self, **kwargs):
        source_entity = kwargs[SOURCE_ENTITY]
        return max_throw_distance(source_entity.strength.value)


def rock_hit_position(dungeon_level, position, source_entity):
    target_entity = dungeon_level.get_tile(position).get_first_entity()
    if target_entity is None:
        return
    # TODO cant be sure range attack is thrown rock, could possibly be a gun. Refactoring needed
    source_entity.ranged_attacker.hit(target_entity)


def max_throw_distance(strength):
    return strength + 1


class PlayerSlingStoneAction(PlayerMissileAction):
    def __init__(self, sling_weapon):
        super(PlayerSlingStoneAction, self).__init__(GraphicChar(None, colors.GRAY, icon.STONE))
        self.component_type = "sling_stone_action"
        self.name = "Throw Stone"
        self.display_order = 95
        self.sling_weapon = sling_weapon

    def add_energy_spent_to_entity(self, entity):
        """
        Help method for spending energy for the act performing entity.

        """
        entity.actor.newly_spent_energy += entity.throw_speed.value

    def missile_hit_effect(self, dungeon_level, position, game_state, source_entity):
        self.hit_position(dungeon_level, position, source_entity)

    def hit_position(self, dungeon_level, position, source_entity):
        target_entity = dungeon_level.get_tile(position).get_first_entity()
        if target_entity is None:
            return
        source_entity.ranged_attacker.hit(target_entity)


    def can_act(self, **kwargs):
        return True

    def max_missile_distance(self, **kwargs):
        source_entity = kwargs[SOURCE_ENTITY]
        return max_throw_distance(source_entity.strength.value) + self.sling_weapon.weapon_range.value


class PlayerCastMissileSpellAction(PlayerMissileAction):
    def __init__(self, item, missile_graphic):
        super(PlayerCastMissileSpellAction, self).__init__(missile_graphic)
        self.component_type = "cast_spell_action"
        self.name = "Cast Spell"
        self.display_order = 95
        self.item = item

    def add_energy_spent_to_entity(self, entity):
        """
        Help method for spending energy for the act performing entity.
        """
        entity.actor.newly_spent_energy += entity.cast_speed.value

    def missile_hit_effect(self, dungeon_level, position, game_state, source_entity):
        self.hit_position(dungeon_level, position, source_entity)

    def hit_position(self, dungeon_level, position, source_entity):
        target_entity = dungeon_level.get_tile(position).get_first_entity()
        if target_entity is None:
            return
        source_entity.ranged_attacker.try_hit(target_entity)

    def can_act(self, **kwargs):
        return True

    def max_missile_distance(self, **kwargs):
        return self.item.weapon_range.value


class PlayerShootWeaponAction(PlayerMissileAction):
    def __init__(self, ranged_weapon):
        super(PlayerShootWeaponAction, self).__init__()
        self.name = "Shoot"
        self.display_order = 85
        self.ranged_weapon = ranged_weapon
        self._missile_graphic = GraphicChar(None, colors.WHITE, icon.BIG_CENTER_DOT)

    @property
    def missile_graphic(self):
        return self._missile_graphic

    def add_energy_spent_to_entity(self, entity):
        """
        Help method for spending energy for the act performing entity.
        """
        entity.actor.newly_spent_energy += entity.shoot_speed.value

    def missile_hit_effect(self, dungeon_level, position, game_state, source_entity):
        self.remove_ammo_from_inventory(source_entity.inventory)
        self.hit_position(dungeon_level, position, source_entity)

    def can_act(self, **kwargs):
        source_entity = kwargs[SOURCE_ENTITY]
        ammo_items = [item for item in source_entity.inventory.items
                      if item.has("is_ammo")]
        return len(ammo_items) > 0

    def hit_position(self, dungeon_level, position, source_entity):
        target_entity = dungeon_level.get_tile(position).get_first_entity()
        if target_entity is None:
            return
        source_entity.ranged_attacker.hit(target_entity)

    def max_missile_distance(self, **kwargs):
        return self.ranged_weapon.weapon_range.value

    def remove_ammo_from_inventory(self, inventory):
        ammo_items = [item for item in inventory.items if item.has("is_ammo")]
        ammo_item_with_least_ammo = min(ammo_items, key=lambda e: e.stacker.size)
        inventory.remove_one_item_from_stack(ammo_item_with_least_ammo)


class MonsterTargetAction(MonsterWeightedAction):
    def __init__(self, min_range, max_range, weight=100):
        super(MonsterTargetAction, self).__init__(weight)
        self.tags.add("monster_target_action")
        self.weight = weight
        self.min_range = min_range
        self.max_range = max_range
        self.target_chooser_function = GetSuitableEnemyTarget()

    def get_target_options(self):
        return self.target_chooser_function(self.parent)


#  TODO Introduce Gaze effect super class?
class ParalyzeOnStare(MonsterTargetAction):
    def __init__(self, min_range, max_range, weight=100):
        super(ParalyzeOnStare, self).__init__(min_range, max_range, weight)
        self.component_type = "monster_paralyze_on_stare"

    def can_act(self, **kwargs):
        possible_targets = self.get_target_options()
        return any([target for target in possible_targets
                    if target.dungeon_mask.can_see_point(self.parent.position.value)])

    def act(self, destination):
        if not self.parent.dungeon_mask.can_see_point(destination):
            return
        if coin_flip():  # Should be replaced by spell resist.
            return
        targets = self.parent.dungeon_level.value.get_tile_or_unknown(destination).get_entities()
        if not any(targets):
            return
        for target_entity in targets:
            if target_entity.dungeon_mask.can_see_point(self.parent.position.value):
                target_entity.effect_queue.add(self.effect_factory())
        self.add_energy_spent_to_entity(self.parent)

    def effect_factory(self):
        min_turns = 1
        max_turns = 3
        turns = random.randrange(min_turns, max_turns + 1)
        return AddSpoofChild(self.parent, ParalyzedActor(), turns * gametime.single_turn,
                             message_effect=STARE_PARALYZE_MESSAGE, effect_id="paralyze")


class MonsterMissileAction(MonsterTargetAction):
    def __init__(self, min_range, max_range, missile_graphic, weight=100):
        super(MonsterMissileAction, self).__init__(min_range, max_range, weight)
        self.missile_graphic = missile_graphic

    def can_act(self, **kwargs):
        possible_targets = self.get_target_options()
        return any([target for target in possible_targets
                    if self.is_destination_within_range(target.position.value)
                    and not self.is_something_blocking(target.position.value)])

    def is_destination_within_range(self, destination):
        return self.min_range <= geometry.chess_distance(self.parent.position.value, destination) <= self.max_range

    def is_something_blocking(self, destination):
        """
        What about selfish creatures? that don't care about other creatures. Must know what kind of obstacle is blocking
        """
        path = get_path(self.parent.position.value, destination)
        hit_detector = shoot.MissileHitDetection(False, False)
        dungeon_level = self.parent.dungeon_level.value
        path_taken = hit_detector.get_path_taken(path, dungeon_level)
        return geometry.chess_distance(self.parent.position.value, destination) != len(path_taken)

    def act(self, destination):
        path = get_path(self.parent.position.value, destination)
        if path is None or path[-1] == self.parent.position.value:
            return False
        dungeon_level = self.parent.dungeon_level.value
        hit_detector = shoot.MissileHitDetection(False, False)
        path_taken = hit_detector.get_path_taken(path, dungeon_level)
        if path_taken is None or len(path_taken) < 1:
            return False
        animate_flight(self.parent.game_state.value, path_taken, self.missile_graphic.icon, self.missile_graphic.color_fg)
        self.missile_hit_effect(dungeon_level, path[-1])
        self.add_energy_spent_to_entity(self.parent)


#TODO: Most of content has moved to super class and should be removed.
class MonsterThrowStoneAction(MonsterMissileAction):
    def __init__(self, weight=100):
        super(MonsterThrowStoneAction, self).__init__(2, 4, GraphicChar(None, colors.GRAY, icon.STONE), weight)
        self.component_type = "monster_throw_stone_action"

    def add_energy_spent_to_entity(self, entity):
        """
        Help method for spending energy for the act performing entity.
        """
        entity.actor.newly_spent_energy += entity.throw_speed.value

    def missile_hit_effect(self, dungeon_level, position):
        rock_hit_position(dungeon_level, position, self.parent)


class MonsterThrowRockAction(MonsterThrowStoneAction):
    def __init__(self, weight):
        super(MonsterThrowRockAction, self).__init__(weight=weight)
        self.component_type = "monster_throw_rock_action"
        self.missile_graphic = GraphicChar(None, colors.GRAY, icon.DUNGEON_WALLS_ROW)


class MonsterMagicRangeAction(MonsterMissileAction):
    def __init__(self, damage, graphic_char, weight=100):
        super(MonsterMagicRangeAction, self).__init__(2, 4, graphic_char, weight)
        self.component_type = "monster_range_attack_action"
        self.damage = damage

    def missile_hit_effect(self, dungeon_level, position):
        magic_hit_position(self.damage, dungeon_level, position, self.parent)

    def is_destination_within_range(self, destination):
        return (1 < geometry.chess_distance(self.parent.position.value, destination) <=
                self.parent.sight_radius.value)


class SpiritMissile(MonsterMagicRangeAction):
    def __init__(self, weight=100):
        super(SpiritMissile, self).__init__(1, GraphicChar(None, colors.LIGHT_BLUE, icon.BIG_CENTER_DOT), weight)
        self.component_type = "monster_range_attack_action"


def magic_hit_position(damage, dungeon_level, position, source_entity):
    target_entity = dungeon_level.get_tile(position).get_first_entity()
    if target_entity is None:
        return
    damage_types = [DamageTypes.MAGIC]
    thrown_damage = UndodgeableAttack(damage, damage, damage_types)
    thrown_damage.damage_entity(source_entity, target_entity)


class MonsterMissileApplyEntityEffect(MonsterMissileAction):
    def __init__(self, min_range, max_range, missile_graphic, weight=100):
        super(MonsterMissileApplyEntityEffect, self).__init__(min_range, max_range, missile_graphic, weight)

    def effect_factory(self):
        pass

    def missile_hit_effect(self, dungeon_level, position):
        target_entity = dungeon_level.get_tile_or_unknown(position).get_first_entity()
        target_entity.effect_queue.add(self.effect_factory())

    def hit_animation(self, dungeon_level, position):
        pass


class MonsterHealTargetEntityEffect(MonsterMissileApplyEntityEffect):
    def __init__(self,  weight=100):
        heart_graphic = GraphicChar(None, colors.RED, icon.HEART)
        super(MonsterHealTargetEntityEffect, self).__init__(2, 4, heart_graphic, weight)
        self.component_type = "monster_range_heal_action"
        self.target_chooser_function = GetSuitableHealingTarget()

    def effect_factory(self):
        return Heal(self.parent, random.randrange(1, 3))


class MonsterTripTargetEffect(MonsterMissileApplyEntityEffect):
    def __init__(self,  weight=100):
        missile_graphic = GraphicChar(None, colors.YELLOW, icon.MAGIC_SHOT)
        super(MonsterTripTargetEffect, self).__init__(2, 4, missile_graphic, weight)
        self.component_type = "monster_range_trip_action"

    def effect_factory(self):
        return AddSpoofChild(self.parent, RandomStepper(), gametime.single_turn)


def get_suitable_enemy_target(my_faction, seen_entities):
    return [entity for entity in seen_entities if seen_entities.faction.value == my_faction]


class GetSuitableEnemyTarget(object):
    def __call__(self, source_entity):
        seen_entities = source_entity.vision.get_seen_entities()
        my_faction = source_entity.faction.value
        return [entity for entity in seen_entities if entity.faction.value != my_faction]


class GetSuitableHealingTarget(object):
    def __call__(self, source_entity):
        seen_entities = source_entity.vision.get_seen_entities()
        my_faction = source_entity.faction.value
        return [entity for entity in seen_entities
                if entity.faction.value == my_faction and
                entity.health.is_damaged()]
