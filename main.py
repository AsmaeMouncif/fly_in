import sys
from src.parser import Parser, ParserError
# from src.dijkstra import Dijkstra


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
    # graph = parser.graph
    # dijkstra = Dijkstra(graph)
    # distances = dijkstra.shortest_path(
    #     parser.start_hub_name
    # )
    # print(distances)


if __name__ == "__main__":
    main()
