import pygame

screen_width = 800
screen_height = 600
resolution = (screen_width, screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))
title = "Corrida de Fórmula E"
fullscreen = False
language = 'English'
master_volume = 0.5
sfx_volume = 0.5
music_volume = 0.5
ambient_volume = 0.5

# Definir cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
light_gray = (220, 220, 220)
black_alpha = pygame.Color(0, 0, 0, 15)
