import pygame
import random

# Carregar imagem do carro
car_image = pygame.image.load('./img/car.png').convert_alpha()
car_width = car_image.get_width()
car_height = car_image.get_height()
car_mask = pygame.mask.from_surface(car_image)

# Carregar imagens dos obstáculos
obstacle_options = ['./img/obstacle.png', './img/obstacle1.png', './img/obstacle2.png', './img/obstacle3.png']
obstacle_images = [pygame.image.load(image).convert_alpha() for image in obstacle_options]
obstacle_image = random.choice(obstacle_images)
obstacle_mask = pygame.mask.from_surface(obstacle_image)

# Carregar imagens dos pads
pad_image = pygame.image.load('./img/pad.png').convert_alpha()
pad_mask = pygame.mask.from_surface(pad_image)


back_image = pygame.image.load('./img/back.jpg')
back_menu = pygame.image.load('./img/back_menu.jpg')

# Carregar imagens dos obstáculos de redução de velocidade
slow_obstacles_options = ['./img/slow_pad.png']  # Substitua com as imagens dos obstáculos que reduzem a velocidade
slow_obstacles_images = [pygame.image.load(image).convert_alpha() for image in slow_obstacles_options]
slow_obstacle_image = random.choice(slow_obstacles_images)
slow_obstacle_mask = pygame.mask.from_surface(slow_obstacle_image)
