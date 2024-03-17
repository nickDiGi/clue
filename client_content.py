import pygame
from constants import *
from button import Button
from character import Character

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 24)


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue-Less")


def draw_menu():
    pygame.draw.rect(WINDOW, (0), [0, 0, WIDTH, HEIGHT])
    text = font.render("Welcome to Clue-Less", False, (155, 155, 155))
    WINDOW.blit(text, ((WIDTH / 2) - (BTN_WIDTH / 2), 200))
    join_game_btn = Button(
        WINDOW,
        (WIDTH / 2) - (BTN_WIDTH / 2),
        (HEIGHT / 2) - (BTN_HEIGHT / 2),
        "Select a Character",
    )
    join_game_btn.draw()
    return join_game_btn.clicked()


def draw_characters():
    pygame.draw.rect(WINDOW, (0), [0, 0, WIDTH, HEIGHT])
    file_names = [
        "Colonel_Mustard",
        "Miss_Scarlet",
        "Mr_Green",
        "Mrs_Peacock",
        "Mrs_White",
        "Professor_Plum",
    ]
    display_x = 200
    display_y = 200
    for i in range(len(file_names)):
        if i == len(file_names) / 2:
            display_y += 300
            display_x = 200
        char = Character(
            WINDOW, display_x, display_y, 150, 250, f"./assets/{file_names[i]}.png"
        )
        char.draw()
        display_x += 200
        if char.clicked():
            print(file_names[i].replace("_", " "))


def running():
    main_menu = True
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if main_menu:
            main_menu = draw_menu()
        else:
            draw_characters()
        pygame.display.flip()

    pygame.quit()


running()
