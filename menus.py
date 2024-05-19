import pygame
from config import screen_width, screen_height, white, black
from buttons import draw_button, Button
from sprite import back_menu

def draw_transparent_background(screen, alpha):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, alpha))  # Alpha value (0-255)
    screen.blit(overlay, (0, 0))

# Função para exibir o menu principal
def main_menu(screen):
    menu_active = True
    font = pygame.font.Font(None, 74)

    start_button_rect = pygame.Rect(screen_width // 2-100, screen_height // 2, 200, 50)
    quit_button_rect = pygame.Rect(screen_width // 2-100, screen_height // 2 + 60, 200, 50)
    

    def start_game():
        nonlocal menu_active
        menu_active = False

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
                    menu_active = False

        screen.fill(white)
        screen.blit(back_menu, (-35, 0))

        draw_button(screen, "Iniciar", font, black, start_button_rect, start_game)
        draw_button(screen, "Sair", font, black, quit_button_rect, quit_game)
        pygame.display.update()

#Função para exibir o menu de pause
def pause_menu(screen):
    paused = True
    font = pygame.font.Font(None, 74)


    resume_button_rect = pygame.Rect(screen_width // 2-125, screen_height // 2, 250, 50)
    quit_button_rect = pygame.Rect(screen_width // 2-100, screen_height // 2 + 60, 200, 50)

    def resume_game():
        nonlocal paused
        paused = False

    def quit_game():
        pygame.quit()
        quit()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        draw_transparent_background(screen, 150)  # Background transparency

        draw_button(screen, "Continuar", font, black, resume_button_rect, resume_game)
        draw_button(screen, "Sair", font, black, quit_button_rect, quit_game)
        pygame.display.update()