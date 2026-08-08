import sys
from src.parser import Parser, ParserError
from src.pathfinder import Pathfinder
from src.visualizer import Visualizer

class SimulationError(Exception):
    pass


def main() -> None:
    if len(sys.argv) != 2:
        print("Please use: 'make run FILE=<path_to_file>'")
        sys.exit(1)
    parser = Parser(sys.argv[1])
    try:
        parser.parse_file()
    except ParserError as e:
        print(e)
        sys.exit(1)
    pathfinder = Pathfinder(parser.graph)
    assert parser.start_hub_name is not None
    assert parser.end_hub_name is not None
    zone_load: dict[str, int] = {}
    link_load: dict[int, int] = {}
    paths = []
    try:
        for _ in range(parser.nb_drones):
            _, predecessors = pathfinder.dijkstra_capacity_aware(
                parser.start_hub_name, zone_load, link_load
            )
            path = pathfinder.reconstruct_path(
                predecessors, parser.start_hub_name, parser.end_hub_name
            )
            if path is None:
                raise SimulationError(
                    f"No path found from '{parser.start_hub_name}' "
                    f"to '{parser.end_hub_name}'"
                )
            paths.append(path)
            for i in range(len(path) - 1):
                zone_load[path[i + 1]] = zone_load.get(path[i + 1], 0) + 1
                connection = parser.graph.get_connection(path[i], path[i + 1])
                if connection is not None:
                    link_load[id(connection)] = link_load.get(id(connection), 0) + 1
    except SimulationError as e:
        print(e)
        sys.exit(1)
    visualizer = Visualizer(
        parser.graph, parser.start_hub_name,
        parser.end_hub_name, parser.nb_drones, paths
    )
    visualizer.run()


if __name__ == "__main__":
    main()
