import pygame

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
track_left_limit = 100  # Posição X inicial da pista
track_right_limit = screen_width - 100  # Posição X final da pista

# Definição de cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
light_gray = (220, 220, 220)
black_alpha = pygame.Color(0, 0, 0, 15)
