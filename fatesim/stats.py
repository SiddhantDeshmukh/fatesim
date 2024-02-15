from typing import List


from fatesim.simulation import determine_new_units, simulate_battle
from fatesim.unit import UnitGroup, renown_difference


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

    def print_stats(self):
        num_trials = len(self.deficits)
        summary = f"{num_trials} trials: {self.ug1.uid} - {self.ug2.uid}\n"
        # Calculate victories (there might be draws)
        num_ug1_victories = sum([v == self.ug1.uid for v in self.victors])
        num_ug2_victories = sum([v == self.ug2.uid for v in self.victors])
        summary += f"Wins: {num_ug1_victories} - {num_ug2_victories}\n"
        # Average roll deficit
        average_roll_deficit = sum(self.deficits) / num_trials
        summary += f"Average Roll Deficit: {average_roll_deficit}\n"
        # Average renown costs overall and for losses
        average_ug1_cost = sum(self.ug1_costs) / num_trials
        average_ug2_cost = sum(self.ug2_costs) / num_trials
        summary += f"Average Overall Cost: {average_ug1_cost} - {average_ug2_cost}\n"
        average_ug1_loss_cost = sum([c for i, c in enumerate(self.ug1_costs)
                                     if self.losers[i] == self.ug1.uid])
        average_ug2_loss_cost = sum([c for i, c in enumerate(self.ug2_costs)
                                     if self.losers[i] == self.ug2.uid])
        summary += f"Average Loss Cost: {average_ug1_loss_cost} - {average_ug2_loss_cost}\n"

        print(summary)


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
