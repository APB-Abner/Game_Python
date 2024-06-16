import pygame 
from config import screen_width, screen_height, title
from menus import Menu

def initialize_game():
    pygame.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen

def main_game_loop(screen):
    menu = Menu()
    menu.main_menu(screen)

def run_game():
    screen, name_player = initialize_game()
    main_game_loop(screen, name_player)

if __name__ == "__main__":
    run_game()
