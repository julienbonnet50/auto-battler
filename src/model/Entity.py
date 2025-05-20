from typing import List, Tuple

from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.EntityType import EntityType
from src.model.StatusEffect import StatusEffect


class Entity:
    def __init__(self, name: str, entity_type: EntityType, 
                 max_hp: int, attack: int, defense: int, 
                 magic_attack: int, magic_defense: int, speed: int,
                 abilities: List[Ability] = None):
        self.name = name
        self.entity_type = entity_type
        
        # Base Stats
        self.max_hp = max_hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_magic_attack = magic_attack
        self.base_magic_defense = magic_defense
        self.base_speed = speed
        
        # Current Stats (can be modified by status effects)
        self.current_hp = max_hp
        
        # Initialize abilities
        self.abilities = abilities or []
        
        # Status effects
        self.status_effects: List[StatusEffect] = []
        
        # State
        self.is_alive = True
    
    @property
    def attack(self) -> int:
        """Get attack value after applying status effect modifiers"""
        modifier = 1.0
        for effect in self.status_effects:
            modifier += effect.stats_modifier.get("attack", 0)
        return max(int(self.base_attack * modifier), 0)
    
    @property
    def defense(self) -> int:
        """Get defense value after applying status effect modifiers"""
        modifier = 1.0
        for effect in self.status_effects:
            modifier += effect.stats_modifier.get("defense", 0)
        return max(int(self.base_defense * modifier), 0)
    
    @property
    def magic_attack(self) -> int:
        """Get magic attack value after applying status effect modifiers"""
        modifier = 1.0
        for effect in self.status_effects:
            modifier += effect.stats_modifier.get("magic_attack", 0)
        return max(int(self.base_magic_attack * modifier), 0)
    
    @property
    def magic_defense(self) -> int:
        """Get magic defense value after applying status effect modifiers"""
        modifier = 1.0
        for effect in self.status_effects:
            modifier += effect.stats_modifier.get("magic_defense", 0)
        return max(int(self.base_magic_defense * modifier), 0)
    
    @property
    def speed(self) -> int:
        """Get speed value after applying status effect modifiers"""
        modifier = 1.0
        for effect in self.status_effects:
            modifier += effect.stats_modifier.get("speed", 0)
        return max(int(self.base_speed * modifier), 0)
    
    def can_act(self) -> bool:
        """Check if entity can act based on status effects"""
        for effect in self.status_effects:
            if not effect.can_act:
                return False
        return True
    
    def heal(self, amount: int) -> int:
        """Heal entity and return the amount healed"""
        if not self.is_alive:
            return 0
        
        before = self.current_hp
        self.current_hp = min(self.current_hp + amount, self.max_hp)
        healed = self.current_hp - before
        return healed
    
    def take_damage(self, damage: int, damage_type: DamageType) -> int:
        """
        Entity takes damage and returns the actual damage dealt
        """
        if not self.is_alive:
            return 0
        
        # Calculate damage reduction based on defense
        if damage_type == DamageType.PHYSICAL:
            reduction = self.defense / (self.defense + 100)  # Defense formula
        elif damage_type == DamageType.MAGICAL:
            reduction = self.magic_defense / (self.magic_defense + 100)  # Magic defense formula
        else:  # TRUE damage
            reduction = 0
        
        actual_damage = max(int(damage * (1 - reduction)), 1)
        self.current_hp -= actual_damage
        
        # Check if entity died
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False
        
        return actual_damage
    
    def add_status_effect(self, effect: StatusEffect) -> bool:
        """Add a status effect, returns True if new, False if refreshed"""
        # Check if this type of effect already exists
        for i, existing in enumerate(self.status_effects):
            if existing.name == effect.name:
                # Refresh the duration
                self.status_effects[i] = effect
                return False
        
        # Add new effect
        self.status_effects.append(effect)
        return True
    
    def update_status_effects(self, battle) -> List[str]:
        """
        Update status effects at the beginning of entity's turn
        Returns a list of effect messages
        """
        messages = []
        
        # Apply effects and collect messages
        for effect in self.status_effects[:]:  # Create a copy for safe iteration
            effect_messages = effect.apply_turn_effects(self, battle)
            messages.extend(effect_messages)
            
            # Remove expired effects
            if effect.duration <= 0:
                self.status_effects.remove(effect)
                messages.append(f"{self.name} is no longer affected by {effect.name}")
        
        return messages
    
    def reduce_cooldowns(self) -> None:
        """Reduce cooldowns for all abilities"""
        for ability in self.abilities:
            ability.reduce_cooldown()
    
    def select_ability(self, battle) -> Tuple[Ability, List['Entity']]:
        """
        Select an ability and targets - to be overridden by subclasses
        Returns the selected ability and a list of targets
        """
        raise NotImplementedError("Subclasses must implement select_ability")
    
    def get_available_abilities(self) -> List[Ability]:
        """Get list of abilities that are ready to use"""
        return [ability for ability in self.abilities if ability.is_ready()]
    
    def get_stats_display(self) -> str:
        """Get a formatted string of the entity's stats"""
        status_effects_str = ", ".join(str(effect) for effect in self.status_effects) if self.status_effects else "None"
        
        return (
            f"{self.name} ({self.entity_type.value}):\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"ATK: {self.attack} | DEF: {self.defense}\n"
            f"MAG: {self.magic_attack} | MDEF: {self.magic_defense}\n"
            f"SPD: {self.speed}\n"
            f"Status: {status_effects_str}\n"
            f"Abilities: {', '.join(str(ability) for ability in self.abilities)}"
        )
