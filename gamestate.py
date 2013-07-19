import dungeonlevel
import settings
import player
import dungeon
import monster
import geometry as geo
import item
import gui
import camera
import constants
import rectfactory
import turn
import messenger
import state


def reset_globals():
    turn.current_turn = 0
    messenger.messenger = messenger.Messenger()


class GameStateBase(state.State):
    def __init__(self):
        reset_globals()
        self.player = player.Player(self)
        self._init_gui()
        camera_position = (constants.MONSTER_STATUS_BAR_WIDTH, 0)
        self.camera = camera.Camera(camera_position, geo.zero2d())
        self.has_won = False
        self.dungeon_level = None
        self._should_draw = True

    def signal_should_redraw_screen(self):
        self._should_draw = True

    def draw(self):
        if(self._should_draw or not settings.lazy_draw):
            self.force_draw()

    def force_draw(self):
        dungeon_level = self.player.dungeon_level
        dungeon_level.draw(self.camera)
        self.player_status_bar.draw()
        self.message_bar.draw()
        self.monster_status_bar.draw()
        self._should_draw = False

    def update(self):
        self.message_bar.update()

        dungeon_level = self.player.dungeon_level
        dungeon_level.update()

        self._update_gui()

        if(self.player.is_dead()):
            self.current_stack.pop()
        if(self.has_won):
            self.current_stack.pop()

    def _update_gui(self):
        self.monster_status_bar.update(self.player)
        self.player_status_bar.update()
        self.camera.update(self.player)

    def _init_gui(self):
        player_status_rect = rectfactory.player_status_rect()
        self.player_status_bar =\
            gui.PlayerStatusBar(player_status_rect,
                                self.player)

        monster_status_rect = geo.Rect(geo.zero2d(),
                                       constants.MONSTER_STATUS_BAR_WIDTH,
                                       constants.MONSTER_STATUS_BAR_HEIGHT)

        self.monster_status_bar =\
            gui.EntityStatusList(monster_status_rect,
                                 vertical_space=1)

        self.message_bar =\
            gui.MessageDisplay(rectfactory.message_display_rect())


class GameState(GameStateBase):
    def __init__(self):
        super(GameState, self).__init__()
        self.dungeon = dungeon.Dungeon(self)
        self._init_player_position()

    def _init_player_position(self):
        first_level = self.dungeon.get_dungeon_level(0)
        self.dungeon_level = first_level
        for stairs in first_level.up_stairs:
            move_succeded = self.player.try_move(stairs.position, first_level)
            if(move_succeded):
                return
        raise


class TestGameState(GameStateBase):
    def __init__(self):
        super(TestGameState, self).__init__()
        self.dungeon_level =\
            dungeonlevel.dungeon_level_from_file("test.level")

        self._init_player()
        self._init_items()
        self._init_monsters()

    def _init_player(self):
        start_position = (20, 10)
        player_move_success = self.player.try_move(start_position,
                                                   self.dungeon_level)
        if(not player_move_success):
            self.player.try_move((1, 1), self.dungeon_level)

    def _init_items(self):
        gun1 = item.Gun()
        gun2 = item.Gun()
        gun1_position = (20, 20)
        gun2_position = (22, 20)

        potion = item.HealthPotion()
        potion_position = (24, 16)

        ring = item.RingOfInvisibility()
        ring_position = (20, 13)

        gun1.try_move(gun1_position, self.dungeon_level)
        gun2.try_move(gun2_position, self.dungeon_level)
        potion.try_move(potion_position, self.dungeon_level)
        ring.try_move(ring_position, self.dungeon_level)

    def _init_monsters(self):
        rat = monster.RatMan()
        rat_pos = (15, 15)
        rat.try_move(rat_pos, self.dungeon_level)

        rat2 = monster.Jerico()
        rat2_pos = (15, 25)
        rat2.try_move(rat2_pos, self.dungeon_level)

        statue = monster.StoneStatue()
        statue_pos = (25, 7)
        statue.try_move(statue_pos, self.dungeon_level)
