import pygame
import time
import pygame_assets as assets
from sys import exit
"""Simple game with a goal to catch flowers and avoid bad stuff"""


class MainGame:
    def __init__(self):
        """initializes game"""
        pygame.init()
        """title bar"""
        pygame.display.set_caption("Welcome to Blossom \
        by: Tim and Trenton")
        """Create Window"""
        SCR_WIDTH, SCR_HEIGHT = 800, 600
        self.WINDOW = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
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
        for i in range(1, 16):
            self.idle.append(pygame.transform.scale(assets.load.image('Idle ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE))
        for i in range(1, 16):
            self.run_right.append(pygame.transform.scale(assets.load.image('Run ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE))
        for i in range(1, 16):
            img = pygame.transform.scale(assets.load.image('Run ({}).png'.format(i)).convert_alpha(), DEFAULT_SIZE)
            img = pygame.transform.flip(img, True, False)
            self.run_left.append(img)

    def player_movement(self, keys_pressed):
        """Handles player movemnet"""
        if keys_pressed[pygame.K_LEFT]:
            self.x += -10
            self.player_state = self.run_left
        if keys_pressed[pygame.K_RIGHT]:
            self.x += 10
            self.player_state = self.run_right
        if time.time() - self.walk_frame_start > 0.1:
            if self.walk_count < 14:
                self.walk_count += 1
            else:
                self.walk_count = 0
            self.walk_frame_start = time.time()

    def draw_window(self):
        self.WINDOW.fill(self.SKY_COLOR)
        self.WINDOW.blit(self.GROUND_SURFACE,(0,500))
        self.WINDOW.blit(self.player_state[self.walk_count], (self.x,400))
        pygame.display.update()

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
        self.draw_window()


if __name__ == "__main__":
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    game = MainGame()

    """Main game loop"""
    while (running):
        clock.tick(FPS)
        game.level_one()
