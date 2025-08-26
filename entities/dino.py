import pygame
from core.config import GROUND_Y

class Dino:
    def __init__(self):
        self.x = 60
        self.width = 48
        self.height = 48
        self.y = float(GROUND_Y - 80)
        self.vel_y = 0.0
        self.on_ground = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, keys):
        if not self.on_ground:
            self.vel_y += 0.6
            self.y += self.vel_y
            if self.y >= float(GROUND_Y - 80):
                self.y = float(GROUND_Y - 80)
                self.vel_y = 0.0
                self.on_ground = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -11.5
            self.on_ground = False

    def draw(self, surface):
        # Sprite pixel-art del dino clásico
        # Mapa de píxeles (1 = gris, 0 = transparente, 2 = blanco para el ojo)
        dino_pixels = [
    "0000000000000000000001111111111110000000",
    "0000000000000000000011111111111111100000",
    "0000000000000000000011100111111111100000",
    "0000000000000000000011101111111111100000",
    "0000000000000000000011111111111111100000",
    "0000000000000000000011111111111111100000",
    "0000000000000000000011111111111111100000",
    "0000000000000000000011111111111111100000",
    "0000000000000000000011111110000000000000",
    "0000000000000000000011111111000000000000",
    "0000000000000000000011111111111100000000",
    "0000010000000000001111111100000000000000",
    "0000010000000000001111111100000000000000",
    "0000010000000000111111111100000000000000",
    "0000011000000011111111111111110000000000",
    "0000011100000111111111111101100000000000",
    "0000011110001111111111111100100000000000",
    "0000011111111111111111111100000000000000",
    "0000011111111111111111111100000000000000",
    "0000011111111111111111111100000000000000",
    "0000001111111111111111111100000000000000",
    "0000000111111111111111110000000000000000",
    "0000000011111111111111110000000000000000",
    "0000000001111111111111100000000000000000",
    "0000000001111111111111100000000000000000",
    "0000000000011111111110000000000000000000",
    "0000000000001111101110000000000000000000",
    "0000000000001111001110000000000000000000",
    "0000000000001110000010000000000000000000",
    "0000000000001100000010000000000000000000",
    "0000000000001000000010000000000000000000",
    "0000000000001110000011100000000000000000",
]



        # Ajusta el tamaño del sprite y color
        pixel_size = 2  # Tamaño de cada "pixel"
        color = (83, 83, 83)         # Color principal original (gris oscuro)
        eye_color = (255, 255, 255)  # Ojo original (blanco)
        for row_idx, row in enumerate(dino_pixels):
            for col_idx, px in enumerate(row):
                if px == "1":
                    pygame.draw.rect(
                        surface,
                        color,
                        (
                            int(self.x) + col_idx * pixel_size,
                            int(self.y) + row_idx * pixel_size,
                            pixel_size,
                            pixel_size,
                        ),
                    )
                elif px == "2":
                    pygame.draw.rect(
                        surface,
                        eye_color,
                        (
                            int(self.x) + col_idx * pixel_size,
                            int(self.y) + row_idx * pixel_size,
                            pixel_size,
                            pixel_size,
                        ),
                    )
