# simulation.py
from typing import List
from itertools import combinations
from ball import Ball
import pygame
import math

class Simulation:
    def __init__(self):
        self.balls: List[Ball] = []
        self.gravity = (0, 0.098)
        self.dt = 0.1
        self.height = 600
        self.width = 800
        self.debug_mode = False
        self.first_ball_added = False
        self.collision_sound = None
        self.number_collisions = 0
        self.distance_table = {}  # Dynamic programming table for storing distances between ball pairs

    def add_ball(self, ball: Ball):
        self.balls.append(ball)
        self.first_ball_added = True

    def update(self):
        for ball in self.balls:
            ball.update(self.gravity, self.dt, self.width, self.height)
        self.distance_table.clear()  # Clear the table on each update
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
            # Check if the distance between these two balls has been calculated before
            if (ball1, ball2) not in self.distance_table:
                distance = math.sqrt((ball2.position[0] - ball1.position[0]) ** 2 + (ball2.position[1] - ball1.position[1]) ** 2)
                self.distance_table[(ball1, ball2)] = distance
            else:
                distance = self.distance_table[(ball1, ball2)]

            if distance <= ball1.radius + ball2.radius:
                self.number_collisions += 1
                self.resolve_collision(ball1, ball2)

    def resolve_collision(self, ball1, ball2):
        # Calculate the relative position and velocity
        relative_position = (ball2.position[0] - ball1.position[0], ball2.position[1] - ball1.position[1])
        relative_velocity = (ball2.velocity[0] - ball1.velocity[0], ball2.velocity[1] - ball1.velocity[1])

        # Calculate the dot product of the relative position and velocity
        dot_product = relative_position[0] * relative_velocity[0] + relative_position[1] * relative_velocity[1]

        # Check if the balls are moving towards each other
        if dot_product >= 0:
            return

        # Calculate the distance between the balls
        distance = math.sqrt(relative_position[0] ** 2 + relative_position[1] ** 2)

        # Calculate the unit normal vector
        normal = (relative_position[0] / distance, relative_position[1] / distance)

        # Calculate the impulse
        impulse = (2 * dot_product) / (distance * (1 / ball1.radius + 1 / ball2.radius))

        # Calculate the new velocities
        new_velocity1 = (
            ball1.velocity[0] + impulse * normal[0] / ball1.radius,
            ball1.velocity[1] + impulse * normal[1] / ball1.radius
        )
        new_velocity2 = (
            ball2.velocity[0] - impulse * normal[0] / ball2.radius,
            ball2.velocity[1] - impulse * normal[1] / ball2.radius
        )

        # Update the velocities of the balls
        ball1.velocity = new_velocity1
        ball2.velocity = new_velocity2
