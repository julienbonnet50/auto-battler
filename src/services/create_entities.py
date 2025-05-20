from src.services.create_placeholder import create_placeholder_sprite


def create_entity_sprites(font):
    entity_sprites = {
        # Player sprites (60x80 pixels)
        "Warrior": create_placeholder_sprite(60, 80, (200, 100, 100), font, "Warrior"),
        "Mage": create_placeholder_sprite(60, 80, (100, 100, 200), font, "Mage"),
        "Healer": create_placeholder_sprite(60, 80, (100, 200, 100), font, "Healer"),
        "Rogue": create_placeholder_sprite(60, 80, (150, 150, 100), font, "Rogue"),
        "Paladin": create_placeholder_sprite(60, 80, (200, 200, 100), font, "Paladin"),
        "Battlemage": create_placeholder_sprite(60, 80, (150, 100, 200), font, "B.Mage"),
        
        # Enemy sprites (60x60 pixels)
        "Wolf": create_placeholder_sprite(60, 60, (130, 80, 80), "Wolf font,"),
        "Alpha Wolf": create_placeholder_sprite(70, 70, (180, 80, 80), font, "Alpha"),
        "Spider": create_placeholder_sprite(50, 50, (80, 80, 130), "Spider font,"),
        "Spider Queen": create_placeholder_sprite(70, 70, (100, 80, 180), font, "Queen"),
        "Slime": create_placeholder_sprite(55, 55, (80, 180, 180), "Slime font,"),
        "King Slime": create_placeholder_sprite(90, 90, (80, 180, 230), font, "King"),
        
        # Ability effect sprites
        "physical_attack": create_placeholder_sprite(30, 30, (255, 100, 100), font),
        "magic_attack": create_placeholder_sprite(30, 30, (100, 100, 255), font),
        "heal": create_placeholder_sprite(30, 30, (100, 255, 100), font),
    }
    
    # Add more specific enemy sprites
    for i in range(1, 7):
        entity_sprites[f"Wolf {i}"] = entity_sprites["Wolf"]
        entity_sprites[f"Spider {i}"] = entity_sprites["Spider"]
        entity_sprites[f"Slime {i}"] = entity_sprites["Slime"]
    
    # Add boss variants
    for i in range(4, 10):
        entity_sprites[f"Dire Wolf Alpha {i}"] = entity_sprites["Alpha Wolf"]
        entity_sprites[f"Giant Spider Matriarch {i}"] = entity_sprites["Spider Queen"]
        entity_sprites[f"Ancient Slime {i}"] = entity_sprites["King Slime"]
    
    return entity_sprites

