import pygame
from constants import *
from button import Button
from character import Character

# initialize pygame
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue-Less")

# font declaration
font = pygame.font.Font(pygame.font.get_default_font(), 54)


# draw menu function to display on pygame load
def draw_menu():
    # draw clue img background
    img = pygame.image.load("./assets/clue_home_background.png").convert()
    img_scaled = pygame.transform.scale(img, (WIDTH, HEIGHT))
    WINDOW.blit(img_scaled, (0, 0))
    # draw window header message
    welcome_surf = font.render("Clue-Less", False, (0))
    welcome_rect = welcome_surf.get_rect(center=(WIDTH / 2, 150))
    WINDOW.blit(welcome_surf, welcome_rect)
    # draw join game button
    join_game_btn = Button(
        WINDOW,
        (WIDTH / 2) - (BTN_WIDTH / 2),
        (HEIGHT / 2) - (BTN_HEIGHT / 2),
        "Join Game",
    )
    join_game_btn.draw()
    return join_game_btn.clicked()


# draw character function to display the character options once user selects "Join Game" button from draw_menu()
def draw_characters():
    # draw background
    pygame.draw.rect(WINDOW, (0), [0, 0, WIDTH, HEIGHT])
    # draw window header message
    char_msg_text = font.render("Choose a Character", False, (255, 255, 255))
    char_msg_rect = char_msg_text.get_rect(center=(WIDTH / 2, 100))
    WINDOW.blit(char_msg_text, char_msg_rect)
    # file names to grab character images in loop, as well as output name
    file_names = [
        "Colonel_Mustard",
        "Miss_Scarlet",
        "Mr_Green",
        "Mrs_Peacock",
        "Mrs_White",
        "Professor_Plum",
    ]
    # iterate through the img files, output characters to window
    display_x = 375
    display_y = 200
    for i in range(len(file_names)):
        # limit 3 characters per row
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
            send_character_to_backend(selected character)

def send_character_to_backend(character):
    try:
        response = requests.post(BACKEND_URL, json = {"character": character})
        if response.status_code == 200:
            print("Thank you for selecting character!")
        else:
            print("Failed to select character. Please try again.")
    except Exception as e:
        print ("An error has occured.", str(e)) 


# run pygame
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
