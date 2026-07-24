import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import math
from .drone import Drone


class Visualizer:
    def __init__(self, graph, start_hub_name=None, end_hub_name=None, nb_drones=0, path=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name
        self.nb_drones = nb_drones
        self.path = path if path else [start_hub_name]
        self.path_index = 0
        self.padding = 100
        self.zone_occupancy = {name: 0 for name in self.graph.zones}
        self.zone_occupancy[start_hub_name] = nb_drones
        self.drones = [Drone(self.path) for _ in range(self.nb_drones)]
        self.move_interval = 800  # ms entre chaque mouvement
        self.last_move_time = 0
    #cette comprendre
    def compute_bounds(self):
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for zone in self.graph.zones.values():
            if min_x is None or zone.x < min_x:
                min_x = zone.x
            if max_x is None or zone.x > max_x:
                max_x = zone.x
            if min_y is None or zone.y < min_y:
                min_y = zone.y
            if max_y is None or zone.y > max_y:
                max_y = zone.y
        return min_x, max_x, min_y, max_y
    #cette comprendre
    def to_screen_coords(self, x, y, screen_width, screen_height,
                         min_x, max_x, min_y, max_y):
        range_x = max_x - min_x
        range_y = max_y - min_y
        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1
        proportion_x = (x - min_x) / range_x
        proportion_y = (y - min_y) / range_y
        usable_width = screen_width - 2 * self.padding
        usable_height = screen_height - 2 * self.padding
        screen_x = self.padding + proportion_x * usable_width
        screen_y = self.padding + proportion_y * usable_height
        return int(screen_x), int(screen_y)

    def draw_connections(self, screen, screen_w, screen_h, min_x, max_x, min_y, max_y):
        for connection in self.graph.connections:
            zone1 = self.graph.zones[connection.zone1]
            zone2 = self.graph.zones[connection.zone2]
            sx1, sy1 = self.to_screen_coords(
                zone1.x, zone1.y, screen_w, screen_h,
                min_x, max_x, min_y, max_y
            )
            sx2, sy2 = self.to_screen_coords(
                zone2.x, zone2.y, screen_w, screen_h,
                min_x, max_x, min_y, max_y
            )
            dx = sx2 - sx1
            dy = sy2 - sy1
            distance = math.sqrt(dx * dx + dy * dy)
            if distance == 0:
                continue
            #3lines
            ux, uy = dx / distance, dy / distance
            start_point = (sx1 + ux * 80, sy1 + uy * 80)
            end_point = (sx2 - ux * 80, sy2 - uy * 80)
            pygame.draw.line(screen, (200, 200, 200), start_point, end_point, 1)

    def draw_drones(self, screen, screen_w, screen_h, min_x, max_x, min_y, max_y):
        start_zone = self.graph.zones[self.start_hub_name]
        sx, sy = self.to_screen_coords(
                start_zone.x, start_zone.y, screen_w, screen_h,
                min_x, max_x, min_y, max_y
            )
        pygame.draw.circle(screen, (255, 255, 255), (sx, sy), 7)

    def can_enter_zone(self, zone_name):
        zone = self.graph.zones[zone_name]
        return self.zone_occupancy[zone_name] < zone.max_drones

    def try_move_drone(self, drone):
        next_zone = drone.next_zone
        if next_zone is None:
            return False
        if self.can_enter_zone(next_zone) is False:
            return False
        self.zone_occupancy[drone.current_zone] -= 1
        self.zone_occupancy[next_zone] += 1
        drone.path_index += 1
        return True

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")
        background = pygame.image.load("assets/background.png")
        background = pygame.transform.scale(background, screen.get_size())
        min_x, max_x, min_y, max_y = self.compute_bounds()
        font_small = pygame.font.SysFont(None, 23)
        font_big = pygame.font.SysFont(None, 30)
        running = True
        while running:
            screen_w, screen_h = screen.get_size()
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    background = pygame.transform.scale(
                        pygame.image.load("assets/background.png"),
                        (event.w, event.h),
                    )
            # cette
            now = pygame.time.get_ticks()
            if now - self.last_move_time >= self.move_interval:
                for drone in self.drones:
                    self.try_move_drone(drone)
                self.last_move_time = now
            self.draw_connections(screen, screen_w, screen_h, min_x, max_x, min_y, max_y)
            for zone in self.graph.zones.values():
                sx, sy = self.to_screen_coords(
                    zone.x, zone.y, screen_w, screen_h,
                    min_x, max_x, min_y, max_y
                )
                pygame.draw.circle(screen, zone.color, [sx, sy], 80, 3)
                pygame.draw.circle(screen, zone.color, [sx, sy], 30)
                if len(zone.name) <= 6:
                    display_text = zone.name
                    font = font_small
                else:
                    display_text = zone.name[0]
                    font = font_big
                shadow_surface = font.render(display_text, True, (0, 0, 0))
                shadow_rect = shadow_surface.get_rect(center=[sx + 2, sy + 2])
                screen.blit(shadow_surface, shadow_rect)
                text_surface = font.render(display_text, True, (200, 200, 200))
                text_rect = text_surface.get_rect(center=[sx, sy])
                screen.blit(text_surface, text_rect)
                if zone.name not in (self.start_hub_name, self.end_hub_name):
                    capacity_text = f"0 ⁄ {zone.max_drones}"
                    capacity_surface = font_small.render(capacity_text, True, (200, 200, 200))
                    capacity_rect = capacity_surface.get_rect(center=[sx, sy + 110])
                    screen.blit(capacity_surface, capacity_rect)
            self.draw_drones(screen, screen_w, screen_h, min_x, max_x, min_y, max_y)
            pygame.display.flip()
        pygame.quit()
