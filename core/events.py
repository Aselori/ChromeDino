import pygame

def handle_global_events(event, game):
    # Puedes expandir aquí para manejar eventos globales (pausa, salir, etc.)
    if event.type == pygame.QUIT:
        return False
    game.handle_event(event)
    return True
