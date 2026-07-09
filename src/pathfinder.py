
class Pathfinder:
    def __init__(self, graph):
        self.graph = graph
    
    def shortest_path(self, start):
        distances = {}

        for zone in self.graph:
            distances[zone] = float("inf")
        distances[start] = 0
        return distances

graph = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4},
    "C": {"A": 2}
}

p = Pathfinder(graph)
print(p.shortest_path("A"))

