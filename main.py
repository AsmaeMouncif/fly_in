import sys
from src.parser import Parser, ParserError


def main():
    if len(sys.argv) != 2:
        print("Please use: 'make run FILE=<path_to_file>'")
        sys.exit(1)
    parser = Parser(sys.argv[1])
    try:
        parser.parse_file()
        for zone_name, conns in parser.graph.adjacency.items():
            neighbors = [c.find_other_end(zone_name) for c in conns]
            print(f"{zone_name} -> {neighbors}")
    except ParserError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
