# window.py
import pygame
import random
from ball import Ball
import sys

class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = None
        self.mouse_start_pos = None
        self.mouse_start_time = None
        self.is_running = False

        # Cache dictionary for pygame.font.Font
        self.font_cache = {}

    def create(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.is_running = True

    def handle_events(self, simulation):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

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
                    ball = Ball(self.mouse_start_pos, (0, 0), radius, color)
                    simulation.add_ball(ball)

        return self.is_running

    def get_screen(self):
        return self.screen

    def clear(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()

    def close(self):
        pygame.quit()
        sys.exit()

    def get_font(self, font_name, font_size):
        key = f"{font_name}_{font_size}"
        if key not in self.font_cache:
            self.font_cache[key] = pygame.font.Font(font_name, font_size)
        return self.font_cache[key]
