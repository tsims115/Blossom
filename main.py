import pygame
import pygame_assets as assets
from sys import exit
"""Simple game with a goal to catch flowers and avoid bad stuff"""

"""init pygame"""
pygame.init()

"""set frames per second"""
FPS = 60

"""create screen"""
WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

"""create sky"""
SKY_COLOR = (77, 204, 255)
WINDOW.fill(SKY_COLOR)

"""create ground"""
GROUND_WIDTH = 800
GROUND_HEIGHT = 200
GROUND_SURFACE = pygame.Surface((GROUND_WIDTH,GROUND_HEIGHT))
GROUND_SURFACE.fill('LawnGreen')


"""title bar"""
pygame.display.set_caption("Welcome to Blossom \
by: Tim and Trenton")

"""level control"""
class GameState():
    def __ini__(self):
        self.state = 'intro';

    def intro(self):
        pass

    def main_game(self):
        pass
        

if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    """Main game loop"""
    while (running):
        clock.tick(FPS)
        """Main event loop"""
        for event in pygame.event.get():
            """ player exit"""
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            """player left"""
            if event.type == pygame.K_LEFT:
                #move left
                pass
            """player right"""
            if event.type == pygame.K_RIGHT:
                #move right
                pass
            """player up or space"""
            if event.type == pygame.KEYUP or event.type == pygame.K_SPACE:
                #jump
                pass
        WINDOW.blit(GROUND_SURFACE,(0,500))
        pygame.display.update()

        
