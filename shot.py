from circleshape import CircleShape
import pygame

class Shot(CircleShape):
    containers = ()  # Static containers for sprite groups 

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt 

    def detectColision(self, object):
        distance = self.position.distance_to(object.position)
        return distance < self.radius + object.radius
