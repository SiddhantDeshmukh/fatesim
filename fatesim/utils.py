from typing import Tuple
import re
import random


# Generic utilities
def clamp(value, minv, maxv):
    max(min(value, maxv), minv)


# Utilities for bonuses and modifiers
def parse_bonus_str(bonus_str: str) -> Tuple:
    # 'bonus_str' is in format "<NUMBER> <TARGET_UNIT_TYPE>", returns
    # (<NUMBER> <TARGET_UNIT_TYPE>)
    pattern = r"([-+]?\d+)\s*(\w+(\s+\w+)*)"
    match = re.match(pattern, bonus_str)
    modifier = int(match.group(1))
    target = match.group(2)

    return (modifier, target)


# RNG
def roll_d6() -> int:
    return random.randint(1, 6)


def roll_d3() -> int:
    return random.randint(1, 3)
