import pygame, sys, os
from frontend.lobby import Lobby
from frontend.game import Game
from frontend.button import Button
from frontend.create_game import CreateGame
from frontend.join_game import JoinGame
from frontend.test_lobby import LobbyScreen
from frontend.choose_character import ChooseCharacter
from frontend.constants import *

import threading #TODO: Maybe move this

import clue_client as client_backend

pygame.init()

pygame.display.set_caption("Clue-Less Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 36)

click = False

join_game = JoinGame(screen, font)
create_game = CreateGame(screen, font)
choose_character = ChooseCharacter(screen, font)
lobby_screen = LobbyScreen(screen, font)
       

create_game_btn = Button(screen, (WIDTH / 2) - (75), (HEIGHT / 2) - (135), "Create Game")
join_game_btn = Button(screen, (WIDTH / 2) - (75), (HEIGHT / 2) - (35), "Join Game")

def show_main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        img = pygame.image.load("./assets/clue_home_background.png").convert()
        img_scaled = pygame.transform.scale(img, (WIDTH, HEIGHT))
        screen.blit(img_scaled, (0, 0))
        text_srf = title_font.render(
            "Welcome to Clue-Less Digital", True, (255, 255, 255)
        )
        screen.blit(text_srf, ((WIDTH / 2) - (text_srf.get_width() / 2), 50))
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

def main():
    player_name = ""
    game_id = -1

    selections = show_main_menu()
    if len(selections) > 1:
        player_name = selections[1]
        game_id = selections[0]
    else:
        player_name = selections[0]

    character_choice = choose_character.menu()
    print(character_choice)

    print("1")
    if(game_id == -1):
        print("2")
        message_thread = threading.Thread(target=client_backend.create_game(player_name))
        print("3")
    else:
        message_thread = threading.Thread(target=client_backend.join_game(player_name, game_id))
    print("4")
    message_thread.daemon = True
    print("5")
    message_thread.start()
    print("6")

    lobby_screen.menu()

