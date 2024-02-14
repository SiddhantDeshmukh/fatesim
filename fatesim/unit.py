from typing import List
from utils import consolidate_bonuses, parse_bonus_str


UNIT_TYPES = ["infantry", "cavalry", "siege", "naval"]

class Unit:
    def __init__(self, movement: int, has_military: bool,
                 type: str, affiliation: str, bonuses_strs: List) -> None:
        self.movement = movement
        self.has_military = has_military
        self.type = type
        self.affiliation = affiliation
        self.bonuses_strs = bonuses_strs
        self.bonuses = consolidate_bonuses([parse_bonus_str(bonus_str)
                                            for bonus_str in bonuses_strs])