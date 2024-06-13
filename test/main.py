import pygame
import random
import json
import os

# Definição da resolução padrão
screen_width = 800
screen_height = 600
resolution = (screen_width, screen_height)

# Criação da janela de exibição do jogo
screen = pygame.display.set_mode(resolution)

# Título do jogo
title = "Corrida de Fórmula E"

# Configurações de tela cheia
fullscreen = False

# Idioma do jogo
language = 'English'

# Configurações de áudio
master_volume = 0.5
sfx_volume = 0.5
music_volume = 0.5
ambient_volume = 0.5

# Limites da pista
track_left_limit = 175  # Posição X inicial da pista
track_right_limit = screen_width - 175  # Posição X final da pista

# Definição de cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
light_gray = (220, 220, 220)
black_alpha = pygame.Color(0, 0, 0, 15)

# Carregar imagem do carro
car_image = pygame.image.load('./img/car.png').convert_alpha()
car_boost_image = pygame.image.load('./img/car_boost.png').convert_alpha()
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

SCORE_FILE = './scores.json'

def save_score(score):
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'w') as file:
            json.dump([], file)
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    scores.append(score)
    
    with open(SCORE_FILE, 'w') as file:
        json.dump(scores, file)

def get_high_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    if not scores:
        return 0
    
    return max(scores)

def display_scores():
    if not os.path.exists(SCORE_FILE):
        return "No scores available"
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    if not scores:
        return "No scores available"
    
    scores.sort(reverse=True)
    top_scores = scores[:5]
    return "\n".join([f"{i+1}. {score}" for i, score in enumerate(top_scores)])



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

class Options:
    def toggle_fullscreen():
        global fullscreen
        fullscreen = not fullscreen
        if fullscreen:
            pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((screen_width, screen_height))

    def change_language():
        global language
        language = 'English' if language == 'Portuguese' else 'Portuguese'

    def change_resolution(new_resolution):
        global resolution
        resolution = new_resolution
        pygame.display.set_mode(resolution)

    def draw_slider(screen, x, y, w, h, value):
        pygame.draw.rect(screen, gray, (x, y, w, h))
        handle_pos = int(x + (w - 20) * value)
        pygame.draw.rect(screen, black, (handle_pos, y, 20, h))

    def adjust_slider_value(x, y, w, value):
        mouse_x = pygame.mouse.get_pos()[0]
        new_value = (mouse_x - x) / (w - 20)
        return max(0, min(1, new_value))

def draw_button(screen, text, font, color, rect, color_text, action=None):
    
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if rect.collidepoint(mouse) and click[0] == 1 and action:
        action()

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
spritesheet = Spritesheet('./img/sprit_road-0.png')

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

