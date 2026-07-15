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
                x = 100 + zone.x * 200
                y = 100 + zone.y * 200
                color = pygame.Color(zone.color)
                pygame.draw.circle(screen, color, [x, y], 80, 3)
                pygame.draw.circle(screen, color, [x, y], 30)
            pygame.display.flip()
        pygame.quit()
