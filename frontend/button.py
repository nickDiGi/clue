import pygame

pygame.init()

font = pygame.font.SysFont(None, 24)


class Button:
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.width = 150
        self.height = 70

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def rect_bg(self):
        pygame.draw.rect(self.screen, (155, 155, 155), self.rect())

    def rect_text(self):
        text_img = font.render(self.text, True, (255, 255, 255))
        text_len = text_img.get_width()
        text_height = text_img.get_height()
        self.screen.blit(
            text_img,
            (
                self.x + int(self.width / 2) - int(text_len / 2),
                self.y + int(self.height / 2) - int(text_height / 2),
            ),
        )
