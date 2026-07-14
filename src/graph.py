class Graph:
    def __init__(self):
        self.zones = {}
        self.connections = []
        self.adjacency = {}

    def add_zone(self, zone):
        self.zones[zone.name] = zone
        self.adjacency[zone.name] = []

    def add_connection(self, connection):
        self.connections.append(connection)
        self.adjacency[connection.zone1].append(connection)
        self.adjacency[connection.zone2].append(connection)

    def neighbors(self, zone_name):
        return self.adjacency.get(zone_name, [])
