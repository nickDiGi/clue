import pygame, sys
from button import Button
from game import Game

clock = pygame.time.Clock()


class ChooseCharacter:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.character_hover = ""

    def display_characters(self):
        x = 50
        y = 100
        num = 1
        clue_characters = [
            ["Prof. Plum", "Miss Scarlett", "Mr. Green"],
            ["Mrs. White", "Mrs. Peacock", "Colonel Mustard"],
        ]
        mx, my = pygame.mouse.get_pos()
        for i in range(len(clue_characters)):
            for j in range(len(clue_characters[i])):
                Button(self.screen, x, y, f"{clue_characters[i][j]}").rect()
                if (
                    Button(self.screen, x, y, f"{clue_characters[i][j]}")
                    .rect()
                    .collidepoint((mx, my))
                ):
                    self.character_hover = clue_characters[i][j]
                Button(self.screen, x, y, f"{clue_characters[i][j]}").rect_bg()
                Button(self.screen, x, y, f"{clue_characters[i][j]}").rect_text()
                x += 200
                num += 1
            x = 50
            y += 100

    def character_clicked(self):
        return self.character_hover

    def menu(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_srf = self.font.render("Choose Character", True, (255, 255, 255))
            self.screen.blit(text_srf, (50, 50))
            self.display_characters()
            # self.character_clicked()
            # if self.click:
            # print(self.character_clicked())
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.character_clicked())
                    if Game(self.screen, self.font).menu() == False:
                        running = False
                    else:
                        Game(self.screen, self.font).menu()
            pygame.display.update()
            clock.tick(60)
        return running
