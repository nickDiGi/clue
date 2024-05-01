import pygame, sys

pygame.init()

font = pygame.font.SysFont(None, 24)


class Character:
    def __init__(self, screen, starting_x, starting_y, text=None):
        self.screen = screen
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.text = text
        self.width = 50
        self.height = 50

    def display(self, x_inc=0, y_inc=0):
        x_value = self.starting_x + x_inc
        y_value = self.starting_y + y_inc
        char_rect = pygame.Rect(x_value, y_value, self.width, self.height)
        pygame.draw.rect(self.screen, (155, 155, 155), char_rect)
