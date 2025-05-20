
from src.model.Ability import Ability
from src.model.DamageType import DamageType
from src.model.StatusEffect import StatusEffect
from src.model.TargetType import TargetType

# Create a set of sample abilities
def create_sample_abilities():
    # Player abilities
    fireball = Ability(
        name="Fireball",
        cooldown=3,
        damage=40,
        damage_type=DamageType.MAGICAL,
        target_type=TargetType.SINGLE,
        description="Launch a ball of fire at a single enemy."
    )
    
    heal = Ability(
        name="Healing Light",
        cooldown=4,
        healing=50,
        target_type=TargetType.LOWEST_HP_ALLY,
        description="Heal the ally with the lowest health."
    )
    
    group_heal = Ability(
        name="Divine Blessing",
        cooldown=6,
        healing=30,
        target_type=TargetType.ALLIES,
        description="Heal all allies for a moderate amount."
    )
    
    slash = Ability(
        name="Power Slash",
        cooldown=2,
        damage=35,
        damage_type=DamageType.PHYSICAL,
        target_type=TargetType.SINGLE,
        description="A powerful slash against a single enemy."
    )
    
    flame_nova = Ability(
        name="Flame Nova",
        cooldown=5,
        damage=30,
        damage_type=DamageType.MAGICAL,
        target_type=TargetType.ALL,
        description="Unleash a nova of flames that hits all enemies."
    )
    
    taunt = Ability(
        name="Taunt",
        cooldown=4,
        target_type=TargetType.SELF,
        status_effect=StatusEffect(
            name="Defense Up",
            duration=3,
            stats_modifier={"defense": 0.5}  # +50% defense
        ),
        description="Increase your defense for 3 turns."
    )
    
    poison_strike = Ability(
        name="Poison Strike",
        cooldown=4,
        damage=20,
        damage_type=DamageType.PHYSICAL,
        target_type=TargetType.SINGLE,
        status_effect=StatusEffect(
            name="Poison",
            duration=3,
            dot_damage=10,
            dot_type=DamageType.MAGICAL
        ),
        description="Strike an enemy and poison them for 3 turns."
    )
    
    stun = Ability(
        name="Concussive Blow",
        cooldown=5,
        damage=25,
        damage_type=DamageType.PHYSICAL,
        target_type=TargetType.SINGLE,
        status_effect=StatusEffect(
            name="Stunned",
            duration=2,
            can_act=False
        ),
        description="Strike an enemy with a blow that stuns them for 2 turns."
    )
    
    # Enemy abilities
    bite = Ability(
        name="Bite",
        cooldown=2,
        damage=25,
        damage_type=DamageType.PHYSICAL,
        target_type=TargetType.SINGLE,
        description="A vicious bite attack."
    )
    
    howl = Ability(
        name="Howl",
        cooldown=5,
        target_type=TargetType.ALLIES,
        status_effect=StatusEffect(
            name="Enraged",
            duration=3,
            stats_modifier={"attack": 0.3}  # +30% attack
        ),
        description="A howl that increases attack for all allies."
    )
    
    web = Ability(
        name="Sticky Web",
        cooldown=4,
        target_type=TargetType.RANDOM,
        status_effect=StatusEffect(
            name="Slowed",
            duration=2,
            stats_modifier={"speed": -0.3}  # -30% speed
        ),
        description="Cast a sticky web that slows random enemies."
    )
    
    acid_spray = Ability(
        name="Acid Spray",
        cooldown=4,
        damage=15,
        damage_type=DamageType.MAGICAL,
        target_type=TargetType.ALL,
        status_effect=StatusEffect(
            name="Acid Burn",
            duration=2,
            stats_modifier={"defense": -0.2},  # -20% defense
            dot_damage=5,
            dot_type=DamageType.MAGICAL
        ),
        description="Spray acid on all enemies, reducing defense and causing damage over time."
    )
    
    # Return dictionaries of abilities by role
    return {
        "warrior": [slash, taunt],
        "mage": [fireball, flame_nova],
        "healer": [heal, group_heal],
        "rogue": [poison_strike, stun],
        "wolf": [bite, howl],
        "spider": [web, poison_strike],
        "slime": [acid_spray]
    }
