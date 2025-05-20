import time
from typing import List, Optional, Tuple
import random

from src.model.EntityType import EntityType
from src.model.Entity import Entity
from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.StatusEffect import StatusEffect
from src.model.TargetType import TargetType
from src.model.Player import Player
from src.model.Enemy import Enemy   

class Battle:
    def __init__(self, players: List[Player], enemies: List[Enemy], delay: float = 0.5):
        self.players = players
        self.enemies = enemies
        self.turn_order: List[Entity] = []
        self.current_turn_index = 0
        self.round_number = 0
        self.battle_log: List[str] = []
        self.delay = delay  # Delay between turns (for display purposes)
        self.battle_ended = False
    
    def start_battle(self) -> None:
        """Initialize and start the battle"""
        self.calculate_turn_order()
        self.battle_log.append("=== Battle Start ===")
        self.log_turn_order()
        
        while not self.is_battle_over():
            self.process_turn()
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
            
            # Check if we've completed a round
            if self.current_turn_index == 0:
                self.round_number += 1
                self.battle_log.append(f"\n=== Round {self.round_number} ===")
                self.calculate_turn_order()
                self.log_turn_order()
        
        self.end_battle()

    @property
    def current_entity(self) -> Optional[Entity]:
        if not self.turn_order:
            return None
        return self.turn_order[self.current_turn_index]

    
    def calculate_turn_order(self) -> None:
        """Calculate the turn order based on speed"""
        all_entities = []
        
        # Only include living entities
        for entity in self.players + self.enemies:
            if entity.is_alive:
                all_entities.append(entity)
        
        # Sort by speed (higher speed goes first)
        self.turn_order = sorted(all_entities, key=lambda e: e.speed, reverse=True)
    
    def process_turn(self) -> None:
        """Process a single turn"""
        if self.current_turn_index >= len(self.turn_order):
            return
        
        entity = self.turn_order[self.current_turn_index]
        
        # Skip if entity is no longer alive (might have died during the round)
        if not entity.is_alive:
            return
        
        # Update status effects
        status_messages = entity.update_status_effects(self)
        for msg in status_messages:
            self.battle_log.append(msg)
        
        # Check if entity can act
        if not entity.can_act():
            self.battle_log.append(f"{entity.name} is unable to act!")
            return
        
        # Reduce cooldowns
        entity.reduce_cooldowns()
        
        # Select ability and targets
        ability, targets = entity.select_ability(self)
        
        # Execute ability
        self.execute_ability(entity, ability, targets)
        
        # Add some delay for better readability when displaying
        if self.delay > 0:
            time.sleep(self.delay)
    
    def execute_ability(self, caster: Entity, ability: Ability, targets: List[Entity]) -> None:
        """Execute an ability on targets"""
        if not targets:
            self.battle_log.append(f"{caster.name} uses {ability.name} but there are no valid targets!")
            return
        
        # Set ability on cooldown
        ability.use()
        
        # Log ability use
        target_names = ", ".join([t.name for t in targets])
        self.battle_log.append(f"{caster.name} uses {ability.name} on {target_names}!")
        
        # Apply damage
        if ability.damage > 0:
            is_aoe = len(targets) > 1 and ability.target_type in [TargetType.ALL, TargetType.ALLIES, TargetType.RANDOM]
            
            for target in targets:
                # Calculate damage
                base_damage = ability.damage
                
                # For AOE attacks, reduce damage per target
                if is_aoe:
                    base_damage = int(base_damage * ability.aoe_damage_reduction)
                
                # Apply stat modifiers
                if ability.damage_type == DamageType.PHYSICAL:
                    actual_damage = base_damage + (caster.attack // 3)
                elif ability.damage_type == DamageType.MAGICAL:
                    actual_damage = base_damage + (caster.magic_attack // 3)
                else:  # TRUE damage
                    actual_damage = base_damage
                
                # Apply damage to target
                damage_dealt = target.take_damage(actual_damage, ability.damage_type)
                self.battle_log.append(f"{target.name} takes {damage_dealt} {ability.damage_type.value} damage!")
                
                # Check if target died
                if not target.is_alive:
                    self.battle_log.append(f"{target.name} has been defeated!")
        
        # Apply healing
        if ability.healing > 0:
            for target in targets:
                if target.is_alive:  # Only heal living targets
                    healing_amount = ability.healing
                    # Boost healing based on magic attack for healers
                    if caster.magic_attack > caster.attack:
                        healing_amount += caster.magic_attack // 5
                    
                    amount_healed = target.heal(healing_amount)
                    self.battle_log.append(f"{target.name} is healed for {amount_healed} HP!")
        
        # Apply status effects
        if ability.status_effect:
            for target in targets:
                if target.is_alive:  # Only apply effects to living targets
                    # Create a new instance of the status effect for each target
                    new_effect = StatusEffect(
                        ability.status_effect.name,
                        ability.status_effect.duration,
                        ability.status_effect.stats_modifier,
                        ability.status_effect.dot_damage,
                        ability.status_effect.dot_type,
                        ability.status_effect.heal_per_turn,
                        ability.status_effect.can_act
                    )
                    
                    is_new = target.add_status_effect(new_effect)
                    if is_new:
                        self.battle_log.append(f"{target.name} is affected by {new_effect.name}!")
                    else:
                        self.battle_log.append(f"{target.name}'s {new_effect.name} is refreshed!")
    
    def select_targets(self, caster: Entity, ability: Ability) -> List[Entity]:
        """Select targets for an ability based on target type"""
        enemies = self.get_living_entities(EntityType.ENEMY if caster.entity_type == EntityType.PLAYER else EntityType.PLAYER)
        allies = self.get_living_entities(caster.entity_type)
        
        if ability.target_type == TargetType.SINGLE:
            # Target a single enemy
            if enemies:
                return [random.choice(enemies)]
            return []
            
        elif ability.target_type == TargetType.ALL:
            # Target all enemies
            return enemies
            
        elif ability.target_type == TargetType.SELF:
            # Target self
            return [caster] if caster.is_alive else []
            
        elif ability.target_type == TargetType.ALLIES:
            # Target all allies including self
            return allies
            
        elif ability.target_type == TargetType.RANDOM:
            # Target random enemies (1-3)
            if enemies:
                num_targets = min(random.randint(1, 3), len(enemies))
                return random.sample(enemies, num_targets)
            return []
            
        elif ability.target_type == TargetType.LOWEST_HP_ALLY:
            # Target ally with lowest HP
            if allies:
                return [min(allies, key=lambda e: e.current_hp / e.max_hp)]
            return []
            
        elif ability.target_type == TargetType.LOWEST_HP_ENEMY:
            # Target enemy with lowest HP
            if enemies:
                return [min(enemies, key=lambda e: e.current_hp / e.max_hp)]
            return []
            
        return []
    
    def get_living_entities(self, entity_type: EntityType) -> List[Entity]:
        """Get all living entities of a specific type"""
        if entity_type == EntityType.PLAYER:
            return [p for p in self.players if p.is_alive]
        else:
            return [e for e in self.enemies if e.is_alive]
    
    def is_battle_over(self) -> bool:
        """Check if the battle is over"""
        if self.battle_ended:
            return True
            
        players_alive = any(p.is_alive for p in self.players)
        enemies_alive = any(e.is_alive for e in self.enemies)
        
        return not (players_alive and enemies_alive)
    
    def get_winner(self) -> Optional[EntityType]:
        """Returns the type of the winning side, or None if battle isn't over"""
        if not self.is_battle_over():
            return None
            
        players_alive = any(p.is_alive for p in self.players)
        
        if players_alive:
            return EntityType.PLAYER
        else:
            return EntityType.ENEMY
    
    def end_battle(self) -> None:
        """End the battle and announce the winner"""
        self.battle_ended = True
        winner = self.get_winner()
        
        self.battle_log.append("\n=== Battle End ===")
        if winner == EntityType.PLAYER:
            self.battle_log.append("Players are victorious!")
        else:
            self.battle_log.append("Enemies are victorious!")
    
    def log_turn_order(self) -> None:
        """Log the turn order for the current round"""
        order_str = " → ".join([entity.name for entity in self.turn_order])
        self.battle_log.append(f"Turn order: {order_str}\n")
    
    def display_battle_state(self) -> None:
        """Display the current state of the battle"""
        print("\n=== Battle State ===")
        print("PLAYERS:")
        for player in self.players:
            status = "ALIVE" if player.is_alive else "DEFEATED"
            print(f"{player.name}: HP {player.current_hp}/{player.max_hp} [{status}]")
        
        print("\nENEMIES:")
        for enemy in self.enemies:
            status = "ALIVE" if enemy.is_alive else "DEFEATED"
            print(f"{enemy.name}: HP {enemy.current_hp}/{enemy.max_hp} [{status}]")
        
        print("\nNext up:", self.turn_order[self.current_turn_index].name if self.turn_order else "None")
        print("====================\n")
    
    def print_battle_log(self) -> None:
        """Print the battle log"""
        for entry in self.battle_log:
            print(entry)

