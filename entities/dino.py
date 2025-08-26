import pygame
from core.config import GROUND_Y
from core.assets import asset_manager

class Dino:
    def __init__(self):
        self.x = 60
        # Ajustar la posición Y para que el dinosaurio esté más cerca del suelo
        self.y = float(GROUND_Y - 45)
        self.vel_y = 0.0
        self.on_ground = True
        self.step_index = 0
        self.animation_speed = 0.2

    @property
    def rect(self):
        # Obtener el sprite actual para calcular el rectángulo
        if self.on_ground:
            current_sprite = asset_manager.get_dino_running(self.step_index // 5)
        else:
            current_sprite = asset_manager.dino_jumping
        
        return pygame.Rect(int(self.x), int(self.y), 
                          current_sprite.get_width(), current_sprite.get_height())

    def update(self, keys):
        # Actualizar animación
        if self.on_ground:
            self.step_index += 1
            if self.step_index >= 10:
                self.step_index = 0
        
        # Física del salto
        if not self.on_ground:
            self.vel_y += 0.6
            self.y += self.vel_y
            # Ajustar la posición de aterrizaje para que coincida con la posición inicial
            if self.y >= float(GROUND_Y - 45):
                self.y = float(GROUND_Y - 45)
                self.vel_y = 0.0
                self.on_ground = True
        
        # Controles
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -11.5
            self.on_ground = False

    def draw(self, surface):
        # Dibujar el sprite apropiado según el estado
        if self.on_ground:
            sprite = asset_manager.get_dino_running(self.step_index // 5)
        else:
            sprite = asset_manager.dino_jumping
        
        surface.blit(sprite, (int(self.x), int(self.y)))
