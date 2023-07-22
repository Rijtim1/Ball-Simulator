# ball.py
import pygame
import numpy as np
import random

class Ball:
    def __init__(self, position, velocity, radius, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.radius = radius
        self.radius_squared = radius ** 2
        self.color = color
        self.damping = 0.9
        self.random_values = {}  # Dynamic programming table for storing random values

    def get_random_value(self, key: str, probability: float, value_range: tuple) -> float:
        """
        Get a random value for the given key from the dynamic programming table.
        If the key is not present, generate a new random value and store it in the table.
        """
        if key not in self.random_values:
            self.random_values[key] = random.uniform(value_range[0], value_range[1])
        if random.random() < probability:
            return 1.0 + self.random_values[key]
        return 1.0

    def update(self, gravity, dt, width, height):
        dt_squared = dt * dt

        # Convert gravity and dt_squared to NumPy arrays
        gravity = np.array(gravity, dtype=float)
        dt_squared = np.array(dt_squared, dtype=float)

        # Update position using Verlet integration with caching
        new_position = self.position + self.velocity * dt + 0.5 * gravity * dt_squared

        self.position = new_position

        # Update velocity using Verlet integration with caching
        new_velocity = self.velocity + 0.5 * gravity * dt

        self.velocity = new_velocity

        # Check for collisions with the edges of the window
        self.handle_collisions(width, height)

    def handle_collisions(self, width, height):
        x, y = self.position
        vx, vy = self.velocity
        radius = self.radius

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

        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))
