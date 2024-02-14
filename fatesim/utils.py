from typing import Dict, List
import re


# Generic utilities
def clamp (value, minv, maxv):
    max(min(value, maxv), minv)


# Utilities for bonuses and modifiers
def parse_bonus_str(bonus_str: str) -> Dict:
    # 'bonus_str' is in format "<NUMBER> <UNIT_TYPE>", returns
    # {<UNIT_TYPE> (str): <NUMBER> (int)} for easy consolidation later
    pattern = r'([-+]?\d+)\s*(.*)'
    match = re.match(pattern, bonus_str)
    modifier = int(match.group(1))
    unit_type = match.group(2).strip()

    return {unit_type: modifier}

def consolidate_bonuses(bonuses: List[Dict]) -> Dict:
    # Takes in a list of dicts as made from 'parse_bonus_str' and
    # consolidates into a single dict, adding up modifiers for duplicate
    # keys
    consolidated = {}
    for bonus in bonuses:
        for bk in bonus:
            if bk in consolidated:
                consolidated[bk] += bonus[bk]
            else:
                consolidated[bk] = bonus[bk]

    return consolidated