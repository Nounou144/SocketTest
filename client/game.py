import pygame
from sys import exit
from protocols import Protocols

class SocketTest:
    #Initiate Game
    def __init__(self, client):
        self.client = client
        client.run()
        self.FPS = 60 # FPS

        # Fonts
        self.txt_font = None

    def handle_events(self, event):
        # Connected
        if self.client.connected:
            # If you have count
            if self.client.count != None:
                # When holding mouse down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.client.send(Protocols.HOLD, None)
                # When releasing mouse
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.client.send(Protocols.RELEASE, None)
    
    # Draw
    def draw(self, screen):
        # Fill screen with white
        screen.fill((255, 255, 255))

        # Draw
        # Loading screen if not connected
        if not self.client.connected:
            self.draw_loading(screen)
        #Draw Count
        self.draw_count(screen)

        # Update Game State
        pygame.display.update()

    # Loading Screen
    def draW_loading(self, screen):
        loading_surface = self.txt_font.reder("Loading...", True, (0, 0, 0))
        loading_rect = loading_surface.get_rect(center = (400, 300))
        screen.blit(loading_surface, loading_rect)
    
    # Count
    def draw_count(self, screen):
        count_surface = self.txt_font.render(f"Count: {self.client.count}", True, (0, 0, 0))
        count_rect = count_surface.get_rect(center = (400, 300))
        screen.blit(count_surface, count_rect)

    #Running game
    def run(self):
        #Initiate PyGame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Socket Test")
        clock = pygame.time.Clock()

        #Fonts
        self.txt_font = pygame.font.SysFont("Arial", 50)

        # Start up
        self.client.connect()

        while True:
            clock.tick(self.FPS)

            # Events
            for event in pygame.event.get():
                # User exits the game
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                    exit()
                else:
                    self.handle_events(event)

            # Draw
            self.draw(screen)