import random
import time
import pygame
from systems.difficulty import AdaptiveManager
from entities.obstacles import Spawner, Obstacle
from entities.dino import Dino
from entities.ground import Ground
from entities.cloud import Cloud
from systems.scoring import HiScore, Telemetry
from core.config import WIDTH, HEIGHT, GROUND_Y

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
        if self.score % 1000 < 500:
            self.bg_color = (245, 245, 245)
        else:
            self.bg_color = (40, 40, 60)
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
        font = pygame.font.SysFont("Arial", 32, bold=True)
        score_surf = font.render(f"{self.score:05d}", True, (60, 60, 60) if self.score % 1000 < 500 else (220,220,220))
        screen.blit(score_surf, (WIDTH-120, 20))
        hi_font = pygame.font.SysFont("Arial", 20)
        hi_surf = hi_font.render(f"HI {self.hiscores[self.difficulty]:05d} ({self.difficulty.capitalize()})", True, (120, 120, 120))
        screen.blit(hi_surf, (20, 20))
        if self.show_start:
            title_font = pygame.font.SysFont("Arial", 40, bold=True)
            title_surf = title_font.render("CHROME DINO", True, (60, 60, 60))
            screen.blit(title_surf, (WIDTH//2-150, HEIGHT//2-60))
            instr_font = pygame.font.SysFont("Arial", 24)
            instr_surf = instr_font.render("Presiona SPACE para iniciar", True, (80, 80, 80))
            screen.blit(instr_surf, (WIDTH//2-150, HEIGHT//2))
            # Muestra el valor de aceleración actual (auto-ajuste)
            accel_font = pygame.font.SysFont("Arial", 20)
            accel_surf = accel_font.render(
                f"Dificultad: {self.difficulty.capitalize()}  |  Aceleración: {self.acceleration:.4f}",
                True, (40, 120, 40)
            )
            screen.blit(accel_surf, (WIDTH//2-150, HEIGHT//2+40))
            # Muestra historial de ajuste para depuración visual
            if self.adjust_history:
                hist_font = pygame.font.SysFont("Arial", 16)
                hist_surf = hist_font.render(
                    "Historial ajuste: " + ", ".join(f"{r:.2f}" for r in self.adjust_history),
                    True, (100, 100, 100)
                )
                screen.blit(hist_surf, (WIDTH//2-150, HEIGHT//2+70))
        elif self.game_over:
            over_font = pygame.font.SysFont("Arial", 36, bold=True)
            over_surf = over_font.render("GAME OVER", True, (200, 0, 0))
            screen.blit(over_surf, (WIDTH//2-120, HEIGHT//2-40))
            restart_font = pygame.font.SysFont("Arial", 20)
            restart_surf = restart_font.render("Presiona SPACE para reiniciar", True, (80, 80, 80))
            screen.blit(restart_surf, (WIDTH//2-120, HEIGHT//2+10))

    def end_run(self):
        ttf = self.frames / 60.0
        self.adapt.update_after_run(ttf_seconds=ttf, score=self.score)
        self.telemetry.append_run(ttf, self.score, self.profile, self.seed_used)

