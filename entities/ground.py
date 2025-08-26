import pygame
from core.config import WIDTH, GROUND_Y

class Ground:
    def __init__(self):
        self.x = 0

    def update(self, speed, dt):
        self.x -= speed * dt
        if self.x <= -WIDTH:
            self.x += WIDTH

    def draw(self, surface):
        y = GROUND_Y - 14
        # Dibuja el suelo dos veces para cubrir el ancho completo y evitar "render lento"
        for offset in [0, WIDTH]:
            base_x = self.x + offset
            pygame.draw.line(surface, (120,120,120), (base_x, y), (base_x + WIDTH, y), 4)
            for dx in range(0, WIDTH, 24):
                pygame.draw.rect(surface, (80,80,80), (base_x+dx, y+8, 12, 3))
            for dx in range(0, WIDTH, 40):
                pygame.draw.circle(surface, (160,160,160), (int(base_x+dx+8), y+16), 3)
