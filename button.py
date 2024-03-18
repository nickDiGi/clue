import pygame
from constants import *

pygame.font.init()


# button class to create buttons on various windows
class Button:
    def __init__(self, WINDOW, x, y, text):
        self.WINDOW = WINDOW
        self.x = x
        self.y = y
        self.text = text
        self.button = pygame.rect.Rect((self.x, self.y), (BTN_WIDTH, BTN_HEIGHT))

    # draw button to screen
    def draw(self):
        pygame.draw.rect(self.WINDOW, (255, 255, 255), self.button)
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        text = font.render(self.text, True, (0))
        self.WINDOW.blit(
            text,
            text.get_rect(center=(self.x + (BTN_WIDTH / 2), self.y + (BTN_HEIGHT / 2))),
        )

    # determine if button has been clicked
    def clicked(self):
        if (
            self.button.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            return False
        else:
            return True
