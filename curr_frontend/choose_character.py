import pygame, sys, os
from button import Button
from game import Game
from constants import *
from character_button import CharacterButton

clock = pygame.time.Clock()
choose_character_title_font = pygame.font.SysFont(None, 36)


class ChooseCharacter:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.character_hover = ""

    def character_names(self):
        character_list = []
        path = "./assets"
        directory = os.listdir(path)
        for file in directory:
            character_list.append(file.replace("_", " ").replace(".png", ""))
        return character_list[1:]

    def character_files(self):
        character_files = []
        path = "./assets"
        directory = os.listdir(path)
        for file in directory:
            character_files.append(file)
        return character_files[1:]

    def display_characters(self):
        x = (WIDTH / 3) - 80
        y = HEIGHT / 4
        num = 1
        clue_characters = [
            self.character_names()[:3],
            self.character_names()[3:],
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
                x += 250
                num += 1
            x = (WIDTH / 3) - 80
            y += 200

    def select_character_img(self):
        x = (WIDTH / 3) - 90
        y = HEIGHT / 5
        mx, my = pygame.mouse.get_pos()
        clue_characters = [
            self.character_files()[:3],
            self.character_files()[3:],
        ]
        for i in range(len(clue_characters)):
            for j in range(len(clue_characters[i])):
                CharacterButton(
                    self.screen, x, y, 160, 280, "", f"./assets/{clue_characters[i][j]}"
                ).rect()
                if (
                    CharacterButton(
                        self.screen,
                        x,
                        y,
                        160,
                        280,
                        "",
                        f"./assets/{clue_characters[i][j]}",
                    )
                    .rect()
                    .collidepoint((mx, my))
                ):
                    self.character_hover = (
                        clue_characters[i][j].replace("_", " ").replace(".png", "")
                    )
                CharacterButton(
                    self.screen, x, y, 160, 280, "", f"./assets/{clue_characters[i][j]}"
                ).rect_bg()
                CharacterButton(
                    self.screen, x, y, 160, 280, "", f"./assets/{clue_characters[i][j]}"
                ).rect_img()
                x += 250
            x = (WIDTH / 3) - 90
            y += 350

    def character_clicked(self):
        return self.character_hover

    def menu(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_srf = choose_character_title_font.render(
                "Choose Character", True, (255, 255, 255)
            )
            self.screen.blit(text_srf, ((WIDTH / 2) - (text_srf.get_width() / 2), 50))
            # self.display_characters()
            self.select_character_img()
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
