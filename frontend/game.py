import pygame, sys
from frontend.character import Character
from frontend.constants import *

# from client import main

clock = pygame.time.Clock()
details_font = pygame.font.SysFont(None, 28)


# counter code, button text - https://www.youtube.com/watch?v=jyrP0dDGqgY


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
        self.pos = pygame.mouse.get_pos()
        self.board_pos = [0, 0]

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
            pygame.display.update()
            clock.tick(60)
        return running

    def welcome(self):
        return self.name
