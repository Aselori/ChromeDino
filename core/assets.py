import pygame
import os
import random

# Inicializar pygame
pygame.init()

# Constantes globales
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 800

# Cargar sprites del dinosaurio
RUNNING = [
    pygame.image.load(os.path.join("assets", "Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets", "Dino", "DinoRun2.png"))
]
JUMPING = pygame.image.load(os.path.join("assets", "Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets", "Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets", "Dino", "DinoDuck2.png"))
]

# Cargar sprites de cactus
SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets", "Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets", "Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets", "Cactus", "SmallCactus3.png"))
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets", "Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets", "Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets", "Cactus", "LargeCactus3.png"))
]

# Cargar sprites de pájaros
BIRD = [
    pygame.image.load(os.path.join("assets", "Aves", "Bird1.png")),
    pygame.image.load(os.path.join("assets", "Aves", "Bird2.png"))
]

# Cargar otros elementos
CLOUD = pygame.image.load(os.path.join("assets", "Otros", "Cloud.png"))
BG = pygame.image.load(os.path.join("assets", "Otros", "Track.png"))

class AssetManager:
    """Gestor centralizado de assets del juego"""
    
    def __init__(self):
        self.dino_running = RUNNING
        self.dino_jumping = JUMPING
        self.dino_ducking = DUCKING
        self.small_cactus = SMALL_CACTUS
        self.large_cactus = LARGE_CACTUS
        self.bird = BIRD
        self.cloud = CLOUD
        self.background = BG
        
        # Escalar sprites si es necesario para el tamaño del juego
        self.scale_assets()
    
    def scale_assets(self):
        """Escala los assets al tamaño apropiado del juego"""
        scale_factor = 0.5  # Ajustar según el tamaño deseado
        
        # Escalar dinosaurio
        self.dino_running = [pygame.transform.scale(img, 
            (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) 
            for img in self.dino_running]
        self.dino_jumping = pygame.transform.scale(self.dino_jumping,
            (int(self.dino_jumping.get_width() * scale_factor), 
             int(self.dino_jumping.get_height() * scale_factor)))
        self.dino_ducking = [pygame.transform.scale(img,
            (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
            for img in self.dino_ducking]
        
        # Escalar cactus
        self.small_cactus = [pygame.transform.scale(img,
            (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
            for img in self.small_cactus]
        self.large_cactus = [pygame.transform.scale(img,
            (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
            for img in self.large_cactus]
        
        # Escalar pájaros
        self.bird = [pygame.transform.scale(img,
            (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
            for img in self.bird]
        
        # Escalar nube
        self.cloud = pygame.transform.scale(self.cloud,
            (int(self.cloud.get_width() * scale_factor), 
             int(self.cloud.get_height() * scale_factor)))
        
        # Escalar fondo
        self.background = pygame.transform.scale(self.background,
            (SCREEN_WIDTH, int(self.background.get_height() * scale_factor)))
    
    def get_dino_running(self, frame):
        """Obtiene el sprite de correr del dinosaurio según el frame"""
        return self.dino_running[frame % len(self.dino_running)]
    
    def get_dino_ducking(self, frame):
        """Obtiene el sprite de agacharse del dinosaurio según el frame"""
        return self.dino_ducking[frame % len(self.dino_ducking)]
    
    def get_small_cactus(self, index=None):
        """Obtiene un cactus pequeño aleatorio o específico"""
        if index is None:
            return random.choice(self.small_cactus)
        return self.small_cactus[index % len(self.small_cactus)]
    
    def get_large_cactus(self, index=None):
        """Obtiene un cactus grande aleatorio o específico"""
        if index is None:
            return random.choice(self.large_cactus)
        return self.large_cactus[index % len(self.large_cactus)]
    
    def get_bird(self, frame):
        """Obtiene el sprite del pájaro según el frame"""
        return self.bird[frame % len(self.bird)]
    
    def get_cloud(self):
        """Obtiene el sprite de la nube"""
        return self.cloud
    
    def get_background(self):
        """Obtiene el sprite del fondo"""
        return self.background

# Instancia global del gestor de assets
asset_manager = AssetManager()
