# simulation.py
from typing import List
from itertools import combinations
from ball import Ball
import pygame
import math
from quadtree import Quadtree  # Import the Quadtree class

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
        self.quadtree = Quadtree((0, 0, self.width, self.height), capacity=4)

    def add_ball(self, ball: Ball):
        self.balls.append(ball)
        self.quadtree.insert(ball)  # Add the ball to the quadtree
        self.first_ball_added = True

    def remove_ball(self, ball: Ball):
        """Remove a ball from the simulation and the quadtree."""
        if ball in self.balls:
            self.balls.remove(ball)
            self.quadtree.remove(ball)

    def update(self):
        # Rebuild the quadtree for the current frame
        self.quadtree = Quadtree((0, 0, self.width, self.height), capacity=max(4, len(self.balls) // 10))
        for ball in self.balls:
            self.quadtree.insert(ball)

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
        # Check for collisions using the quadtree
        for ball in self.balls:
            # Query nearby balls within a range (ball's radius)
            nearby_balls = self.quadtree.query((
                ball.position[0] - ball.radius,
                ball.position[1] - ball.radius,
                ball.radius * 2,
                ball.radius * 2
            ))

            # Check collisions with nearby balls
            for other_ball in nearby_balls:
                if ball is not other_ball:
                    distance = math.sqrt(
                        (other_ball.position[0] - ball.position[0]) ** 2 +
                        (other_ball.position[1] - ball.position[1]) ** 2
                    )
                    if distance <= ball.radius + other_ball.radius:
                        self.number_collisions += 1
                        self.resolve_collision(ball, other_ball)

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

        # Positional correction to prevent overlapping
        penetration_depth = ball1.radius + ball2.radius - distance
        correction_factor = 0.5  # Adjust this factor as needed
        correction = (
            correction_factor * penetration_depth * normal[0],
            correction_factor * penetration_depth * normal[1]
        )
        ball1.position = (
            ball1.position[0] - correction[0] / ball1.radius,
            ball1.position[1] - correction[1] / ball1.radius
        )
        ball2.position = (
            ball2.position[0] + correction[0] / ball2.radius,
            ball2.position[1] + correction[1] / ball2.radius
        )

        # Clamp velocities to prevent excessive speed
        max_velocity = 10.0  # Adjust as needed
        ball1.velocity = (
            max(-max_velocity, min(ball1.velocity[0], max_velocity)),
            max(-max_velocity, min(ball1.velocity[1], max_velocity))
        )
        ball2.velocity = (
            max(-max_velocity, min(ball2.velocity[0], max_velocity)),
            max(-max_velocity, min(ball2.velocity[1], max_velocity))
        )

        # Apply a small damping factor to reduce numerical instability
        damping_factor = 0.99  # Slightly reduce velocity
        ball1.velocity = (ball1.velocity[0] * damping_factor, ball1.velocity[1] * damping_factor)
        ball2.velocity = (ball2.velocity[0] * damping_factor, ball2.velocity[1] * damping_factor)

