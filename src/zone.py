import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
DEFAULT_COLOR = list(pygame.color.THECOLORS.keys())


class Zone:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = "normal"
        self.color = random.choice(DEFAULT_COLOR)
        self.max_drones = 1
