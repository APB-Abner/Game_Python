import pygame
from config import resolution, language, screen_width, screen_height, gray, black

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def draw_button(screen, text, font, color, rect, color_text, action=None):
    
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if rect.collidepoint(mouse) and click[0] == 1 and action:
        action()

class Options:
    def toggle_fullscreen():
        global fullscreen
        fullscreen = not fullscreen
        if fullscreen:
            pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((screen_width, screen_height))

    def change_language():
        global language
        language = 'English' if language == 'Portuguese' else 'Portuguese'

    def change_resolution(new_resolution):
        global resolution
        resolution = new_resolution
        pygame.display.set_mode(resolution)

    def draw_slider(screen, x, y, w, h, value):
        pygame.draw.rect(screen, gray, (x, y, w, h))
        handle_pos = int(x + (w - 20) * value)
        pygame.draw.rect(screen, black, (handle_pos, y, 20, h))

    def adjust_slider_value(x, y, w, value):
        mouse_x = pygame.mouse.get_pos()[0]
        new_value = (mouse_x - x) / (w - 20)
        return max(0, min(1, new_value))