import pygame
import random
from config import screen_width, screen_height, track_left_limit, track_right_limit, white, black
from graphics import Renderer, display_text, draw_with_perspective, Animation, Spritesheet
from sprite import car_image, car_mask, obstacle_images, pad_image, pad_mask, back_image, back_menu, slow_obstacle_image, slow_obstacle_mask, car_height, car_width

class GameLogic:
    def __init__(self):
        self.car_x = (screen_width * 0.45)
        self.car_y = (screen_height * 0.8)
        self.car_x_change = 0
        self.speed_player_r = 5
        self.speed_player_l = -5

        self.speed_basic = 3
        self.speed_boost = self.speed_basic * 2
        self.speed_slow = self.speed_basic / 2
        
        self.obst_startx = random.randrange(0, screen_width - car_width)
        self.obst_starty = -car_height
        self.obst_speed = self.speed_basic
        self.obst_scale = 0
        self.obstacle_image = random.choice(obstacle_images)
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)

        self.pad_startx = random.randrange(0, screen_width - car_width)
        self.pad_starty = -car_height
        self.pad_scale = 0
        self.pad_speed = self.speed_basic

        self.slow_obst_startx = (track_left_limit + track_right_limit) // 2
        self.slow_obst_starty = screen_height // 2
        self.slow_obst_scale = 0.1
        self.slow_obst_speed = self.speed_basic

        
        self.pads_collected = 0
        self.boost_active = False
        self.boost_timer = 0

        self.road_speed = self.speed_basic
        self.distance = 0
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.spritesheet = Spritesheet('./sprit_road-0.png')
        frame_width = 600
        frame_height = 700
        num_frames = 64

        self.animation = Animation(self.spritesheet, frame_width, frame_height, num_frames)
        self.sprite_pos = pygame.Rect(100, 100, frame_width, frame_height)

        self.game_exit = False

    def crash(self, screen, distance):
        crashed = True
        clock = pygame.time.Clock()

        while crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        self.main_loop(screen)  # Reinicia o jogo
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            
            # Exibe mensagem de "Game Over" e distância percorrida
            screen.fill((0, 0, 0))
            display_text("Você bateu!", 36, (255, 0, 0), screen_width // 2 - 100, screen_height // 2 - 50)
            display_text(f"Distância: {int(distance)}", 30, white, screen_width // 2 - 100, screen_height // 2)
            display_text("Pressione R para reiniciar ou Q para sair", 30, white, screen_width // 2 - 200, screen_height // 2 + 50)
            
            pygame.display.update()
            clock.tick(15)

    def reset(self):
        self.car_x = (screen_width * 0.45)
        self.car_y = (screen_height * 0.8)
        self.car_x_change = 0
        self.speed_player_r = 5
        self.speed_player_l = -5

        self.speed_basic = 3
        self.speed_boost = self.speed_basic * 2
        self.speed_slow = self.speed_basic / 2
        
        self.obst_startx = random.randrange(0, screen_width - car_width)
        self.obst_starty = screen_height//2
        self.obst_speed = self.speed_basic
        self.obst_scale = 0
        self.obstacle_image = random.choice(obstacle_images)
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)

        self.pad_startx = random.randrange(0, screen_width - car_width)
        self.pad_starty = -car_height
        self.pad_scale = 0
        self.pad_speed = self.speed_basic

        self.slow_obst_startx = (track_left_limit + track_right_limit) // 2
        self.slow_obst_starty = screen_height // 2
        self.slow_obst_scale = 0.1
        self.slow_obst_speed = self.speed_basic

        
        self.pads_collected = 0
        self.boost_active = False
        self.boost_timer = 0

        self.road_speed = self.speed_basic
        self.distance = 0
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
    def main_loop(self, screen):

        while not self.game_exit:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_change = self.speed_player_l
                    elif event.key == pygame.K_RIGHT:
                        self.car_x_change = self.speed_player_r
                    elif event.key == pygame.K_SPACE and self.pads_collected >= 3:
                        self.boost_active = True
                        self.boost_timer = pygame.time.get_ticks()
                        self.pads_collected = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.car_x_change = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        # menu.pause(screen)
                        self.clock.tick()

            self.render(screen)
            self.car_x += self.car_x_change

            if self.boost_active:
                if pygame.time.get_ticks() - self.boost_timer < 5000:
                    self.obst_speed = self.speed_boost
                    self.pad_speed = self.speed_boost
                    self.road_speed = self.speed_boost
                    self.pads_collected = 0
                else:
                    self.boost_active = False
                    self.obst_speed = self.speed_basic
                    self.pad_speed = self.speed_basic
                    self.road_speed = self.speed_basic

            if self.car_x > track_right_limit - car_width:
                self.car_x = track_right_limit - car_width
            if self.car_x < track_left_limit:
                self.car_x = track_left_limit

            self.obst_starty += self.obst_speed
            self.pad_starty += self.pad_speed
            self.slow_obst_starty += self.slow_obst_speed
            self.distance += self.road_speed

            if self.pad_starty > screen_height:
                self.pad_starty = screen_height//2 - car_height
                self.pad_startx = random.randrange(track_left_limit, track_right_limit)

            if self.obst_starty > screen_height:
                self.obst_starty = screen_height//2 - car_height
                self.obst_startx = random.randrange(track_left_limit, track_right_limit)

            if self.slow_obst_starty > screen_height:
                self.slow_obst_starty = screen_height//2 - car_height
                self.slow_obst_startx = random.randrange(track_left_limit, track_right_limit)

            self.animation.update(dt)
            self.render(screen)

            if self.collision_check(self.car_x, self.car_y, car_mask, self.obst_startx, self.obst_starty, self.obstacle_mask):
                self.crash(screen, self.distance)

            if self.collision_check(self.car_x, self.car_y, car_mask, self.pad_startx, self.pad_starty, pad_mask):
                self.pads_collected += 1
                self.pad_starty = screen_height + car_height

            if self.collision_check(self.car_x, self.car_y, car_mask, self.slow_obst_startx, self.slow_obst_starty, slow_obstacle_mask):
                self.obst_speed = self.speed_slow

            pygame.display.update()

        pygame.quit()

    def render(self, screen):
        renderer = Renderer(screen)
        screen.fill(white)
        renderer.render_animation(self.animation, self.sprite_pos.x, self.sprite_pos.y)
        renderer.render_obstacle(self.obst_startx, self.obst_starty)
        renderer.render_pad( self.pad_startx, self.pad_starty)
        renderer.render_slow_obstacle( self.slow_obst_startx, self.slow_obst_starty)
        renderer.render_car(self.car_x, self.car_y)
        renderer.render_hud(self.distance, self.pads_collected, self.boost_active, self.boost_timer, black)

    def collision_check(self, x1, y1, mask1, x2, y2, mask2):
        offset = (int(x2 - x1), int(y2 - y1))
        overlap = mask1.overlap(mask2, offset)
        return overlap is not None
    