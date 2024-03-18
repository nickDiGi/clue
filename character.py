import pygame


# character class to create each clue character
class Character:
    def __init__(self, WINDOW, x, y, width, height, filename):
        self.WINDOW = WINDOW
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filename = filename
        self.char_name = self.filename[10:-4].replace("_", " ")
        self.char_img = pygame.rect.Rect((self.x, self.y), (self.width, self.height))

    # draw character to window
    def draw(self):
        img = pygame.image.load(self.filename)
        img_scaled = pygame.transform.scale(img, (self.width, self.height))
        self.WINDOW.blit(img_scaled, (self.x, self.y))

    # determine which character has been clicked by user
    def clicked(self):
        if (
            self.char_img.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        ):
            return True
