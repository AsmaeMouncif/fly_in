from .zone import Zone
from .connection import Connection


class Graph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.adjacency: dict[str, list[Connection]] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
        self.adjacency[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        self.adjacency[connection.zone1].append(connection)
        self.adjacency[connection.zone2].append(connection)

    def neighbors(self, zone_name: str) -> list[Connection]:
        return self.adjacency.get(zone_name, [])

    def get_connection(self, zone1: str, zone2: str) -> Connection | None:
        for connection in self.adjacency.get(zone1, []):
            if connection.find_other_end(zone1) == zone2:
                return connection
        return None
