from typing import List
from io import TextIOWrapper


from fatesim.simulation import determine_new_units, simulate_battle
from fatesim.unit import Unit, UnitGroup, renown_difference


class SimulationStats():
    # Assumes two unit groups (UG1 & UG2) fighting each other multiple
    # times without any changes in the battle
    # Usually created from the 'simulate_n_stats' function
    def __init__(self, ug1: UnitGroup, ug2: UnitGroup,
                 deficits: List[int], victors: List[str],
                 losers: List[str], ug1_costs: List[int],
                 ug2_costs: List[int]) -> None:
        self.ug1 = ug1
        self.ug2 = ug2
        self.deficits = deficits
        self.victors = victors
        self.losers = losers
        self.ug1_costs = ug1_costs
        self.ug2_costs = ug2_costs

    @classmethod
    def blank(cls):
        # For when starting a new simulation
        return cls(None, None, [], [], [], [], [])

    def compute_summary_stats(self):
        self.num_trials = len(self.deficits)
        # Calculate victories (there might be draws)
        self.num_ug1_victories = sum([v == self.ug1.uid for v in self.victors])
        self.num_ug2_victories = sum([v == self.ug2.uid for v in self.victors])
        # Average roll deficit
        self.average_roll_deficit = sum(self.deficits) / self.num_trials
        # Average renown costs overall and for losses
        self.average_ug1_cost = sum(self.ug1_costs) / self.num_trials
        self.average_ug2_cost = sum(self.ug2_costs) / self.num_trials
        # UG1 Loss Cost
        average_ug1_loss_cost = 0
        count = 0
        for i, c in enumerate(self.ug1_costs):
            if self.losers[i] == self.ug1.uid:
                average_ug1_loss_cost += c
                count += 1
        if count == 0:
            self.average_ug1_loss_cost = 0
        else:
            self.average_ug1_loss_cost = average_ug1_loss_cost / count
        # UG2 Loss Cost
        average_ug2_loss_cost = 0
        count = 0
        for i, c in enumerate(self.ug2_costs):
            if self.losers[i] == self.ug2.uid:
                average_ug2_loss_cost += c
                count += 1
        if count == 0:
            self.average_ug2_loss_cost = 0
        else:
            self.average_ug2_loss_cost = average_ug2_loss_cost / count

    def generate_summary(self) -> str:
        self.compute_summary_stats()  # make sure things are updated
        summary = f"{self.num_trials} trials: {self.ug1.uid} - {self.ug2.uid}\n"
        summary += f"Wins: {self.num_ug1_victories} - {self.num_ug2_victories}\n"
        summary += f"Average Roll Deficit: {self.average_roll_deficit}\n"
        summary += f"Average Overall Cost: {self.average_ug1_cost:.2f} - {self.average_ug2_cost:.2f}\n"
        summary += f"Average Loss Cost: {self.average_ug1_loss_cost:.2f} - {self.average_ug2_loss_cost:.2f}\n"

        return summary

    def write_summary(self, f: TextIOWrapper) -> None:
        # Generates summary and dumps it to f
        summary = self.generate_summary()
        f.write(summary)

    def generate_csv_header(self) -> str:
        # Convenience function for getting the column names of the rows
        columns = ["sim_uid", "num_trials", "num_ug1_victories",
                   "num_ug2_victories", "avg_roll_deficit", "avg_ug1_cost",
                   "avg_ug2_cost", "avg_ug1_loss_cost", "avg_ug2_loss_cost"]
        unit_attributes = ["name", "kind", "modifiers", "cost"]
        for i in range(3):
            for attr in unit_attributes:
                columns.append(f"ug1_{i+1}_{attr}")
        for i in range(3):
            for attr in unit_attributes:
                columns.append(f"ug2_{i+1}_{attr}")

        return ",".join(columns)

    def generate_csv_row(self) -> str:
        # Generate a row to be saved in a CSV and loaded later for plotting
        # This does not save everything, just the UIDs, unit attributes and
        # battle simulation statistics
        # columns: [sim_uid, [sim_stats], [ug1 attributes], [ug2 attributes]]
        sim_uid = f"{self.num_trials}-{self.ug1.uid}-{self.ug2.uid}"
        csv_row = f"{sim_uid},{self.num_trials},{self.num_ug1_victories}," +\
            f"{self.num_ug2_victories},{self.average_roll_deficit}," +\
            f"{self.average_ug1_cost},{self.average_ug2_cost}," +\
            f"{self.average_ug1_loss_cost},{self.average_ug2_loss_cost},"
        unit_attributes = ["name", "kind", "modifiers", "cost"]
        for i in range(3):
            try:
                unit = self.ug1.units[i]
                for attr in unit_attributes:
                    csv_row += f"{unit[attr]},"
            except IndexError:
                csv_row += ","*len(unit_attributes)
                continue
        for i in range(3):
            try:
                unit = self.ug2.units[i]
                for attr in unit_attributes:
                    csv_row += f"{unit[attr]},"
            except IndexError:
                csv_row += ","*len(unit_attributes)
                continue
        csv_row.rstrip(",")

        return csv_row


# Simulate the same battle N times, get summary statistics
def simulate_n_stats(ug1: UnitGroup, ug2: UnitGroup,
                     is_open: bool, n=100):
    sim_stats = SimulationStats.blank()
    sim_stats.ug1 = ug1
    sim_stats.ug2 = ug2
    for i in range(n):
        result = simulate_battle(ug1, ug2, is_open)
        new_ug1 = UnitGroup(determine_new_units(ug1, result),
                            f"{ug1.uid}_n")
        new_ug2 = UnitGroup(determine_new_units(ug2, result),
                            f"{ug2.uid}_n")

        sim_stats.deficits.append(result.deficit)
        sim_stats.victors.append(result.victor)
        sim_stats.losers.append(result.loser)
        sim_stats.ug1_costs.append(renown_difference(ug1, new_ug1))
        sim_stats.ug2_costs.append(renown_difference(ug2, new_ug2))

    return sim_stats
