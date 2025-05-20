from enum import Enum

class TargetType(Enum):
    SINGLE = "single"
    ALL = "all"
    SELF = "self"
    ALLIES = "allies"
    RANDOM = "random"
    LOWEST_HP_ALLY = "lowest_hp_ally"
    LOWEST_HP_ENEMY = "lowest_hp_enemy"  # <- Fixed missing quote here
