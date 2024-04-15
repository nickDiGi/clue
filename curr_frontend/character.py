import pygame, sys

pygame.init()

font = pygame.font.SysFont(None, 24)


class Character:
    def __init__(self, screen, text=None):
        self.screen = screen
        self.text = text
        self.width = 50
        self.height = 50

    def display(self, x_inc=0, y_inc=0):
        x_value = 0 + x_inc
        y_value = 0 + y_inc
        char_rect = pygame.Rect(x_value, y_value, self.width, self.height)
        pygame.draw.rect(self.screen, (155, 155, 155), char_rect)
