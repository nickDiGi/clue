import pygame, sys, os
from lobby import Lobby
from game import Game
from button import Button
from create_game import CreateGame
from join_game import JoinGame
from constants import *

pygame.init()

pygame.display.set_caption("Clue-Less Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 36)

click = False

start_game = JoinGame(screen, font)

start_game_btn = Button(screen, (WIDTH / 2) - (75), (HEIGHT / 2) - (35), "Start Game")


def main():
    while True:
        screen.fill((0, 0, 0))
        img = pygame.image.load("./assets/clue_home_background.png").convert()
        img_scaled = pygame.transform.scale(img, (WIDTH, HEIGHT))
        screen.blit(img_scaled, (0, 0))
        text_srf = title_font.render(
            "Welcome to Clue-Less Digital", True, (255, 255, 255)
        )
        screen.blit(text_srf, ((WIDTH / 2) - (text_srf.get_width() / 2), 50))
        mx, my = pygame.mouse.get_pos()
        if start_game_btn.rect().collidepoint((mx, my)):
            if click:
                start_game.menu()
        start_game_btn.rect_bg(), start_game_btn.rect_text()
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


# main()

game_screen = Game(screen, font)


def work_on_game_screen():
    game_screen.menu()


work_on_game_screen()
