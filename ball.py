import pygame
from typing import Tuple
import random

class Ball:
    def __init__(self, position, velocity, radius, color):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.damping = 0.9

    def update(self, gravity: Tuple[float, float], dt: float, width: int, height: int):
        self.position = (self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt)
        self.velocity = (self.velocity[0], self.velocity[1] + gravity[1] * dt)

        if self.position[1] + self.radius >= height:
            self.velocity = (
                self.velocity[0] * self.damping + random.uniform(-0.2, 0.2),
                -self.velocity[1] * self.damping + random.uniform(-0.2, 0.2)
            )
            self.position = (self.position[0], height - self.radius)
            self.is_squished = True

            if random.random() < 0.2:  # Adjust the probability as desired
                extra_velocity = random.uniform(0.2, 0.5)  # Adjust the range as desired
                self.velocity = (
                    self.velocity[0] * (1 + extra_velocity),
                    self.velocity[1] * (1 + extra_velocity)
                )

        if self.position[1] - self.radius <= 0:
            self.velocity = (
                self.velocity[0] * self.damping + random.uniform(-0.2, 0.2),
                -self.velocity[1] * self.damping + random.uniform(-0.2, 0.2)
            )
            self.position = (self.position[0], self.radius)

            if random.random() < 0.2:
                extra_velocity = random.uniform(0.2, 0.5)
                self.velocity = (
                    self.velocity[0] * (1 + extra_velocity),
                    self.velocity[1] * (1 + extra_velocity)
                )

        if self.position[0] - self.radius <= 0:
            self.velocity = (
                -self.velocity[0] * self.damping + random.uniform(-0.2, 0.2),
                self.velocity[1] * self.damping + random.uniform(-0.2, 0.2)
            )
            self.position = (self.radius, self.position[1])

            if random.random() < 0.2:
                extra_velocity = random.uniform(0.2, 0.5)
                self.velocity = (
                    self.velocity[0] * (1 + extra_velocity),
                    self.velocity[1] * (1 + extra_velocity)
                )

        if self.position[0] + self.radius >= width:
            self.velocity = (
                -self.velocity[0] * self.damping + random.uniform(-0.2, 0.2),
                self.velocity[1] * self.damping + random.uniform(-0.2, 0.2)
            )
            self.position = (width - self.radius, self.position[1])

            if random.random() < 0.2:
                extra_velocity = random.uniform(0.2, 0.5)
                self.velocity = (
                    self.velocity[0] * (1 + extra_velocity),
                    self.velocity[1] * (1 + extra_velocity)
                )


    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))
