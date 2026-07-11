
class Pathfinder:
    def __init__(self, graph):
        self.graph = graph
    
    def shortest_path(self, start):
        pq = []
        distances = {}
        for zone in self.graph.zones:
            distances[zone] = float("inf")
        distances[start] = 0
        pq.append((0, start))
        while pq:
            min_zone = pq[0]
            for item in pq:
                if min_zone[0] > item[0]:
                    min_zone = item
            current_distance = min_zone[0]
            current_zone = min_zone[1]
            pq.remove(min_zone)
            neighbors = self.graph.neighbors(current_zone)
            for connection in neighbors:
                neighbor = connection.find_other_end(current_zone)
                distance = 1
                new_distance = current_distance + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    pq.append((new_distance, neighbor))
        return distances
