import pygame, sys
#from frontend.game import Game
from frontend.choose_character import ChooseCharacter
from frontend.button import Button
from frontend.constants import *

clock = pygame.time.Clock()
create_title_font = pygame.font.SysFont(None, 36)
label_font = pygame.font.SysFont(None, 28)


class CreateGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.screen = screen
        self.font = font
        self.username_text = ""
        self.input_clicked_color = (215, 215, 215)
        self.input_not_clicked_color = (155, 155, 155)
        self.username_input_color = self.input_not_clicked_color
        self.submit_btn = Button(self.screen, (WIDTH / 2) - 75, 220, "Submit")

    def username(self):
        username_srf = label_font.render("Enter Username:", True, (255, 255, 255))
        self.screen.blit(username_srf, ((WIDTH / 2) - 200, 160))

    def username_input_rect(self):
        input_rect = pygame.Rect((WIDTH / 2), 160, 200, 25)
        return pygame.draw.rect(self.screen, self.username_input_color, input_rect, 2)

    def username_input(self):
        text_surface = label_font.render(self.username_text, True, (255, 255, 255))
        self.screen.blit(text_surface, ((WIDTH / 2) + 5, 160 + 3))

    def input_information(self):
        return [self.username_text]

    def welcome(self):
        return self.name

    def menu(self):
        username_active = False
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            mx, my = pygame.mouse.get_pos()
            text_srf = create_title_font.render("Create Game", True, (255, 255, 255))
            self.screen.blit(text_srf, ((WIDTH / 2) - (text_srf.get_width() / 2), 50))
            self.username()
            self.username_input_rect()
            self.username_input()
            self.submit_btn.rect(), self.submit_btn.rect_bg(), self.submit_btn.rect_text()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                            return self.input_information()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif username_active == True:
                        if event.key == pygame.K_BACKSPACE:
                            self.username_text = self.username_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            username_active = False
                        else:
                            self.username_text += event.unicode
                    if event.key == pygame.K_RETURN:
                        if (
                            len(self.input_information()[0]) > 0
                            and len(self.input_information()[0]) > 0
                        ):
                            print(self.input_information())
                            if (
                                ChooseCharacter(
                                    self.screen, self.font, self.input_information()[0]
                                ).menu()
                                == False
                            ):
                                running = False
                            else:
                                ChooseCharacter(
                                    self.screen, self.font, self.input_information()[0]
                                ).menu()
            if username_active:
                self.username_input_color = self.input_clicked_color
            elif not username_active:
                self.username_input_color = self.input_not_clicked_color
            pygame.display.update()
            clock.tick(60)
        return running
