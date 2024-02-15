from fatesim.modifier import combine_modifiers

SETTLEMENT_KINDS = ["Village", "Town", "City", "Capital"]
GARRISON_CAP = 3


class Settlement():
    def __init__(self, name: str, kind: str, structures=[],
                 garrisoned_units=[]) -> None:
        self.name = name
        self.kind = kind
        # Check to make sure structure is allowed to be in a settlement
        self.structures = [s for s in structures if s.in_settlement]
        self.defensive_structures = [s for s in self.structures
                                     if s.is_defensive]
        self.production_structures = [s for s in structures
                                      if not s in self.defensive_structures]
        # Defensive modifiers from structures that provide them
        self.defense_modifier = combine_modifiers(s.modifier
                                                  for s in self.defensive_structures)
        self.garrisoned_units = garrisoned_units
