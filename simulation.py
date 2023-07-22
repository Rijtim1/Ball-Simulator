# simulation.py
from typing import List
from itertools import combinations
import numpy as np
import pygame
import random
import math
from ball import Ball

class Simulation:
    def __init__(self):
        self.balls: List[Ball] = []
        self.gravity = np.array([0, 0.098], dtype=float)  # Set gravity as a NumPy array
        self.dt = 0.1
        self.height = 600
        self.width = 800
        self.debug_mode = False
        self.first_ball_added = False
        self.collision_sound = None
        self.number_collisions = 0

    def add_ball(self, ball: Ball):
        self.balls.append(ball)
        self.first_ball_added = True

    def update(self):
        for ball in self.balls:
            ball.update(self.gravity, self.dt, self.width, self.height)
        self.check_collisions()

    def draw(self, surface):
        for ball in self.balls:
            ball.draw(surface)
            
        if not self.first_ball_added:
            font = pygame.font.Font(None, 36)
            text = font.render("Press the mouse button to create a new ball, or keep the button pressed to enlarge the ball's size.", True, (255, 255, 255))
            surface.blit(text, (0, 0))
        
        if self.debug_mode:
            font = pygame.font.Font(None, 36)
            debug_text = f"Number of balls: {len(self.balls)}"
            text = font.render(debug_text, True, (255, 255, 255))
            surface.blit(text, (0, 0))

            collision_text = f"Number of collisions: {self.number_collisions}"
            collision_text_render = font.render(collision_text, True, (255, 255, 255))
            surface.blit(collision_text_render, (0, 40))

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        
    def check_collisions(self):
        for ball1, ball2 in combinations(self.balls, 2):
            distance = np.linalg.norm(ball2.position - ball1.position)
            if distance <= ball1.radius + ball2.radius:
                self.number_collisions += 1
                self.resolve_collision(ball1, ball2)

    def resolve_collision(self, ball1, ball2):
        # Calculate the relative position and velocity
        relative_position = ball2.position - ball1.position
        relative_velocity = ball2.velocity - ball1.velocity

        # Calculate the dot product of the relative position and velocity
        dot_product = np.dot(relative_position, relative_velocity)

        # Check if the balls are moving towards each other
        if dot_product >= 0:
            return

        # Calculate the distance between the balls
        distance = np.linalg.norm(relative_position)

        # Calculate the unit normal vector
        normal = relative_position / distance

        # Calculate the impulse
        impulse = (2 * dot_product) / (distance * (1 / ball1.radius + 1 / ball2.radius))

        # Calculate the new velocities
        new_velocity1 = ball1.velocity + impulse * normal / ball1.radius
        new_velocity2 = ball2.velocity - impulse * normal / ball2.radius

        # Update the velocities of the balls
        ball1.velocity = new_velocity1
        ball2.velocity = new_velocity2
