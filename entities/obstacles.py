import pygame
import random
from core.config import WIDTH, GROUND_Y

class Obstacle:
    def __init__(self):
        self.kind = random.choice(["cactus_small", "cactus_large"])
        # Ajusta la posición vertical para que los obstáculos estén ligeramente más arriba
        if self.kind == "cactus_small":
            self.rect = pygame.Rect(WIDTH + 20, GROUND_Y - 42 - 6, 18, 42)
        else:
            self.rect = pygame.Rect(WIDTH + 20, GROUND_Y - 64 - 6, 24, 64)

    def update(self, speed, dt):
        self.rect.x -= int(speed * dt)

    def draw(self, surface):
        color = (0, 120, 0)
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        if self.kind == "cactus_small":
            pygame.draw.rect(surface, color, (self.rect.x-6, self.rect.y+18, 6, 14), border_radius=2)
            pygame.draw.rect(surface, color, (self.rect.x+self.rect.w, self.rect.y+10, 6, 12), border_radius=2)
        else:
            pygame.draw.rect(surface, color, (self.rect.x-8, self.rect.y+24, 8, 18), border_radius=3)
            pygame.draw.rect(surface, color, (self.rect.x+self.rect.w, self.rect.y+16, 8, 20), border_radius=3)

class Spawner:
    def __init__(self, profile, rng):
        self.p = profile
        self.rng = rng
        self.time_to_next = 0

    def schedule_next(self, speed):
        base = max(self.p.spawn_base_ms - speed*15, int(self.p.spawn_base_ms*0.5))
        jitter = self.rng.randint(-self.p.spawn_jitter_ms, self.p.spawn_jitter_ms)
        self.time_to_next = int(base + jitter)

    def update(self, obstacles, speed, dt_ms, WIDTH, GROUND_Y):
        self.time_to_next -= dt_ms
        if self.time_to_next > 0: return
        if self.rng.random() < (1.0 - self.p.ptero_p):
            # cactus con probabilidad de stack configurable
            # ...
            pass
        else:
            # ptero con alturas de self.p.ptero_heights
            # ...
            pass
        self.schedule_next(speed)
