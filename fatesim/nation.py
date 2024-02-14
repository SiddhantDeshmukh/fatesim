from fatesim.utils import clamp


class Nation:
    def __init__(self, renown: int, fate: int,
                 prosperity: int, happiness: int) -> None:
        # Resources are unbounded
        self.renown = renown
        self.fate = fate
        # Indicators are clamped between [-3, 3]
        self.prosperity = clamp(prosperity, -3, 3)
        self.happiness = clamp(happiness, -3, 3)