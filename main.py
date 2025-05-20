import pygame
import sys
import os

# Add the src directory to the path so we can import modules
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.conf.conf import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH
from src.model.BattleGame import BattleGame

# Initialize pygame
pygame.init()

# Run the game if this script is executed
if __name__ == "__main__":
    game = BattleGame()
    game.run()