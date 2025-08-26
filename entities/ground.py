import pygame
import random
from core.config import WIDTH, GROUND_Y
from core.assets import asset_manager

class Ground:
    def __init__(self):
        self.x = 0
        self.background = asset_manager.get_background()

    def update(self, speed, dt):
        self.x -= speed * dt
        if self.x <= -WIDTH:
            self.x += WIDTH

    def draw(self, surface):
        # Dibuja el fondo dos veces para cubrir el ancho completo
        for offset in [0, WIDTH]:
            base_x = self.x + offset
            surface.blit(self.background, (base_x, GROUND_Y - self.background.get_height()))
