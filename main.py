import pygame
from config import screen_width, screen_height, title
from game_logic import GameLogic
from menus import Menu


def initialize_game():
    pygame.init()
    pygame.display.set_caption(title)
    return pygame.display.set_mode((screen_width, screen_height))

def main_game_loop(screen):
    game_logic = GameLogic()
    menu = Menu()
    menu.main_menu(screen)
    
    while not game_logic.game_exit:
        dt = game_logic.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_logic.game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game_logic.car_x_change = game_logic.speed_player_l
                elif event.key == pygame.K_RIGHT:
                    game_logic.car_x_change = game_logic.speed_player_r
                elif event.key == pygame.K_SPACE and game_logic.pads_collected >= 3:
                    game_logic.boost_active = True
                    game_logic.boost_timer = pygame.time.get_ticks()
                    game_logic.pads_collected = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    game_logic.car_x_change = 0
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    menu.pause_menu(screen)

        pygame.display.update()  # Atualiza a lógica do jogo
        
        screen.fill((0, 0, 0))  # Limpa a tela

        pygame.display.update()

    pygame.quit()
    quit()


def run_game():
    screen = initialize_game()
    main_game_loop(screen)

if __name__ == "__main__":
    run_game()
