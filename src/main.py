import sys
from parser import Parser


def main():
    if len(sys.argv) != 2:
        print("Please use: 'make run FILE=<path_to_file>'")
        sys.exit(1)

    parser = Parser(sys.argv[1])
    parser.parse_file()


if __name__ == "__main__":
    main()
