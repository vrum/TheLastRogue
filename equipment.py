import icon
from compositecore import Leaf


class EquipmentSlot(object):
    def __init__(self, name, equipment_type, icon):
        self.name = name
        self.equipment_type = equipment_type
        self.icon = icon

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class EquipmentTypes(object):
    #  Armor
    HEADGEAR = 0
    ARMOR = 1
    BOOTS = 2

    #  Jewelry
    RING = 3
    AMULET = 4

    #  Weapons
    MELEE_WEAPON = 5
    RANGED_WEAPON = 6

    ALL = [HEADGEAR, ARMOR, BOOTS,
           RING, AMULET, MELEE_WEAPON, RANGED_WEAPON]


class EquipmentSlots(object):
    #  Weapons
    MELEE_WEAPON = EquipmentSlot("Melee Weapon", EquipmentTypes.MELEE_WEAPON, icon.SWORD)
    RANGED_WEAPON = EquipmentSlot("Ranged Weapon", EquipmentTypes.RANGED_WEAPON, icon.GUN)

    #  Armor
    HEADGEAR = EquipmentSlot("Headgear", EquipmentTypes.HEADGEAR, icon.HELM)
    ARMOR = EquipmentSlot("Armor", EquipmentTypes.ARMOR, icon.ARMOR)
    BOOTS = EquipmentSlot("Boots", EquipmentTypes.BOOTS, icon.BOOTS)

    #  Jewelry
    RIGHT_RING = EquipmentSlot("Right Ring", EquipmentTypes.RING, icon.RING)
    LEFT_RING = EquipmentSlot("Left Ring", EquipmentTypes.RING, icon.RING)
    AMULET = EquipmentSlot("Amulet", EquipmentTypes.AMULET, icon.AMULET)

    ALL = [MELEE_WEAPON, RANGED_WEAPON, HEADGEAR, ARMOR,
           BOOTS, RIGHT_RING, LEFT_RING, AMULET]


class Equipment(Leaf):
    def __init__(self):
        super(Equipment, self).__init__()
        self.component_type = "equipment"
        self._equipment = {
            EquipmentSlots.HEADGEAR: None,
            EquipmentSlots.ARMOR: None,
            EquipmentSlots.BOOTS: None,

            EquipmentSlots.RIGHT_RING: None,
            EquipmentSlots.LEFT_RING: None,
            EquipmentSlots.AMULET: None,

            EquipmentSlots.MELEE_WEAPON: None,
            EquipmentSlots.RANGED_WEAPON: None
        }

    def get(self, equipment_slot):
        return self._equipment[equipment_slot]

    def has_type(self, equipment_type):
        slots = [slot for slot in EquipmentSlots.ALL
                 if slot.equipment_type == equipment_type]
        return not len(slots) < 0

    def slot_is_equiped(self, equipment_slot):
        return not self._equipment[equipment_slot] is None

    def unequip(self, equipment_slot):
        equipment = self._equipment[equipment_slot]
        for e in equipment.get_children_with_tag("unequip_effect"):
            e.effect()
        self._equipment[equipment_slot] = None
        return equipment

    def can_unequip_to_inventory(self, equipment_slot):
        item = self.get(equipment_slot)
        return (self.slot_is_equiped(equipment_slot) and
                self.parent.inventory.has_room_for_item(item))

    def unequip_to_inventory(self, equipment_slot):
        equipment = self.unequip(equipment_slot)
        succeded = self.parent.inventory.try_add(equipment)
        return succeded

    def get_slots_of_type(self, equipment_type):
        return [slot for slot in EquipmentSlots.ALL
                if slot.equipment_type == equipment_type]

    def get_open_slots_of_type(self, equipment_type):
        return [slot for slot in self.get_slots_of_type(equipment_type)
                if self._equipment[slot] is None]

    def _all_slots_of_type_are_used(self, equipment_type):
        return len(self.get_open_slots_of_type(equipment_type)) < 1

    def can_equip(self, equipment):
        if self._all_slots_of_type_are_used(equipment.equipment_type.value):
            return False
        return True

    def try_equip(self, equipment):
        if self.can_equip(equipment):
            self._equip(equipment)
            return True
        return False

    def force_equip(self, equipment):
        self._equip_into_slot(equipment, self.get_slots_of_type(equipment.equipment_type.value)[0])

    def _equip(self, equipment):
        open_slots = self.get_open_slots_of_type(equipment.equipment_type.value)
        self._equip_into_slot(equipment, open_slots[0])

    def _equip_into_slot(self, equipment, slot):
        self._equipment[slot] = equipment
        for e in equipment.get_children_with_tag("on_equip_effect"):
            e.effect(self.parent)

    def _reset_equipment_spoofed_children(self):
        for _, equipment in self._equipment.iteritems():
            if equipment:
                equipment.reset_spoofed_children()

    def first_tick(self, time_spent):
        self._reset_equipment_spoofed_children()
        self.execute_equip_effects()

    def execute_equip_effects(self):
        for equipment_slot in EquipmentSlots.ALL:
            if self.slot_is_equiped(equipment_slot):
                equipment = self._equipment[equipment_slot]
                for e in equipment.get_children_with_tag("equipped_effect"):
                    e.equipped_effect(self.parent)

    def print_equipment(self):
        print("###############################")
        for slot, content in self._equipment.iteritems():
            print(slot, content)
        print("###############################")

    def after_tick(self, time):
        """
        Runs after_tick on all child components.
        """
        for key, e in self._equipment.iteritems():
            if e:
                e.after_tick(time)
