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
        self.padding = 100
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

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")
        background = pygame.image.load("assets/background.png")
        background = pygame.transform.scale(background, screen.get_size())
        min_x, max_x, min_y, max_y = self.compute_bounds()
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
            for zone in self.graph.zones.values():
                sx, sy = self.to_screen_coords(
                    zone.x, zone.y, screen_w, screen_h,
                    min_x, max_x, min_y, max_y
                )
                pygame.draw.circle(screen, zone.color, [sx, sy], 80, 3)
                pygame.draw.circle(screen, zone.color, [sx, sy], 30)
            pygame.display.flip()
        pygame.quit()
