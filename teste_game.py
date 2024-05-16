import pygame
import random
import time

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Corrida de Fórmula E")

# Definir cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Carregar imagens dos obstáculos
obstacle_options = ['./obstacle.png', './obstacle1.png', './obstacle2.png', './obstacle3.png']
obstacle_images = [pygame.image.load(img) for img in obstacle_options]

# Carregar imagem do carro
car_image = pygame.image.load('./carro.png')
car_width = car_image.get_width()
car_height = car_image.get_height()

# Carregar imagem do pad
pad_image = pygame.image.load('./pad.png')
pad_width = pad_image.get_width()
pad_height = pad_image.get_height()

# Função para exibir o carro
def car(x, y):
    screen.blit(car_image, (x, y))

# Função para desenhar obstáculos
def obstacles(obst_x, obst_y, obstacle_image):
    screen.blit(obstacle_image, (obst_x, obst_y))

# Função para desenhar pads
def pad(x, y):
    screen.blit(pad_image, (x, y))

# Função para verificar colisão
def is_collision(car_x, car_y, obst_x, obst_y, obst_width, obst_height):
    if car_y < obst_y + obst_height and car_y + car_height > obst_y:
        if car_x > obst_x and car_x < obst_x + obst_width or \
           car_x + car_width > obst_x and car_x + car_width < obst_x + obst_width:
            return True
    return False

# Função principal do jogo
def game_loop():
    # Posição inicial do carro
    car_x = (screen_width * 0.45)
    car_y = (screen_height * 0.8)
    car_x_change = 0

    # Inicializar a posição do obstáculo
    obst_startx = random.randrange(0, screen_width - car_width)
    obst_starty = -car_height
    obst_speed = 7

    # Inicializar a posição do pad
    pad_startx = random.randrange(0, screen_width - pad_width)
    pad_starty = -pad_height
    pad_speed = 5
    pad_visible = True

    # Selecionar uma imagem de obstáculo aleatória
    current_obstacle_image = random.choice(obstacle_images)

    # Configurar temporizadores
    start_time = time.time()
    boost_start_time = None
    boost_duration = 15
    speed_increment_interval = 20
    speed_increment_factor = 1.15

    # Boost inicial
    is_boost_active = False
    pads_collected = 0

    # Iniciar a contagem de frames
    clock = pygame.time.Clock()
    
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
                elif event.key == pygame.K_SPACE and not is_boost_active and pads_collected >= 3:
                    is_boost_active = True
                    boost_start_time = time.time()
                    pads_collected = 0  # Resetar o contador de pads

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0

        # Atualizar a posição do carro
        car_x += car_x_change

        # Preencher a tela com branco
        screen.fill(white)

        # Desenhar o obstáculo
        obstacles(obst_startx, obst_starty, current_obstacle_image)
        obst_starty += obst_speed

        # Desenhar o pad
        if pad_visible:
            pad(pad_startx, pad_starty)
            pad_starty += pad_speed

        # Desenhar o carro
        car(car_x, car_y)

        # Verificar colisão com o obstáculo
        if is_collision(car_x, car_y, obst_startx, obst_starty, current_obstacle_image.get_width(), current_obstacle_image.get_height()):
            print("Colisão!")
            game_exit = True

        # Verificar colisão com o pad
        if pad_visible and is_collision(car_x, car_y, pad_startx, pad_starty, pad_width, pad_height):
            pads_collected += 1
            pad_visible = False

        # Resetar o obstáculo quando sair da tela
        if obst_starty > screen_height:
            obst_starty = -current_obstacle_image.get_height()
            obst_startx = random.randrange(0, screen_width - current_obstacle_image.get_width())
            current_obstacle_image = random.choice(obstacle_images)

        # Resetar o pad quando sair da tela e torná-lo visível novamente
        if pad_starty > screen_height or pad_visible == False:
            pad_starty = -pad_height
            pad_startx = random.randrange(0, screen_width - pad_width)
            pad_visible = True

        # Incrementar a velocidade dos obstáculos a cada 20 segundos
        if time.time() - start_time > speed_increment_interval:
            obst_speed *= speed_increment_factor
            start_time = time.time()

        # Gerenciar o boost
        if is_boost_active:
            car_x += car_x_change * 2  # Aumentar a velocidade do carro
            if time.time() - boost_start_time > boost_duration:
                is_boost_active = False

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de frames
        clock.tick(60)

    pygame.quit()
    quit()

# Iniciar o jogo
game_loop()



'''
import pygame.examples.joystick
pygame.examples.joystick.main()
import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Corrida")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Carro
carro_img = pygame.image.load("carro.png")
carro_largura = 73
carro_altura = 82
carro_x = (largura * 0.45)
carro_y = (altura * 0.8)

# Função para desenhar o carro na tela
def desenhar_carro(x, y):
    tela.blit(carro_img, (x, y))

# Loop principal do jogo
jogo_ativo = True
while jogo_ativo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_ativo = False

    # Verificar teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        carro_x -= 5
    if teclas[pygame.K_RIGHT]:
        carro_x += 5
    if teclas[pygame.K_UP]:
        carro_y -= 5
    if teclas[pygame.K_DOWN]:
        carro_y += 5

    # Limpar tela
    tela.fill(branco)

    # Desenhar o carro na tela
    desenhar_carro(carro_x, carro_y)

    # Atualizar tela
    pygame.display.update()

    # Controlar taxa de frames por segundo
    pygame.time.Clock().tick(60)

# Finalizar o Pygame
pygame.quit()
sys.exit()
'''
