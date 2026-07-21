import math
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Visualizer:
    def __init__(self, graph, start_hub_name=None, end_hub_name=None, nb_drones=0, path=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name
        self.nb_drones = nb_drones
        self.path = path if path else [start_hub_name]
        self.path_index = 0

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
    
    def draw_drones(self, screen):
        current_zone_name = self.path[self.path_index]
        zone = self.graph.zones[current_zone_name]
        for i in range(self.nb_drones):
            offset_x = (i % 3) * 15 - 15    # petit décalage horizontal pour ne pas superposer
            offset_y = (i // 3) * 15
            pygame.draw.circle(
                screen,
                (0, 0, 0),
                (zone.x + offset_x, zone.y + offset_y),
                6,
            )

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")
        background = pygame.image.load("assets/background.png").convert_alpha()
        background = pygame.transform.scale(background, screen.get_size())
        font_small = pygame.font.SysFont(None, 23)
        font_big = pygame.font.SysFont(None, 30)
        MOVE_EVENT = pygame.USEREVENT + 1          # <-- AJOUT
        pygame.time.set_timer(MOVE_EVENT, 1000)  
        try:
            running = True
            while running:
                screen.blit(background, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.VIDEORESIZE:
                        background = pygame.transform.scale(
                            pygame.image.load("assets/background.png").convert_alpha(),
                            (event.w, event.h),
                        )
                    elif event.type == MOVE_EVENT:                              # <-- AJOUT
                        if self.path_index + 1 < len(self.path):
                            self.path_index += 1
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
                self.draw_drones(screen)
                pygame.display.flip()
        except KeyboardInterrupt:
            print("The drones await your command.", end="")
        finally:
            pygame.quit()
