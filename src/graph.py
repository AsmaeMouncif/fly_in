"""Graph module.

Defines the Graph class, which represents the network of zones and
connections used for pathfinding and simulation of drone movements.
"""

from .zone import Zone
from .connection import Connection


class Graph:
    """Represents the zone network as an undirected graph.

    The graph stores all zones and connections parsed from the input
    file, along with an adjacency structure that allows efficient
    lookup of neighboring zones for pathfinding and simulation
    purposes.

    Attributes:
        zones (dict[str, Zone]): Mapping of zone names to their
            corresponding Zone objects.
        connections (list[Connection]): All connections defined in
            the graph.
        adjacency (dict[str, list[Connection]]): Mapping of each zone
            name to the list of connections attached to it.
    """

    def __init__(self) -> None:
        """Initialize an empty Graph with no zones or connections."""
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.adjacency: dict[str, list[Connection]] = {}

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph.

        Args:
            zone (Zone): The zone to add to the graph.
        """
        self.zones[zone.name] = zone
        self.adjacency[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        """Add a connection between two zones to the graph.

        The connection is registered in the adjacency list of both
        zones it links, since connections are bidirectional.

        Args:
            connection (Connection): The connection to add to the
                graph.
        """
        self.connections.append(connection)
        self.adjacency[connection.zone1].append(connection)
        self.adjacency[connection.zone2].append(connection)

    def neighbors(self, zone_name: str) -> list[Connection]:
        """Return all connections attached to a given zone.

        Args:
            zone_name (str): Name of the zone whose connections
                should be retrieved.

        Returns:
            list[Connection]: The list of connections attached to the
            given zone, or an empty list if the zone is unknown.
        """
        return self.adjacency.get(zone_name, [])

    def get_connection(self, zone1: str, zone2: str) -> Connection | None:
        """Find the connection linking two given zones, if any.

        Args:
            zone1 (str): Name of the first zone.
            zone2 (str): Name of the second zone.

        Returns:
            Connection | None: The connection linking `zone1` and
            `zone2`, or None if no such connection exists.
        """
        for connection in self.adjacency.get(zone1, []):
            if connection.find_other_end(zone1) == zone2:
                return connection
        return None
