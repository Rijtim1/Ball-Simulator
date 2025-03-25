from typing import List, Tuple
from ball import Ball

class Quadtree:
    def __init__(self, boundary: Tuple[int, int, int, int], capacity: int):
        self.boundary = boundary  # (x, y, width, height)
        self.capacity = capacity  # Maximum number of balls before subdivision
        self.balls: List[Ball] = []
        self.divided = False
        self.children = []  # Subdivided quadrants

    def subdivide(self):
        x, y, w, h = self.boundary
        half_w, half_h = w // 2, h // 2
        self.children = [
            Quadtree((x, y, half_w, half_h), self.capacity),  # Top-left
            Quadtree((x + half_w, y, half_w, half_h), self.capacity),  # Top-right
            Quadtree((x, y + half_h, half_w, half_h), self.capacity),  # Bottom-left
            Quadtree((x + half_w, y + half_h, half_w, half_h), self.capacity),  # Bottom-right
        ]
        self.divided = True

    def contains(self, ball: Ball) -> bool:
        """Check if a ball is within the boundary."""
        x, y, w, h = self.boundary
        return x <= ball.position[0] < x + w and y <= ball.position[1] < y + h

    def insert(self, ball: Ball):
        if not self.contains(ball):
            return False  # Ball is outside this boundary

        if len(self.balls) < self.capacity:
            self.balls.append(ball)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(ball):
                return True

        return False

    def remove(self, ball: Ball):
        """Remove a ball from the quadtree."""
        if not self.contains(ball):
            return False  # Ball is outside this boundary

        if ball in self.balls:
            self.balls.remove(ball)
            return True

        if self.divided:
            for child in self.children:
                if child.remove(ball):
                    return True

        return False

    def query(self, range_boundary: Tuple[int, int, int, int], found: List[Ball] = None):
        if found is None:
            found = []

        x, y, w, h = self.boundary
        rx, ry, rw, rh = range_boundary

        # Check if the range intersects this boundary
        if not (x < rx + rw and x + w > rx and y < ry + rh and y + h > ry):
            return found

        for ball in self.balls:
            if rx <= ball.position[0] < rx + rw and ry <= ball.position[1] < ry + rh:
                found.append(ball)

        if self.divided:
            for child in self.children:
                child.query(range_boundary, found)

        return found
