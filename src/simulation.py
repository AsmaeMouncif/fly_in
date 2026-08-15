class SimulationDeadlockError(Exception):
    pass


class Simulation:
    def __init__(self, graph, start_hub_name,
                 end_hub_name, drones, pathfinder):
        self.graph = graph
        self.start_hub_name = start_hub_name
        self.end_hub_name = end_hub_name
        self.drones = drones
        self.pathfinder = pathfinder
        self.zone_occupancy = {}
        for name in self.graph.zones:
            self.zone_occupancy[name] = 0
        self.zone_occupancy[start_hub_name] = len(drones)
        self.turn_count = 0
        self.transit_connections = {}
        self.stagnant_turns = 0
        self.max_stagnant_turns = len(self.graph.zones) + 1

    def can_enter_zone(self, zone_name):
        zone = self.graph.zones[zone_name]
        return self.zone_occupancy[zone_name] < zone.max_drones

    def can_use_link(self, connection, link_usage):
        if connection is None:
            return True
        key = id(connection)
        current_usage = link_usage.get(key, 0) + self.transit_connections.get(key, 0)
        return current_usage < connection.max_link_capacity

    def try_move_drone(self, drone, link_usage):
        if drone.in_transit:
            drone.transit_turns_left -= 1
            if drone.transit_turns_left <= 0:
                drone.in_transit = False
                drone.path_index += 1
                connection = self.graph.get_connection(
                    drone.path[drone.path_index - 1], drone.current_zone
                )
                if connection is not None:
                    key = id(connection)
                    self.transit_connections[key] = (
                        self.transit_connections.get(key, 0) - 1
                    )
            return True
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
        next_zone_obj = self.graph.zones[next_zone]
        if next_zone_obj.zone_type == "restricted":
            drone.in_transit = True
            drone.transit_turns_left = 1
            if connection is not None:
                key = id(connection)
                self.transit_connections[key] = (
                    self.transit_connections.get(key, 0) + 1
                )
        else:
            drone.path_index += 1
        return True

    def replan_drone(self, drone, link_usage):
        full_zones = set()
        for zone_name in self.graph.zones:
            if self.can_enter_zone(zone_name) is False:
                full_zones.add(zone_name)
        full_connections = set()
        for connection in self.graph.connections:
            if self.can_use_link(connection, link_usage) is False:
                full_connections.add(id(connection))
        _, predecessors = self.pathfinder.dijkstra(
            drone.current_zone, blocked_zones=full_zones,
            blocked_connections=full_connections
        )
        new_path = self.pathfinder.reconstruct_path(
            predecessors, drone.current_zone, self.end_hub_name
        )
        if new_path is not None:
            drone.assign_new_path(new_path)

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
                self.replan_drone(drone, link_usage)
                destination = drone.next_zone
                if destination is None:
                    continue
            was_in_transit_before = drone.in_transit
            moved = self.try_move_drone(drone, link_usage)
            if moved:
                if drone.in_transit:
                    connection = self.graph.get_connection(
                        drone.current_zone, drone.next_zone
                    )
                    label = f"{connection.zone1}-{connection.zone2}"
                    moved_this_turn.append(f"D{drone.drone_id + 1}-{label}")
                elif was_in_transit_before:
                    moved_this_turn.append(
                        f"D{drone.drone_id + 1}-{drone.current_zone}"
                    )
                else:
                    moved_this_turn.append(
                        f"D{drone.drone_id + 1}-{destination}"
                    )
            else:
                self.replan_drone(drone, link_usage)
        self.turn_count += 1
        if moved_this_turn:
            print(" ".join(moved_this_turn))
            self.stagnant_turns = 0
        else:
            self.stagnant_turns += 1
            if self.stagnant_turns >= self.max_stagnant_turns:
                raise SimulationDeadlockError("Drones are stuck and cannot move forward")
        if self.all_delivered():
            print(f"All drones delivered in {self.turn_count} turns.")
