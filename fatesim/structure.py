from fatesim.modifier import Modifier


class Structure():
    def __init__(self, in_settlement: bool, is_defensive: bool,
                 desc="", bonus_str="") -> None:
        # Structures can have modifiers they give for defense, else
        # modifiers they impart on units built there
        self.in_settlement = in_settlement
        self.is_defensive = is_defensive  # for modifiers against attacks
        self.desc = desc
        self.bonus_str = bonus_str
        self.modifier = Modifier.from_bonus_str(bonus_str)
