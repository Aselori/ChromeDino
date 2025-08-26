# dino_runner.py
import pygame, sys, time
from core.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 300))
    clock = pygame.time.Clock()
    game = Game(seed=None)  # o una semilla fija para test

    running = True
    while running:
        dt_ms = clock.tick(60)
        dt = dt_ms / (1000/60.0)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            else: game.handle_event(e)

        game.update(dt, dt_ms)
        game.draw(screen)
        pygame.display.flip()

        if game.game_over and game.should_commit_run:  # flag interno
            game.end_run()         # aquí se llama al AdaptiveManager y Telemetry
            game.reset()           # nueva partida con NUEVO perfil

    pygame.quit(); sys.exit(0)

if __name__ == "__main__":
    main()
