import pygame, sys

clock = pygame.time.Clock()


class Lobby:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.name = "Lobby"

    def lobby(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_srf = self.font.render("Lobby", True, (255, 255, 255))
            self.screen.blit(text_srf, (50, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            pygame.display.update()
            clock.tick(60)

    def welcome(self):
        return self.name
