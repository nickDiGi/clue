import pygame, sys
from frontend.create_game import CreateGame
from frontend.join_game import JoinGame
from frontend.button import Button
from frontend.constants import *

pygame.display.set_caption("Clue-Less Game")
title_font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
click = False

class MainMenu:
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

    def menu(self):
        running = True
        join_game = JoinGame(self.screen, self.font)
        create_game = CreateGame(self.screen, self.font)

        create_game_btn = Button(self.screen, (WIDTH / 2) - (75), (HEIGHT / 2) - (135), "Create Game")
        join_game_btn = Button(self.screen, (WIDTH / 2) - (75), (HEIGHT / 2) - (35), "Join Game")
        while running:
            self.screen.fill((0, 0, 0))
            img = pygame.image.load("./assets/clue_home_background.png").convert()
            img_scaled = pygame.transform.scale(img, (WIDTH, HEIGHT))
            self.screen.blit(img_scaled, (0, 0))
            text_srf = title_font.render(
                "Welcome to Clue-Less Digital", True, (255, 255, 255)
            )
            self.screen.blit(text_srf, ((WIDTH / 2) - (text_srf.get_width() / 2), 50))
            mx, my = pygame.mouse.get_pos()

            if create_game_btn.rect().collidepoint((mx, my)):
                if click:
                    running = False
                    return create_game.menu()
            create_game_btn.rect_bg(), create_game_btn.rect_text()

            if join_game_btn.rect().collidepoint((mx, my)):
                if click:
                    running = False
                    return join_game.menu()
            join_game_btn.rect_bg(), join_game_btn.rect_text()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            clock.tick(60)

