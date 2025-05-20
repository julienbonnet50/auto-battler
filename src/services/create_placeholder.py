# Function to create placeholder sprites (replace with actual sprites later)
import pygame

from src.conf.conf import BLACK


def create_placeholder_sprite(width, height, color, font, text=None):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    
    if text:
        font_render = font.render(text, True, BLACK)
        text_rect = font_render.get_rect(center=(width//2, height//2))
        surf.blit(font_render, text_rect)
        
    return surf