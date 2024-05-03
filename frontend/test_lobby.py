import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character

class LobbyScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.players = []
        self.font = font

    def add_player(self, name, character):
        self.players.append(Player(name, character))

    def draw(self):
        self.screen.fill(BLACK)

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

        # Sample players
        self.add_player("Player 1", "Character A")
        self.add_player("Player 2", "Character B")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.draw()
            clock.tick(60)

    def welcome(self):
        return self.name
