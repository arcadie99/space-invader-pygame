import pygame
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    containers = ()

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 200, 200), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def detectColision(self, object):
        distance = self.position.distance_to(object.position)
        if distance < self.radius + object.radius:
            return True
        return False

    def detectShotColision(self, object):
        distance = self.position.distance_to(object.position)
        if distance < self.radius + object.radius:
            self.kill()
            return True
        return False

    def split(self):
        if self.radius < ASTEROID_MIN_RADIUS:
            self.kill()
            return False

        angle = random.uniform(20, 50)
        self.radius /= 2
        self.velocity = self.velocity.rotate(angle)


        asteroid1 = Asteroid(self.position.x, self.position.y, self.radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, self.radius)
        
        asteroid1.velocity = self.velocity.rotate(angle) * 2
        asteroid2.velocity = self.velocity.rotate(-angle) * 2
        return [asteroid1, asteroid2]
