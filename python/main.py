import pygame 
from config import screen_width, screen_height, title
from menus import Menu

def initialize_game():
    name_player= input("Enter your name: ")
    pygame.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen, name_player

def main_game_loop(screen, name_player):
    menu = Menu()
    menu.main_menu(screen, name_player)

def run_game():
    screen, name_player = initialize_game()
    main_game_loop(screen, name_player)

if __name__ == "__main__":
    run_game()
