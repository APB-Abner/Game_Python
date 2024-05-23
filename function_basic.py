import pygame
from config import screen, white, black, green, black_alpha, track_left_limit, track_right_limit
from sprite import car_image, obstacle_image, pad_image, slow_obstacle_image, obstacle_mask

# Funções relacionadas ao desenho dos elementos visuais do jogo
def car(x, y):
    """Desenha o carro na tela."""
    screen.blit(car_image, (x, y))

def pad(x, y):
    """Desenha um pad na tela."""
    screen.blit(pad_image, (x, y))

def obstacles(obst_x, obst_y):
    """Desenha obstáculos na tela."""
    screen.blit(obstacle_image, (obst_x, obst_y))

def slow_obstacle(x, y):
    """Desenha um obstáculo de redução de velocidade na tela."""
    screen.blit(slow_obstacle_image, (x, y))

def draw_boost_bar(pads_collected, boost_active, boost_timer):
    """Desenha a barra de boost na tela."""
    bar_width = 200
    bar_height = 20
    bar_x = 10
    bar_y = 100
    padding = 3

    pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

    if boost_active:
        elapsed = (pygame.time.get_ticks() - boost_timer) / 5000
        boost_progress = max(0, 1 - elapsed)
        pygame.draw.rect(screen, green, (bar_x + padding, bar_y + padding, (bar_width - 2 * padding) * boost_progress, bar_height - 2 * padding))
    elif not boost_active and pads_collected <= 3:
            boost_progress = pads_collected / 3
            pygame.draw.rect(screen, green, (bar_x + padding, bar_y + padding, (bar_width - 2 * padding) * boost_progress, bar_height - 2 * padding))
    else:
        boost_progress = 1
        pygame.draw.rect(screen, green, (bar_x + padding, bar_y + padding, (bar_width - 2 * padding) * boost_progress, bar_height - 2 * padding))

    pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width, bar_height), 2)
