# ball.py
import pygame
from typing import Tuple
import random
import math

class Ball:
    def __init__(self, position, velocity, radius, color):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.radius_squared = radius ** 2
        self.color = color
        self.damping = 0.9
        self.random_values = {}  # Dynamic programming table for storing random values

    def get_random_value(self, key: str, probability: float, value_range: Tuple[float, float]) -> float:
        """
        Get a random value for the given key from the dynamic programming table.
        If the key is not present, generate a new random value and store it in the table.
        """
        if key not in self.random_values:
            self.random_values[key] = random.uniform(value_range[0], value_range[1])
        if random.random() < probability:
            return 1.0 + self.random_values[key]
        return 1.0

    def update(self, gravity: Tuple[float, float], dt: float, width: int, height: int):
        dt_squared = dt * dt

        x, y = self.position
        vx, vy = self.velocity
        radius = self.radius

        # Update position using Verlet integration with caching
        new_x = x + vx * dt + 0.5 * gravity[0] * dt_squared
        new_y = y + vy * dt + 0.5 * gravity[1] * dt_squared

        self.position = (new_x, new_y)

        # Update velocity using Verlet integration with caching
        new_vx = vx + 0.5 * gravity[0] * dt
        new_vy = vy + 0.5 * gravity[1] * dt

        self.velocity = (new_vx, new_vy)

        # Check for collisions with the edges of the window
        self.handle_collisions(width, height)

    def handle_collisions(self, width: int, height: int):
        x, y = self.position
        vx, vy = self.velocity
        radius = self.radius
        radius_squared = self.radius_squared

        # Handle collisions with the edges of the window
        if x - radius < 0:
            x = radius
            vx = -vx * self.damping
        elif x + radius > width:
            x = width - radius
            vx = -vx * self.damping

        if y - radius < 0:
            y = radius
            vy = -vy * self.damping
        elif y + radius > height:
            y = height - radius
            vy = -vy * self.damping

        self.position = (x, y)
        self.velocity = (vx, vy)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))
