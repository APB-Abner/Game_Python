import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo 2D com Sprites")

# Carregar as imagens/sprites
sprite_sheet = pygame.image.load('spritesheet.png').convert_alpha()  # Substitua pelo seu sprite sheet
sprite_width, sprite_height = 95, 217  # Tamanho de cada sprite individual
frames_per_row = 8  # Número de sprites por linha
total_frames = 60

# Função para obter um sprite específico do sprite sheet
def get_sprite(frame):
    if frame >= total_frames:
        frame = frame % total_frames
    row = frame // frames_per_row
    col = frame % frames_per_row
    sprite = sprite_sheet.subsurface((col * sprite_width, row * sprite_height, sprite_width, sprite_height))
    return sprite

# Coordenadas do personagem
x, y = screen_width // 2, screen_height // 2
speed = 5

# Índices para os sprites de animação
current_frame = 0
frames_per_animation = 40  # Número de frames por animação
frame_count = 0

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento do personagem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
        current_frame = (current_frame - 1) % frames_per_animation
    if keys[pygame.K_RIGHT]:
        x += speed
        current_frame = (current_frame - 1) % frames_per_animation
    if keys[pygame.K_UP]:
        y -= speed
        current_frame = (current_frame - 1) % frames_per_animation
    if keys[pygame.K_DOWN]:
        y += speed
        current_frame = (current_frame - 1) % frames_per_animation

    # Atualizar a tela
    screen.fill((0, 0, 0))  # Limpa a tela com a cor preta
    sprite = get_sprite(current_frame)  # Obtém o sprite atual
    screen.blit(sprite, (x, y))  # Desenha o sprite na tela

    pygame.display.flip()  # Atualiza a tela

    frame_count += 1
    if frame_count >= 10:  # Controla a velocidade da animação
        current_frame = (current_frame - 1) % frames_per_animation
        frame_count = 0

    pygame.time.Clock().tick(60)  # Controla a taxa de quadros (FPS)
