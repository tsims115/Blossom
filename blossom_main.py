import pygame
import time
import random
import math
import pygame_assets as assets
from sys import exit

"""Simple game with a goal to catch flowers and avoid bad stuff"""


class MainGame:
    def __init__(self):
        """initializes game"""
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.game_state = "intro"
        """title bar"""
        pygame.display.set_caption("Welcome to Blossom \
        by: Tim and Trenton")
        """Create Window"""
        self.SCR_WIDTH, self.SCR_HEIGHT = 800, 600
        self.WINDOW = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))
        """Create Ground"""
        GROUND_WIDTH, GROUND_HEIGHT = 800, 200
        self.GROUND_SURFACE = pygame.Surface((GROUND_WIDTH, GROUND_HEIGHT))
        self.GROUND_SURFACE.fill('LawnGreen')
        self.SKY_COLOR = (77, 204, 255)
        self.x = 400
        """Creates Player"""
        DEFAULT_SIZE = (224, 224)
        self.walk_count = 0
        self.idle = []
        self.run_left = []
        self.run_right = []
        self.player_state = self.idle
        self.walk_frame_start = 0
        self.cur_state = self.player_state
        for i in range(1, 16):
            self.idle.append(pygame.transform.scale(assets.load.image('Idle ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE))
        for i in range(1, 16):
            self.run_right.append(pygame.transform.scale(assets.load.image('RunRight ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE))
        for i in range(1, 16):
            img = pygame.transform.scale(assets.load.image('RunLeft ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE)
            self.run_left.append(img)
        self.rect = pygame.Rect(400, 400, DEFAULT_SIZE[0] - 100, DEFAULT_SIZE[1])
        """create fruit"""
        self.FRUIT_SPEED = 5
        self.fruit_x = random.randrange(0, self.SCR_WIDTH)
        # fruit_y = -50
        self.cherry = []
        CHERRY_SIZE = (64,64)
        for i in range (0, 16):
            self.cherry.append(pygame.transform.scale(assets.load.image('cherry ({}).png'.format(i)).convert_alpha(),CHERRY_SIZE))
        self.cherry_rect = pygame.Rect(self.fruit_x, -50, DEFAULT_SIZE[0] - 100, DEFAULT_SIZE[1])
        """setup bee"""
        self.bee_timer = 10
        self.bee_spawn = False
        self.bee_speed = 8
        self.bee_x = random.randrange(0, self.SCR_WIDTH)
        self.bee = []
        bee_size = (64, 64)
        for i in range (1, 8):
            self.bee.append(pygame.transform.scale(assets.load.image('bee ({}).png'.format(i)).convert_alpha(), bee_size))
        self.bee_rect = pygame.Rect(self.bee_x, -50, DEFAULT_SIZE[0] - 100, DEFAULT_SIZE[1])

    def fruit_movement(self):
        self.WINDOW.blit(self.cherry[self.walk_count], (self.cherry_rect.x, self.cherry_rect.y))
        self.cherry_rect.y += self.FRUIT_SPEED
        if self.cherry_rect.y > self.SCR_HEIGHT:
            self.cherry_rect.x = random.randrange(0, self.SCR_WIDTH)
            self.cherry_rect.y = -50

    def bee_movement(self):
        """Handles bee movement and spawning"""
        if ((pygame.time.get_ticks() - self.start_time) % 100 == 0) and not self.bee_spawn:
            if self.bee_spawn:
                self.bee_spawn = False
                self.bee_timer = random.randrange(3, 11)
            else:
                self.bee_rect.x = random.randrange(0, self.SCR_WIDTH)
                self.bee_rect.y = -50
                self.bee_spawn = True
        if self.bee_spawn:
            self.WINDOW.blit(self.bee[0], (self.bee_rect.x, self.bee_rect.y))
            self.bee_rect.y += self.bee_speed
            if self.bee_rect.y > self.SCR_HEIGHT:
                self.bee_spawn = False

    def player_movement(self, keys_pressed):
        """Handles player movemnet"""
        if self.cur_state is not self.player_state:
            self.cur_state = self.player_state
            self.walk_count = 0
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x += -10
            self.player_state = self.run_left
            if self.rect.x < 0:
                self.rect.x = 0
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += 10
            self.player_state = self.run_right
            if self.rect.x > 690:
                self.rect.x = 690
        if time.time() - self.walk_frame_start > 0.1:
            if self.walk_count < 14:
                self.walk_count += 1
            else:
                self.walk_count = 0
            self.walk_frame_start = time.time()

    def state_manager(self):
        """Manages state and what level the game is on"""
        if self.game_state == "intro":
            self.intro()
        if self.game_state == "level_one":
            self.level_one()

    def draw_intro_window(self):
        """Draws Window for intro"""
        self.WINDOW.fill(self.SKY_COLOR)
        self.WINDOW.blit(self.GROUND_SURFACE,(0,500))
        self.WINDOW.blit(self.player_state[self.walk_count], (self.rect.x, self.rect.y))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Ready?(Press space bar to start)", True, (255, 255, 255))
        self.WINDOW.blit(text, (150, 250))
        pygame.draw.rect(self.WINDOW, (0, 0, 0), self.rect, 4)
        pygame.display.update()

    def draw_one_window(self):
        """Window for level one"""
        self.WINDOW.fill(self.SKY_COLOR)
        self.WINDOW.blit(self.GROUND_SURFACE,(0,500))
        self.WINDOW.blit(self.player_state[self.walk_count], (self.rect.x, self.rect.y))
        self.fruit_movement()
        self.bee_movement()
        pygame.draw.rect(self.WINDOW, (0, 0, 0), self.rect, 4)
        pygame.display.update()

    def intro(self):
        """Start screen"""
        event_list = pygame.event.get()
        for event in event_list:
                """ player exit"""
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_state = "level_one"
        self.draw_intro_window()

    def level_one(self):
        """First level of the game"""
        event_list = pygame.event.get()
        if len(event_list) == 0:
            self.player_state = self.idle
        else:
            for event in event_list:
                """ player exit"""
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        keys_pressed = pygame.key.get_pressed()
        self.player_movement(keys_pressed)
        self.draw_one_window()


if __name__ == "__main__":
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    game = MainGame()

    """Main game loop"""
    while (running):
        clock.tick(FPS)
        game.state_manager()
