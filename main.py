import sys
from src.parser import Parser, ParserError
from src.pathfinder import Pathfinder
from src.visualizer import Visualizer
from src.simulation import Simulation
from src.drone import Drone


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
    try:
        _, predecessors = pathfinder.dijkstra(parser.start_hub_name)
        path = pathfinder.reconstruct_path(
            predecessors, parser.start_hub_name, parser.end_hub_name
        )
        if path is None:
            raise SimulationError(
                f"No path found from '{parser.start_hub_name}' "
                f"to '{parser.end_hub_name}'"
            )
    except SimulationError as e:
        print(e)
        sys.exit(1)
    drones: list[Drone] = []
    for i in range(parser.nb_drones):
        drone = Drone(path, drone_id=i)
        drones.append(drone)
    simulation = Simulation(
        parser.graph, parser.start_hub_name,
        parser.end_hub_name, drones, pathfinder
    )
    visualizer = Visualizer(
        parser.graph, simulation, parser.start_hub_name,
        parser.end_hub_name, parser.nb_drones, path
    )
    visualizer.run()


if __name__ == "__main__":
    main()
