import pygame, sys
from character import Character

# from client import main

clock = pygame.time.Clock()


# counter code, button text - https://www.youtube.com/watch?v=jyrP0dDGqgY


class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.name = "Game"
        self.clicked_up = False
        self.clicked_down = False
        self.clicked_right = False
        self.clicked_left = False
        self.pos = pygame.mouse.get_pos()
        self.board_pos = [0, 0]

    def game_board(self):
        pass

    def menu(self):
        x_inc, y_inc = 0, 0
        player = Character(self.screen)
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_srf = self.font.render("Game", True, (255, 255, 255))
            self.screen.blit(text_srf, (50, 50))
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
                if event.type == pygame.KEYUP and self.clicked_up == True:
                    y_inc -= 30
                    self.clicked_up = False
                elif event.type == pygame.KEYDOWN and self.clicked_down == True:
                    y_inc += 30
                    self.clicked_down = False
                elif event.type == pygame.KEYDOWN and self.clicked_right == True:
                    x_inc += 30
                    self.clicked_right = False
                elif event.type == pygame.KEYDOWN and self.clicked_left == True:
                    x_inc -= 30
                    self.clicked_left = False
            pygame.display.update()
            clock.tick(60)
        return running

    def welcome(self):
        return self.name
