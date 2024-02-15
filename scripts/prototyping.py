from typing import List
import random

from fatesim.simulation import determine_new_units, simulate_battle
from fatesim.stats import simulate_n_stats
from fatesim.unit import UnitGroup, UNIT_TEMPLATES


def main():
    # random.seed(420)
    # Create units on both sides and simualte battles
    ug1 = UnitGroup([
        UNIT_TEMPLATES["basic_infantry"],
        UNIT_TEMPLATES["basic_infantry"],
        UNIT_TEMPLATES["basic_siege"],
    ], "IIS")

    ug2 = UnitGroup([
        UNIT_TEMPLATES["basic_cavalry"],
        UNIT_TEMPLATES["basic_cavalry"],
        UNIT_TEMPLATES["basic_siege"],
    ], "CCS")

    # Many battles
    sim_stats_open = simulate_n_stats(ug1, ug2, is_open=True, n=1000)
    sim_stats_struct = simulate_n_stats(ug1, ug2, is_open=False, n=1000)
    # print(ug1)
    # print(ug2)
    print("Open Battle")
    sim_stats_open.print_stats()
    print("Siege Battle")
    sim_stats_struct.print_stats()

    # Individual battles
    # open_battle = simulate_battle(ug1, ug2, True)
    # print("Open Battle")
    # print(open_battle.summary())
    # Determine bloodied/dead units
    # new_units_1 = determine_new_units(ug1, "U1", open_battle)
    # new_units_2 = determine_new_units(ug2, "U2", open_battle)
    # structure_battle = simulate_battle(ug1, ug2, False)
    # print("\nStructure Battle")
    # print(structure_battle.summary())


if __name__ == "__main__":
    main()
