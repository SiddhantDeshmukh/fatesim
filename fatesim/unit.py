from typing import List
from fatesim.modifier import Modifier, combine_modifiers


UNIT_KINDS = ["infantry", "cavalry", "naval", "siege"]
UNIT_COSTS = {
    # for now just renown cost, but for the AI to figure out what to kill
    "infantry": 5,
    "cavalry": 8,
    "naval": 8,
    "siege": 12,
}


class Unit:
    def __init__(self, movement: int, has_military: bool,
                 kind: str, bonuses_strs: List,
                 name="", affiliation="", is_bloodied=False) -> None:
        self.movement = movement
        self.has_military = has_military
        self.kind = kind
        self.affiliation = affiliation  # usually name of producing Nation
        self.bonuses_strs = bonuses_strs
        self.modifiers = combine_modifiers([Modifier.from_bonus_str(bonus_str)
                                            for bonus_str in bonuses_strs])
        self.name = name
        self.is_bloodied = is_bloodied
        # Unit cost (to AI) is total renown cost to replace it
        self.cost = UNIT_COSTS[self.kind] + 2*sum(m.bonus
                                                  for m in self.modifiers)
        # Fix Renown costs for unit types that give preset bonuses
        if self.kind == "infantry":
            self.cost -= 4
        if self.kind == "cavalry":
            self.cost -= 2
        if self.kind == "siege":
            self.cost -= 2

        self.data_dict = {
            "movement": self.movement,
            "has_military": self.has_military,
            "kind": self.kind,
            "affiliation": self.affiliation,
            "modifiers": self.modifiers_str(),
            "name": f"\"{self.name}\"",
            "is_bloodied": self.is_bloodied,
            "cost": self.cost
        }

    def __str__(self) -> str:
        desc = f"{self.name} ({self.cost} Renown)"
        desc += f"\n\tKind = {self.kind}"
        desc += f"\n\tHas Military? {self.has_military}"
        desc += f"\n\tMovement = {self.movement}"
        desc += f"\n\tModifiers:"
        if self.modifiers:
            desc += "\n\t\t"
        desc += "\n\t\t".join(str(modifier) for modifier in self.modifiers)
        desc += f"\n\tIs Bloodied? {self.is_bloodied}"

        return desc

    def __getitem__(self, key: str):
        return self.data_dict[key]

    def renown_value(self):
        # Renown value is cost, halved if unit is bloodied
        value = self.cost
        if self.is_bloodied:
            value //= 2
        return value

    def modifiers_str(self) -> str:
        # Get all the modifiers as a csv string
        mstr = ""
        for m in self.modifiers:
            mstr += f"{m},"
        mstr.rstrip(",")
        return f"\"{mstr}\""


class UnitGroup():
    def __init__(self, units: List[Unit], uid: str) -> None:
        self.units = units
        self.uid = uid
        self.modifiers = combine_modifiers([m for u in units
                                           for m in u.modifiers])

    def __str__(self) -> str:
        desc = "\n\n".join([str(unit) for unit in self.units])
        desc += "\nTotal Modifiers:"
        if self.modifiers:
            desc += "\n\t"
            desc += "\n\t".join(str(ug_mod) for ug_mod in self.modifiers)
        return desc

    def renown_value(self):
        if not self.units:
            return 0  # no units left
        total_value = sum([unit.renown_value() for unit in self.units])
        return total_value


def renown_difference(ug1: UnitGroup, ug2: UnitGroup) -> int:
    # Calculate difference in renown between two sets of units
    return ug1.renown_value() - ug2.renown_value()


UNIT_TEMPLATES = {
    "basic_infantry": lambda: Unit(4, True, "infantry", [],
                                   name="Basic Infantry"),
    "basic_cavalry": lambda: Unit(7, True, "cavalry", ["+2 siege open",
                                                       "+1 infantry open",
                                                       "-2 all struct"],
                                  name="Basic Cavalry"),
    "basic_siege": lambda: Unit(3, True, "siege", ["-2 all open",
                                                   "+3 all struct"],
                                name="Basic Siege"),
    # "basic_naval": lambda: Unit(10, True, "naval", [],
    #                             name="Basic Naval")
    "extra_infantry": lambda: Unit(4, True, "infantry", ["+3 infantry open",
                                                         "+3 cavalry open",
                                                         "+3 siege open"],
                                   name="Basic Infantry"),
    "extra_cavalry": lambda: Unit(7, True, "cavalry", ["+3 siege open",
                                                       "+3 infantry open",
                                                       "-2 all struct"],
                                  name="Basic Cavalry"),
    "extra_siege": lambda: Unit(3, True, "siege", ["+1 all open",
                                                   "+3 all struct"],
                                name="Basic Siege"),
}
