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
        pygame.mixer.init()
        self.start_time = pygame.time.get_ticks()
        print(self.start_time // 1000)
        self.game_state = "intro"
        self.score = 0
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
        self.cur_player_state = self.player_state
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
        self.CHERRY_SIZE = (64,64)
        for i in range (0, 16):
            self.cherry.append(pygame.transform.scale(assets.load.image('cherry ({}).png'.format(i)).convert_alpha(),self.CHERRY_SIZE))
        self.cherry_rect = pygame.Rect(self.fruit_x, -50, self.CHERRY_SIZE[0], self.CHERRY_SIZE[1] - 50)
        """setup bee"""
        self.bee_timer = 10
        self.bee_spawn = False
        self.bee_speed = 8
        self.bee_x = random.randrange(0, self.SCR_WIDTH)
        self.bee = []
        self.BEE_SIZE = (64, 64)
        for i in range (1, 8):
            self.bee.append(pygame.transform.scale(assets.load.image('bee ({}).png'.format(i)).convert_alpha(), self.BEE_SIZE))
        self.bee_rect = pygame.Rect(self.bee_x, -50, self.BEE_SIZE[0] - 100, self.BEE_SIZE[1])
        """Create Clouds"""
        self.CLOUD_SIZE = (512, 256)
        self.cloud_speed = 1
        self.cloud_x = 850
        self.cloud_y = 0
        self.cloud = pygame.transform.scale(assets.load.image('cloud (1).png'.format(i)).convert_alpha(), self.CLOUD_SIZE)
        self.cloud_rect = pygame.Rect(self.cloud_x, self.cloud_y, self.CLOUD_SIZE[0], self.CLOUD_SIZE[1])
        self.cloud_2 = pygame.transform.scale(assets.load.image('cloud (3).png'.format(i)).convert_alpha(), self.CLOUD_SIZE)
        self.cloud_rect_2 = pygame.Rect(self.cloud_x + 500, self.cloud_y - 50, self.CLOUD_SIZE[0], self.CLOUD_SIZE[1])
        """Create Music and sound effects"""
        self.music = assets.load.music('Strike the Earth!.mp3')
        self.game_start_sound = assets.load.sound('game_start.ogg')
        self.bee_sting_sound = assets.load.sound('pop.flac')
        self.coin_sound = assets.load.sound('coin.wav')

    def detect_collisions(self):
        """Detects collisions and updates the score accordingly"""
        if self.rect.colliderect(self.cherry_rect):
            self.coin_sound.play()
            self.cherry_rect.y = -50
            self.score += 1
            self.cherry_rect.x = random.randrange(0, self.SCR_WIDTH)
        if self.rect.colliderect(self.bee_rect) and (self.bee_rect.y < self.SCR_HEIGHT - 115):
            self.bee_sting_sound.play()
            self.bee_spawn = False
            self.bee_rect.y = -50
            self.bee_rect.x = random.randrange(0, self.SCR_WIDTH)
            if self.score - 2 < 0:
                self.score = 0
            else:
                self.score += -2


    def fruit_movement(self):
        self.WINDOW.blit(self.cherry[self.walk_count], (self.cherry_rect.x, self.cherry_rect.y))
        self.cherry_rect.y += self.FRUIT_SPEED
        if self.cherry_rect.y > self.SCR_HEIGHT:
            self.cherry_rect.x = random.randrange(0, self.SCR_WIDTH - 100)
            self.cherry_rect.y = -50

    def cloud_movement(self):
        self.WINDOW.blit(self.cloud, (self.cloud_rect.x, self.cloud_rect.y))
        self.cloud_rect.x -= self.cloud_speed
        if self.cloud_rect.x < -1024:
            self.cloud_rect.x = 850
            self.cloud_rect.y = random.randrange(0, 50)
        self.WINDOW.blit(self.cloud_2, (self.cloud_rect_2.x - 50, self.cloud_rect_2.y))
        self.cloud_rect_2.x = self.cloud_rect.x + 512



    def bee_movement(self):
        """Handles bee movement and spawning"""
        if ((pygame.time.get_ticks() - self.start_time) % 100 == 0) and not self.bee_spawn:
            self.bee_rect.x = random.randrange(0, self.SCR_WIDTH - 100)
            self.bee_rect.y = -50
            self.bee_spawn = True
        if self.bee_spawn:
            self.WINDOW.blit(self.bee[0], (self.bee_rect.x, self.bee_rect.y))
            self.bee_rect.y += self.bee_speed
            if self.bee_rect.y > self.SCR_HEIGHT - 100:
                self.bee_spawn = False

    def player_movement(self, keys_pressed):
        """Handles player movemnet"""
        if self.cur_player_state is not self.player_state:
            self.cur_player_state = self.player_state
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
        if self.game_state == "game_exit":
            self.game_exit()

    def draw_score(self):
        """Draws and controls the score on the screen"""
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render("Score: {}".format(self.score), True, (255, 255, 255))
        self.WINDOW.blit(text, (710, 10))
        if self.score < 0:
            self.score = 0

    def draw_timer(self):
        """Displays timer in the top right"""
        self.current_time = 60 - ((pygame.time.get_ticks()-self.start_ticks)//1000)
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render("Timer: {}".format(self.current_time), True, (255, 255, 255))
        self.WINDOW.blit(text, (10, 10))
        if self.current_time == 0:
            self.game_state = "game_exit"

    def draw_background(self):
        """Draws the basic background"""
        self.WINDOW.fill(self.SKY_COLOR)
        self.WINDOW.blit(self.GROUND_SURFACE,(0,500))
        self.WINDOW.blit(self.player_state[self.walk_count], (self.rect.x, self.rect.y))

    def draw_intro_window(self):
        """Draws Window for intro"""
        self.draw_background()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Ready?(Press space bar to start)", True, (255, 255, 255))
        self.WINDOW.blit(text, (150, 250))
        #pygame.draw.rect(self.WINDOW, (0, 0, 0), self.cherry_rect, 4)
        pygame.display.update()

    def draw_one_window(self):
        """Window for level one"""
        self.draw_background()
        self.draw_timer()
        self.draw_score()
        self.cloud_movement()
        self.fruit_movement()
        self.bee_movement()
        # """pygame.draw.rect(self.WINDOW, (0, 0, 0), self.rect, 4)"""
        #pygame.draw.rect(self.WINDOW, (0, 0, 0), self.cherry_rect, 4)
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
                        self.start_ticks = pygame.time.get_ticks()
                        self.game_start_sound.play()
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_volume(0.3)
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
        self.detect_collisions()
        self.draw_one_window()

    def game_exit(self):
        """Displays Exit screen"""
        self.draw_background()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Score: {}".format(self.score), True, (255, 255, 255))
        self.WINDOW.blit(text, (150, 250))
        event_list = pygame.event.get()
        for event in event_list:
                """ player exit"""
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.game_state = "intro"
                    self.start_ticks = pygame.time.get_ticks()
                    self.score = 0
        pygame.display.update()

if __name__ == "__main__":
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    game = MainGame()

    """Main game loop"""
    while (running):
        clock.tick(FPS)
        game.state_manager()
