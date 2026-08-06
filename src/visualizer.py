from .drone import Drone
from .colors import DRONE_COLORS
import os
import math
import random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


class Visualizer:
    def __init__(self, graph, start_hub_name=None,
                 end_hub_name=None, nb_drones=0, path=None):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name
        self.nb_drones = nb_drones
        if path:
            self.path = path
        else:
            self.path = [start_hub_name]
        self.last_move_time = 0
        self.zone_occupancy = {}
        for name in self.graph.zones:
            self.zone_occupancy[name] = 0
        self.zone_occupancy[start_hub_name] = nb_drones
        self.path_index = 0
        self.turn_count = 0
        self.drone_colors = []
        for i in range(nb_drones):
            color = random.choice(DRONE_COLORS)
            self.drone_colors.append(color)
        self.padding = 100
        self.drones = [Drone(self.path, drone_id=i) for i in range(self.nb_drones)]
        self.move_interval = 1500
        self.propeller_angle = 0

    def reset(self):
        self.zone_occupancy = {}
        for name in self.graph.zones:
            self.zone_occupancy[name] = 0
        self.zone_occupancy[self.start_hub_name] = self.nb_drones
        self.drones = []
        for i in range(self.nb_drones):
            drone = Drone(self.path, drone_id=i)
            self.drones.append(drone)
        self.last_move_time = pygame.time.get_ticks()
        self.turn_count = 0

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

    def draw_connections(self, screen, screen_w, screen_h,
                         min_x, max_x, min_y, max_y):
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
            # 3 lines
            ux = dx / distance
            uy = dy / distance
            start_point = (sx1 + ux * 80, sy1 + uy * 80)
            end_point = (sx2 - ux * 80, sy2 - uy * 80)
            pygame.draw.line(screen, (200, 200, 200),
                             start_point, end_point, 1)

    def draw_drones(self, screen, screen_w, screen_h,
                    min_x, max_x, min_y, max_y, font):
        drones_by_zone = {}
        for drone in self.drones:
            if drone.current_zone not in drones_by_zone:
                drones_by_zone[drone.current_zone] = []
            drones_by_zone[drone.current_zone].append(drone)
        for zone_name, drones in drones_by_zone.items():
            zone = self.graph.zones[zone_name]
            sx, sy = self.to_screen_coords(
                zone.x, zone.y, screen_w, screen_h,
                min_x, max_x, min_y, max_y
            )
            count = len(drones)
            for i, drone in enumerate(drones):
                color = self.drone_colors[drone.drone_id]
                angle_deg = (360 / count) * i
                angle = math.radians(angle_deg)
                cx = sx + math.cos(angle) * 55
                cy = sy + math.sin(angle) * 55
                drone_arms = [
                    (cx - 11, cy - 11, cx - 31, cy - 31),
                    (cx + 11, cy - 11, cx + 31, cy - 31),
                    (cx - 11, cy + 11, cx - 31, cy + 31),
                    (cx + 11, cy + 11, cx + 31, cy + 31),
                ]
                for start_x, start_y, end_x, end_y in drone_arms:
                    pygame.draw.line(screen, color,
                                     (start_x, start_y), (end_x, end_y), 4)
                    ux = end_x - start_x
                    uy = end_y - start_y
                    length = math.sqrt(ux * ux + uy * uy)
                    ux, uy = ux / length, uy / length
                    px, py = -uy, ux
                    d1x, d1y = ux + px * 0.5, uy + py * 0.5
                    d2x, d2y = ux - px * 0.5, uy - py * 0.5
                    d1x, d1y = d1x / math.hypot(d1x, d1y), d1y / math.hypot(d1x, d1y)
                    d2x, d2y = d2x / math.hypot(d2x, d2y), d2y / math.hypot(d2x, d2y)
                    cos_a = math.cos(math.radians(self.propeller_angle))
                    sin_a = math.sin(math.radians(self.propeller_angle))
                    d1x, d1y = d1x * cos_a - d1y * sin_a, d1x * sin_a + d1y * cos_a
                    d2x, d2y = d2x * cos_a - d2y * sin_a, d2x * sin_a + d2y * cos_a
                    pygame.draw.line(screen, (200, 200, 200),
                                    (end_x - d1x * 10, end_y - d1y * 10),
                                    (end_x + d1x * 10, end_y + d1y * 10), 2)
                    pygame.draw.line(screen, (200, 200, 200),
                                    (end_x - d2x * 10, end_y - d2y * 10),
                                    (end_x + d2x * 10, end_y + d2y * 10), 2)
                    pygame.draw.circle(screen, (200, 200, 200), (end_x, end_y), 3)
                pygame.draw.circle(screen, color, (cx, cy), 18)
                pygame.draw.circle(screen, (200, 200, 200), (cx, cy), 13)
                label_text = f"D{drone.drone_id + 1}"
                shadow = font.render(label_text, True, (0, 0, 0))
                screen.blit(shadow, shadow.get_rect(center=(cx + 2, cy - 26)))
                label = font.render(label_text, True, color)
                screen.blit(label, label.get_rect(center=(cx, cy - 28)))

    def can_enter_zone(self, zone_name):
        zone = self.graph.zones[zone_name]
        return self.zone_occupancy[zone_name] < zone.max_drones

    def can_use_link(self, connection, link_usage):
        if connection is None:
            return True
        return link_usage.get(id(connection), 0) < connection.max_link_capacity

    def try_move_drone(self, drone, link_usage):
        next_zone = drone.next_zone
        if next_zone is None:
            return False
        if self.can_enter_zone(next_zone) is False:
            return False
        connection = self.graph.get_connection(drone.current_zone, next_zone)
        if self.can_use_link(connection, link_usage) is False:
            return False
        self.zone_occupancy[drone.current_zone] -= 1
        self.zone_occupancy[next_zone] += 1
        if connection is not None:
            # ce line
            link_usage[id(connection)] = link_usage.get(id(connection), 0) + 1
        drone.path_index += 1
        return True

    def all_delivered(self):
        for drone in self.drones:
            if drone.current_zone != self.end_hub_name:
                return False
        return True

    def step(self):
        if self.all_delivered():
            return
        link_usage = {}
        moved_this_turn = []
        for drone in self.drones:
            if drone.current_zone == self.end_hub_name:
                continue
            destination = drone.next_zone
            if destination is None:
                continue
            moved = self.try_move_drone(drone, link_usage)
            if moved:
                moved_this_turn.append(f"D{drone.drone_id + 1}-{destination}")
        self.turn_count += 1
        if moved_this_turn:
            print(" ".join(moved_this_turn))
        if self.all_delivered():
            print(f"All drones delivered in {self.turn_count} turns.")

    def draw_hint(self, screen, screen_h, font):
        hint_text = "Press F5 to reset the simulation"
        shadow_surface = font.render(hint_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(bottomleft=(12, screen_h - 8))
        screen.blit(shadow_surface, shadow_rect)
        text_surface = font.render(hint_text, True, (200, 200, 200))
        text_rect = text_surface.get_rect(bottomleft=(10, screen_h - 10))
        screen.blit(text_surface, text_rect)

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
        try:
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
                now = pygame.time.get_ticks()
                if now - self.last_move_time >= self.move_interval:
                    self.step()
                    self.last_move_time = now
                self.propeller_angle += 0.5
                if self.propeller_angle >= 360:
                    self.propeller_angle = 0
                self.draw_connections(screen, screen_w, screen_h,
                                      min_x, max_x, min_y, max_y)
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
                        shadow_surface = font_small.render(capacity_text, True, (0, 0, 0))
                        shadow_rect = shadow_surface.get_rect(center=[sx + 2, sy + 112])
                        screen.blit(shadow_surface, shadow_rect)
                        capacity_surface = font_small.render(capacity_text, True, (200, 200, 200))
                        capacity_rect = capacity_surface.get_rect(center=[sx, sy + 110])
                        screen.blit(capacity_surface, capacity_rect)
                self.draw_drones(screen, screen_w, screen_h, min_x, max_x, min_y, max_y, font_small)
                self.draw_hint(screen, screen_h, font_small)
                pygame.display.flip()
        except KeyboardInterrupt:
            print("\033[H\033[J", end="")
            print("Interrupted by user, exiting cleanly.", end="")
        finally:
            pygame.quit()
