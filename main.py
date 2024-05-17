import pygame
import random
from config import screen_width, screen_height, title, white, black
from function_basic import is_collision, car, pad, obstacles, draw_road, display_text, draw_boost_bar
from sprite import car_mask, car_width, car_height, obstacle_images, pad_mask

# Função principal do jogo
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(title)
    # Posição inicial do carro
    car_x = (screen_width * 0.45)
    car_y = (screen_height * 0.8)
    car_x_change = 0

    # Inicializar a posição dos obstáculos
    obst_startx = random.randrange(0, screen_width - car_width)
    obst_starty = -car_height
    obst_speed = 7
    obstacle_image = random.choice(obstacle_images)
    obstacle_mask = pygame.mask.from_surface(obstacle_image)


    # Inicializar a posição dos pads
    pad_startx = random.randrange(0, screen_width - car_width)
    pad_starty = -car_height
    pad_speed = 7

    # Variáveis do boost
    pads_collected = 0
    boost_active = False
    boost_timer = 0

    # Variável de pontuação
    score = 0

    # Variáveis de rolagem da estrada
    road_y = 0
    road_speed = 7

    # Iniciar a contagem de frames
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    # Variável para controlar o loop principal
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 5
                elif event.key == pygame.K_SPACE and pads_collected >= 3:
                    boost_active = True
                    boost_timer = pygame.time.get_ticks()
                    pads_collected = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0

        # Atualizar a posição do carro
        car_x += car_x_change

        # Preencher a tela com branco
        screen.fill(white)

        # Desenhar a estrada
        draw_road(road_y)
        road_y += road_speed
        if road_y >= screen_height:
            road_y = 0

        # Desenhar o obstáculo
        obstacles(obst_startx, obst_starty, obstacle_image)
        obst_starty += obst_speed

        # Desenhar o pad
        pad(pad_startx, pad_starty)
        pad_starty += pad_speed

        # Desenhar o carro
        car(car_x, car_y)

        # Verificar colisão com obstáculos
        if is_collision(car_x, car_y, obst_startx, obst_starty, car_mask, obstacle_mask):
            print("Colisão!")
            game_exit = True

        # Verificar colisão com pads
        if is_collision(car_x, car_y, pad_startx, pad_starty, car_mask, pad_mask):
            pad_starty = -car_height
            pad_startx = random.randrange(0, screen_width - car_width)
            pads_collected += 1

        # Resetar o obstáculo quando sair da tela
        if obst_starty > screen_height:
            obst_starty = -car_height
            obst_startx = random.randrange(0, screen_width - car_width)
            obstacle_image = random.choice(obstacle_images)
            obstacle_mask = pygame.mask.from_surface(obstacle_image)
            score += 1

        # Resetar o pad quando sair da tela
        if pad_starty > screen_height:
            pad_starty = -car_height
            pad_startx = random.randrange(0, screen_width - car_width)

        # Incrementar a dificuldade a cada 20 segundos
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time > 20:
            obst_speed *= 1.15
            road_speed *= 1.15
            pad_speed *= 1.15
            start_time = pygame.time.get_ticks()

        # Atualizar o boost
        if boost_active:
            if pygame.time.get_ticks() - boost_timer < 5000:
                obst_speed = 14
                pad_speed = 14
                road_speed = 14
            else:
                boost_active = False
                obst_speed = 7
                pad_speed = 7
                road_speed = 7

        # Mostrar informações na tela
        display_text(f'Pontuação: {score}', 30, black, 10, 10)
        draw_boost_bar(pads_collected, boost_active, boost_timer)

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de frames
        clock.tick(60)

    pygame.quit()
    quit()


# Iniciar o jogo
if __name__ == "__main__":
    game_loop()