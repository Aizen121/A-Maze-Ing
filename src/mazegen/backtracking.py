from .generator import MazeGenerator
import random


class backtracking:
    def __init__(self, maze: MazeGenerator):
        self.maze: MazeGenerator = maze
        self._generate()

    def _get_unvisited_neighbors(self, cell: object) -> list:
        neighbors: list = []
        for dx, dy in self.maze.Directions.values():
            nx: int = cell.x + dx
            ny: int = cell.y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                neighbor = self.maze.grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        return neighbors

    def _generate(self) -> None:
        start_x, start_y = self.maze.entry
        start_cell = self.maze.get_cell(start_x, start_y)
        start_cell.visited = True

        stack: list = [start_cell]

        while stack:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(current)
            if neighbors:
                chosen = random.choice(neighbors)
                self.maze.remove_wall(current, chosen)
                chosen.visited = True
                stack.append(chosen)
            else:
                stack.pop()
