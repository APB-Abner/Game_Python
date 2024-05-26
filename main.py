import pygame 
import asyncio                                                                                                                                                       
from config import screen_width, screen_height, title
from menus import Menu

def initialize_game():
    pygame.init()
    pygame.display.set_caption(title)
    return pygame.display.set_mode((screen_width, screen_height))

async def main_game_loop(screen):
    menu = Menu()
    await menu.main_menu(screen)
    
async def run_game():
    screen = initialize_game()
    await main_game_loop(screen)

if __name__ == "__main__":
    asyncio.run(run_game())
