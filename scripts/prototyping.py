from copy import deepcopy
from typing import List, Tuple
import random

from fatesim.simulation import determine_new_units, simulate_battle
from fatesim.stats import simulate_n_stats, SimulationStats
from fatesim.unit import UnitGroup, UNIT_TEMPLATES


def random_unit_group():
    unit_kinds = list(UNIT_TEMPLATES.keys())
    num_units = random.randint(1, 3)
    units = []
    uid = ""
    for i in range(num_units):
        unit_kind = random.choice(unit_kinds)
        units.append(UNIT_TEMPLATES[unit_kind]())
        # capital letter of template type
        unit_level, unit_type = unit_kind.split("_")
        uid += f"{unit_level[0].capitalize()}{unit_type[0].capitalize()}_"

    uid = uid.rstrip("_")

    return UnitGroup(units, uid)


def random_unit_group_sims(num_sims=5, num_trials=100) -> Tuple[SimulationStats]:
    open_sim_stats = []
    struct_sim_stats = []
    for i in range(num_sims):
        # Generate random groups
        ug1, ug2 = random_unit_group(), random_unit_group()
        # Open battle
        open_sim_stats.append(simulate_n_stats(ug1, ug2, True, n=num_trials))
        # Structure battle
        struct_sim_stats.append(simulate_n_stats(
            ug1, ug2, False, n=num_trials))

    return open_sim_stats, struct_sim_stats


def main():
    # random.seed(420)
    open_sim_stats, struct_sim_stats = random_unit_group_sims(num_sims=20,
                                                              num_trials=100)
    outfile_name = "./sim_stats.txt"
    txt_file = open(outfile_name, "w")
    csv_file = open(outfile_name.replace(".txt", ".csv"), "w")
    # TODO:
    # - refactor 'is_open' into a battle_type ((land, naval), (open, siege))
    #   and save this as well
    # For now just saving open battles in CSV
    for i, (sim_open, sim_struct) in enumerate(zip(open_sim_stats, struct_sim_stats)):
        # Write text file
        print(f"=== Simulation {i+1} ===\n", file=txt_file)
        print("Open Battle:\n", file=txt_file)
        sim_open.write_summary(txt_file)
        print("Structure Battle:\n", file=txt_file)
        sim_struct.write_summary(txt_file)
        print("\n" + "-"*40 + "\n", file=txt_file)
        # Write CSV file
        if i == 0:
            print(sim_open.generate_csv_header(), file=csv_file)
        print(sim_open.generate_csv_row(), file=csv_file)

    txt_file.close()
    csv_file.close()
    # Create units on both sides and simualte battles
    # ug_iis = UnitGroup([
    #     UNIT_TEMPLATES["basic_infantry"],
    #     UNIT_TEMPLATES["basic_infantry"],
    #     UNIT_TEMPLATES["basic_siege"],
    # ], "IIS")

    # ug_ccs = UnitGroup([
    #     UNIT_TEMPLATES["basic_cavalry"],
    #     UNIT_TEMPLATES["basic_cavalry"],
    #     UNIT_TEMPLATES["basic_siege"],
    # ], "CCS")

    # ug_iii = UnitGroup([
    #     UNIT_TEMPLATES["basic_infantry"](),
    #     UNIT_TEMPLATES["basic_infantry"](),
    #     UNIT_TEMPLATES["basic_infantry"](),
    # ], "III")

    # ug_iic = UnitGroup([
    #     UNIT_TEMPLATES["basic_infantry"](),
    #     UNIT_TEMPLATES["basic_cavalry"](),
    #     UNIT_TEMPLATES["basic_cavalry"](),
    # ], "ICC")

    # Many battles
    # sim_stats_open = simulate_n_stats(ug_iis, ug_ccs, is_open=True, n=1000)
    # sim_stats_struct = simulate_n_stats(ug_iis, ug_ccs, is_open=False, n=1000)
    # sim_stats_open = simulate_n_stats(ug_iii, ug_iic, is_open=True, n=1000)
    # sim_stats_struct = simulate_n_stats(ug_iii, ug_iic, is_open=False, n=1000)
    # print(ug1)
    # print(ug2)
    # print("Open Battle")
    # sim_stats_open.print_stats()
    # print("Siege Battle")
    # sim_stats_struct.print_stats()

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
