import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.conf.display import SCREEN
from src.conf.fonts import Fonts


class TextAnimation:
    def __init__(self, text, position, color, duration=1000, move_distance=50):
        self.font = Fonts.FONT_MD
        self.text = text
        self.position = position
        self.color = color
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.completed = False
        self.move_distance = move_distance
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        if elapsed >= self.duration:
            self.completed = True
            return self.position, 0  # ✅ Always return (pos, alpha)

        # Move text upward
        progress = elapsed / self.duration
        alpha = int(255 * (1 - progress))
        y_offset = self.move_distance * progress

        return (self.position[0], self.position[1] - y_offset), alpha

    
    def draw(self, screen):
        if self.completed:
            raise Exception("Animation is completed, cannot draw.")

        pos, alpha = self.update()

        # Ensure pos is a tuple of integers
        pos = (int(pos[0]), int(pos[1]))

        # Create text surface with alpha
        text_surf = self.font.render(self.text, True, self.color)
        alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, alpha))
        text_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(text_surf, pos)
        pygame.display.flip()


