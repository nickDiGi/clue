import pygame
from constants import *

pygame.init()


class CharacterButton:
    def __init__(self, screen, x, y, width, height, text, filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.filename = filename

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def rect_bg(self):
        pygame.draw.rect(self.screen, (155, 155, 155), self.rect())

    def rect_img(self):
        img = pygame.image.load(self.filename).convert()
        img_scaled = pygame.transform.scale(img, (self.width, self.height))
        self.screen.blit(img_scaled, (self.x, self.y))
