import pygame 
from config import screen_width, screen_height, title
from menus import Menu

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
