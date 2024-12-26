import pygame
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot


def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    asteroid = Asteroid(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ASTEROID_MIN_RADIUS)


    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    updatable.add(player)
    drawable.add(player)

    updatable.add(asteroid)
    drawable.add(asteroid)

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

 
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))

        for sprite in drawable:
            sprite.draw(screen)

        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.detectShotColision(shot):
                    asteroid.split()
                    shot.kill()
                    break

            if asteroid.detectColision(player):
                print("Game Over!")


        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Convert milliseconds to seconds
        print(f"FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
        main()
