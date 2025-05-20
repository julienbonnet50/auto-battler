from typing import List, Tuple
import random

from src.model.EntityType import EntityType
from src.model.Entity import Entity
from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.TargetType import TargetType



class Enemy(Entity):
    def __init__(self, name: str, max_hp: int, attack: int, defense: int, 
                 magic_attack: int, magic_defense: int, speed: int,
                 abilities: List[Ability] = None, aggression: float = 0.7):
        super().__init__(name, EntityType.ENEMY, max_hp, attack, defense, 
                         magic_attack, magic_defense, speed, abilities)
        self.aggression = aggression  # 0.0 to 1.0, higher means more aggressive
    
    def select_ability(self, battle) -> Tuple[Ability, List[Entity]]:
        """
        Enemy AI logic for selecting abilities and targets
        """
        available_abilities = self.get_available_abilities()
        
        if not available_abilities:
            # Default attack if no abilities are available
            default_attack = Ability("Basic Attack", 0, 
                                    damage=self.attack // 2 + 5,
                                    damage_type=DamageType.PHYSICAL, 
                                    target_type=TargetType.SINGLE)
            ability = default_attack
        else:
            # Random choice but weighted by aggression
            if random.random() < self.aggression:
                # More aggressive: prefer damage abilities
                damage_abilities = [a for a in available_abilities if a.damage > 0]
                if damage_abilities:
                    ability = random.choice(damage_abilities)
                else:
                    ability = random.choice(available_abilities)
            else:
                # Less aggressive: might choose support abilities
                ability = random.choice(available_abilities)
        
        # Select appropriate targets based on ability type
        targets = battle.select_targets(self, ability)
        
        return ability, targets

