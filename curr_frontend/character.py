import pygame, sys

pygame.init()

font = pygame.font.SysFont(None, 24)


class Character:
    def __init__(self, screen, starting_x, starting_y, text=None):
        self.screen = screen
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.text = text
        self.width = 50
        self.height = 50

    def curr_location(self, x_inc=0, y_inc=0):
        x_value = self.starting_x + x_inc
        y_value = self.starting_y + y_inc
        return [x_value, y_value]

    def room_location(self, x_inc=0, y_inc=0):
        x_val = self.curr_location(x_inc, y_inc)[0]
        y_val = self.curr_location(x_inc, y_inc)[1]
        # column 1
        if (x_val >= 150 and x_val <= 250) and (y_val >= 150 and y_val <= 250):
            return "Study"
        elif (x_val >= 150 and x_val <= 250) and (y_val >= 350 and y_val <= 450):
            return "Library"
        elif (x_val >= 150 and x_val <= 250) and (y_val >= 550 and y_val <= 650):
            return "Conservatory"
        # column 2
        elif (x_val >= 350 and x_val <= 450) and (y_val >= 150 and y_val <= 250):
            return "Hall"
        elif (x_val >= 350 and x_val <= 450) and (y_val >= 350 and y_val <= 450):
            return "Billiard Room"
        elif (x_val >= 350 and x_val <= 450) and (y_val >= 550 and y_val <= 650):
            return "Ballroom"
        # column 3
        elif (x_val >= 550 and x_val <= 650) and (y_val >= 150 and y_val <= 250):
            return "Lounge"
        elif (x_val >= 550 and x_val <= 650) and (y_val >= 350 and y_val <= 450):
            return "Dining Room"
        elif (x_val >= 550 and x_val <= 650) and (y_val >= 550 and y_val <= 650):
            return "Kitchen"
        else:
            return "Hallway"

    def display(self, x_inc=0, y_inc=0):
        char_rect = pygame.Rect(
            self.curr_location(x_inc, y_inc)[0],
            self.curr_location(x_inc, y_inc)[1],
            self.width,
            self.height,
        )
        pygame.draw.rect(self.screen, (155, 155, 155), char_rect)
