import pygame
import random
from core.config import WIDTH
from core.assets import asset_manager

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 200)
        self.y = random.randint(30, 120)
        self.speed = random.uniform(1.0, 2.0)
        self.sprite = asset_manager.get_cloud()

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x < -80:
            self.x = WIDTH + random.randint(0, 200)
            self.y = random.randint(30, 120)

    def draw(self, surface):
        surface.blit(self.sprite, (int(self.x), int(self.y)))
