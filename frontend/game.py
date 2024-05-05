import pygame, sys
from frontend.character import Character
from frontend.constants import *
import clue_game_logic

# from client import main

clock = pygame.time.Clock()
details_font = pygame.font.SysFont(None, 28)


# counter code, button text - https://www.youtube.com/watch?v=jyrP0dDGqgY

# Button constants
BUTTON_WIDTH = 170
BUTTON_HEIGHT = 30
BUTTON_MARGIN = 10

class Game:
    def __init__(self, screen, font, username, character_chosen, gamename=None):
        self.screen = screen
        self.font = font
        self.username = username
        self.character_chosen = character_chosen
        self.gamename = gamename
        self.name = "Game"
        self.clicked_up = False
        self.clicked_down = False
        self.clicked_right = False
        self.clicked_left = False
        self.valid_move = False
        self.buttons_enabled = False
        self.pos = pygame.mouse.get_pos()
        self.board_pos = [0, 0]

        # Buttons
        self.buttons = [
            ("Move", (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 300, HEIGHT - BUTTON_HEIGHT * 5 - BUTTON_MARGIN * 5 - 200)),
            ("Suggest", (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 300, HEIGHT - BUTTON_HEIGHT * 4 - BUTTON_MARGIN * 4 - 200)),
            ("Accuse", (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 300, HEIGHT - BUTTON_HEIGHT * 3 - BUTTON_MARGIN * 3 - 200)),
            ("View Cards", (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 300, HEIGHT - BUTTON_HEIGHT * 2 - BUTTON_MARGIN * 2 - 200)),
            ("End Turn", (WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 300, HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN - 200)),
        ]

    def get_room_names(self):
        room_list = list(clue_game_logic.Room)
        room_array = []
        for room in room_list:
            room_array.append(room.name)
        return room_array

    def game_board(self):
        block_size = 50
        y_counter = 0
        for x in range(150, 700, block_size):
            x_counter = 0
            for y in range(150, 700, block_size):
                if x == 300 or x == 500:
                    if x_counter % 4 == 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                elif y == 300 or y == 500:
                    if y_counter % 4 == 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.screen, color, rect, 1)
                x_counter += 1
            y_counter += 1

    def draw_buttons(self):
        for button_text, button_pos in self.buttons:
            button_rect = pygame.Rect(button_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            text_surface = self.font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def disable_buttons(self):
        for button_text, button_pos in self.buttons:
            button_rect = pygame.Rect(button_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)  # Gray out the button
            text_surface = self.font.render(button_text, True, (150, 150, 150))  # Dim the text color
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def enable_buttons(self):
        for button_text, button_pos in self.buttons:
            button_rect = pygame.Rect(button_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)  # Restore the button color
            text_surface = self.font.render(button_text, True, (255, 255, 255))  # Restore the text color
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def create_additional_buttons(self, button_names):
        additional_buttons = []
        for idx, name in enumerate(button_names):
            x = WIDTH - BUTTON_WIDTH - BUTTON_MARGIN - 100  # Move 100 pixels to the left
            y = HEIGHT - BUTTON_HEIGHT * (len(self.buttons) + idx + 1) - BUTTON_MARGIN * (len(self.buttons) + idx + 1)
            additional_buttons.append((name, (x, y)))
        self.buttons.extend(additional_buttons)

    def remove_extra_buttons(self):
        self.buttons = [button for button in self.buttons if button[0] in ["Move", "Suggest", "Accuse", "View Cards", "End Turn"]]

    def valid_grid_locations(self):
        valid_grid_locations = []
        block_size = 50
        y_counter = 0
        for x in range(150, 700, block_size):
            x_counter = 0
            for y in range(150, 700, block_size):
                if x == 300 or x == 500:
                    if x_counter % 4 == 1:
                        valid_grid_locations.append([x, y])
                elif y == 300 or y == 500:
                    if y_counter % 4 == 1:
                        valid_grid_locations.append([x, y])
                else:
                    valid_grid_locations.append([x, y])
                x_counter += 1
            y_counter += 1
        return valid_grid_locations

    def is_valid_grid_location(self, x_location, y_location):
        for i in self.valid_grid_locations():
            if (x_location == i[0]) and (y_location == i[1]):
                return True

    def display_username(self):
        username_srf = details_font.render(
            (f"Welcome, {self.username}"), True, (255, 255, 255)
        )
        self.screen.blit(username_srf, (1100, 100))

    def display_gamename(self):
        if self.gamename != None:
            msg = f"Gamename: {self.gamename}"
        else:
            msg = ""
        gamename_srf = details_font.render((msg), True, (255, 255, 255))
        self.screen.blit(gamename_srf, (1100, 200))

    def display_character_chosen(self):
        char_chosen_srf = details_font.render(
            (f"Character: {self.character_chosen}"), True, (255, 255, 255)
        )
        self.screen.blit(char_chosen_srf, (1100, 150))

    def starting_loc(self):
        char_starting_loc = {
            "MUSTARD": [600, 300],
            "SCARLET": [500, 200],
            "GREEN": [300, 600],
            "PEACOCK": [200, 500],
            "WHITE": [500, 600],
            "PLUM": [200, 300],
        }

        for key, value in char_starting_loc.items():
            if self.character_chosen == key:
                return value

    def menu(self):
        x_inc, y_inc = 0, 0
        player = Character(self.screen, self.starting_loc()[0], self.starting_loc()[1])
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_srf = self.font.render("Game", True, (255, 255, 255))
            self.screen.blit(text_srf, (50, 50))
            self.display_username()
            self.display_character_chosen()
            self.display_gamename()
            self.game_board()
            player.curr_location(x_inc=x_inc, y_inc=y_inc)
            player.display_curr_location(x_inc=x_inc, y_inc=y_inc)
            x_location = player.curr_location(x_inc=x_inc, y_inc=y_inc)[0]
            y_location = player.curr_location(x_inc=x_inc, y_inc=y_inc)[1]
            player.display_room_location(x_inc=x_inc, y_inc=y_inc)
            player.display(x_inc=x_inc, y_inc=y_inc)

            self.draw_buttons()  # Draw buttons

            if self.buttons_enabled:
                self.enable_buttons()
            else:
                self.disable_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_UP:
                        self.clicked_up = True
                    if event.key == pygame.K_DOWN:
                        self.clicked_down = True
                    if event.key == pygame.K_RIGHT:
                        self.clicked_right = True
                    if event.key == pygame.K_LEFT:
                        self.clicked_left = True
                if event.type == pygame.KEYDOWN and self.clicked_up == True:
                    # if player.curr_location(x_inc=x_inc, y_inc=y_inc)[1] > 150:
                    if self.is_valid_grid_location(x_location, y_location - 50):
                        y_inc -= 50
                        self.clicked_up = False
                    else:
                        y_inc -= 0
                elif event.type == pygame.KEYDOWN and self.clicked_down == True:
                    # if player.curr_location(x_inc=x_inc, y_inc=y_inc)[1] < 650:
                    if self.is_valid_grid_location(x_location, y_location + 50):
                        y_inc += 50
                        self.clicked_down = False
                    else:
                        y_inc += 0
                elif event.type == pygame.KEYDOWN and self.clicked_right == True:
                    # if player.curr_location(x_inc=x_inc, y_inc=y_inc)[0] < 650:
                    if self.is_valid_grid_location(x_location + 50, y_location):
                        x_inc += 50
                        self.clicked_right = False
                    else:
                        x_inc += 0
                elif event.type == pygame.KEYDOWN and self.clicked_left == True:
                    # if player.curr_location(x_inc=x_inc, y_inc=y_inc)[0] > 150:
                    if self.is_valid_grid_location(x_location - 50, y_location):
                        x_inc -= 50
                        self.clicked_left = False
                    else:
                        x_inc -= 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button_text, button_pos in self.buttons:
                        button_rect = pygame.Rect(button_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
                        if button_rect.collidepoint(mouse_pos):
                            if button_text == "Move" and self.buttons_enabled:
                                # Call move function
                                print("Move")
                                self.remove_extra_buttons()
                                return "1"
                            elif button_text == "Suggest" and self.buttons_enabled:
                                # Call suggest function
                                print("Suggest")
                                self.remove_extra_buttons()
                            elif button_text == "Accuse" and self.buttons_enabled:
                                # Call accuse function
                                print("Accuse")
                                self.remove_extra_buttons()
                            elif button_text == "View Cards" and self.buttons_enabled:
                                # Call view cards function
                                print("View Cards")
                                self.remove_extra_buttons()
                            elif button_text == "End Turn" and self.buttons_enabled:
                                # Call end turn function
                                print("End Turn")
                                self.remove_extra_buttons()
                            elif button_text in self.get_room_names():
                                return button_text
                            else:
                                print(f"Clicked on button: {button_text}")  # Print button name

            pygame.display.update()
            clock.tick(60)
        return running

    def welcome(self):
        return self.name
