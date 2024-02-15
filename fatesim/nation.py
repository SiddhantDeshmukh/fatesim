from fatesim.utils import clamp


class Nation:
    def __init__(self, name: str, renown: int, fate: int,
                 prosperity: int, happiness: int,
                 units=None,
                 military_unit_cap=5, diplomatic_unit_cap=5,
                 settlements=None, structures=None) -> None:
        self.name = name
        # Resources are unbounded
        self.renown = renown
        self.fate = fate
        # Indicators are clamped between [-3, 3]
        self._prosperity = clamp(prosperity, -3, 3)
        self._happiness = clamp(happiness, -3, 3)
        # Units and structures
        self.units = units
        self.military_unit_cap = military_unit_cap
        self.diplomatic_unit_cap = diplomatic_unit_cap
        self.settlements = settlements
        self.structures = structures

    @property
    def prosperity(self):
        return self._prosperity

    @prosperity.setter
    def prosperity(self, value: int):
        self._prosperity = clamp(value, -3, 3)

    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value: int):
        self._prosperity = clamp(value, -3, 3)
