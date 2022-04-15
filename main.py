import pygame
import pygame_assets as assets
from sys import exit
"""Simple game with a goal to catch flowers and avoid bad stuff"""

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
SKY_COLOR = (77, 204, 255)
FPS = 60
WINDOW.fill(SKY_COLOR)
pygame.display.update()



if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    """Main game loop"""
    while running:
        clock.tick(60)

        """Main event loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
