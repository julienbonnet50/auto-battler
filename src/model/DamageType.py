from enum import Enum

class DamageType(Enum):
    PHYSICAL = "physical"
    MAGICAL = "magical"
    HEALING = "healing"  # Healing type
    DOT = "dot"  # Damage over time
    TRUE = "true"  # Damage that ignores defense