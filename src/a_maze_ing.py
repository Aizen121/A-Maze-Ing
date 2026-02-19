import sys
from mazegen.maze_parser import MazeParser
from mazegen.generator import MazeGenerator
from mazegen.backtracking import backtracking


def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing "
              "<config.txt>")
        sys.exit(1)
    config = MazeParser.parser(sys.argv[1])
    maze = MazeGenerator(config)
    backtracking(maze)
    maze.print_grid()


if __name__ == "__main__":
    main()
