import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Visualizer:
    def __init__(self, graph, start_hub_name=None, end_hub_name=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")
        font_small = pygame.font.SysFont(None, 23)
        font_big = pygame.font.SysFont(None, 30)
        try:
            running = True
            while running:
                screen.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                for zone in self.graph.zones.values():
                    pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 80, 3)
                    pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 30)
                    pygame.draw.line(screen, (200, 200, 200), [100, 300], [550, 300], 1)
                    if len(zone.name) <= 6:
                        display_text = zone.name
                        font = font_small
                    else:
                        display_text = zone.name[0]
                        font = font_big
                    text_surface = font.render(display_text, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=[zone.x, zone.y])
                    screen.blit(text_surface, text_rect)
                    if zone.name not in (self.start_hub_name, self.end_hub_name):
                        capacity_text = f"0 ⁄ {zone.max_drones}"
                        capacity_surface = font_small.render(capacity_text, True, (200, 200, 200))
                        capacity_rect = capacity_surface.get_rect(center=[zone.x, zone.y + 110])
                        screen.blit(capacity_surface, capacity_rect)
                pygame.display.flip()
        except KeyboardInterrupt:
            print("The drones await your command.", end="")
        finally:
            pygame.quit()
