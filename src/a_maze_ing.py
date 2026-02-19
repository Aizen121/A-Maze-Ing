import sys
from mazegen.maze_parser import MazeParser
from mazegen.generator import MazeGenerator
from mazegen.backtracking import backtracking
from mazegen.bfs import bfs


def main() -> None:
    if not len(sys.argv) == 2:
        print("Error: No arguments provided.\nUsage: python3 a-maze-ing "
              "<config.txt>")
        sys.exit(1)
    config = MazeParser.parser(sys.argv[1])
    maze = MazeGenerator(config)
    backtracking(maze)
    solver = bfs(maze)
    print(f"Shortest path: {solver.get_path_string()}")
    maze.print_grid(path=solver.path)


if __name__ == "__main__":
    main()
