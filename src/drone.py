"""Drone module.

Defines the Drone class, which represents an individual drone moving
along a path through the zone network during the simulation.
"""


class Drone:
    """Represents a single drone navigating through the zone network.

    A drone follows a precomputed path (a sequence of zone names) from
    the start zone to the end zone. It keeps track of its current
    position in the path as well as its transit state when crossing a
    connection that requires multiple turns (e.g., toward a restricted
    zone).

    Attributes:
        path (list[str]): Ordered sequence of zone names the drone
            must follow to reach its destination.
        path_index (int): Index of the drone's current zone within
            `path`.
        drone_id (int): Unique identifier of the drone.
        in_transit (bool): Whether the drone is currently traveling
            over a multi-turn connection (e.g., toward a restricted
            zone).
        transit_turns_left (int): Number of turns remaining before the
            drone arrives at its destination while in transit.
    """

    def __init__(self, path: list[str], drone_id: int = 0) -> None:
        """Initialize a Drone with its assigned path and identifier.

        Args:
            path (list[str]): Ordered sequence of zone names
                representing the drone's route from start to end.
            drone_id (int): Unique identifier of the drone.
                Defaults to 0.
        """
        self.path: list[str] = path
        self.path_index: int = 0
        self.drone_id: int = drone_id
        self.in_transit: bool = False
        self.transit_turns_left: int = 0

    @property
    def current_zone(self) -> str:
        """str: Name of the zone the drone currently occupies."""
        return self.path[self.path_index]

    @property
    def next_zone(self) -> str | None:
        """str | None: Name of the next zone in the drone's path.

        Returns:
            str | None: The name of the next zone to move to, or
            None if the drone has already reached the end of its
            path.
        """
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def assign_new_path(self, new_path: list[str]) -> None:
        """Assign a new path to the drone and reset its progress.

        This is typically used when a drone must be rerouted (e.g.,
        due to a blocked zone or connection), restarting its position
        tracking at the beginning of the new path.

        Args:
            new_path (list[str]): The new ordered sequence of zone
                names the drone should follow.
        """
        self.path = new_path
        self.path_index = 0
