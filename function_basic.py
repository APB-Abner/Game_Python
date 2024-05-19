import pygame
from config import screen_width, screen_height, screen, white, black, green, black_alpha
from sprite import car_image, car_mask, car_width, car_height, obstacle_images, pad_image, pad_mask, road_image, back_image

# Função para exibir o carro
def car(x, y):
    screen.blit(car_image, (x, y))

# Função para desenhar pads
def pad(x, y):
    screen.blit(pad_image, (x, y))

# Função para desenhar obstáculos
def obstacles(obst_x, obst_y, obstacle_image):
    screen.blit(obstacle_image, (obst_x, obst_y))

# Função para verificar colisão pixel-perfect
def is_collision(car_x, car_y, obj_x, obj_y, car_mask, obj_mask):
    offset_x = int(obj_x - car_x)
    offset_y = int(obj_y - car_y)
    return car_mask.overlap(obj_mask, (offset_x, offset_y)) is not None

# Função para exibir texto
def display_text(text, font_size, color, x, y):
    font = pygame.font.SysFont(None, font_size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Função para desenhar a estrada
def draw_road(y):
    back_image_d = pygame.transform.flip(back_image, True, False)
    # screen.blit(road_image, (250, y))
    # screen.blit(road_image, (250, y - screen_height))
    screen.blit(road_image, (125, y))
    screen.blit(road_image, (125, y - screen_height))
    screen.blit(road_image, (375, y))
    screen.blit(road_image, (375, y - screen_height))
    screen.blit(back_image, (0, y))
    screen.blit(back_image, (0, y - screen_height))
    screen.blit(back_image_d, (675, y))
    screen.blit(back_image_d, (675, y - screen_height))

# Função para desenhar a barra de boost
def draw_boost_bar(pads_collected, boost_active, boost_timer):
    bar_width = 200
    bar_height = 20
    bar_x = 10
    bar_y = 100
    padding = 3

    # Fundo da barra
    pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

    # Barra de progresso
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
        

    # Bordas da barra
    pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width, bar_height), 2)
