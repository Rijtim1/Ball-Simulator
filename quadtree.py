# quadtree.py
class QuadTree:
    def __init__(self, bounds, capacity=4):
        self.bounds = bounds
        self.capacity = capacity
        self.balls = []
        self.children = None

    def insert(self, ball):
        if not self.in_bounds(ball.position):
            return False

        if len(self.balls) < self.capacity:
            self.balls.append(ball)
            return True
        else:
            if self.children is None:
                self.subdivide()

            if self.children[0].insert(ball):
                return True
            elif self.children[1].insert(ball):
                return True
            elif self.children[2].insert(ball):
                return True
            elif self.children[3].insert(ball):
                return True

        return False

    def subdivide(self):
        x, y, w, h = self.bounds
        half_w = w / 2
        half_h = h / 2

        self.children = [
            QuadTree((x, y, half_w, half_h), self.capacity),
            QuadTree((x + half_w, y, half_w, half_h), self.capacity),
            QuadTree((x, y + half_h, half_w, half_h), self.capacity),
            QuadTree((x + half_w, y + half_h, half_w, half_h), self.capacity),
        ]

    def in_bounds(self, position):
        x, y, w, h = self.bounds
        return x <= position[0] < x + w and y <= position[1] < y + h

    def get_collidable_balls(self, ball):
        collidable_balls = []

        if self.in_bounds(ball.position):
            for other_ball in self.balls:
                if other_ball != ball:
                    collidable_balls.append(other_ball)

            if self.children is not None:
                collidable_balls.extend(self.children[0].get_collidable_balls(ball))
                collidable_balls.extend(self.children[1].get_collidable_balls(ball))
                collidable_balls.extend(self.children[2].get_collidable_balls(ball))
                collidable_balls.extend(self.children[3].get_collidable_balls(ball))

        return collidable_balls
