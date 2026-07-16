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
        font_small = pygame.font.SysFont(None, 23)
        font_big = pygame.font.SysFont(None, 30)
        running = True
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for zone in self.graph.zones.values():
                pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 80, 3)
                pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 30)
                if len(zone.name) <= 6:
                    display_text = zone.name
                    font = font_small
                else:
                    display_text = zone.name[0]
                    font = font_big
                text_surface = font.render(display_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=[zone.x, zone.y])
                screen.blit(text_surface, text_rect)
            pygame.display.flip()
        pygame.quit()
