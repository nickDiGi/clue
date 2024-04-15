import pygame

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
        pass
