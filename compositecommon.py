from Status import POISON_STATUS_DESCRIPTION
from attacker import DamageTypes
from compositecore import Leaf
from entityeffect import DamageOverTimeEffect, AddSpoofChild
import gametime
import messenger
from stats import DataPointBonusSpoof, DataTypes


class EntityShareTileEffect(Leaf):
    """
    Defines an effect that sharing tile with this parent entity will result in.
    """

    def __init__(self):
        super(EntityShareTileEffect, self).__init__()
        self.tags.add("entity_share_tile_effect")

    def share_tile_effect_tick(self, sharing_entity, time_spent):
        if (not sharing_entity is self.parent and
                self.can_effect(source_entity=self.parent, target_entity=sharing_entity, time=time_spent)):
            self.effect(source_entity=self.parent, target_entity=sharing_entity, time=time_spent)

    def effect(self, **kwargs):
        pass

    def can_effect(self, **kwargs):
        return True


class PoisonEntityEffectFactory(object):
    def __init__(self, source_entity, total_damage, turn_interval, turns_to_live):
        self.source_entity = source_entity
        self.total_damage = total_damage
        self.turn_interval = turn_interval
        self.turns_to_live = turns_to_live

    def __call__(self):
        damage_per_turn = self.total_damage / (self.turns_to_live / self.turn_interval)
        return DamageOverTimeEffect(self.source_entity, damage_per_turn, [DamageTypes.POISON],
                                    self.turn_interval, self.turns_to_live,
                                    messenger.POISON_MESSAGE, POISON_STATUS_DESCRIPTION, meld_id="poison")


class AddEffectToOtherSeenEntities(Leaf):
    """
    Adds effects to seen entities other than self.
    """

    def __init__(self, effect_factory, ttl=1):
        super(AddEffectToOtherSeenEntities, self).__init__()
        self.component_type = "add_effect_to_other_seen_entities_" + str(effect_factory)
        self.effect_factory = effect_factory
        self.ttl = ttl

    def before_tick(self, time):
        seen_entities = self.parent.vision.get_seen_entities()
        for entity in seen_entities:
            if not entity is self.parent:
                entity.effect_queue.add(AddSpoofChild(self.parent, self.effect_factory(), self.ttl))


class HealAnEntityOnDeath(Leaf):
    """
    Will Heal an entity when parent has died.
    """

    def __init__(self, source_entity):
        super(HealAnEntityOnDeath, self).__init__()
        self.component_type = "heal_entity_on_death"
        self.source_entity = source_entity
        self.target_entity = source_entity

    def on_tick(self, time):
        if self.parent.health.is_dead():
            self.target_entity.health_modifier.heal(1)


frost_effect_factory = lambda: DataPointBonusSpoof(DataTypes.MOVEMENT_SPEED, gametime.half_turn)
