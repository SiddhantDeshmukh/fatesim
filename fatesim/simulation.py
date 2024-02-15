from typing import List
from copy import deepcopy

from fatesim.modifier import Modifier
from fatesim.unit import Unit, UnitGroup
from fatesim.utils import roll_d3, roll_d6


class BattleResult():
    def __init__(self, ug1: UnitGroup,
                 units_1_modifier: int, units_1_dice: int,
                 ug2: UnitGroup,
                 units_2_modifier: int, units_2_dice: int) -> None:
        self.units_1 = ug1.units
        self.units_1_id = ug1.uid
        self.units_1_modifier = units_1_modifier
        self.units_1_dice = units_1_dice

        self.units_2 = ug2.units
        self.units_2_id = ug2.uid
        self.units_2_modifier = units_2_modifier
        self.units_2_dice = units_2_dice

        self.units_1_total = sum(units_1_dice) + units_1_modifier
        self.units_2_total = sum(units_2_dice) + units_2_modifier

        self.victor, self.loser, self.deficit = self.determine_victor()

    def summary(self) -> str:
        summ = f"Battle between {self.units_1_id} and {self.units_2_id}\n"
        summ += "-"*40 + "\n"
        summ += f"{self.units_1_id} Units:"
        for unit in self.units_1:
            summ += f"\n\n\t{unit}"
        summ += "\n" + "-"*40 + "\n"
        summ += f"{self.units_2_id} Units:"
        for unit in self.units_2:
            summ += f"\n\n\t{unit}"
        summ += f"\nVictor is {self.victor} by {self.deficit}!"
        summ += f"\nModifiers: {self.units_1_modifier}, {self.units_2_modifier}"

        return summ

    def determine_victor(self):
        deficit = self.units_1_total - self.units_2_total
        if deficit == 0:
            return None, None, deficit

        victor, loser = (self.units_1_id,
                         self.units_2_id) if deficit > 0 else (self.units_2_id,
                                                               self.units_1_id)
        deficit = abs(deficit)

        return victor, loser, deficit


def check_open(is_open: bool, target: str):
    return (is_open and target.endswith("open")) or\
        (not is_open and not target.endswith("open"))


def is_applicable_modifier(modifier: Modifier, is_open: bool,
                           target: str):
    # Check if the modifier is applicable to the target
    if is_open and not modifier.target.endswith("open"):
        return False
    if modifier.target.startswith("all"):
        return True
    return target == modifier.target


def determine_total_modifier(attacking_ug: UnitGroup,
                             defending_ug: UnitGroup,
                             is_open: bool) -> int:
    # Determine the total modifier attacking units should have, avoiding
    # multiple counting (e.g. cav does not get multiple boosts for multiple
    # opposing siege)
    total_modifier = 0
    defending_unit_kinds = set([u.kind for u in defending_ug.units])
    for mod in attacking_ug.modifiers:
        if check_open(is_open, mod.target):
            if mod.target.startswith("all") or mod.target.split(" ")[0] in defending_unit_kinds:
                total_modifier += mod.bonus
    return total_modifier


def determine_combat_dice(units: List[Unit]) -> List[callable]:
    return [roll_d3 if unit.is_bloodied else roll_d6 for unit in units]


def roll_combat_dice(dice: List[callable]) -> List[int]:
    return [d() for d in dice]


def determine_new_units(ug: UnitGroup,
                        result: BattleResult) -> List[Unit]:
    units, units_id = deepcopy(ug.units), ug.uid
    if units_id == result.victor:
        return units

    # Find how many multiples of 6 there are in the deficit, then
    # multiples of 3, then remaining deficit and decide which units to
    # remove and bloody based on cost (lower cost ones go first)
    deficit = result.deficit
    new_units = deepcopy(units)
    # Sort in ascending order so cheapest units are at the front
    new_units.sort(key=lambda unit: unit.cost)
    # Unit deaths
    num_deaths = deficit // 6
    for _ in range(num_deaths):
        try:
            new_units.remove(new_units[0])
            deficit -= 6
        except IndexError:
            # no more units
            return new_units
    # Check if any units left
    if not new_units:
        return new_units

    # Bloodied units; prefer bloodied unit to dead one
    num_bloodied = deficit // 3
    while num_bloodied > 0:
        # Check if any units left
        if not new_units:
            return new_units  # all units killed
        # Only bloodied, units, remove low value ones
        if all(unit.is_bloodied for unit in new_units):
            new_units.pop()
            deficit -= 3
            num_bloodied -= 1
        # Iterate in ascending order
        for unit in new_units:
            if not unit.is_bloodied:
                unit.is_bloodied = True
                deficit -= 3
                num_bloodied -= 1
                if num_bloodied <= 0:
                    break

    # Bloody / remove another unit if deficit remains
    if deficit > 0:
        # print("Final deficit")
        if all(unit.is_bloodied for unit in new_units):
            new_units.pop()
            return new_units
        else:
            for unit in new_units:
                if not unit.is_bloodied:
                    unit.is_bloodied = True
                    return new_units
    return new_units  # deficit is <= 0


def simulate_battle(ug1: UnitGroup, ug2: UnitGroup, is_open: bool):
    # Simulate a battle between two sets of units
    # 'is_open' is used to determine modifier applicability for open
    # battles vs sieges
    # In Fatecraft, only sets of up to 3 units can fight each other
    # at a time, but there is no restriction made here
    # Create copies to avoid overwriting original unit groups
    units_1 = deepcopy(ug1.units)
    units_2 = deepcopy(ug2.units)
    # Remove all non-military units locally
    for u in units_1:
        if not u.has_military:
            units_1.remove(u)
    for u in units_2:
        if not u.has_military:
            units_2.remove(u)

    if not units_1 or not units_2:
        print("Both units_1 and units_2 must be non-empty")
        return None

    # Determine total modifiers each side should apply
    units_1_modifier = determine_total_modifier(ug1, ug2, is_open)
    units_2_modifier = determine_total_modifier(ug2, ug1, is_open)

    # Determine dice rolls
    units_1_dice = roll_combat_dice(determine_combat_dice(units_1))
    units_2_dice = roll_combat_dice(determine_combat_dice(units_2))

    # Compute result, but do not update units
    result = BattleResult(ug1, units_1_modifier, units_1_dice,
                          ug2, units_2_modifier, units_2_dice)

    return result
