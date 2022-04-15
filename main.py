import pygame
import pygame_assets as assets
"""Simple game with a goal to catch flowers and avoid bad stuff"""

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
SKY_COLOR = (77, 204, 255)

def draw_window():
    WINDOW.fill(SKY_COLOR)
    pygame.display.update()


if __name__ == "__main__":
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    """Main game loop"""
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_window()
    pygame.quit()
