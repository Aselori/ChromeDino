import pygame
import random
from core.config import WIDTH, GROUND_Y
from core.assets import asset_manager

class Obstacle:
    def __init__(self):
        self.kind = random.choice(["cactus_small", "cactus_large"])
        # Obtener sprite del asset manager
        if self.kind == "cactus_small":
            self.sprite = asset_manager.get_small_cactus()
            self.rect = pygame.Rect(WIDTH + 20, GROUND_Y - self.sprite.get_height() - 6, 
                                  self.sprite.get_width(), self.sprite.get_height())
        else:  # cactus_large
            self.sprite = asset_manager.get_large_cactus()
            self.rect = pygame.Rect(WIDTH + 20, GROUND_Y - self.sprite.get_height() - 6, 
                                  self.sprite.get_width(), self.sprite.get_height())

    def update(self, speed, dt):
        self.rect.x -= int(speed * dt)

    def draw(self, surface):
        surface.blit(self.sprite, (self.rect.x, self.rect.y))

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
