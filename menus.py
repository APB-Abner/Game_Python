import pygame
import asyncio
from config import screen_width, screen_height, white, black, fullscreen, language, resolution
from buttons import draw_button, toggle_fullscreen, change_language, draw_slider, adjust_slider_value, change_resolution
from game_logic import GameLogic
from sprite import back_menu

class Menu:
    def __init__(self):
        self.master_volume = 1.0
        self.sfx_volume = 1.0
        self.music_volume = 1.0
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

    async def main_menu(self, screen):
        menu_active = True
        font = pygame.font.Font(None, 74)
        game_logic = GameLogic()

        start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)

        async def start_game():
            nonlocal menu_active
            menu_active = False
            await game_logic.main_loop(screen)

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
                        await start_game()

            screen.blit(back_menu, (-35, 0))

            draw_button(screen, "Iniciar", font, white, start_button_rect, black, lambda: asyncio.ensure_future(start_game()))
            draw_button(screen, "Sair", font, white, quit_button_rect, black, quit_game)
            pygame.display.update()
            await asyncio.sleep(0)  # Permitir que outras coroutines rodem
