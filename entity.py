import random
import turn
import numpy
import vector2d
import counter
import constants
import gamepiece
import entityeffect
import equipment
import terrain
import libtcodpy as libtcod


class Faction(object):
    PLAYER = 0
    MONSTER = 1


class StatusFlags(object):
    INVISIBILE = 0
    SEE_INVISIBILITY = 1
    FLYING = 2
    HAS_MIND = 3
    CAN_OPEN_DOORS = 4


class Entity(gamepiece.GamePiece):

    def __init__(self):
        super(Entity, self).__init__()
        self.hp = counter.Counter(1, 1)
        self._sight_radius = 8
        self._strength = 1
        self.equipment = equipment.Equipment(self)

        self._faction = Faction.MONSTER
        self.effect_queue = entityeffect.EffectQueue()
        self._status_flags = set()
        self._status_flags.add(StatusFlags.CAN_OPEN_DOORS)

        self.piece_type = gamepiece.GamePieceType.ENTITY
        self.max_instances_in_single_tile = 1
        self.draw_order = 2
        self.path = None
        self.__dungeon_level = None
        self._init_entity_effects()

        #  Pathfinding Cache
        self._walkable_positions_dictionary_cache = {}
        self._walkable_positions_cache_timestamp = -1

    def _init_entity_effects(self):
        can_open_doors_flag = StatusFlags.CAN_OPEN_DOORS
        effect = entityeffect.StatusAdder(self, self,
                                          can_open_doors_flag,
                                          time_to_live=numpy.inf)
        self.add_entity_effect(effect)

    @property
    def dungeon_level(self):
        return self.__dungeon_level

    @dungeon_level.setter
    def dungeon_level(self, value):
        if((not self.dungeon_level is value) and (not value is None)):
            self.__dungeon_level = value
            self.dungeon_map = libtcod.map_new(value.width, value.height)
            self.update_dungeon_map()
            self.path = libtcod.path_new_using_map(self.dungeon_map, 1.0)

    def update(self, player):
        pass

    def step_random_direction(self):
        direction = random.sample(list(constants.DIRECTIONS.values()), 1)
        new_position = self.position + direction[0]
        self.try_step_to(new_position)

    def try_step_to(self, new_position):
        x, y = new_position.x, new_position.y
        terrain_to_step = self.dungeon_level.tile_matrix[y][x].get_terrain()
        if(self.try_open_door(terrain_to_step)):
            return True
        if(self.try_hit(new_position)):
            return True
        if(self.try_move(new_position)):
            return True
        return False

    def try_open_door(self, terrain_to_step):
        if(isinstance(terrain_to_step, terrain.Door)):
            door = terrain_to_step
            if(not door.is_open):
                door.is_open = True
                return True
        return False

    def try_move(self, new_position, new_dungeon_level=None):
        if(new_dungeon_level is None):
            new_dungeon_level = self.dungeon_level
        old_dungeon_level = self.dungeon_level
        move_succeded = super(Entity, self).\
            try_move(new_position, new_dungeon_level)
        if(move_succeded):
            if(not old_dungeon_level is None and
               (not old_dungeon_level is new_dungeon_level)):
                old_dungeon_level.remove_entity_if_present(self)
            new_dungeon_level.add_entity_if_not_present(self)
        return move_succeded

    def try_remove_from_dungeon(self):
        old_dungeon_level = self.dungeon_level
        remove_succeded = super(Entity, self).\
            try_remove_from_dungeon()
        if(remove_succeded and (not old_dungeon_level is None)):
            old_dungeon_level.remove_entity_if_present(self)
        return remove_succeded

    def get_seen_entities(self):
        seen_entities = []
        for entity in self.dungeon_level.entities:
            if self.can_see_point(entity.position.x, entity.position.y):
                seen_entities.append(entity)
        return [entity for entity in seen_entities if not entity is self]

    def can_see_point(self, x, y):
        return libtcod.map_is_in_fov(self.dungeon_map, x, y)

    def hurt(self, damage, entity=None):
        self.hp.decrease(damage)
        if(self.is_dead):
            self.killer = entity

    def heal(self, health):
        self.hp.increase(health)

    def is_dead(self):
        return self.hp.value == 0

    def kill(self):
        self.hp.set_min()

    def try_hit(self, position):
        entity = self.dungeon_level.get_tile(position).get_first_entity()
        if(entity is None or
           entity._faction == self._faction):
            return False
        self.hit(entity)
        return True

    def hit(self, target_entity):
        damage = random.randrange(0, self._strength)
        damage_types = [entityeffect.DamageTypes.PHYSICAL]
        damage_effect = entityeffect.Damage(self, target_entity,
                                            damage, damage_types=damage_types)
        target_entity.add_entity_effect(damage_effect)

    def add_entity_effect(self, effect):
        self.effect_queue.add(effect)

    def update_effect_queue(self):
        self.effect_queue.update()

    def update_fov(self):
        libtcod.map_compute_fov(self.dungeon_map,
                                self.position.x,
                                self.position.y,
                                self._sight_radius, True)

    def has_path(self):
        if(self.path is None or libtcod.path_is_empty(self.path)):
            return False
        return True

    def print_walkable_map(self):
        for y in range(libtcod.map_get_height(self.dungeon_map)):
            line = ""
            for x in range(libtcod.map_get_width(self.dungeon_map)):
                if(libtcod.map_is_walkable(self.dungeon_map, x, y)):
                    line += " "
                else:
                    line += "#"
            print(line)

    def print_is_transparent_map(self):
        for y in range(libtcod.map_get_height(self.dungeon_map)):
            line = ""
            for x in range(libtcod.map_get_width(self.dungeon_map)):
                if(libtcod.map_is_transparent(self.dungeon_map, x, y)):
                    line += " "
                else:
                    line += "#"
            print(line)

    def print_visible_map(self):
        for y in range(libtcod.map_get_height(self.dungeon_map)):
            line = ""
            for x in range(libtcod.map_get_width(self.dungeon_map)):
                if(libtcod.map_is_in_fov(self.dungeon_map, x, y)):
                    line += " "
                else:
                    line += "#"
            print(line)

    def try_step_path(self):
        if(not self.has_path()):
            return False
        x, y = libtcod.path_walk(self.path, True)
        step_succeeded = self.try_step_to(vector2d.Vector2D(x, y))
        return step_succeeded

    def set_path_to_random_walkable_point(self):
        positions = self.get_walkable_positions_from_my_position()
        destination = random.sample(positions, 1)[0]
        libtcod.path_compute(self.path, self.position.x, self.position.y,
                             destination.x, destination.y)

    def has_status(self, status):
        return status in self._status_flags

    def add_status(self, status):
        return self._status_flags.add(status)

    def clear_all_status(self):
        self._status_flags = set()

    def _can_pass_terrain(self, terrain_to_pass):
        if(terrain_to_pass is None):
            return False
        if(not terrain_to_pass.is_solid()):
            return True
        if(self.has_status(StatusFlags.CAN_OPEN_DOORS) and
           isinstance(terrain_to_pass, terrain.Door)):
            return True
        return False

    def get_walkable_positions_from_my_position(self):
        position = self.position
        if(not (position in self._walkable_positions_dictionary_cache.keys()
                and self.dungeon_level._terrain_changed_timestamp <=
                self._walkable_positions_cache_timestamp)):
            self._calculate_walkable_positions_from_start_position(position)
        return self._walkable_positions_dictionary_cache[position]

    def _calculate_walkable_positions_from_start_position(self, position):
        visited = set()
        visited.add(position)
        queue = [position]
        queue.extend(self._get_walkable_neighbors(position))
        while (len(queue) > 0):
            position = queue.pop()
            while(len(queue) > 0 and position in visited):
                position = queue.pop()
            visited.add(position)
            neighbors = set(self._get_walkable_neighbors(position)) - visited
            queue.extend(neighbors)
        visited = list(visited)
        for point in visited:
            self._walkable_positions_dictionary_cache[point] = visited
        self._walkable_positions_cache_timestamp = turn.current_turn

    def _get_walkable_neighbors(self, position):
        result_positions = []
        for direction in constants.DIRECTIONS.values():
            neighbor_position = position + direction
            x, y = neighbor_position.x, neighbor_position.y
            try:
                neighbor = self.dungeon_level.tile_matrix[y][x]
                if(self._can_pass_terrain(neighbor.get_terrain())):
                    result_positions.append(neighbor_position)
            except IndexError:
                pass
        return result_positions

    def update_dungeon_map(self):
        for y in range(self.dungeon_level.height):
            for x in range(self.dungeon_level.width):
                terrain = self.dungeon_level.tile_matrix[y][x].get_terrain()
                libtcod.map_set_properties(self.dungeon_map, x, y,
                                           terrain.is_transparent(),
                                           self._can_pass_terrain(terrain))
        self.update_fov()
