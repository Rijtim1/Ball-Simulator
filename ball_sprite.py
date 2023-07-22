# ballSprite
import pygame

class BallSprite(pygame.sprite.Sprite):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball
        self.image = pygame.Surface((2 * ball.radius, 2 * ball.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.ball.color, (ball.radius, ball.radius), ball.radius)
        self.rect = self.image.get_rect(center=ball.position)

    def update(self):
        self.rect.center = self.ball.position
