import sys
from src.parser import Parser, ParserError
from src.pathfinder import Pathfinder
from src.visualizer import Visualizer


def main():
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
    distances, predecessors = pathfinder.dijkstra(parser.start_hub_name)
    path = pathfinder.reconstruct_path(predecessors, parser.start_hub_name, parser.end_hub_name)
    visualizer = Visualizer(parser.graph, parser.start_hub_name, parser.end_hub_name, parser.nb_drones)
    visualizer.run()


if __name__ == "__main__":
    main()
