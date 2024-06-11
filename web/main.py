import pygame
import random

# Inicializa o Pygame
pygame.init()

# Definindo constantes
screen_width = 800
screen_height = 600
resolution = (screen_width, screen_height)
screen = pygame.display.set_mode(resolution)
title = "Corrida de Fórmula E"
fullscreen = False
speed_basic = 1.5
speed_p = 5
track_left_limit = 175
track_right_limit = screen_width - 175 
scale = 0

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
light_gray = (220, 220, 220)
black_alpha = pygame.Color(0, 0, 0, 15)

# Configurações da screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Corrida Interminável")

# Carregar imagens
car_image = car_image = pygame.image.load('./img/car.png')
obstacle_options = ['./img/obstacle.png', './img/obstacle1.png', './img/obstacle2.png', './img/obstacle3.png']
obstacle_images = [pygame.image.load(image).convert_alpha() for image in obstacle_options]

# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 100)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > track_left_limit:
            self.rect.x -= speed_p
        if keys[pygame.K_RIGHT] and self.rect.right < track_right_limit:
            self.rect.x += speed_p

# Classe do Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.obst_startx = screen_width // 2
        self.obst_starty = screen_height // 2
        self.obst_targetx = random.randrange(track_left_limit, track_right_limit)
        self.obst_speed = speed_basic
        self.obst_targety = screen_height

        self.image = random.choice(obstacle_images)
        self.mask = pygame.mask.from_surface(self.image)
        self.scale = (self.obst_starty - screen_height // 2) / (screen_height // 2) if self.obst_starty > screen_height // 2 else 0
        self.scaled_image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.rect = self.scaled_image.get_rect()
        self.rect.x = (screen_width//2)-self.rect.width//2
        self.rect.y = -self.rect.height

        self.direction_x_obst = (self.obst_targetx - self.obst_startx) / (screen_height / self.obst_speed)
        self.direction_y_obst = self.obst_speed

    def update(self):
        # Atualiza a escala dinamicamente baseado na posição
        self.scale = (self.obst_starty - screen_height // 2) / (screen_height // 2) if self.obst_starty > screen_height // 2 else 0
        self.scaled_image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.rect = self.scaled_image.get_rect(center=self.rect.center)

        # Atualiza a posição
        self.rect.x += self.direction_x_obst
        self.rect.y += self.direction_y_obst

        # Reinicializa o obstáculo se ele sair da tela
        if self.rect.top > screen_height:
            self.obst_startx = screen_width // 2
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = -self.rect.height
            self.obst_targetx = random.randrange(track_left_limit, track_right_limit)
            self.direction_x_obst = (self.obst_targetx - self.obst_startx) / (screen_height / self.obst_speed)
            self.scale = (self.obst_starty - screen_height // 2) / (screen_height // 2) if self.obst_starty > screen_height // 2 else 0

# Grupos de Sprites
todos_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()

# Instância do jogador
jogador = Jogador()
todos_sprites.add(jogador)
# obstaculo = Obstaculo()
'''
# Instanciar obstáculos
for _ in range(random.choice(range(5))):
'''
obstaculo = Obstaculo()
todos_sprites.add(obstaculo)
obstaculos.add(obstaculo)

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

while rodando:
    start_time_d = pygame.time.get_ticks()
    start_time = start_time_d
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar
    todos_sprites.update()

    # Verificar colisões
    if pygame.sprite.spritecollide(jogador, obstaculos, False, pygame.sprite.collide_mask):
        print("Game Over")
        rodando = False

    # Desenhar
    screen.fill(black)
    todos_sprites.draw(screen)

    # Atualizar display
    pygame.display.flip()
    
    # Incrementar a dificuldade a cada 20 segundos
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time > 5:
        speed_basic *= 1.05
        obstaculos.obst_speed *= 1.15
        start_time = pygame.time.get_ticks()

    # Controlar FPS
    clock.tick(60)

menu = True
pygame.quit()
