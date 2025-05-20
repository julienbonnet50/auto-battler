import random
from typing import List, Tuple
from src.model.EntityType import EntityType
from src.model.Entity import Entity
from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.TargetType import TargetType

class Player(Entity):
    def __init__(self, 
                name: str,
                max_hp: int,
                attack: int,
                defense: int, 
                magic_attack: int,
                magic_defense: int,
                speed: int,
                abilities: List[Ability] = None
            ):
        super().__init__(name, EntityType.PLAYER, max_hp, attack, defense, 
                         magic_attack, magic_defense, speed, abilities)
        
    def select_ability(self, battle) -> Tuple[Ability, List[Entity]]:
        """
        In a real game, this would get player input.
        For this auto-battler, we'll implement a simple AI.
        """
        available_abilities = self.get_available_abilities()
        
        if not available_abilities:
            # Default attack if no abilities are available
            default_attack = Ability("Basic Attack", 0, 
                                    damage=self.attack // 2 + 10,
                                    damage_type=DamageType.PHYSICAL, 
                                    target_type=TargetType.SINGLE)
            ability = default_attack
        else:
            # Simple logic: prefer healing when allies are low, otherwise attack
            healing_threshold = 0.5  # 50% HP
            
            # Find low HP allies
            low_hp_allies = [ally for ally in battle.get_living_entities(EntityType.PLAYER) 
                            if ally.current_hp / ally.max_hp < healing_threshold]
            
            # Look for healing abilities when allies are low on health
            if low_hp_allies:
                healing_abilities = [a for a in available_abilities 
                                    if a.healing > 0 and a.target_type in 
                                    [TargetType.SINGLE, TargetType.ALLIES, TargetType.ALL]]
                if healing_abilities:
                    ability = random.choice(healing_abilities)
                else:
                    ability = random.choice(available_abilities)
            else:
                # Prioritize damage abilities
                damage_abilities = [a for a in available_abilities if a.damage > 0]
                if damage_abilities:
                    ability = random.choice(damage_abilities)
                else:
                    ability = random.choice(available_abilities)
        
        # Select appropriate targets based on ability type
        targets = battle.select_targets(self, ability)
        
        return ability, targets

