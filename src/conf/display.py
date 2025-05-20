import pygame
from src.conf.conf import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize Pygame display
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Turn-Based Battle Game")
