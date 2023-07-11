# window.py
import pygame
import random
from ball import Ball

class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = None
        self.mouse_start_pos = None
        self.mouse_start_time = None

    def create(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def handle_events(self, simulation):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.mouse_start_pos = pygame.mouse.get_pos()
                    self.mouse_start_time = pygame.time.get_ticks()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    hold_time = pygame.time.get_ticks() - self.mouse_start_time
                    radius = max(10, min(100, hold_time // 100))  # Limit the radius between 10 and 100
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    # mass = radius**3  # Calculate the mass based on the radius (you can adjust this calculation if needed)
                    ball = Ball(self.mouse_start_pos, (0, 0), radius, color)
                    simulation.add_ball(ball)

        return True

    def get_screen(self):
        return self.screen

    def clear(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()

    def close(self):
        pygame.quit()
        exit()
