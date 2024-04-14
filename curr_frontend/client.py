import pygame, sys
from lobby import Lobby
from game import Game
from button import Button
from create_game import CreateGame
from join_game import JoinGame

pygame.init()

pygame.display.set_caption("Clue-Less Game")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

click = False

start_game = JoinGame(screen, font)

start_game_btn = Button(screen, 50, 150, "Start Game")


def main():
    while True:
        screen.fill((0, 0, 0))
        text_srf = font.render("Welcome to Clue-Less Digital", True, (255, 255, 255))
        screen.blit(text_srf, (50, 50))
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


main()
# clue_characters = [
#     ["Prof. Plum", "Miss Scarlett", "Mr. Green"],
#     ["Mrs. White", "Mrs. Peacock", "Colonel Mustard"],
# ]

# print(len(clue_characters))
