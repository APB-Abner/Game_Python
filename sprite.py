import pygame

# Carregar imagens
car_image = pygame.image.load('./img/car.png').convert_alpha()
car_width = car_image.get_width()
car_height = car_image.get_height()
car_mask = pygame.mask.from_surface(car_image)

obstacle_options = ['./img/obstacle.png', './img/obstacle1.png', './img/obstacle2.png', './img/obstacle3.png']
obstacle_images = [pygame.image.load(image).convert_alpha() for image in obstacle_options]
pad_image = pygame.image.load('./img/pad.png').convert_alpha()
pad_mask = pygame.mask.from_surface(pad_image)
road_image = pygame.image.load('./img/road.png').convert_alpha()
back_image = pygame.image.load('./img/back.jpg')
back_menu = pygame.image.load('./img/back_menu.jpg')
