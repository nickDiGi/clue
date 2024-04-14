import pygame, sys
from game import Game
from choose_character import ChooseCharacter
from button import Button

clock = pygame.time.Clock()


class JoinGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.name = "Join Game"
        self.gamename_text = ""
        self.username_text = ""
        self.input_clicked_color = (215, 215, 215)
        self.input_not_clicked_color = (155, 155, 155)
        self.gamename_input_color = self.input_not_clicked_color
        self.username_input_color = self.input_not_clicked_color
        self.submit_btn = Button(self.screen, 50, 180, "Submit")

    def gamename(self):
        game_name_srf = self.font.render("Enter Gamename:", True, (255, 255, 255))
        self.screen.blit(game_name_srf, (50, 100))

    def gamename_input_rect(self):
        input_rect = pygame.Rect(205, 100, 200, 25)
        return pygame.draw.rect(self.screen, self.gamename_input_color, input_rect, 2)

    def gamename_input(self):
        text_surface = self.font.render(self.gamename_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (205 + 5, 100 + 3))

    def username(self):
        username_srf = self.font.render("Enter Username:", True, (255, 255, 255))
        self.screen.blit(username_srf, (50, 130))

    def username_input_rect(self):
        input_rect = pygame.Rect(205, 130, 200, 25)
        return pygame.draw.rect(self.screen, self.username_input_color, input_rect, 2)

    def username_input(self):
        text_surface = self.font.render(self.username_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (205 + 5, 130 + 3))

    def input_information(self):
        return [self.gamename_text, self.username_text]

    def welcome(self):
        return self.name

    def menu(self):
        gamename_active = False
        username_active = False
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            mx, my = pygame.mouse.get_pos()
            text_srf = self.font.render(self.name, True, (255, 255, 255))
            self.screen.blit(text_srf, (50, 50))
            self.gamename(), self.username()
            self.gamename_input_rect(), self.username_input_rect()
            self.gamename_input(), self.username_input()
            self.submit_btn.rect(), self.submit_btn.rect_bg(), self.submit_btn.rect_text()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gamename_input_rect().collidepoint(mx, my):
                        gamename_active = True
                    elif (
                        self.gamename_input_rect()
                        != self.gamename_input_rect().collidepoint(mx, my)
                    ):
                        gamename_active = False
                    if self.username_input_rect().collidepoint(mx, my):
                        username_active = True
                    elif (
                        self.username_input_rect()
                        != self.username_input_rect().collidepoint(mx, my)
                    ):
                        username_active = False
                    if self.submit_btn.rect().collidepoint(mx, my):
                        if (
                            len(self.input_information()[0]) > 0
                            and len(self.input_information()[0]) > 0
                        ):
                            print(self.input_information())
                            ChooseCharacter(self.screen, self.font).menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if gamename_active == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.gamename_text = self.gamename_text[:-1]
                        elif event.key == pygame.K_TAB:
                            gamename_active = False
                            username_active = True
                        else:
                            self.gamename_text += event.unicode
                    elif username_active == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.username_text = self.username_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            username_active = False
                        else:
                            self.username_text += event.unicode
                    if event.key == pygame.K_RETURN:
                        print(self.input_information())
                        if ChooseCharacter(self.screen, self.font).menu() == False:
                            running = False
                        else:
                            ChooseCharacter(self.screen, self.font).menu()
            if gamename_active:
                self.gamename_input_color = self.input_clicked_color
            elif not gamename_active:
                self.gamename_input_color = self.input_not_clicked_color
            if username_active:
                self.username_input_color = self.input_clicked_color
            elif not username_active:
                self.username_input_color = self.input_not_clicked_color
            pygame.display.update()
            clock.tick(60)