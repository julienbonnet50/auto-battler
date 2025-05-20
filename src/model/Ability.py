
from src.model.DamageType import DamageType
from src.model.StatusEffect import StatusEffect
from src.model.TargetType import TargetType


class Ability:
    def __init__(self, name: str, cooldown: int, 
                 damage: int = 0, damage_type: DamageType = None,
                 healing: int = 0,
                 target_type: TargetType = TargetType.SINGLE,
                 status_effect: StatusEffect = None,
                 aoe_damage_reduction: float = 0.7,  # AOE abilities do less damage per target
                 description: str = ""):
        self.name = name
        self.max_cooldown = cooldown
        self.current_cooldown = 0
        self.damage = damage
        self.damage_type = damage_type
        self.healing = healing
        self.target_type = target_type
        self.status_effect = status_effect
        self.aoe_damage_reduction = aoe_damage_reduction
        self.description = description or "No description available."
    
    def is_ready(self) -> bool:
        return self.current_cooldown == 0
    
    def use(self) -> None:
        if self.max_cooldown > 0:
            self.current_cooldown = self.max_cooldown
    
    def reduce_cooldown(self) -> None:
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def __str__(self) -> str:
        status = "Ready" if self.is_ready() else f"Cooldown: {self.current_cooldown}"
        return f"{self.name} [{status}]"