class GameLogic:
    def __init__(self):
        self.car_x = (screen_width * 0.5)
        self.car_y = (screen_height * 0.85)
        self.car_x_change = 0
        self.speed_player_r = 5
        self.speed_player_l = -5

        self.speed_basic = 1.5
        self.speed_boost = self.speed_basic * 2
        self.speed_slow = self.speed_basic / 2
        
        # Inicializar a posição dos obstáculos
        self.obstacle_image = random.choice(obstacle_images)
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obst_startx = screen_width // 2
        self.pad_startx = screen_width // 2
        self.slow_obst_startx = screen_width // 2
        self.obst_starty = screen_height-car_height//2
        self.pad_starty = screen_height-car_height//2
        self.slow_obst_starty = screen_height-car_height//2
        
        self.obst_speed = self.speed_basic
        self.pad_speed = self.speed_basic
        self.slow_obst_speed = self.speed_basic
        self.obst_scale = 0
        self.pad_scale = 0
        self.slow_obst_scale = 0

        # Definir a posição alvo para o obstáculo
        self.obst_targetx = random.randrange(track_left_limit, track_right_limit)
        self.pad_targetx = random.randrange(track_left_limit, track_right_limit)
        self.slow_obst_targetx = random.randrange(track_left_limit, track_right_limit)
        self.obst_targety = screen_height
        self.pad_targety = screen_height
        self.slow_obst_targety = screen_height

        
        self.pads_collected = 0
        self.boost_active = False
        self.slow_active = False
        self.boost_timer = 0

        self.road_speed = self.speed_basic
        self.distance = 0
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.spritesheet = Spritesheet('./sprit_road-0.png')
        frame_width = 600
        frame_height = 700
        num_frames = 64

        self.animation = Animation(self.spritesheet, frame_width, frame_height, num_frames)
        self.sprite_pos = pygame.Rect(100, 100, frame_width, frame_height)

        self.start_delay = 3000  # 3 segundos em milissegundos
        self.start_time_d = pygame.time.get_ticks()
        self.start_time = self.start_time_d

        self.obst_delay = random.randint(1000, 3000)
        self.pad_delay = random.randint(1000, 3000)
        self.slow_obst_delay = random.randint(1000, 3000)
        self.last_obst_time = pygame.time.get_ticks()
        self.last_pad_time = pygame.time.get_ticks()
        self.last_slow_obst_time = pygame.time.get_ticks()

        self.game_exit = False

    def crash(self, screen, distance):
        save_score(distance)  # Salvar pontuação quando o jogador colidir
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        self.main_loop(screen)  # Reinicia o jogo
                        return  # Sai da função para reiniciar o jogo
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        
            # Exibe mensagem de "Game Over" e distância percorrida
            screen.fill((0, 0, 0))
            display_text("Você bateu!", 36, (255, 0, 0), screen_width // 2 - 100, screen_height // 2 - 50)
            display_text(f"Distância: {int(distance)}", 30, white, screen_width // 2 - 100, screen_height // 2)
            display_text(f"Recorde: {get_high_score()}", 30, white, screen_width // 2 - 100, screen_height // 2 + 30)
            display_text("Pressione R para reiniciar ou Q para sair", 30, white, screen_width // 2 - 200, screen_height // 2 + 50)
            
            pygame.display.update()
            clock.tick(15)

    def reset_obstacle(self):
        self.obst_startx = screen_width // 2
        self.obst_starty = screen_height // 2
        self.obst_speed = self.speed_basic
        self.obst_scale = 0
        self.obstacle_image = random.choice(obstacle_images)
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obst_targetx = random.randrange(track_left_limit, track_right_limit)
        self.obst_delay = random.randint(1000, 3000)

    def reset_pad(self):
        self.pad_startx = screen_width // 2
        self.pad_starty = screen_height // 2
        self.pad_scale = 0
        self.pad_speed = self.speed_basic
        self.pad_targetx = random.randrange(track_left_limit, track_right_limit)
        self.pad_delay = random.randint(1000, 3000)

    def reset_slow_obstacle(self):
        self.slow_obst_startx = screen_width // 2
        self.slow_obst_starty = screen_height // 2
        self.slow_obst_scale = 0
        self.slow_obst_speed = self.speed_basic
        self.slow_obst_targetx = random.randrange(track_left_limit, track_right_limit)
        self.slow_obst_delay = random.randint(5000, 10000)

    def reset(self):
            self.car_x = (screen_width * 0.5)
            self.car_y = (screen_height * 0.85)
            self.car_x_change = 0
            self.speed_player_r = 5
            self.speed_player_l = -5

            self.speed_basic = 1.5
            self.speed_boost = self.speed_basic * 2
            self.speed_slow = self.speed_basic / 2
            
            self.obstacle_image = random.choice(obstacle_images)
            self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
            self.obst_startx = screen_width // 2
            self.pad_startx = screen_width // 2
            self.slow_obst_startx = screen_width // 2
            self.obst_starty = screen_height-car_height//2
            self.pad_starty = screen_height-car_height//2
            self.slow_obst_starty = screen_height-car_height//2
            
            self.obst_speed = self.speed_basic
            self.pad_speed = self.speed_basic
            self.slow_obst_speed = self.speed_basic
            self.obst_scale = 0
            self.pad_scale = 0
            self.slow_obst_scale = 0

            self.obst_targetx = random.randrange(track_left_limit, track_right_limit)
            self.pad_targetx = random.randrange(track_left_limit, track_right_limit)
            self.slow_obst_targetx = random.randrange(track_left_limit, track_right_limit)
            self.obst_targety = screen_height
            self.pad_targety = screen_height
            self.slow_obst_targety = screen_height

            
            self.pads_collected = 0
            self.boost_active = False
            self.slow_active = False
            self.boost_timer = 0

            self.road_speed = self.speed_basic
            self.distance = 0
            self.clock = pygame.time.Clock()
            self.start_time = pygame.time.get_ticks()

            self.spritesheet = Spritesheet('./sprit_road-0.png')
            frame_width = 600
            frame_height = 700
            num_frames = 64

            self.animation = Animation(self.spritesheet, frame_width, frame_height, num_frames)
            self.sprite_pos = pygame.Rect(100, 100, frame_width, frame_height)

            self.start_delay = 3000  # 3 segundos em milissegundos
            self.start_time_d = pygame.time.get_ticks()
            self.start_time = self.start_time_d

            self.obst_delay = random.randint(1000, 3000)
            self.pad_delay = random.randint(1000, 3000)
            self.slow_obst_delay = random.randint(1000, 3000)
            self.last_obst_time = pygame.time.get_ticks()
            self.last_pad_time = pygame.time.get_ticks()
            self.last_slow_obst_time = pygame.time.get_ticks()
  
    def main_loop(self, screen):

        while not self.game_exit:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_change = self.speed_player_l
                    elif event.key == pygame.K_RIGHT:
                        self.car_x_change = self.speed_player_r
                    elif event.key == pygame.K_SPACE and self.pads_collected >= 3:
                        self.boost_active = True
                        self.boost_timer = pygame.time.get_ticks()
                        self.pads_collected = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.car_x_change = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.pause_menu(screen)

            screen.fill((0, 0, 0))
            self.car_x += self.car_x_change
            self.render(screen, self.boost_active)


            if self.boost_active:
                if pygame.time.get_ticks() - self.boost_timer < 5000:
                    self.obst_speed = self.speed_boost
                    self.pad_speed = self.speed_boost
                    self.road_speed = self.speed_boost
                    self.pads_collected = 0
                else:
                    self.boost_active = False
                    self.obst_speed = self.speed_basic
                    self.pad_speed = self.speed_basic
                    self.road_speed = self.speed_basic
            if self.slow_active:
                if pygame.time.get_ticks() - self.slow_timer < 5000:
                    self.obst_speed = self.speed_slow
                    self.pad_speed = self.speed_slow
                    self.road_speed = self.speed_slow
                    self.speed_player_r = 2.5
                    self.speed_player_l = -2.5
                else:
                    self.slow_active = False
                    self.obst_speed = self.speed_basic
                    self.pad_speed = self.speed_basic
                    self.road_speed = self.speed_basic
                    self.speed_player_r = 5
                    self.speed_player_l = -5

            if self.car_x > track_right_limit - car_width:
                self.car_x = track_right_limit - car_width
            if self.car_x < track_left_limit:
                self.car_x = track_left_limit

            # Calcular a direção do movimento
            self.direction_x_obst = (self.obst_targetx - self.obst_startx) / (screen_height / self.obst_speed)
            self.direction_x_pad = (self.pad_targetx - self.pad_startx) / (screen_height / self.pad_speed)
            self.direction_x_slow_obst = (self.slow_obst_targetx - self.slow_obst_startx) / (screen_height / self.slow_obst_speed)
            self.direction_y_obst = self.obst_speed
            self.direction_y_pad = self.pad_speed
            self.direction_y_slow_obst = self.slow_obst_speed
            
            # Atualizar a posição do obstáculo
            self.obst_startx += self.direction_x_obst
            self.obst_starty += self.direction_y_obst
            # Atualizar a posição do pad
            self.pad_startx += self.direction_x_pad
            self.pad_starty += self.direction_y_pad
            # Atualizar a posição do slow
            self.slow_obst_startx += self.direction_x_slow_obst
            self.slow_obst_starty += self.direction_y_slow_obst
            self.distance += self.road_speed

            # Calcular a escala baseada na posição Y (perspectiva)
            self.obst_scale = (self.obst_starty - screen_height // 2) / (screen_height // 2) if self.obst_starty > screen_height // 2 else 0
            self.pad_scale = (self.pad_starty - screen_height // 2) / (screen_height // 2) if self.pad_starty > screen_height // 2 else 0
            self.slow_obst_scale = (self.slow_obst_starty - screen_height // 2) / (screen_height // 2) if self.slow_obst_starty > screen_height // 2 else 0
            
            current_time = pygame.time.get_ticks()

            # Resetar o obstáculo quando sair da tela
            if self.obst_starty > screen_height and current_time - self.last_obst_time >= self.obst_delay:
                self.reset_obstacle()
            if self.pad_starty > screen_height and current_time - self.last_pad_time >= self.pad_delay:
                self.reset_pad()
            if self.slow_obst_starty > screen_height and current_time - self.last_slow_obst_time >= self.slow_obst_delay:
                self.reset_slow_obstacle()

            self.animation.update(dt)
            self.render(screen, self.boost_active)

            if not pygame.time.get_ticks() - self.start_time_d < self.start_delay:
                if self.collision_check(self.car_x, self.car_y, car_image, self.obst_startx, self.obst_starty, self.obstacle_image, self.obst_scale):
                    print('Colisão!')
                    self.crash(screen, self.distance)

                if self.collision_check(self.car_x, self.car_y, car_image, self.pad_startx, self.pad_starty, pad_image, self.pad_scale):
                    self.pads_collected += 1
                    self.pad_starty = screen_height + car_height

                if self.collision_check(self.car_x, self.car_y, car_image, self.slow_obst_startx, self.slow_obst_starty, slow_obstacle_image, self.slow_obst_scale):
                    self.slow_active = True
                    self.slow_timer = pygame.time.get_ticks()

            # Incrementar a dificuldade a cada 20 segundos
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if elapsed_time > 5:
                self.obst_speed *= 1.15
                self.start_time = pygame.time.get_ticks()

            pygame.display.update()
        if not self.game_exit:    
            pygame.quit()
            quit()

    def render(self, screen, boost_active):
        renderer = Renderer(screen)
        
        renderer.render_animation(self.animation, self.sprite_pos.x, self.sprite_pos.y)
        renderer.render_obstacle(self.obst_startx, self.obst_starty, self.obstacle_image, self.obst_scale)
        renderer.render_pad( self.pad_startx, self.pad_starty, self.pad_scale)
        renderer.render_slow_obstacle( self.slow_obst_startx, self.slow_obst_starty, self.slow_obst_scale)
        renderer.render_car(self.car_x, self.car_y, boost_active)
        renderer.render_hud(self.distance, self.pads_collected, self.boost_active, self.boost_timer, white)

    def collision_check(self, x1, y1, car, x2, y2, obstacle, scale):
        scaled = (int(obstacle.get_width() * scale * 0.85), int(obstacle.get_height() * scale * 0.7))
        mask1 = pygame.mask.from_surface(car).scale(scaled)
        mask2 = pygame.mask.from_surface(obstacle).scale(scaled)
        offset = (int(x2 - x1*1.14), int(y2 - y1))
        overlap = mask1.overlap(mask2, offset)
        return overlap is not None
    
    def pause_menu(self, screen):
        paused = True
        font = pygame.font.Font(None, 74)

        resume_button_rect = pygame.Rect(screen_width // 2 - 125, screen_height // 2 - 60, 250, 50)
        options_button_rect = pygame.Rect(screen_width // 2 - 125, screen_height // 2, 250, 50)
        quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

        def resume_game():
            nonlocal paused
            paused = False

        def open_options():
            self.options_menu(screen)

        def quit_game():
            pygame.quit()
            quit()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT or event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_o:
                        self.options_menu(screen)
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_p:
                        paused = False

            screen.fill(white)
            self.draw_transparent_background(screen, 150)  # Background transparency

            display_text("Pontuações:", 36, white, screen_width // 2 - 100, screen_height // 2 - 100)
            draw_button(screen, "Continuar", font, black, resume_button_rect,white, resume_game)
            draw_button(screen, "Opções", font, black, options_button_rect,white, open_options)
            draw_button(screen, "Sair", font, black, quit_button_rect,white, quit_game)
            pygame.display.update()

    def options_menu(self, screen):
        self.options_open = True
        selected_resolution = resolution
        # Fontes
        large_font = pygame.font.Font(None, 74)
        font = pygame.font.Font(None, 36)
        master_volume = 0.5
        sfx_volume = 0.5
        music_volume = 0.5
        ambient_volume = 0.5
        options = Options()

        while self.options_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options_open = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if master_volume_rect.collidepoint(mouse_x, mouse_y):
                        master_volume = adjust_slider_value(master_volume_rect.x, master_volume_rect.y, master_volume_rect.width, master_volume)
                    elif sfx_volume_rect.collidepoint(mouse_x, mouse_y):
                        sfx_volume = adjust_slider_value(sfx_volume_rect.x, sfx_volume_rect.y, sfx_volume_rect.width, sfx_volume)
                    elif music_volume_rect.collidepoint(mouse_x, mouse_y):
                        music_volume = adjust_slider_value(music_volume_rect.x, music_volume_rect.y, music_volume_rect.width, music_volume)
                    elif ambient_volume_rect.collidepoint(mouse_x, mouse_y):
                        ambient_volume = adjust_slider_value(ambient_volume_rect.x, ambient_volume_rect.y, ambient_volume_rect.width, ambient_volume)

            screen.fill(white)
            self.draw_text('Menu de Opções', large_font, black, screen, 20, 20)

            # Modos de Tela
            self.draw_text('Modo de Tela:', font, black, screen, 20, 100)
            draw_button(screen, 'Fullscreen' if fullscreen else 'Windowed Fullscreen', font, black, pygame.Rect(250, 100, 200, 40), white, options.toggle_fullscreen)

            # Resolução
            self.draw_text('Resolução:', font, black, screen, 20, 160)
            resolution_options = ['800x600', '1024x768', '1280x720']
            for i, res in enumerate(resolution_options):
                draw_button(screen, res, font, black, pygame.Rect(250, 160 + i * 50, 200, 40), white, lambda r=res: options.change_resolution(tuple(map(int, r.split('x')))))

            # Linguagem
            self.draw_text('Linguagem:', font, black, screen, 20, 320)
            draw_button(screen, language, font, black, pygame.Rect(250, 320, 200, 40), white, options.change_language)

            # Volumes
            self.draw_text('Volume Mestre:', font, black, screen, 20, 380)
            master_volume_rect = pygame.Rect(250, 380, 300, 40)
            draw_slider(screen, master_volume_rect.x, master_volume_rect.y, master_volume_rect.width, master_volume_rect.height, master_volume)

            self.draw_text('Volume de Efeitos Sonoros:', font, black, screen, 20, 440)
            sfx_volume_rect = pygame.Rect(250, 440, 300, 40)
            draw_slider(screen, sfx_volume_rect.x, sfx_volume_rect.y, sfx_volume_rect.width, sfx_volume_rect.height, sfx_volume)

            self.draw_text('Volume da Música:', font, black, screen, 20, 500)
            music_volume_rect = pygame.Rect(250, 500, 300, 40)
            draw_slider(screen, music_volume_rect.x, music_volume_rect.y, music_volume_rect.width, music_volume_rect.height, music_volume)

            self.draw_text('Som Ambiente:', font, black, screen, 20, 560)
            ambient_volume_rect = pygame.Rect(250, 560, 300, 40)
            draw_slider(screen, ambient_volume_rect.x, ambient_volume_rect.y, ambient_volume_rect.width, ambient_volume_rect.height, ambient_volume)

            pygame.display.update()

    def draw_transparent_background(self, screen, alpha):
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))  # Alpha value (0-255)
            screen.blit(overlay, (0, 0))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

class Menu:
    def __init__(self):
        self.master_volume = 1.0
        self.sfx_volume = 1.0
        self.music_volume = 1.0
        self.ambient_volume = 1.0
        self.options_open = False

    def draw_transparent_background(self, screen, alpha):
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, alpha))  # Alpha value (0-255)
        screen.blit(overlay, (0, 0))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self, screen):
        menu_active = True
        font = pygame.font.Font(None, 74)
        game_logic = GameLogic()

        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

        def start_game():
            nonlocal menu_active
            menu_active = False
            game_logic.main_loop(screen)

        def quit_game():
            pygame.quit()
            quit()

        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Pressione Enter para iniciar o jogo
                        start_game()

            screen.blit(back_menu, (-35, 0))

            draw_button(screen, "Iniciar", font, white, start_button_rect, black, start_game())
            draw_button(screen, "Sair", font, white, quit_button_rect, black, quit_game)
            pygame.display.update()

def initialize_game():
    pygame.init()
    pygame.display.set_caption(title)
    return pygame.display.set_mode((screen_width, screen_height))

def main_game_loop(screen):
    menu = Menu()
    menu.main_menu(screen)

def run_game():
    screen = initialize_game()
    main_game_loop(screen)

if __name__ == "__main__":
    run_game()
