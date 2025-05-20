from typing import Dict
from src.model import DamageType, Entity


class StatusEffect:
    def __init__(self, name: str, duration: int, 
                 stats_modifier: Dict[str, float] = None,
                 dot_damage: int = 0, dot_type: DamageType = None,
                 heal_per_turn: int = 0,
                 can_act: bool = True):
        self.name = name
        self.duration = duration
        self.stats_modifier = stats_modifier or {}
        self.dot_damage = dot_damage  # Damage over time
        self.dot_type = dot_type
        self.heal_per_turn = heal_per_turn
        self.can_act = can_act  # If False, entity can't act

    def __str__(self):
        return f"{self.name} ({self.duration} turns left)"

    def apply_turn_effects(self, entity: Entity, battle):
        """Apply effects that happen at the start of an entity's turn"""
        messages = []
        
        # Apply DOT damage
        if self.dot_damage > 0 and self.dot_type:
            damage = self.dot_damage
            entity.take_damage(damage, self.dot_type)
            messages.append(f"{entity.name} takes {damage} {self.dot_type.value} damage from {self.name}")
        
        # Apply healing
        if self.heal_per_turn > 0:
            entity.heal(self.heal_per_turn)
            messages.append(f"{entity.name} heals for {self.heal_per_turn} from {self.name}")
        
        self.duration -= 1
        return messages

