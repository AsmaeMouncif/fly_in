import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import math
import random
from .drone import Drone
from .colors import DRONE_COLORS


class Visualizer:
    def __init__(self, graph, start_hub_name=None, end_hub_name=None, nb_drones=0, path=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name
        self.nb_drones = nb_drones
        if path:
            self.path = path
        else:
            self.path = [start_hub_name]
        # self.path_index = 0
        # self.padding = 100
        # self.zone_occupancy = {name: 0 for name in self.graph.zones}
        # self.zone_occupancy[start_hub_name] = nb_drones
        # self.drones = [Drone(self.path, drone_id=i) for i in range(self.nb_drones)]
        # self.move_interval = 1500
        # self.last_move_time = 0
        # self.drone_colors = [random.choice(DRONE_COLORS) for _ in range(nb_drones)]
        # self.propeller_angle = 0

    # def reset(self):
    #     self.zone_occupancy = {name: 0 for name in self.graph.zones}
    #     self.zone_occupancy[self.start_hub_name] = self.nb_drones
    #     self.drones = [Drone(self.path, drone_id=i) for i in range(self.nb_drones)]
    #     self.last_move_time = pygame.time.get_ticks()

    # def compute_bounds(self):
    #     min_x = None
    #     max_x = None
    #     min_y = None
    #     max_y = None
    #     for zone in self.graph.zones.values():
    #         if min_x is None or zone.x < min_x:
    #             min_x = zone.x
    #         if max_x is None or zone.x > max_x:
    #             max_x = zone.x
    #         if min_y is None or zone.y < min_y:
    #             min_y = zone.y
    #         if max_y is None or zone.y > max_y:
    #             max_y = zone.y
    #     return min_x, max_x, min_y, max_y

    # def to_screen_coords(self, x, y, screen_width, screen_height,
    #                      min_x, max_x, min_y, max_y):
    #     range_x = max_x - min_x
    #     range_y = max_y - min_y
    #     if range_x == 0:
    #         range_x = 1
    #     if range_y == 0:
    #         range_y = 1
    #     proportion_x = (x - min_x) / range_x
    #     proportion_y = (y - min_y) / range_y
    #     usable_width = screen_width - 2 * self.padding
    #     usable_height = screen_height - 2 * self.padding
    #     screen_x = self.padding + proportion_x * usable_width
    #     screen_y = self.padding + proportion_y * usable_height
    #     return int(screen_x), int(screen_y)

    # def draw_connections(self, screen, screen_w, screen_h, min_x, max_x, min_y, max_y):
    #     for connection in self.graph.connections:
    #         zone1 = self.graph.zones[connection.zone1]
    #         zone2 = self.graph.zones[connection.zone2]
    #         sx1, sy1 = self.to_screen_coords(
    #             zone1.x, zone1.y, screen_w, screen_h,
    #             min_x, max_x, min_y, max_y
    #         )
    #         sx2, sy2 = self.to_screen_coords(
    #             zone2.x, zone2.y, screen_w, screen_h,
    #             min_x, max_x, min_y, max_y
    #         )
    #         dx = sx2 - sx1
    #         dy = sy2 - sy1
    #         distance = math.sqrt(dx * dx + dy * dy)
    #         if distance == 0:
    #             continue
    #         #3lines
    #         ux, uy = dx / distance, dy / distance
    #         start_point = (sx1 + ux * 80, sy1 + uy * 80)
    #         end_point = (sx2 - ux * 80, sy2 - uy * 80)
    #         pygame.draw.line(screen, (200, 200, 200), start_point, end_point, 1)

    # def draw_drones(self, screen, screen_w, screen_h, min_x, max_x, min_y, max_y, font):
    #     drones_by_zone = {}
    #     for drone in self.drones:
    #         drones_by_zone.setdefault(drone.current_zone, []).append(drone)
    #     radius = 55
    #     for zone_name, drones in drones_by_zone.items():
    #         zone = self.graph.zones[zone_name]
    #         sx, sy = self.to_screen_coords(
    #             zone.x, zone.y, screen_w, screen_h,
    #             min_x, max_x, min_y, max_y
    #         )
    #         count = len(drones)
    #         for i, drone in enumerate(drones):
    #             color = self.drone_colors[drone.drone_id]
    #             angle = (2 * math.pi / count) * i
    #             dx = math.cos(angle) * radius
    #             dy = math.sin(angle) * radius
    #             cx = sx + dx
    #             cy = sy + dy
    #             arm = 20
    #             arm_width = 4
    #             arm_color = color
    #             x_color = (200, 200, 200)
    #             prop_size = 10
    #             prop_spread = 0.5
    #             prop_width = 2
    #             circle_radius = 3
    #             arm_ends = [
    #                 (cx - 11, cy - 11, cx - 11 - arm, cy - 11 - arm),
    #                 (cx + 11, cy - 11, cx + 11 + arm, cy - 11 - arm),
    #                 (cx - 11, cy + 11, cx - 11 - arm, cy + 11 + arm),
    #                 (cx + 11, cy + 11, cx + 11 + arm, cy + 11 + arm),
    #             ]
    #             for start_x, start_y, end_x, end_y in arm_ends:
    #                 pygame.draw.line(screen, arm_color, (start_x, start_y), (end_x, end_y), arm_width)
    #                 bdx, bdy = end_x - start_x, end_y - start_y
    #                 length = math.hypot(bdx, bdy)
    #                 ux, uy = bdx / length, bdy / length
    #                 px, py = -uy, ux
    #                 d1x, d1y = ux + px * prop_spread, uy + py * prop_spread
    #                 d2x, d2y = ux - px * prop_spread, uy - py * prop_spread
    #                 n1 = math.hypot(d1x, d1y)
    #                 n2 = math.hypot(d2x, d2y)
    #                 d1x, d1y = d1x / n1, d1y / n1
    #                 d2x, d2y = d2x / n2, d2y / n2
    #                 angle = math.radians(self.propeller_angle)
    #                 cos_a = math.cos(angle)
    #                 sin_a = math.sin(angle)
    #                 old_d1x = d1x
    #                 old_d1y = d1y
    #                 d1x = old_d1x * cos_a - old_d1y * sin_a
    #                 d1y = old_d1x * sin_a + old_d1y * cos_a
    #                 old_d2x = d2x
    #                 old_d2y = d2y
    #                 d2x = old_d2x * cos_a - old_d2y * sin_a
    #                 d2y = old_d2x * sin_a + old_d2y * cos_a
    #                 pygame.draw.line(screen, x_color,
    #                                   (end_x - d1x * prop_size, end_y - d1y * prop_size),
    #                                   (end_x + d1x * prop_size, end_y + d1y * prop_size), prop_width)
    #                 pygame.draw.line(screen, x_color,
    #                                   (end_x - d2x * prop_size, end_y - d2y * prop_size),
    #                                   (end_x + d2x * prop_size, end_y + d2y * prop_size), prop_width)
    #                 pygame.draw.circle(screen, x_color, (end_x, end_y), circle_radius)
    #             pygame.draw.circle(screen, color, (cx, cy), 18)
    #             pygame.draw.circle(screen, (200, 200, 208), (cx, cy), 13)
    #             label_text = f"D{drone.drone_id + 1}"
    #             shadow_surface = font.render(label_text, True, (0, 0, 0))
    #             shadow_rect = shadow_surface.get_rect(center=(cx + 2, cy - 28 + 2))
    #             screen.blit(shadow_surface, shadow_rect)
    #             label_surface = font.render(label_text, True, color)
    #             label_rect = label_surface.get_rect(center=(cx, cy - 28))
    #             screen.blit(label_surface, label_rect)
        
    # def can_enter_zone(self, zone_name):
    #     zone = self.graph.zones[zone_name]
    #     return self.zone_occupancy[zone_name] < zone.max_drones

    # #comprendre cette
    # def can_use_link(self, connection, link_usage):
    #     if connection is None:
    #         return True
    #     return link_usage.get(id(connection), 0) < connection.max_link_capacity
    # #name fonction check linj_usage
    # def try_move_drone(self, drone, link_usage):
    #     next_zone = drone.next_zone
    #     if next_zone is None:
    #         return False
    #     if self.can_enter_zone(next_zone) is False:
    #         return False
    #     #check cette
    #     connection = self.graph.get_connection(drone.current_zone, next_zone)
    #     if self.can_use_link(connection, link_usage) is False:
    #         return False
    #     self.zone_occupancy[drone.current_zone] -= 1
    #     self.zone_occupancy[next_zone] += 1
    #     ##check cette
    #     if connection is not None:
    #         link_usage[id(connection)] = link_usage.get(id(connection), 0) + 1
    #     drone.path_index += 1
    #     return True

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.reset()
            # cette
            # now = pygame.time.get_ticks()
            # if now - self.last_move_time >= self.move_interval:
            #     link_usage = {}
            #     for drone in self.drones:
            #         self.try_move_drone(drone, link_usage)
            #     self.last_move_time = now
            # self.propeller_angle += 0.5
            # if self.propeller_angle >= 360:
            #     self.propeller_angle = 0
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
                    capacity_text = f"{self.zone_occupancy[zone.name]} ⁄ {zone.max_drones}"
                    capacity_surface = font_small.render(capacity_text, True, (200, 200, 200))
                    capacity_rect = capacity_surface.get_rect(center=[sx, sy + 110])
                    screen.blit(capacity_surface, capacity_rect)
            self.draw_drones(screen, screen_w, screen_h, min_x, max_x, min_y, max_y, font_small)
            pygame.display.flip()
        pygame.quit()
