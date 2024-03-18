import pygame
from constants import *
from button import Button
from character import Character

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 54)


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue-Less")


def draw_menu():
    img = pygame.image.load("./assets/clue_home_background.png").convert()
    img_scaled = pygame.transform.scale(img, (WIDTH, HEIGHT))
    WINDOW.blit(img_scaled, (0, 0))
    welcome_surf = font.render("Clue-Less", False, (0))
    welcome_rect = welcome_surf.get_rect(center=(WIDTH / 2, 150))
    WINDOW.blit(welcome_surf, welcome_rect)
    join_game_btn = Button(
        WINDOW,
        (WIDTH / 2) - (BTN_WIDTH / 2),
        (HEIGHT / 2) - (BTN_HEIGHT / 2),
        "Join Game",
    )
    join_game_btn.draw()
    return join_game_btn.clicked()


def draw_characters():
    pygame.draw.rect(WINDOW, (0), [0, 0, WIDTH, HEIGHT])
    char_msg_text = font.render("Choose a Character", False, (255, 255, 255))
    char_msg_rect = char_msg_text.get_rect(center=(WIDTH / 2, 100))
    WINDOW.blit(char_msg_text, char_msg_rect)
    file_names = [
        "Colonel_Mustard",
        "Miss_Scarlet",
        "Mr_Green",
        "Mrs_Peacock",
        "Mrs_White",
        "Professor_Plum",
    ]
    display_x = 375
    display_y = 200
    for i in range(len(file_names)):
        if i == len(file_names) / 2:
            display_y += 350
            display_x = 375
        char = Character(
            WINDOW, display_x, display_y, 175, 275, f"./assets/{file_names[i]}.png"
        )
        char.draw()
        display_x += 225
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
