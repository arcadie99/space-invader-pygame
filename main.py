#!/usr/bin/env python3

import pygame
from constants import *  # Ensure constants.py defines necessary constants
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from fps import Text


def button_create(text, rect, inactive_color, active_color, action):
    """Creates a button with text, color, and an action."""
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)

    return [text_surface, text_rect, button_rect, inactive_color, active_color, action, False]


def button_check(info, event):
    """Handles button hover and click events."""
    _, _, rect, _, _, action, hover = info

    if event.type == pygame.MOUSEMOTION:
        info[-1] = rect.collidepoint(event.pos)  # Update hover state

    elif event.type == pygame.MOUSEBUTTONDOWN and hover and action:
        action()


def button_draw(screen, info):
    """Draws the button on the screen."""
    text_surface, text_rect, rect, inactive_color, active_color, _, hover = info
    color = active_color if hover else inactive_color
    pygame.draw.rect(screen, color, rect)
    screen.blit(text_surface, text_rect)


# --- Button Actions ---

def on_click_button_1():
    global stage
    stage = 'game'

def on_click_button_2():
    global stage
    stage = 'options'

def on_click_button_3():
    global stage, running
    stage = 'exit'
    running = False

def on_click_button_return():
    global stage
    stage = 'menu'

# --- Main Program ---

def main():
    global stage, running

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")
    clock = pygame.time.Clock()
    dt = 0

    # Game States
    stage = 'menu'
    running = True

    # Button Setup
    button_1 = button_create("GAME", (SCREEN_WIDTH / 2 - 75, 100, 200, 75), RED, GREEN, on_click_button_1)
    button_2 = button_create("OPTIONS", (SCREEN_WIDTH / 2 - 75, 200, 200, 75), RED, GREEN, on_click_button_2)
    button_3 = button_create("EXIT", (SCREEN_WIDTH / 2 - 75, 300, 200, 75), RED, GREEN, on_click_button_3)
    button_return = button_create("RETURN", (SCREEN_WIDTH / 2 - 75, 400, 200, 75), RED, GREEN, on_click_button_return)

    # Initialize Game Objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
    asteroid = Asteroid(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ASTEROID_MIN_RADIUS)
    text_object = Text()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    updatable.add(player, asteroid)
    drawable.add(player, asteroid)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()

    enemy_kills = 0

    # Game Loop
    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if stage == 'menu':
                button_check(button_1, event)
                button_check(button_2, event)
                button_check(button_3, event)
            elif stage == 'options':
                button_check(button_return, event)

        # Update Game Logic
        if stage == 'game':
            updatable.update(dt)

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.detectShotColision(shot):
                        asteroid.split()
                        enemy_kills += 1
                        shot.kill()
                        break

                if asteroid.detectColision(player):
                    print("Game Over!")
                    stage = 'menu'
                    # Reset the game state
                    enemy_kills = 0
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()

                    # Recreate initial game objects
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
                    asteroid_field = AsteroidField()
                    updatable.add(player, asteroid_field)
                    drawable.add(player)

                    # Return to menu
                    stage = 'menu'

        # Draw Everything
        screen.fill(BLACK)
        if stage == 'menu':
            button_draw(screen, button_1)
            button_draw(screen, button_2)
            button_draw(screen, button_3)
        elif stage == 'game':
            for sprite in drawable:
                sprite.draw(screen)
            text_object.draw(f"Score: {enemy_kills}", screen)
            text_object.draw(f"{clock.get_fps():2.0f} FPS", screen, 40, 80, color=RED)
        elif stage == 'options':
            button_draw(screen, button_return)

        # Update Display and Tick Clock
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Frame time in seconds

    pygame.quit()


if __name__ == "__main__":
    main()

