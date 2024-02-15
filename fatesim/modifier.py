from copy import deepcopy
from typing import List
from fatesim.utils import parse_bonus_str


class Modifier():
    def __init__(self, bonus: int, target: str) -> None:
        self.bonus = bonus
        # always two words, first describes unit, second describes kind (open, structure)
        self.target = target

    @classmethod
    def from_bonus_str(cls, bonus_str: str):
        bonus, target = parse_bonus_str(bonus_str)
        modifier = cls(bonus, target)
        return modifier

    def __str__(self):
        if self.bonus > 0:
            return f"+{self.bonus} {self.target}"
        else:
            return f"{self.bonus} {self.target}"


def combine_modifiers(modifiers_: List[Modifier]) -> List[Modifier]:
    # Combines the numerical values of like modifiers
    if not modifiers_:
        return []
    new_modifiers = []
    modifiers = deepcopy(modifiers_)
    for mod in modifiers:
        found = False
        for nmod in new_modifiers:
            if mod.target == nmod.target:
                nmod.bonus += mod.bonus
                found = True
                break
        if not found:
            new_modifiers.append(mod)
    return new_modifiers
