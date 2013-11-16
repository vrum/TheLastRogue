from actor import Actor
from entityeffect import Teleport, StatusAdder, StatusRemover
from equipment import EquipmentSlots
from missileaction import PlayerShootWeaponAction, PlayerThrowRockAction
from statusflags import StatusFlags
import console
import gametime
import geometry as geo
import inputhandler
import menufactory
import positionexaminer
import spawner


class InputActor(Actor):
    def __init__(self):
        super(InputActor, self).__init__()

    def set_path_destination(self, destination):
        if not destination is None:
            if self.parent.memory_map.has_seen_position(destination):
                self.parent.path.compute_path(destination)
            else:
                self.parent.path.set_line_path(destination)

    def handle_move_input(self, key):
        dx, dy = inputhandler.move_controls[key]
        new_position = geo.add_2d(self.parent.position.value, (dx, dy))
        move_succeded = self.parent.mover.try_move_or_bump(new_position)
        if move_succeded:
            self.newly_spent_energy += self.parent.movement_speed.value

    def spawn_context_menu(self):
        context_menu = \
            menufactory.context_menu(self.parent,
                                     self.parent.
                                     game_state.value.menu_prompt_stack)
        self.parent.game_state.value.start_prompt(context_menu)

    def handle_keyboard_input(self):
        key = inputhandler.handler.get_keypress()
        if key in inputhandler.move_controls:
            self.handle_move_input(key)
        elif key == inputhandler.ENTER:
            self.spawn_context_menu()
        elif key == inputhandler.PRINTSCREEN:
            console.console.print_screen()
        elif key == inputhandler.TAB:
            command_list_state = self.parent.game_state.value.command_list_bar.active
            self.parent.game_state.value.command_list_bar.active = not command_list_state

        elif key == inputhandler.PICKUP:  # Pick up
            if self.parent.pick_up_item_action.can_act():
                self.parent.pick_up_item_action.act()
            else:
                self.parent.pick_up_item_action.print_player_error()
        elif key == inputhandler.FIRE:
            equipment = self.parent.equipment
            if equipment.slot_is_equiped(EquipmentSlots.RANGED_WEAPON):
                self.shoot_weapon()
        elif key == inputhandler.STONE:
            self.throw_rock()
        elif key == inputhandler.ESCAPE:
            self.parent.health.hp.set_min()
            self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.REST:  # Rest
            self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.EXAMINE:
            destination_selector = \
                positionexaminer. \
                    PositionSelector(self.parent.game_state.value.menu_prompt_stack,
                                     self.parent.position.value,
                                     self.parent.game_state.value)
            self.parent.game_state.value.start_prompt(destination_selector)
            destination = destination_selector.selected_position
            self.set_path_destination(destination)

        elif key == inputhandler.INVENTORY:
            if not self.parent.inventory.is_empty():
                menu = menufactory.inventory_menu(self.parent, self.parent.game_state.
                value.menu_prompt_stack)
                self.parent.game_state.value.start_prompt(menu)

        elif key == inputhandler.TWO:
            self.parent.health_modifier.heal(300)

        elif key == inputhandler.THREE:
            effect = Teleport(self.parent, time_to_live=1)
            self.parent.effect_queue.add(effect)
            self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.FOUR:
            invisibile_flag = StatusFlags.INVISIBILE
            if not self.parent.status_flags.has_status(invisibile_flag):
                effect = StatusAdder(self.parent,
                                     invisibile_flag,
                                     time_to_live=float("inf"))
                self.parent.effect_queue.add(effect)
            else:
                invisible_status = StatusFlags.INVISIBILE
                effect = StatusRemover(self.parent, invisible_status,
                                       time_to_live=1)
                self.parent.effect_queue.add(effect)
                self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.FIVE:
            spawner.spawn_rat_man(self.parent.dungeon_level.value,
                                  self.parent.game_state.value)
            self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.ZERO:
            self.parent.game_state.value.has_won = True
            self.newly_spent_energy += gametime.single_turn

        elif key == inputhandler.PRINTSCREEN:
            console.console.print_screen()

    def handle_mouse_input(self):
        inputhandler.handler.update_keys()
        mouse_position = inputhandler.handler.get_mouse_position()
        if not mouse_position is None:
            if inputhandler.handler.get_left_mouse_press():
                self.set_path_destination(self.parent.game_state.value.camera.
                screen_to_dungeon_position(mouse_position))
        if self.parent.path.has_path():
            self.parent.path.try_step_path()
            self.newly_spent_energy += self.parent.movement_speed.value

    def act(self):
        self.parent.game_state.value.force_draw()
        self.newly_spent_energy = 0

        self.handle_mouse_input()

        if len(self.parent.vision.get_seen_entities()) > 0:
            self.parent.path.clear()

        if self.newly_spent_energy < 1:
            self.handle_keyboard_input()

        if self.has_sibling("dungeon_mask"):
            self.parent.dungeon_mask.update_fov()
        return self.newly_spent_energy

    def shoot_weapon(self):
        weapon = self.parent.equipment.get(EquipmentSlots.RANGED_WEAPON)
        shooting = PlayerShootWeaponAction(weapon)
        game_state = self.parent.game_state.value
        if shooting.can_act(source_entity=self.parent, game_state=game_state):
            shooting_succeded = shooting.act(source_entity=self.parent,
                                             game_state=game_state)
            if shooting_succeded:
                self.newly_spent_energy += gametime.single_turn

    def throw_rock(self):
        rock_throwing = PlayerThrowRockAction()
        game_state = self.parent.game_state.value
        if (rock_throwing.can_act(source_entity=self.parent,
                                  game_state=game_state)):
            rock_throwing.act(source_entity=self.parent,
                              game_state=game_state)
