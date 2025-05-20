import pygame
import sys
import random
import os
from typing import List

# Add the src directory to the path so we can import modules
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.conf.display import SCREEN
from src.conf.fonts import Fonts
from src.conf.conf import DARK_GRAY, GREEN, LIGHT_GRAY, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, YELLOW
from src.model import Button
from src.model.Animation import Animation
from src.model.TextAnimation import TextAnimation
from src.services.create_entities import create_entity_sprites
from src.model.Button import Button
from src.model.GameState import GameState
from src.model.Battle import Battle
from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.TargetType import TargetType
from src.model.Player import Player
from src.model.Enemy import Enemy
from src.abilities.abilities import create_sample_abilities


class BattleGame:
    def __init__(self):
        self.abilities_dict = create_sample_abilities()
        self.all_players = self.create_player_team()
        self.active_players = []  # Will be filled during team selection
        self.enemies = []
        self.current_wave = 0
        self.game_state = GameState.MAIN_MENU
        self.entity_sprites = create_entity_sprites(Fonts.FONT_MD)
        self.animations = []
        self.text_animations = []
        self.battle = None
        self.battle_log = []
        self.battle_log_index = 0
        self.battle_paused = False
        self.battle_speed = 1.0  # Normal speed
        self.selected_player_index = 0
        self.selected_ability_index = 0
        self.selected_target_index = 0
        self.turn_time = 0
        self.last_log_time = 0
        self.player_positions = []
        self.enemy_positions = []
        self.showing_ability_info = False
        self.ability_info_text = ""
        
        # UI elements
        self.start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "Start Game")
        self.next_wave_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "Next Wave")
        self.retry_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50, "Retry")
        self.quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 120, 200, 50, "Quit Game")
        
        # Player selection buttons
        self.player_select_buttons = []
        self.selected_team = []
        
        # Create player selection buttons
        y_pos = 200
        for i, player in enumerate(self.all_players):
            btn = Button(SCREEN_WIDTH//2 - 150, y_pos, 300, 40, player.name)
            self.player_select_buttons.append(btn)
            y_pos += 60
            
        # Continue button for team selection
        self.team_continue_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Continue")
        
        # Battle control buttons
        self.pause_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Pause")
        self.speed_button = Button(SCREEN_WIDTH - 120, 70, 100, 40, "Speed: 1x")
        
    def create_player_team(self) -> List[Player]:
        """Create the full roster of player characters"""
        players = []
        
        # Warrior
        warrior = Player(
            name="Warrior",
            max_hp=200,
            attack=35,
            defense=30,
            magic_attack=10,
            magic_defense=20,
            speed=35,
            abilities=self.abilities_dict["warrior"].copy()
        )
        players.append(warrior)
        
        # Mage
        mage = Player(
            name="Mage",
            max_hp=120,
            attack=15,
            defense=15,
            magic_attack=45,
            magic_defense=25,
            speed=40,
            abilities=self.abilities_dict["mage"].copy()
        )
        players.append(mage)
        
        # Healer
        healer = Player(
            name="Healer",
            max_hp=140,
            attack=15,
            defense=20,
            magic_attack=35,
            magic_defense=30,
            speed=30,
            abilities=self.abilities_dict["healer"].copy()
        )
        players.append(healer)
        
        # Rogue
        rogue = Player(
            name="Rogue",
            max_hp=150,
            attack=40,
            defense=15,
            magic_attack=15,
            magic_defense=15,
            speed=50,
            abilities=self.abilities_dict["rogue"].copy()
        )
        players.append(rogue)
        
        # Paladin (tank with some healing)
        paladin = Player(
            name="Paladin",
            max_hp=250,
            attack=25,
            defense=35,
            magic_attack=20,
            magic_defense=35,
            speed=25,
            abilities=[self.abilities_dict["warrior"][1], self.abilities_dict["healer"][0]]
        )
        players.append(paladin)
        
        # Battlemage (mage with some warrior abilities)
        battlemage = Player(
            name="Battlemage",
            max_hp=180,
            attack=25,
            defense=20,
            magic_attack=35,
            magic_defense=20,
            speed=35,
            abilities=[self.abilities_dict["mage"][0], self.abilities_dict["warrior"][0]]
        )
        players.append(battlemage)
        
        return players
        
    def create_enemy_wave(self, wave_number: int) -> List[Enemy]:
        """Create a wave of enemies (copied from your original code)"""
        enemies = []
        
        if wave_number == 1:
            # First wave: wolves
            for i in range(3):
                enemies.append(Enemy(
                    name=f"Wolf {i+1}",
                    max_hp=100 + random.randint(-10, 10),
                    attack=25 + random.randint(-5, 5),
                    defense=15 + random.randint(-3, 3),
                    magic_attack=5,
                    magic_defense=10 + random.randint(-3, 3),
                    speed=40 + random.randint(-5, 5),
                    abilities=self.abilities_dict["wolf"].copy(),
                    aggression=0.8
                ))
            
            # Add a stronger alpha wolf
            enemies.append(Enemy(
                name="Alpha Wolf",
                max_hp=150,
                attack=30,
                defense=20,
                magic_attack=5,
                magic_defense=15,
                speed=45,
                abilities=self.abilities_dict["wolf"].copy(),
                aggression=0.9
            ))
        
        elif wave_number == 2:
            # Second wave: spiders
            for i in range(4):
                enemies.append(Enemy(
                    name=f"Spider {i+1}",
                    max_hp=80 + random.randint(-10, 10),
                    attack=20 + random.randint(-3, 3),
                    defense=10 + random.randint(-2, 2),
                    magic_attack=15 + random.randint(-3, 3),
                    magic_defense=15 + random.randint(-3, 3),
                    speed=50 + random.randint(-5, 5),
                    abilities=self.abilities_dict["spider"].copy(),
                    aggression=0.7
                ))
            
            # Add a stronger spider queen
            enemies.append(Enemy(
                name="Spider Queen",
                max_hp=180,
                attack=25,
                defense=15,
                magic_attack=30,
                magic_defense=25,
                speed=40,
                abilities=self.abilities_dict["spider"].copy() + [self.abilities_dict["slime"][0]],
                aggression=0.8
            ))
        
        elif wave_number == 3:
            # Third wave: slimes
            for i in range(6):
                enemies.append(Enemy(
                    name=f"Slime {i+1}",
                    max_hp=60 + random.randint(-10, 10),
                    attack=15 + random.randint(-3, 3),
                    defense=25 + random.randint(-5, 5),
                    magic_attack=25 + random.randint(-5, 5),
                    magic_defense=25 + random.randint(-5, 5),
                    speed=30 + random.randint(-5, 5),
                    abilities=[self.abilities_dict["slime"][0]],
                    aggression=0.6
                ))
            
            # Add a stronger king slime
            enemies.append(Enemy(
                name="King Slime",
                max_hp=250,
                attack=20,
                defense=35,
                magic_attack=35,
                magic_defense=35,
                speed=25,
                abilities=self.abilities_dict["slime"] + [self.abilities_dict["mage"][0]],
                aggression=0.7
            ))
        
        else:
            # Harder waves: mixed enemies with increasing stats
            scale_factor = wave_number / 3
            
            # Add a mix of enemies
            enemy_types = ["wolf", "spider", "slime"]
            for i in range(4 + wave_number):
                enemy_type = random.choice(enemy_types)
                base_hp = {"wolf": 100, "spider": 80, "slime": 60}[enemy_type]
                base_atk = {"wolf": 25, "spider": 20, "slime": 15}[enemy_type]
                base_def = {"wolf": 15, "spider": 10, "slime": 25}[enemy_type]
                base_matk = {"wolf": 5, "spider": 15, "slime": 25}[enemy_type]
                base_mdef = {"wolf": 10, "spider": 15, "slime": 25}[enemy_type]
                base_spd = {"wolf": 40, "spider": 50, "slime": 30}[enemy_type]
                
                enemies.append(Enemy(
                    name=f"{enemy_type.capitalize()} {i+1}",
                    max_hp=int(base_hp * scale_factor) + random.randint(-10, 10),
                    attack=int(base_atk * scale_factor) + random.randint(-5, 5),
                    defense=int(base_def * scale_factor) + random.randint(-3, 3),
                    magic_attack=int(base_matk * scale_factor) + random.randint(-3, 3),
                    magic_defense=int(base_mdef * scale_factor) + random.randint(-3, 3),
                    speed=int(base_spd * scale_factor) + random.randint(-5, 5),
                    abilities=self.abilities_dict[enemy_type].copy(),
                    aggression=0.7 + (wave_number - 3) * 0.05  # Gets more aggressive with higher waves
                ))
            
            # Add a boss appropriate to the wave number
            boss_type = enemy_types[wave_number % 3]
            boss_name = {
                "wolf": f"Dire Wolf Alpha {wave_number}",
                "spider": f"Giant Spider Matriarch {wave_number}",
                "slime": f"Ancient Slime {wave_number}"
            }[boss_type]
            
            # Boss has significantly higher stats
            enemies.append(Enemy(
                name=boss_name,
                max_hp=int(300 * scale_factor),
                attack=int(40 * scale_factor),
                defense=int(30 * scale_factor),
                magic_attack=int(40 * scale_factor),
                magic_defense=int(30 * scale_factor),
                speed=int(45 * scale_factor),
                abilities=[],  # Will be filled below
                aggression=0.8
            ))
            
            # Give the boss abilities from all types
            boss = enemies[-1]
            for enemy_type in enemy_types:
                boss.abilities.extend(self.abilities_dict[enemy_type])
            
            # Add a unique boss ability
            boss_ability = Ability(
                name="Devastating Strike",
                cooldown=4,
                damage=int(50 * scale_factor),
                damage_type=DamageType.TRUE,
                target_type=TargetType.RANDOM,
                description="A powerful attack that bypasses defenses and hits multiple targets."
            )
            boss.abilities.append(boss_ability)
        
        return enemies
    
    def start_new_wave(self):
        """Start a new wave of enemies"""
        self.current_wave += 1
        self.enemies = self.create_enemy_wave(self.current_wave)
        
        # Reset battle variables
        self.battle = Battle(self.active_players, self.enemies, delay=0)
        self.battle_log = []
        self.battle_log_index = 0
        self.battle_paused = False
        
        # Calculate entity positions
        self.calculate_positions()
        
        # Change state to battle
        self.game_state = GameState.BATTLE
        
    def calculate_positions(self):
        """Calculate positions for players and enemies on the battlefield"""
        # Player positions (left side of screen)
        player_area_width = SCREEN_WIDTH // 3
        player_area_height = SCREEN_HEIGHT - 200  # Leave space for UI at bottom
        
        num_players = len(self.active_players)
        player_spacing = player_area_height // (num_players + 1)
        
        self.player_positions = []
        for i in range(num_players):
            pos_x = 150
            pos_y = 100 + player_spacing * (i + 1)
            self.player_positions.append((pos_x, pos_y))
        
        # Enemy positions (right side of screen)
        enemy_area_width = SCREEN_WIDTH // 3
        enemy_area_height = SCREEN_HEIGHT - 200
        
        num_enemies = len(self.enemies)
        enemy_spacing_y = enemy_area_height // min(5, num_enemies + 1)
        
        self.enemy_positions = []
        rows = max(1, (num_enemies + 4) // 5)  # Up to 5 enemies per row
        enemies_per_row = (num_enemies + rows - 1) // rows
        
        for i in range(num_enemies):
            row = i // enemies_per_row
            col = i % enemies_per_row
            
            pos_x = SCREEN_WIDTH - 200 - (col * 80)
            pos_y = 100 + (enemy_spacing_y * (row + 1))
            self.enemy_positions.append((pos_x, pos_y))
    
    def draw_entity(self, entity, position, is_selected=False, show_status=True):
        """Draw an entity on the screen"""
        # Get sprite based on entity name
        sprite_key = entity.name if entity.name in self.entity_sprites else entity.name.split()[0]
        sprite = self.entity_sprites.get(sprite_key, self.entity_sprites.get("Wolf"))  # Default to Wolf if not found
        
        # Draw selection indicator if selected
        if is_selected:
            # Draw yellow outline around selected entity
            outline_rect = pygame.Rect(position[0] - 5, position[1] - 5, 
                                      sprite.get_width() + 10, sprite.get_height() + 10)
            pygame.draw.rect(SCREEN, YELLOW, outline_rect, 3, border_radius=5)
        
        # Draw the entity sprite
        SCREEN.blit(sprite, position)
        
        if show_status:
            # Draw name above entity
            name_text = Fonts.FONT_SM.render(entity.name, True, WHITE)
            name_rect = name_text.get_rect(centerx=position[0] + sprite.get_width() // 2, 
                                          bottom=position[1] - 5)
            pygame.draw.rect(SCREEN, DARK_GRAY, name_rect.inflate(10, 5))
            SCREEN.blit(name_text, name_rect)
            
            # Draw health bar below entity
            health_pct = entity.current_hp / entity.max_hp
            health_bar_width = sprite.get_width()
            health_bar_height = 10
            
            # Background
            health_bg_rect = pygame.Rect(position[0], position[1] + sprite.get_height() + 5, 
                                         health_bar_width, health_bar_height)
            pygame.draw.rect(SCREEN, DARK_GRAY, health_bg_rect)
            
            # Actual health
            health_rect = pygame.Rect(position[0], position[1] + sprite.get_height() + 5, 
                                     int(health_bar_width * health_pct), health_bar_height)
            health_color = GREEN if health_pct > 0.6 else YELLOW if health_pct > 0.3 else RED
            pygame.draw.rect(SCREEN, health_color, health_rect)
            
            # Health text
            health_text = Fonts.FONT_SM.render(f"{entity.current_hp}/{entity.max_hp}", True, WHITE)
            health_text_rect = health_text.get_rect(centerx=position[0] + sprite.get_width() // 2, 
                                                  centery=position[1] + sprite.get_height() + 10)
            SCREEN.blit(health_text, health_text_rect)
            
            # Draw status effects
            if entity.status_effects:
                status_y = position[1] + sprite.get_height() + 20
                for effect in entity.status_effects:
                    # Show status effect icon/text
                    effect_text = Fonts.FONT_SM.render(effect.name, True, YELLOW)
                    effect_rect = effect_text.get_rect(centerx=position[0] + sprite.get_width() // 2, y=status_y)
                    SCREEN.blit(effect_text, effect_rect)
                    status_y += 15
    
    def draw_battle_scene(self):
        """Draw the battle scene with players and enemies"""
        # Draw background
        SCREEN.fill((50, 50, 80))  # Dark blue-gray background
        
        # Draw players
        for i, player in enumerate(self.active_players):
            if i < len(self.player_positions) and player.is_alive:
                is_selected = self.selected_player_index == i if self.battle_paused else False
                self.draw_entity(player, self.player_positions[i], is_selected)
        
        # Draw enemies
        for i, enemy in enumerate(self.enemies):
            if i < len(self.enemy_positions) and enemy.is_alive:
                is_selected = self.selected_target_index == i if self.battle_paused else False
                self.draw_entity(enemy, self.enemy_positions[i], is_selected)
        
        # Draw battle log
        self.draw_battle_log()
        
        # Draw UI elements for battle
        self.draw_battle_ui()
        
        # Draw animations
        for anim in self.animations[:]:
            anim.draw(SCREEN)
            if anim.completed:
                self.animations.remove(anim)
                
        # Draw text animations
        for text_anim in self.text_animations[:]:
            text_anim.draw(SCREEN)
            if text_anim.completed:
                self.text_animations.remove(text_anim)
        
        # Draw current turn info
        if self.battle and self.battle.current_entity:
            current_entity = self.battle.current_entity
            entity_type = "Player" if isinstance(current_entity, Player) else "Enemy"
            turn_text = f"Current Turn: {current_entity.name} ({entity_type})"
            
            turn_surf = Fonts.FONT_MD.render(turn_text, True, WHITE)
            turn_rect = turn_surf.get_rect(centerx=SCREEN_WIDTH//2, top=20)
            pygame.draw.rect(SCREEN, DARK_GRAY, turn_rect.inflate(20, 10))
            SCREEN.blit(turn_surf, turn_rect)
            
        # Draw pause indicator
        if self.battle_paused:
            pause_text = Fonts.FONT_LG.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 60))
            SCREEN.blit(pause_text, pause_rect)
            
            # Draw ability info if showing
            if self.showing_ability_info:
                self.draw_ability_info()
    
    def draw_battle_log(self):
        """Draw the battle log on screen"""
        log_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 200, 290, 190)
        pygame.draw.rect(SCREEN, (30, 30, 30), log_rect)
        pygame.draw.rect(SCREEN, LIGHT_GRAY, log_rect, 2)
        
        # Draw header
        header_text = Fonts.FONT_MD.render("Battle Log", True, WHITE)
        header_rect = header_text.get_rect(centerx=log_rect.centerx, top=log_rect.top + 5)
        SCREEN.blit(header_text, header_rect)
        
        # Draw log entries
        y_pos = log_rect.top + 35
        max_visible_entries = 7
        
        # Get visible log entries
        start_idx = max(0, len(self.battle_log) - max_visible_entries)
        visible_log = self.battle_log[start_idx:]
        # Draw log entries
        y_pos = log_rect.top + 35
        max_visible_entries = 7
        
        # Get visible log entries
        start_idx = max(0, len(self.battle_log) - max_visible_entries)
        visible_log = self.battle_log[start_idx:]
        
        for entry in visible_log:
            log_entry = Fonts.FONT_SM.render(entry, True, LIGHT_GRAY)
            SCREEN.blit(log_entry, (log_rect.left + 10, y_pos))
            y_pos += 24
    
    def draw_battle_ui(self):
        """Draw battle UI elements like buttons and ability list"""
        # Draw control buttons
        self.pause_button.text = "Resume" if self.battle_paused else "Pause"
        self.pause_button.draw(SCREEN)
        self.speed_button.draw(SCREEN)
        
        # If game is paused, show ability selection UI
        if self.battle_paused and self.active_players and self.selected_player_index < len(self.active_players):
            player = self.active_players[self.selected_player_index]
            
            # Draw ability list
            ability_box = pygame.Rect(10, SCREEN_HEIGHT - 200, 300, 190)
            pygame.draw.rect(SCREEN, (30, 30, 30), ability_box)
            pygame.draw.rect(SCREEN, LIGHT_GRAY, ability_box, 2)
            
            # Draw header
            header_text = Fonts.FONT_MD.render(f"{player.name}'s Abilities", True, WHITE)
            header_rect = header_text.get_rect(centerx=ability_box.centerx, top=ability_box.top + 5)
            SCREEN.blit(header_text, header_rect)
            
            # Draw abilities
            y_pos = ability_box.top + 35
            for i, ability in enumerate(player.abilities):
                # Highlight selected ability
                if i == self.selected_ability_index:
                    pygame.draw.rect(SCREEN, (60, 60, 100), pygame.Rect(ability_box.left + 5, y_pos - 3, 290, 26))
                
                cooldown_text = f"({ability.max_cooldown}/{ability.current_cooldown})" if ability.max_cooldown > 0 else ""
                ability_text = f"{ability.name} {cooldown_text}"
                
                # Gray out abilities on cooldown
                text_color = LIGHT_GRAY if ability.current_cooldown == 0 else (100, 100, 100)
                ability_label = Fonts.FONT_SM.render(ability_text, True, text_color)
                SCREEN.blit(ability_label, (ability_box.left + 10, y_pos))
                
                y_pos += 26
                
            # Draw info text
            info_text = Fonts.FONT_SM.render("Press SPACE to use ability", True, LIGHT_GRAY)
            SCREEN.blit(info_text, (ability_box.left + 10, ability_box.bottom - 30))
            info_text = Fonts.FONT_SM.render("Press I for ability info", True, LIGHT_GRAY)
            SCREEN.blit(info_text, (ability_box.left + 10, ability_box.bottom - 50))
    
    def draw_ability_info(self):
        """Draw detailed information about the selected ability"""
        if not self.active_players or self.selected_player_index >= len(self.active_players):
            return
            
        player = self.active_players[self.selected_player_index]
        if self.selected_ability_index >= len(player.abilities):
            return
            
        ability = player.abilities[self.selected_ability_index]
        
        # Draw info box
        info_box = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 150, 400, 300)
        pygame.draw.rect(SCREEN, (40, 40, 60), info_box)
        pygame.draw.rect(SCREEN, WHITE, info_box, 2)
        
        # Draw header
        header_text = Fonts.FONT_MD.render(ability.name, True, WHITE)
        header_rect = header_text.get_rect(centerx=info_box.centerx, top=info_box.top + 10)
        SCREEN.blit(header_text, header_rect)
        
        # Draw ability details
        y_pos = info_box.top + 50
        
        # Cooldown
        cooldown_text = Fonts.FONT_SM.render(f"Cooldown: {ability.current_cooldown} turns", True, LIGHT_GRAY)
        SCREEN.blit(cooldown_text, (info_box.left + 20, y_pos))
        y_pos += 30
        
        # Damage type
        damage_type_text = Fonts.FONT_SM.render(f"Damage Type: {ability.damage_type}", True, LIGHT_GRAY)
        SCREEN.blit(damage_type_text, (info_box.left + 20, y_pos))
        y_pos += 30
        
        # Target type
        target_text = Fonts.FONT_SM.render(f"Target: {ability.target_type}", True, LIGHT_GRAY)
        SCREEN.blit(target_text, (info_box.left + 20, y_pos))
        y_pos += 30
        
        # Damage amount
        damage_text = Fonts.FONT_SM.render(f"Damage: {ability.damage}", True, LIGHT_GRAY)
        SCREEN.blit(damage_text, (info_box.left + 20, y_pos))
        y_pos += 30
        
        # Description
        desc_lines = []
        words = ability.description.split()
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 50:
                current_line += " " + word if current_line else word
            else:
                desc_lines.append(current_line)
                current_line = word
                
        if current_line:
            desc_lines.append(current_line)
            
        for line in desc_lines:
            line_text = Fonts.FONT_SM.render(line, True, LIGHT_GRAY)
            SCREEN.blit(line_text, (info_box.left + 20, y_pos))
            y_pos += 25
        
        # Close instruction
        close_text = Fonts.FONT_SM.render("Press I to close", True, WHITE)
        close_rect = close_text.get_rect(centerx=info_box.centerx, bottom=info_box.bottom - 15)
        SCREEN.blit(close_text, close_rect)
    
    def draw_main_menu(self):
        """Draw the main menu screen"""
        # Fill background
        SCREEN.fill((30, 30, 50))
        
        # Draw title
        title_text = Fonts.FONT_XL.render("Turn-Based Battle Game", True, WHITE)
        title_rect = title_text.get_rect(centerx=SCREEN_WIDTH//2, y=100)
        SCREEN.blit(title_text, title_rect)
        
        # Draw start button
        self.start_button.update(pygame.mouse.get_pos())
        self.start_button.draw(SCREEN)
        
        # Draw version info
        version_text = Fonts.FONT_SM.render("Version 1.0", True, LIGHT_GRAY)
        version_rect = version_text.get_rect(right=SCREEN_WIDTH - 20, bottom=SCREEN_HEIGHT - 20)
        SCREEN.blit(version_text, version_rect)
    
    def draw_team_select(self):
        """Draw the team selection screen"""
        # Fill background
        SCREEN.fill((30, 30, 50))
        
        # Draw title
        title_text = Fonts.FONT_XL.render("Select Your Team", True, WHITE)
        title_rect = title_text.get_rect(centerx=SCREEN_WIDTH//2, y=80)
        SCREEN.blit(title_text, title_rect)
        
        # Draw instruction
        instruction_text = Fonts.FONT_MD.render("Choose 3-4 characters for your team", True, LIGHT_GRAY)
        instruction_rect = instruction_text.get_rect(centerx=SCREEN_WIDTH//2, y=130)
        SCREEN.blit(instruction_text, instruction_rect)
        
        # Draw selected count
        selected_text = Fonts.FONT_MD.render(f"Selected: {len(self.selected_team)}/4", True, WHITE)
        selected_rect = selected_text.get_rect(centerx=SCREEN_WIDTH//2, y=160)
        SCREEN.blit(selected_text, selected_rect)
        
        # Draw player buttons
        for i, btn in enumerate(self.player_select_buttons):
            # Update button color based on selection
            player_name = self.all_players[i].name
            if player_name in [p.name for p in self.selected_team]:
                btn.color = GREEN
            else:
                btn.color = LIGHT_GRAY
                
            # Update and draw button
            btn.update(pygame.mouse.get_pos())
            btn.draw(SCREEN)
            
            # Draw player stats
            player = self.all_players[i]
            stats_x = btn.rect.right + 20
            stats_y = btn.rect.top
            
            stats_text = [
                f"HP: {player.max_hp}",
                f"ATK: {player.attack}",
                f"DEF: {player.defense}",
                f"M.ATK: {player.magic_attack}",
                f"M.DEF: {player.magic_defense}",
                f"SPD: {player.speed}"
            ]
            
            for stat in stats_text:
                stat_surf = Fonts.FONT_SM.render(stat, True, LIGHT_GRAY)
                SCREEN.blit(stat_surf, (stats_x, stats_y))
                stats_y += 20
        
        # Draw continue button
        self.team_continue_button.disabled = len(self.selected_team) < 3
        self.team_continue_button.update(pygame.mouse.get_pos())
        self.team_continue_button.draw(SCREEN)
    
    def draw_wave_transition(self):
        """Draw the wave transition screen"""
        # Fill background
        SCREEN.fill((30, 30, 50))
        
        # Draw wave completed text
        if self.current_wave > 0:
            completed_text = Fonts.FONT_XL.render(f"Wave {self.current_wave} Completed!", True, WHITE)
            completed_rect = completed_text.get_rect(centerx=SCREEN_WIDTH//2, y=150)
            SCREEN.blit(completed_text, completed_rect)
        
        # Draw next wave text
        next_text = Fonts.FONT_LG.render(f"Prepare for Wave {self.current_wave + 1}", True, WHITE)
        next_rect = next_text.get_rect(centerx=SCREEN_WIDTH//2, y=250)
        SCREEN.blit(next_text, next_rect)
        
        # Display team status
        y_pos = 320
        for i, player in enumerate(self.active_players):
            # Draw player info
            status_text = f"{player.name}: {player.current_hp}/{player.max_hp} HP"
            status_surf = Fonts.FONT_MD.render(status_text, True, WHITE)
            status_rect = status_surf.get_rect(centerx=SCREEN_WIDTH//2, y=y_pos)
            SCREEN.blit(status_surf, status_rect)
            y_pos += 40
        
        # Draw next wave button
        self.next_wave_button.update(pygame.mouse.get_pos())
        self.next_wave_button.draw(SCREEN)
    
    def draw_game_over(self):
        """Draw the game over screen"""
        # Fill background
        SCREEN.fill((30, 30, 50))
        
        # Draw game over text
        game_over_text = Fonts.FONT_XL.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(centerx=SCREEN_WIDTH//2, y=150)
        SCREEN.blit(game_over_text, game_over_rect)
        
        # Draw waves survived text
        waves_text = Fonts.FONT_LG.render(f"You survived {self.current_wave} waves", True, LIGHT_GRAY)
        waves_rect = waves_text.get_rect(centerx=SCREEN_WIDTH//2, y=250)
        SCREEN.blit(waves_text, waves_rect)
        
        # Draw buttons
        self.retry_button.update(pygame.mouse.get_pos())
        self.retry_button.draw(SCREEN)
        
        self.quit_button.update(pygame.mouse.get_pos())
        self.quit_button.draw(SCREEN)
    
    def add_battle_log_entry(self, entry: str):
        """Add an entry to the battle log"""
        self.battle_log.append(entry)
        self.last_log_time = pygame.time.get_ticks()
    
    def handle_ability_use(self, entity, ability, targets):
        """Handle visual effects when an ability is used"""
        # Add battle log entry
        if len(targets) == 1:
            target_text = targets[0].name
        else:
            target_text = f"{len(targets)} targets"
            
        self.add_battle_log_entry(f"{entity.name} used {ability.name} on {target_text}")
        
        # Create animations based on ability type
        animation_sprite = None
        if ability.damage_type == DamageType.PHYSICAL:
            animation_sprite = self.entity_sprites["physical_attack"]
        elif ability.damage_type == DamageType.MAGICAL:
            animation_sprite = self.entity_sprites["magic_attack"]
        elif ability.damage_type == DamageType.HEALING:
            animation_sprite = self.entity_sprites["heal"]
        
        # Find entity position
        entity_pos = None
        for i, player in enumerate(self.active_players):
            if player == entity and i < len(self.player_positions):
                entity_pos = self.player_positions[i]
                break
                
        if not entity_pos:
            for i, enemy in enumerate(self.enemies):
                if enemy == entity and i < len(self.enemy_positions):
                    entity_pos = self.enemy_positions[i]
                    break
        
        # Create animations for each target
        if animation_sprite and entity_pos:
            for target in targets:
                # Find target position
                target_pos = None
                for i, player in enumerate(self.active_players):
                    if player == target and i < len(self.player_positions):
                        target_pos = self.player_positions[i]
                        break
                        
                if not target_pos:
                    for i, enemy in enumerate(self.enemies):
                        if enemy == target and i < len(self.enemy_positions):
                            target_pos = self.enemy_positions[i]
                            break
                
                if target_pos:
                    # Create animation
                    self.animations.append(Animation(
                        animation_sprite,
                        (entity_pos[0] + 30, entity_pos[1] + 30),
                        (target_pos[0] + 30, target_pos[1] + 30),
                        duration=500
                    ))
                    
                    # Create damage/heal text animation
                    if ability.damage > 0:
                        if ability.damage_type == DamageType.HEALING:
                            text = f"+{ability.damage}"
                            color = GREEN
                        else:
                            text = f"-{ability.damage}"
                            color = RED
                            
                        self.text_animations.append(TextAnimation(
                            text,
                            (target_pos[0] + 30, target_pos[1]),
                            color
                        ))
    
    def update_battle(self):
        """Update the battle state"""
        if self.battle_paused:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Check if it's time for the next turn
        if current_time - self.turn_time >= 1000 / self.battle_speed:
            # Process turn
            battle_event = self.battle.process_turn()
            
            if battle_event:
                entity = battle_event.entity
                ability = battle_event.ability
                targets = battle_event.targets
                
                # Handle ability use animations
                self.handle_ability_use(entity, ability, targets)
            
            # Check battle state
            if self.battle.is_battle_over():
                # Check if players won or lost
                if all(not player.is_alive for player in self.active_players):
                    # Game over - players lost
                    self.game_state = GameState.GAME_OVER
                else:
                    # Players won - go to next wave
                    self.game_state = GameState.WAVE_TRANSITION
            
            self.turn_time = current_time
    
    def process_events(self):
        """Process pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GameState.MAIN_MENU:
                    if self.start_button.is_clicked(mouse_pos, True):
                        self.game_state = GameState.TEAM_SELECT
                
                elif self.game_state == GameState.TEAM_SELECT:
                    # Handle player selection buttons
                    for i, btn in enumerate(self.player_select_buttons):
                        if btn.is_clicked(mouse_pos, True):
                            player_name = self.all_players[i].name
                            
                            # Check if already selected
                            selected_names = [p.name for p in self.selected_team]
                            
                            if player_name in selected_names:
                                # Remove from team
                                self.selected_team = [p for p in self.selected_team if p.name != player_name]
                            elif len(self.selected_team) < 4:
                                # Add to team
                                self.selected_team.append(self.all_players[i])
                    
                    # Handle continue button
                    if self.team_continue_button.is_clicked(mouse_pos, True) and len(self.selected_team) >= 3:
                        self.active_players = self.selected_team
                        self.game_state = GameState.WAVE_TRANSITION
                
                elif self.game_state == GameState.BATTLE:
                    # Handle battle UI
                    if self.pause_button.is_clicked(mouse_pos, True):
                        self.battle_paused = not self.battle_paused
                    
                    if self.speed_button.is_clicked(mouse_pos, True):
                        # Cycle through speeds: 1x, 2x, 3x
                        speeds = [1.0, 2.0, 3.0]
                        current_index = speeds.index(self.battle_speed)
                        next_index = (current_index + 1) % len(speeds)
                        self.battle_speed = speeds[next_index]
                        self.speed_button.text = f"Speed: {int(self.battle_speed)}x"
                
                elif self.game_state == GameState.WAVE_TRANSITION:
                    if self.next_wave_button.is_clicked(mouse_pos, True):
                        self.start_new_wave()
                
                elif self.game_state == GameState.GAME_OVER:
                    if self.retry_button.is_clicked(mouse_pos, True):
                        # Reset game state
                        self.active_players = []
                        self.enemies = []
                        self.current_wave = 0
                        self.battle_log = []
                        self.selected_team = []
                        self.game_state = GameState.TEAM_SELECT
                    
                    if self.quit_button.is_clicked(mouse_pos, True):
                        return False
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.BATTLE and self.battle_paused:
                    if event.key == pygame.K_UP:
                        self.selected_ability_index = max(0, self.selected_ability_index - 1)
                    
                    elif event.key == pygame.K_DOWN:
                        player = self.active_players[self.selected_player_index]
                        self.selected_ability_index = min(len(player.abilities) - 1, self.selected_ability_index + 1)
                    
                    elif event.key == pygame.K_LEFT:
                        self.selected_player_index = max(0, self.selected_player_index - 1)
                        self.selected_ability_index = 0
                    
                    elif event.key == pygame.K_RIGHT:
                        self.selected_player_index = min(len(self.active_players) - 1, self.selected_player_index + 1)
                        self.selected_ability_index = 0
                    
                    elif event.key == pygame.K_TAB:
                        self.selected_target_index = (self.selected_target_index + 1) % len(self.enemies)
                    
                    elif event.key == pygame.K_i:
                        # Toggle ability info
                        self.showing_ability_info = not self.showing_ability_info
                    
                    elif event.key == pygame.K_SPACE:
                        # Use selected ability on selected target
                        if (self.selected_player_index < len(self.active_players) and 
                            self.active_players[self.selected_player_index].is_alive):
                            
                            player = self.active_players[self.selected_player_index]
                            
                            if self.selected_ability_index < len(player.abilities):
                                ability = player.abilities[self.selected_ability_index]
                                
                                # Check if ability is on cooldown
                                if ability.current_cooldown == 0 and self.selected_target_index < len(self.enemies):
                                    target = self.enemies[self.selected_target_index]
                                    
                                    # Use ability
                                    targets = [target]
                                    self.handle_ability_use(player, ability, targets)
                                    
                                    # Resume battle
                                    self.battle_paused = False

        
        return True
    
    def run(self):
        """Main game loop"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # Process events
            running = self.process_events()
            
            # Update game state
            if self.game_state == GameState.BATTLE:
                self.update_battle()
            
            # Draw the screen based on game state
            if self.game_state == GameState.MAIN_MENU:
                self.draw_main_menu()
            elif self.game_state == GameState.TEAM_SELECT:
                self.draw_team_select()
            elif self.game_state == GameState.BATTLE:
                self.draw_battle_scene()
            elif self.game_state == GameState.WAVE_TRANSITION:
                self.draw_wave_transition()
            elif self.game_state == GameState.GAME_OVER:
                self.draw_game_over()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

