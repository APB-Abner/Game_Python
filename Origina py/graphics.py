import pygame
import json
from config import screen, gray, black, green, white
from sprite import pad_image, slow_obstacle_image, car_image, car_boost_image

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

# Funções relacionadas ao desenho dos elementos visuais do jogo
def car(x, y, boost_active):
    """Desenha o carro na tela."""
    if not boost_active:
        screen.blit(car_image, (x, y))    
    else:
        screen.blit(car_boost_image, (x, y))    

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

# Funções relacionadas à manipulação de texto e imagens
def display_text(text, font_size, color, x, y):
    font = pygame.font.SysFont(None, font_size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_with_perspective(image, x, y, scale):
    scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    screen.blit(scaled_image, (x - scaled_image.get_width() // 2, y - scaled_image.get_height() // 2))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_slider(screen, x, y, w, h, value):
    pygame.draw.rect(screen, gray, (x, y, w, h))
    handle_pos = int(x + (w - 20) * value)
    pygame.draw.rect(screen, black, (handle_pos, y, 20, h))

def adjust_slider_value(x, y, w, value):
    mouse_x = pygame.mouse.get_pos()[0]
    new_value = (mouse_x - x) / (w - 20)
    return max(0, min(1, new_value))

# Carregar spritesheet da estrada
spritesheet = Spritesheet('./sprit_road-0.png')

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render_car(self, car_x, car_y, boost_active):
            car(car_x, car_y, boost_active)

    def render_obstacle(self, obst_startx, obst_starty, obstacle_image, scale):
        draw_with_perspective(obstacle_image, obst_startx, obst_starty, scale)

    def render_pad(self, pad_startx, pad_starty, scale):
        draw_with_perspective(pad_image, pad_startx, pad_starty, scale)

    def render_slow_obstacle(self, slow_obst_startx, slow_obst_starty, scale):
        draw_with_perspective(slow_obstacle_image,slow_obst_startx, slow_obst_starty, scale)

    def render_animation(self, animation, x, y):
        current_frame = animation.get_current_frame()
        self.screen.blit(current_frame, (x, y))

    def render_hud(self, distance, pads_collected, boost_active, boost_timer, color_text):
        record = get_high_score()
        font = pygame.font.Font(None, 36)
        text = font.render(f'Distância: {distance}', True, color_text)
        # text = font.render(f'Recorde: {record}', True, color_text)
        self.screen.blit(text, (10, 10))
        draw_boost_bar(pads_collected, boost_active, boost_timer)

        # Adicionar mais elementos de HUD conforme necessário

def save_score(score):
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append(score)
    with open('scores.json', 'w') as file:
        json.dump(scores, file)

def get_high_score():
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
        return max(scores)
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0

def display_scores():
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
        return scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []
