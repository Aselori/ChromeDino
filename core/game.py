import random
import time
import pygame
from systems.difficulty import AdaptiveManager
from entities.obstacles import Spawner, Obstacle
from entities.dino import Dino
from entities.ground import Ground
from entities.cloud import Cloud
from systems.scoring import HiScore, Telemetry
from systems.daynight import DayNightCycle
from core.config import WIDTH, HEIGHT, GROUND_Y

class PixelFont:
    """Sistema de fuentes pixel art para estilo retro"""
    
    def __init__(self, size=8):
        self.size = size
        self.pixel_size = max(1, size // 8)  # Tamaño de cada píxel de la fuente
        
        # Patrones de números en pixel art (0-9)
        self.number_patterns = {
            '0': [
                " 1111 ",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                " 1111 "
            ],
            '1': [
                "  11  ",
                " 111  ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  ",
                " 1111 "
            ],
            '2': [
                " 1111 ",
                "11  11",
                "    11",
                "   11 ",
                "  11  ",
                " 11   ",
                "111111"
            ],
            '3': [
                " 1111 ",
                "11  11",
                "    11",
                "  111 ",
                "    11",
                "11  11",
                " 1111 "
            ],
            '4': [
                "   11 ",
                "  111 ",
                " 1111 ",
                "11 11 ",
                "111111",
                "   11 ",
                "   11 "
            ],
            '5': [
                "111111",
                "11    ",
                "11111 ",
                "    11",
                "    11",
                "11  11",
                " 1111 "
            ],
            '6': [
                " 1111 ",
                "11  11",
                "11    ",
                "11111 ",
                "11  11",
                "11  11",
                " 1111 "
            ],
            '7': [
                "111111",
                "    11",
                "   11 ",
                "  11  ",
                " 11   ",
                " 11   ",
                " 11   "
            ],
            '8': [
                " 1111 ",
                "11  11",
                "11  11",
                " 1111 ",
                "11  11",
                "11  11",
                " 1111 "
            ],
            '9': [
                " 1111 ",
                "11  11",
                "11  11",
                " 11111",
                "    11",
                "11  11",
                " 1111 "
            ]
        }
        
        # Patrones de letras básicas
        self.letter_patterns = {
            'A': [
                " 1111 ",
                "11  11",
                "11  11",
                "111111",
                "11  11",
                "11  11",
                "11  11"
            ],
            'B': [
                "11111 ",
                "11  11",
                "11  11",
                "11111 ",
                "11  11",
                "11  11",
                "11111 "
            ],
            'C': [
                " 1111 ",
                "11  11",
                "11    ",
                "11    ",
                "11    ",
                "11  11",
                " 1111 "
            ],
            'D': [
                "11111 ",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11111 "
            ],
            'E': [
                "111111",
                "11    ",
                "11    ",
                "11111 ",
                "11    ",
                "11    ",
                "111111"
            ],
            'F': [
                "111111",
                "11    ",
                "11    ",
                "11111 ",
                "11    ",
                "11    ",
                "11    "
            ],
            'G': [
                " 1111 ",
                "11  11",
                "11    ",
                "11 111",
                "11  11",
                "11  11",
                " 1111 "
            ],
            'H': [
                "11  11",
                "11  11",
                "11  11",
                "111111",
                "11  11",
                "11  11",
                "11  11"
            ],
            'I': [
                " 1111 ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  ",
                " 1111 "
            ],
            'J': [
                "  1111",
                "    11",
                "    11",
                "    11",
                "11  11",
                "11  11",
                " 1111 "
            ],
            'K': [
                "11  11",
                "11 11 ",
                "1111  ",
                "111   ",
                "1111  ",
                "11 11 ",
                "11  11"
            ],
            'L': [
                "11    ",
                "11    ",
                "11    ",
                "11    ",
                "11    ",
                "11    ",
                "111111"
            ],
            'M': [
                "11  11",
                "111 111",
                "1111111",
                "11 1 11",
                "11  11",
                "11  11",
                "11  11"
            ],
            'N': [
                "11  11",
                "111 11",
                "111111",
                "111111",
                "11 111",
                "11  11",
                "11  11"
            ],
            'O': [
                " 1111 ",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                " 1111 "
            ],
            'P': [
                "11111 ",
                "11  11",
                "11  11",
                "11111 ",
                "11    ",
                "11    ",
                "11    "
            ],
            'Q': [
                " 1111 ",
                "11  11",
                "11  11",
                "11  11",
                "11 111",
                "11 11 ",
                " 11111"
            ],
            'R': [
                "11111 ",
                "11  11",
                "11  11",
                "11111 ",
                "11 11 ",
                "11  11",
                "11  11"
            ],
            'S': [
                " 1111 ",
                "11  11",
                "11    ",
                " 1111 ",
                "    11",
                "11  11",
                " 1111 "
            ],
            'T': [
                "111111",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  "
            ],
            'U': [
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                " 1111 "
            ],
            'V': [
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                "11  11",
                " 11 11 ",
                "  11  "
            ],
            'W': [
                "11  11",
                "11  11",
                "11  11",
                "11 1 11",
                "1111111",
                "111 111",
                "11  11"
            ],
            'X': [
                "11  11",
                "11  11",
                " 11 11 ",
                "  11  ",
                " 11 11 ",
                "11  11",
                "11  11"
            ],
            'Y': [
                "11  11",
                "11  11",
                " 11 11 ",
                "  11  ",
                "  11  ",
                "  11  ",
                "  11  "
            ],
            'Z': [
                "111111",
                "    11",
                "   11 ",
                "  11  ",
                " 11   ",
                "11    ",
                "111111"
            ],
            ' ': [
                "      ",
                "      ",
                "      ",
                "      ",
                "      ",
                "      ",
                "      "
            ]
        }
    
    def render(self, text, color):
        """Renderiza texto en estilo pixel art"""
        text = text.upper()
        char_width = 6 * self.pixel_size
        char_height = 7 * self.pixel_size
        total_width = len(text) * char_width
        total_height = char_height
        
        # Crear superficie para el texto
        surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        
        for i, char in enumerate(text):
            if char in self.number_patterns:
                pattern = self.number_patterns[char]
            elif char in self.letter_patterns:
                pattern = self.letter_patterns[char]
            else:
                pattern = self.letter_patterns[' ']  # Espacio para caracteres no reconocidos
            
            # Dibujar cada carácter
            for row_idx, row in enumerate(pattern):
                for col_idx, pixel in enumerate(row):
                    if pixel == "1":
                        pygame.draw.rect(
                            surface,
                            color,
                            (
                                i * char_width + col_idx * self.pixel_size,
                                row_idx * self.pixel_size,
                                self.pixel_size,
                                self.pixel_size
                            )
                        )
        
        return surface

class Game:
    def __init__(self, seed=None):
        self.adapt = AdaptiveManager()
        self.profile = self.adapt.profile_for_new_run()
        self.seed_used = seed or time.time_ns()
        self.rng = random.Random(self.seed_used)
        self.spawner = Spawner(self.profile, self.rng)
        self.telemetry = Telemetry()
        self.frames = 0
        self.score = 0
        self.game_over = False
        self.should_commit_run = False
        self.speed = 8.0
        self.bg_color = (245, 245, 245)
        self.dino = Dino()
        self.ground = Ground()
        self.clouds = [Cloud() for _ in range(3)]
        self.obstacles = []
        self.spawn_timer = random.randint(900, 1400)  # Inicializa el timer para que el primer obstáculo no aparezca instantáneamente
        self.hiscore_manager = HiScore()
        self.hiscores = {
            "baja": self.hiscore_manager.load("data/hiscore_baja.dat"),
            "media": self.hiscore_manager.load("data/hiscore_media.dat"),
            "alta": self.hiscore_manager.load("data/hiscore_alta.dat"),
            "muy alta": self.hiscore_manager.load("data/hiscore_muyalta.dat"),
        }
        self.difficulty = "media"
        self.acceleration = 0.01  # Inicializa la aceleración por defecto
        self.last_score = 0
        self.adjust_history = []
        self.show_start = True  # Estado de pantalla de inicio
        self.day_night_cycle = DayNightCycle()
        
        # Inicializar fuentes pixel art
        self.pixel_font_large = PixelFont(24)  # Para títulos
        self.pixel_font_medium = PixelFont(18)  # Para texto normal
        self.pixel_font_small = PixelFont(14)   # Para texto pequeño

    def reset(self):
        self.frames = 0
        self.score = 0
        self.game_over = False
        self.should_commit_run = False
        self.profile = self.adapt.profile_for_new_run()
        self.spawner = Spawner(self.profile, self.rng)
        self.speed = 8.0
        self.bg_color = (245, 245, 245)
        self.dino = Dino()
        self.ground = Ground()
        self.clouds = [Cloud() for _ in range(3)]
        self.obstacles = []
        self.spawn_timer = random.randint(900, 1400)  # Igual que en __init__
        self.show_start = True
        # --- Auto-ajuste con aceleraciones fijas y highscore por dificultad ---
        accel_map = {
            "baja": 0.007,
            "media": 0.01,
            "alta": 0.013,
            "muy alta": 0.017
        }
        # Nueva lógica de rangos para subir dificultad
        if self.last_score > 0:
            # Sube dos dificultades si el score es mayor a 4000
            if self.last_score > 4000:
                if self.difficulty == "baja":
                    self.difficulty = "alta"
                elif self.difficulty == "media":
                    self.difficulty = "muy alta"
                elif self.difficulty == "alta":
                    self.difficulty = "muy alta"
            # Sube una dificultad si el score es mayor a 2500
            elif self.last_score > 2500:
                if self.difficulty == "baja":
                    self.difficulty = "media"
                elif self.difficulty == "media":
                    self.difficulty = "alta"
                elif self.difficulty == "alta":
                    self.difficulty = "muy alta"
            # Baja dificultad si el score es menor a 1500
            elif self.last_score < 1500:
                if self.difficulty == "muy alta":
                    self.difficulty = "alta"
                elif self.difficulty == "alta":
                    self.difficulty = "media"
                elif self.difficulty == "media":
                    self.difficulty = "baja"
        self.acceleration = accel_map[self.difficulty]
        self.day_night_cycle = DayNightCycle()
        
        # Reinicializar fuentes pixel art
        self.pixel_font_large = PixelFont(24)
        self.pixel_font_medium = PixelFont(18)
        self.pixel_font_small = PixelFont(14)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.show_start and event.key in (pygame.K_SPACE, pygame.K_UP):
                self.show_start = False
            elif not self.game_over and not self.show_start and event.key in (pygame.K_SPACE, pygame.K_UP):
                self.dino.update(pygame.key.get_pressed())
            elif self.game_over and event.key in (pygame.K_SPACE, pygame.K_UP):
                self.reset()

    def update(self, dt, dt_ms):
        if self.show_start or self.game_over:
            return
        self.frames += 1
        self.score += 1
        self.speed += self.acceleration  # Usar aceleración ajustada
        keys = pygame.key.get_pressed()
        self.dino.update(keys)
        self.ground.update(self.speed, dt)
        for c in self.clouds:
            c.update(dt)
        # Actualiza el ciclo día/noche con transiciones graduales
        self.day_night_cycle.update(self.score)
        self.bg_color = self.day_night_cycle.get_bg_color()
        self.spawn_timer -= dt_ms
        if self.spawn_timer <= 0:
            self.obstacles.append(Obstacle())
            self.spawn_timer = random.randint(900, 1400)
        for ob in list(self.obstacles):
            ob.update(self.speed, dt)
            if ob.rect.right < -5:
                self.obstacles.remove(ob)
            if self.dino.rect.colliderect(ob.rect):
                self.game_over = True
        # Actualiza el highscore de la dificultad actual
        if self.score > self.hiscores[self.difficulty]:
            self.hiscores[self.difficulty] = self.score
            # Guarda el highscore en el archivo correspondiente
            filename = f"data/hiscore_{self.difficulty.replace(' ', '')}.dat"
            self.hiscore_manager.save(self.score, filename)
        if self.game_over:
            self.last_score = self.score  # Guarda la puntuación para el próximo ajuste

    def draw(self, screen):
        screen.fill(self.bg_color)
        for c in self.clouds:
            c.draw(screen)
        self.ground.draw(screen)
        self.dino.draw(screen)
        for ob in self.obstacles:
            ob.draw(screen)
        
        # Renderizar score con fuente pixel art
        score_color = (60, 60, 60) if not self.day_night_cycle.is_night else (220, 220, 220)
        score_surf = self.pixel_font_medium.render(f"{self.score:05d}", score_color)
        screen.blit(score_surf, (WIDTH-150, 20))
        
        # Renderizar high score con fuente pixel art
        hi_color = (120, 120, 120) if not self.day_night_cycle.is_night else (180, 180, 180)
        hi_text = f"HI {self.hiscores[self.difficulty]:05d} ({self.difficulty.upper()})"
        hi_surf = self.pixel_font_small.render(hi_text, hi_color)
        screen.blit(hi_surf, (20, 20))
        if self.show_start:
            # Título principal con fuente pixel art
            title_surf = self.pixel_font_large.render("CHROME DINO", (60, 60, 60))
            screen.blit(title_surf, (WIDTH//2-200, HEIGHT//2-80))
            
            # Instrucciones con fuente pixel art
            instr_surf = self.pixel_font_medium.render("PRESIONA SPACE PARA INICIAR", (80, 80, 80))
            screen.blit(instr_surf, (WIDTH//2-200, HEIGHT//2-20))
            
            # Información de dificultad con fuente pixel art
            accel_text = f"DIFICULTAD: {self.difficulty.upper()} | ACELERACION: {self.acceleration:.4f}"
            accel_surf = self.pixel_font_small.render(accel_text, (40, 120, 40))
            screen.blit(accel_surf, (WIDTH//2-200, HEIGHT//2+20))
            
            # Historial de ajuste con fuente pixel art
            if self.adjust_history:
                hist_text = "HISTORIAL AJUSTE: " + ", ".join(f"{r:.2f}" for r in self.adjust_history)
                hist_surf = self.pixel_font_small.render(hist_text, (100, 100, 100))
                screen.blit(hist_surf, (WIDTH//2-200, HEIGHT//2+50))
        elif self.game_over:
            # Game Over con fuente pixel art
            over_surf = self.pixel_font_large.render("GAME OVER", (200, 0, 0))
            screen.blit(over_surf, (WIDTH//2-180, HEIGHT//2-60))
            
            # Instrucción de reinicio con fuente pixel art
            restart_surf = self.pixel_font_medium.render("PRESIONA SPACE PARA REINICIAR", (80, 80, 80))
            screen.blit(restart_surf, (WIDTH//2-180, HEIGHT//2))

    def end_run(self):
        ttf = self.frames / 60.0
        self.adapt.update_after_run(ttf_seconds=ttf, score=self.score)
        self.telemetry.append_run(ttf, self.score, self.profile, self.seed_used)

