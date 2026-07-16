import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Visualizer:
    def __init__(self, graph):
        self.graph = graph

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for zone in self.graph.zones.values():
                pygame.draw.circle(screen, zone.color, [550, 300], 80, 3)
                pygame.draw.circle(screen, zone.color, [550, 300], 30)
            pygame.display.flip()
        pygame.quit()
