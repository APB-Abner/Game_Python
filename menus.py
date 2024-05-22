import pygame
from config import screen_width, screen_height, white, black, fullscreen, language, master_volume, sfx_volume, music_volume, ambient_volume, resolution
from function_basic import display_text
from buttons import draw_button, Button, toggle_fullscreen, change_language, draw_slider, adjust_slider_value, change_resolution
from sprite import back_menu

WIDTH, HEIGHT = screen_width, screen_height




def draw_transparent_background(screen, alpha):
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, alpha))  # Alpha value (0-255)
    screen.blit(overlay, (0, 0))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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


    resume_button_rect = pygame.Rect(screen_width // 2-125, screen_height // 2-60, 250, 50)
    options_button_rect = pygame.Rect(screen_width // 2 - 125, screen_height // 2, 250, 50)
    quit_button_rect = pygame.Rect(screen_width // 2-100, screen_height // 2 + 60, 200, 50)

    def resume_game():
        nonlocal paused
        paused = False

    def open_options():
        options_menu(screen)

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
        draw_button(screen, "Opções", font, black, options_button_rect, open_options)
        draw_button(screen, "Sair", font, black, quit_button_rect, quit_game)
        pygame.display.update()

def options_menu(screen):
    global master_volume, sfx_volume, music_volume, ambient_volume, options_open
    options_open = True
    selected_resolution = resolution
    #Fontes
    large_font = pygame.font.Font(None, 74)
    font = pygame.font.Font(None, 36)

    while options_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options_open = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if master_volume_rect.collidepoint(mouse_x, mouse_y):
                    master_volume = adjust_slider_value(master_volume_rect.x, master_volume_rect.y, master_volume_rect.width, master_volume)
                elif sfx_volume_rect.collidepoint(mouse_x, mouse_y):
                    sfx_volume = adjust_slider_value(sfx_volume_rect.x, sfx_volume_rect.y, sfx_volume_rect.width, sfx_volume)
                elif music_volume_rect.collidepoint(mouse_x, mouse_y):
                    music_volume = adjust_slider_value(music_volume_rect.x, music_volume_rect.y, music_volume_rect.width, music_volume)
                elif ambient_volume_rect.collidepoint(mouse_x, mouse_y):
                    ambient_volume = adjust_slider_value(ambient_volume_rect.x, ambient_volume_rect.y, ambient_volume_rect.width, ambient_volume)

        screen.fill(white)
        draw_text('Menu de Opções', large_font, black, screen, 20, 20)
        
        # Modos de Tela
        draw_text('Modo de Tela:', font, black, screen, 20, 100)
        draw_button(screen, 'Fullscreen' if fullscreen else 'Windowed Fullscreen', font, black, pygame.Rect(250, 100, 200, 40), toggle_fullscreen)
        
        # Resolução
        draw_text('Resolução:', font, black, screen, 20, 160)
        resolution_options = ['800x600', '1024x768', '1280x720']
        for i, res in enumerate(resolution_options):
            draw_button(screen, res, font, black, pygame.Rect(250, 160 + i * 50, 200, 40), lambda r=res: change_resolution(tuple(map(int, r.split('x')))))

        # Linguagem
        draw_text('Linguagem:', font, black, screen, 20, 320)
        draw_button(screen, language, font, black, pygame.Rect(250, 320, 200, 40), change_language)
        
        # Volumes
        draw_text('Volume Mestre:', font, black, screen, 20, 380)
        master_volume_rect = pygame.Rect(250, 380, 300, 40)
        draw_slider(screen, master_volume_rect.x, master_volume_rect.y, master_volume_rect.width, master_volume_rect.height, master_volume)
        
        draw_text('Volume de Efeitos Sonoros:', font, black, screen, 20, 440)
        sfx_volume_rect = pygame.Rect(250, 440, 300, 40)
        draw_slider(screen, sfx_volume_rect.x, sfx_volume_rect.y, sfx_volume_rect.width, sfx_volume_rect.height, sfx_volume)
        
        draw_text('Volume da Música:', font, black, screen, 20, 500)
        music_volume_rect = pygame.Rect(250, 500, 300, 40)
        draw_slider(screen, music_volume_rect.x, music_volume_rect.y, music_volume_rect.width, music_volume_rect.height, music_volume)
        
        draw_text('Som Ambiente:', font, black, screen, 20, 560)
        ambient_volume_rect = pygame.Rect(250, 560, 300, 40)
        draw_slider(screen, ambient_volume_rect.x, ambient_volume_rect.y, ambient_volume_rect.width, ambient_volume_rect.height, ambient_volume)
        
        pygame.display.flip()