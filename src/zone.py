from typing import List
import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
PYGAME_COLORS: List[str] = list(pygame.color.THECOLORS.keys())


class Zone:
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = "normal"
        self.color: str = random.choice(PYGAME_COLORS)
        self.max_drones: int = 1
