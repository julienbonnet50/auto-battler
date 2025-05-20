import pygame


class Animation:
    def __init__(self, sprite, start_pos, end_pos, duration=500):
        self.sprite = sprite
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration  # in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.completed = False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed >= self.duration:
            self.completed = True
            return self.end_pos
        
        # Calculate position based on time
        progress = elapsed / self.duration
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        
        return (x, y)
    
    def draw(self, screen):
        if not self.completed:
            pos = self.update()
            screen.blit(self.sprite, pos)

