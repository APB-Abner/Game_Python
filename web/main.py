import pygame
import random
import asyncio

# Inicializa o Pygame
pygame.init()

# Definindo constantes
screen_width = 800
screen_height = 600
resolution = (screen_width, screen_height)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Corrida de Fórmula E")

# Definindo cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Limites da pista
track_left_limit = 175
track_right_limit = screen_width - 175

# Carregar imagens
car_image = pygame.image.load('./img/car.png')
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
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < track_right_limit:
            self.rect.x += 5

# Classe do Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(obstacle_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(track_left_limit, track_right_limit - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 1.5
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(track_left_limit, track_right_limit - self.rect.width)
            self.rect.y = -self.rect.height
            self.speed *= 1.05  # Incrementa a velocidade com o tempo

# Funções adicionais do código original
class GameLogic:
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
        self.obst_starty = screen_height - self.rect.height // 2
        self.pad_starty = screen_height - self.rect.height // 2
        self.slow_obst_starty = screen_height - self.rect.height // 2
        
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
        
        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

        def start_game():
            nonlocal menu_active
            menu_active = False
            game_logic = GameLogic()
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

            screen.fill(black)
            self.draw_text("Iniciar", font, white, screen, screen_width // 2 - 50, screen_height // 2 - 25)
            self.draw_text("Sair", font, white, screen, screen_width // 2 - 50, screen_height // 2 + 35)
            pygame.display.update()

# Loop principal do jogo
async def game_loop():
    jogador = Jogador()
    obstaculos = pygame.sprite.Group()
    
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(jogador)
    
    for _ in range(5):  # Adicionar alguns obstáculos
        obstaculo = Obstaculo()
        todos_sprites.add(obstaculo)
        obstaculos.add(obstaculo)
    
    rodando = True
    clock = pygame.time.Clock()
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        todos_sprites.update()

        if pygame.sprite.spritecollide(jogador, obstaculos, False, pygame.sprite.collide_mask):
            print("Game Over")
            rodando = False

        screen.fill(black)
        todos_sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(30)
    
    pygame.quit()
    await asyncio.sleep(0)

if __name__ == "__main__":
    game_logic = GameLogic()
    game_logic.main_menu(screen)
    asyncio.run(game_loop())
