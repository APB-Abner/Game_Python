import pygame
import random


# Carregar imagem do carro
car_image = pygame.image.load('./img/car.png').convert_alpha()
car_width = car_image.get_width()
car_height = car_image.get_height()
car_mask = pygame.mask.from_surface(car_image)
class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

class Animation:
    def __init__(self, spritesheet, frame_width, frame_height, num_frames):
        self.frames = []
        for i in range(num_frames):
            x = (i % 8) * frame_width
            y = (i // 8) * frame_height
            frame = spritesheet.get_sprite(x, y, frame_width, frame_height)
            self.frames.append(frame)
        self.current_frame = 0
        self.num_frames = num_frames
        self.timer = 0
        self.frame_rate = 100  # milissegundos por frame

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_rate:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def get_current_frame(self):
        return self.frames[self.current_frame]

# Carregar spritesheet da estrada
spritesheet = Spritesheet('./sprit_road-0.png')
# Carregar imagens dos obstáculos
obstacle_options = ['./img/obstacle.png', './img/obstacle1.png', './img/obstacle2.png', './img/obstacle3.png']
obstacle_images = [pygame.image.load(image).convert_alpha() for image in obstacle_options]
# Carregar imagens dos pads
pad_image = pygame.image.load('./img/pad.png').convert_alpha()
pad_mask = pygame.mask.from_surface(pad_image)
# Carregar imagens do background
road_image = pygame.image.load('./img/road.png').convert_alpha()
back_image = pygame.image.load('./img/back.jpg')
back_menu = pygame.image.load('./img/back_menu.jpg')

# Carregar imagens dos obstáculos de redução de velocidade
slow_obstacles_options = ['./img/slow_pad.png','./img/car.png']  # Substitua com as imagens dos obstáculos que reduzem a velocidade
slow_obstacles_images = [pygame.image.load(image).convert_alpha() for image in obstacle_options]
slow_obstacle_image = random.choice(slow_obstacles_images)
slow_obstacle_mask = pygame.mask.from_surface(slow_obstacle_image)
