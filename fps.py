import pygame

class Text:
    def __init__(self):
        pass

    def draw(self, fps, screen, x = 40,y = 40, color = (255,255,255)): 
        font = pygame.font.Font(None, 24) 
        text_surface = font.render(fps, True, color)
        text_rect = text_surface.get_rect(center=(x, y)) 

        screen.blit(text_surface, text_rect)
