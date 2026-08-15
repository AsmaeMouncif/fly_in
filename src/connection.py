"""Connection module.

Defines the Connection class, which represents a bidirectional link
between two zones in the drone routing graph.
"""


class Connection:
    """Represents a bidirectional connection (edge) between two zones.

    A connection links two zones and defines how many drones can
    traverse it simultaneously via its capacity limit.

    Attributes:
        zone1 (str): Name of the first zone.
        zone2 (str): Name of the second zone.
        max_link_capacity (int): Maximum number of drones that can
            traverse this connection simultaneously.
    """

    def __init__(self, zone1: str, zone2: str, max_link_capacity: int) -> None:
        """Initialize a Connection between two zones.

        Args:
            zone1 (str): Name of the first zone.
            zone2 (str): Name of the second zone.
            max_link_capacity (int): Maximum number of drones that can
                traverse this connection simultaneously.
        """
        self.zone1: str = zone1
        self.zone2: str = zone2
        self.max_link_capacity: int = max_link_capacity

    def find_other_end(self, zone_name: str) -> str:
        """Return the zone at the other end of this connection.

        Args:
            zone_name (str): Name of one of the two zones linked by
                this connection.

        Returns:
            str: The name of the other zone connected by this
            connection.
        """
        if zone_name == self.zone1:
            return self.zone2
        else:
            return self.zone1
