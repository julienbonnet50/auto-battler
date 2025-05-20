
# Button class for UI elements
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf.fonts import Fonts
from src.conf.conf import BLACK, DARK_GRAY, LIGHT_GRAY, WHITE


class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY, hover_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.disabled = False
        
    def draw(self, screen):
        color = DARK_GRAY if self.disabled else (self.hover_color if self.is_hovered else self.color)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        text_color = LIGHT_GRAY if self.disabled else BLACK
        text_surf = Fonts.FONT_MD.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        if not self.disabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.is_hovered = False
            
    def is_clicked(self, mouse_pos, mouse_click):
        return not self.disabled and self.rect.collidepoint(mouse_pos) and mouse_click