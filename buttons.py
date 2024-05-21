import pygame
from config import black, gray, resolution, fullscreen, language

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

def draw_button(screen, text, font, color, rect, action=None):
    button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    button_surface.fill((*color, 150))  # 150 = AlphaValue:(0-255)

    screen.blit(button_surface, rect.topleft)
    text_surface = font.render(text, True, (0, 0, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()


def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(resolution)

def change_resolution(new_resolution):
    global resolution
    resolution = new_resolution
    if fullscreen:
        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(resolution)

def change_language():
    global language
    languages = ['English', 'Português', 'Español', 'Français']
    current_index = languages.index(language)
    language = languages[(current_index + 1) % len(languages)]

        
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def draw_slider(screen, x, y, w, h, value):
    pygame.draw.rect(screen, gray, (x, y, w, h))
    handle_pos = int(x + (w - 20) * value)
    pygame.draw.rect(screen, black, (handle_pos, y, 20, h))

def adjust_slider_value(x, y, w, value):
    mouse_x = pygame.mouse.get_pos()[0]
    new_value = (mouse_x - x) / (w - 20)
    return max(0, min(1, new_value))