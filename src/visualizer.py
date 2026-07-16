import math
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Visualizer:
    def __init__(self, graph, start_hub_name=None, end_hub_name=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name

    def draw_connections(self, screen):
        for connection in self.graph.connections:
            zone1 = self.graph.zones[connection.zone1]
            zone2 = self.graph.zones[connection.zone2]
            dx = zone2.x - zone1.x
            dy = zone2.y - zone1.y
            distance = math.hypot(dx, dy)
            if distance == 0:
                continue
            ux, uy = dx / distance, dy / distance
            start_point = (zone1.x + ux * 80, zone1.y + uy * 80)
            end_point = (zone2.x - ux * 80, zone2.y - uy * 80)
            pygame.draw.line(screen, (200, 200, 200), start_point, end_point, 1)

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
                self.draw_connections(screen)
                for zone in self.graph.zones.values():
                    pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 80, 3)
                    pygame.draw.circle(screen, zone.color, [zone.x, zone.y], 30)
                    if len(zone.name) <= 6:
                        display_text = zone.name
                        font = font_small
                    else:
                        display_text = zone.name[0]
                        font = font_big
                    text_surface = font.render(display_text, True, (200, 200, 200))
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
