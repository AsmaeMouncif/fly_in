def dijkstra(graph, start):
    pq = []
    distances = {}
    for zone in graph:
        distances[zone] = float("inf")
    distances[start] = 0
    pq.append((0, start))
    while pq:
        min_zone = pq[0]
        for zone in pq:
            if min_zone[0] > zone[0]:
                min_zone = zone
        current_distance = min_zone[0]
        current_zone = min_zone[1]
        pq.remove(min_zone)
        neighbors = graph[current_zone]
        for neighbor, distance in neighbors.items():
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                pq.append((new_distance, neighbor))
    return distances

graph = {
    "0": {"1": 4, "2": 8},
    "1": {"0": 4, "4": 6},
    "2": {"0": 8, "3": 2},
    "3": {"2": 2, "4": 10},
    "4": {"1": 6, "3": 10}
}

if __name__ == "__main__":
    result = dijkstra(graph, "0")
    print(result)
