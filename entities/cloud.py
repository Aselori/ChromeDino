import pygame
import random
from core.config import WIDTH

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 200)
        self.y = random.randint(30, 120)
        self.speed = random.uniform(1.0, 2.0)
        self.size = random.randint(18, 32)
        self.color_main = (
            random.randint(210, 240),
            random.randint(210, 240),
            random.randint(210, 240)
        )
        self.color_shadow = (
            max(self.color_main[0] - 30, 180),
            max(self.color_main[1] - 30, 180),
            max(self.color_main[2] - 30, 180)
        )

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x < -80:
            self.x = WIDTH + random.randint(0, 200)
            self.y = random.randint(30, 120)
            self.size = random.randint(18, 32)
            self.color_main = (
                random.randint(210, 240),
                random.randint(210, 240),
                random.randint(210, 240)
            )
            self.color_shadow = (
                max(self.color_main[0] - 30, 180),
                max(self.color_main[1] - 30, 180),
                max(self.color_main[2] - 30, 180)
            )

    def draw(self, surface):
        base = (int(self.x), int(self.y))
        # Sombra inferior
        pygame.draw.ellipse(surface, self.color_shadow, (base[0]-self.size//2, base[1], self.size+8, self.size//2+4))
        # Cuerpo principal
        pygame.draw.ellipse(surface, self.color_main, (base[0]-self.size//2, base[1]-self.size//3, self.size, self.size//2))
        # Bultos adicionales para forma orgánica
        pygame.draw.circle(surface, self.color_main, (base[0]+self.size//3, base[1]-self.size//4), self.size//4)
        pygame.draw.circle(surface, self.color_main, (base[0]-self.size//3, base[1]-self.size//5), self.size//5)
        pygame.draw.circle(surface, self.color_main, (base[0]+self.size//5, base[1]), self.size//6)
        pygame.draw.circle(surface, self.color_main, (base[0]-self.size//4, base[1]+self.size//8), self.size//7)
