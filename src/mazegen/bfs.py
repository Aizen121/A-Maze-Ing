from .generator import MazeGenerator
from collections import deque


class bfs:
    def __init__(self, maze: MazeGenerator):
        self.maze: MazeGenerator = maze
        self.path: list = []
        self._find_path(maze)

    def _get_accessible_neighbors(self, cell: object) -> list:
        neighbors: list = []
        if not cell.north and cell.y > 0:
            neighbor = self.maze.grid[cell.y - 1][cell.x]
            neighbors.append((neighbor, "N"))
        if not cell.east and cell.x < self.maze.width - 1:
            neighbor = self.maze.grid[cell.y][cell.x + 1]
            neighbors.append((neighbor, "E"))
        if not cell.south and cell.y < self.maze.height - 1:
            neighbor = self.maze.grid[cell.y + 1][cell.x]
            neighbors.append((neighbor, "S"))
        if not cell.west and cell.x > 0:
            neighbor = self.maze.grid[cell.y][cell.x - 1]
            neighbors.append((neighbor, "W"))
        return neighbors

    def _find_path(self, maze):
        start_x, start_y = self.maze.entry
        start = self.maze.get_cell(start_x, start_y)
        end_x, end_y = self.maze.exit_pos
        end = self.maze.get_cell(end_x, end_y)

        visited: set = set()
        visited.add((start.x, start.y))

        queue: deque = deque()
        queue.append((start, []))
        while queue:
            current, path = queue.popleft()

            if current.x == end.x and current.y == end.y:
                self.path = path
                return
            for neighbor, direction in self._get_accessible_neighbors(current):
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    queue.append(
                        (neighbor, path + [direction])
                    )
        print("Error: no path found from entry to exit")

    def get_path_string(self) -> str:
        return "".join(self.path)
