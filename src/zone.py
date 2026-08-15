"""Zone module.

Defines the Zone class, which represents a single node in the drone
routing graph, along with its position, type, color, and capacity
constraints.
"""

import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402
PYGAME_COLORS: list[str] = list(pygame.color.THECOLORS.keys())


class Zone:
    """Represents a single zone in the drone routing network.

    A zone is a node in the graph that drones can occupy or pass
    through. Its behavior in the simulation depends on its type
    (normal, blocked, restricted, or priority) and on its maximum
    drone capacity.

    Attributes:
        name (str): Unique name identifying the zone.
        x (int): X coordinate of the zone.
        y (int): Y coordinate of the zone.
        zone_type (str): Type of the zone, one of "normal",
            "blocked", "restricted", or "priority". Defaults to
            "normal".
        color (str): Color used for visual representation of the
            zone. Randomly chosen from the available pygame colors
            if not explicitly set.
        max_drones (int): Maximum number of drones that can occupy
            this zone simultaneously. Defaults to 1.
    """

    def __init__(self, name: str, x: int, y: int) -> None:
        """Initialize a Zone with a name and coordinates.

        Default values are applied for the zone's type, color, and
        maximum drone capacity; these can be overridden afterward
        (e.g., during parsing of zone metadata).

        Args:
            name (str): Unique name identifying the zone.
            x (int): X coordinate of the zone.
            y (int): Y coordinate of the zone.
        """
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = "normal"
        self.color: str = random.choice(PYGAME_COLORS)
        self.max_drones: int = 1
