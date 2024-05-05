import pygame
import sys
import clue_game_logic

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

game_id = 11111

#class Player:
#    def __init__(self, name, character):
#        self.name = name
#        self.character = character

class LobbyScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.players = []
        self.font = font
        self.running = True

    def add_player(self, new_player_list):
        for new_player in new_player_list:
            already_in_lobby = False
            for curr_player in self.players:
                if curr_player.name == new_player.get_name():
                    already_in_lobby = True
            if not already_in_lobby: self.players.append(new_player)

    def set_game_id(self, new_game_id):
        global game_id
        game_id = new_game_id

    def draw(self):
        global game_id

        self.screen.fill(BLACK)

        # Draw game ID label
        game_id_font = pygame.font.SysFont(None, 24)
        game_id_text = game_id_font.render(f"Game ID {game_id}", True, WHITE)
        game_id_rect = game_id_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(game_id_text, game_id_rect)

        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("Lobby", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        text_y = 120
        for player in self.players:
            player_text = f"{player.name}: {player.character}"
            player_render = self.font.render(player_text, True, WHITE)
            player_rect = player_render.get_rect(topleft=(50, text_y))
            self.screen.blit(player_render, player_rect)
            text_y += 30

        pygame.display.flip()

    def menu(self):
        pygame.display.set_caption("Lobby Screen")
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            self.draw()
            clock.tick(60)

    def welcome(self):
        return self.name
