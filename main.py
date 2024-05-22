import pygame
import random
from config import screen_width, screen_height, title, white, black, track_left_limit, track_right_limit
from function_basic import is_collision, car, pad, obstacles, draw_road, display_text, draw_boost_bar, draw_with_perspective
from sprite import car_mask, car_width, car_height, obstacle_images, pad_mask, pad_image, Animation, spritesheet
from menus import pause_menu, main_menu

# Função principal do jogo
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(title)
    speed_basic = 3
    speed_boost = speed_basic * 2

    # Posição inicial do carro
    car_x = (screen_width * 0.45)
    car_y = (screen_height * 0.8)
    car_x_change = 0

    # Inicializar a posição dos obstáculos
    obst_startx = random.randrange(0, screen_width - car_width)
    obst_starty = -car_height
    obst_speed = speed_basic
    obstacle_image = random.choice(obstacle_images)
    obstacle_mask = pygame.mask.from_surface(obstacle_image)

    # Inicializar a posição dos pads
    pad_startx = random.randrange(0, screen_width - car_width)
    pad_starty = -car_height
    pad_speed = speed_basic


    # Inicializar a posição e escala do obstáculo que reduz a velocidade
    slow_obst_startx = (track_left_limit + track_right_limit) // 2
    slow_obst_starty = screen_height // 2
    slow_obst_scale = 0.1
    slow_obst_speed = speed_basic

    # Variáveis do boost
    pads_collected = 0
    boost_active = False
    boost_timer = 0

    # Variáveis de rolagem da estrada
    road_y = 0
    road_speed = speed_basic

    
    # Variável de distância percorrida/pontuação
    distance = 0

    # Incrementar a distância percorrida
    distance += road_speed / 60  # Supondo que o jogo roda a 60 FPS

    # Iniciar a contagem de frames
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    # sprites confirguration
    frame_width = 600
    frame_height = 700
    num_frames = 64

    # Criar uma instância da classe Animation
    animation = Animation(spritesheet, frame_width, frame_height, num_frames)

    # Posição do sprite na tela
    sprite_pos = pygame.Rect(100, 100, frame_width, frame_height)


    # Variável para controlar o loop principal
    game_exit = False

    # Mostrar o menu principal antes de iniciar o jogo
    main_menu(screen)

    while not game_exit:
        dt = clock.tick(60)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause_menu(screen)

        # Atualizar a posição do carro
        car_x += car_x_change

        # Limitar o carro para não sair da pista
        if car_x < track_left_limit:
            car_x = track_left_limit
        elif car_x > track_right_limit - car_width:
            car_x = track_right_limit - car_width



        # Preencher a tela com branco
        screen.fill(white)

        # Atualizar a animação
        animation.update(dt)
        
        # Limpar a tela
        screen.fill((0, 0, 0))
        
        # Desenhar o frame atual da animação na tela
        screen.blit(animation.get_current_frame(), sprite_pos)
        
        # Atualizar a posição e escala do obstáculo
        obst_starty += obst_speed
        obst_scale += 0.01  # Aumentar a escala

        # Atualizar a posição e escala do pad
        pad_starty += pad_speed
        pad_scale += 0.01  # Aumentar a escala

        # Desenhar o obstáculo com perspectiva
        draw_with_perspective(obstacle_image, obst_startx, obst_starty, obst_scale)
        if obst_starty > screen_height:
            obst_starty = screen_height // 2
            obst_startx = random.randrange(track_left_limit, track_right_limit)
            obst_scale = 0.1

        # Desenhar o pad com perspectiva
        draw_with_perspective(pad_image, pad_startx, pad_starty, pad_scale)
        if pad_starty > screen_height:
            pad_starty = screen_height // 2
            pad_startx = random.randrange(track_left_limit, track_right_limit)
            pad_scale = 0.1

        # Desenhar o obstáculo que reduz a velocidade com perspectiva
        draw_with_perspective(slow_obstacle_image, slow_obst_startx, slow_obst_starty, slow_obst_scale)
        if slow_obst_starty > screen_height:
            slow_obst_starty = screen_height // 2
            slow_obst_startx = random.randrange(track_left_limit, track_right_limit)
            slow_obst_scale = 0.1

        # Desenhar o carro
        car(car_x, car_y)

        # Verificar colisão com obstáculos
        if is_collision(car_x, car_y, obst_startx, obst_starty, car_mask, obstacle_mask):
            print("Colisão!")
            # game_exit = True

        # Verificar colisão com pads
        if is_collision(car_x, car_y, pad_startx, pad_starty, car_mask, pad_mask):
            pad_starty = 0
            pad_startx = (track_left_limit + track_right_limit) // 2
            pads_collected += 1
            pad_scale = 0.1

        # Verificar colisão com obstáculos que reduzem a velocidade
        if is_collision(car_x, car_y, slow_obst_startx, slow_obst_starty, car_mask, slow_obstacle_mask):
            print("Colidiu com obstáculo que reduz a velocidade!")
            speed_basic /= 2  # Reduzir a velocidade pela metade
            slow_timer = pygame.time.get_ticks()

        # Resetar o obstáculo quando sair da tela
        if obst_starty > screen_height:
            obst_starty = 0
            obst_startx = (track_left_limit + track_right_limit) // 2
            obstacle_image = random.choice(obstacle_images)
            obstacle_mask = pygame.mask.from_surface(obstacle_image)
            obst_scale = 0.1
            distance += 1

        # Resetar o pad quando sair da tela
        if pad_starty > screen_height:
            pad_starty = 0
            pad_startx = (track_left_limit + track_right_limit) // 2
            pad_scale = 0.1


        # Incrementar a dificuldade a cada 20 segundos
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time > 5:
            speed_basic *= 1.15
            start_time = pygame.time.get_ticks()

        # Atualizar o boost
        if boost_active:
            if pygame.time.get_ticks() - boost_timer < 5000:
                obst_speed = speed_boost
                pad_speed = speed_boost
                road_speed = speed_boost
                pads_collected = 0
            else:
                boost_active = False
                obst_speed = speed_basic
                pad_speed = speed_basic
                road_speed = speed_basic

        # Atualizar a redução de velocidade
        if 'slow_timer' in locals():
            if pygame.time.get_ticks() - slow_timer < 5000:
                speed_basic = original_speed_basic / 2
            else:
                speed_basic = original_speed_basic

        # Mostrar informações na tela
        display_text(f'Distância: {int(distance)}', 30, white, 10, 10)
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