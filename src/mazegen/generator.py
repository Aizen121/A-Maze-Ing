import random
from dataclasses import dataclass
from .maze_parser import MazeParser


class MazeGenerator:
    """exportable module to mazegenerator package"""
    Directions: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    Opposite: dict[str, str] = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    Digit_4: list[tuple[int, int]] = [
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
    ]

    Digit_2: list[tuple[int, int]] = [
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4),
    ]
    Pattern_width: int = 7
    Pattern_height: int = 5
    Min_width: int = 9
    Min_height: int = 7

    @dataclass
    class Cell:
        x: int
        y: int
        north: bool = True
        east: bool = True
        south: bool = True
        west: bool = True
        visited: bool = False

    def __init__(self, parameters: MazeParser) -> None:
        """"""
        self.width: int = parameters.width
        self.height: int = parameters.height
        self.entry: tuple[int, int] = parameters.entry
        self.exit_pos: tuple[int, int] = parameters.exit
        self.perfect: bool = parameters.perfect
        self.pattern_cells: set[tuple[int, int]] = set()

        if parameters.seed is not None:
            self.seed: int = parameters.seed
        else:
            self.seed = random.randint(0, 2**32 - 1)
            print(f"Using generated seed: {self.seed}")

        self.grid: list[list] = [
            [self.Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]
        self._place_pattern_42()
        random.seed(self.seed)

    def get_cell(self, x: int, y: int) -> object:
        return self.grid[y][x]

    def _place_pattern_42(self) -> None:
        if (self.width < self.Pattern_width
                or self.height < self.Pattern_height):
            print("Warning: maze too small for 42 pattern")
            return

        offset_x: int = (self.width - self.Min_width) // 2
        offset_y: int = (self.height - self.Min_height) // 2
        for px, py in self.Digit_4:
            self.pattern_cells.add((offset_x + px, offset_y + py))
        for px, py in self.Digit_2:
            self.pattern_cells.add((offset_x + 4 + px, offset_y + py))

        if self.entry in self.pattern_cells:
            print("Warning: entry overlaps 42 pattern, skipping pattern")
            self.pattern_cells.clear()
            return
        if self.exit_pos in self.pattern_cells:
            print("Warning: exit overlaps 42 pattern, skipping pattern")
            self.pattern_cells.clear()
            return
        for px, py, in self.pattern_cells:
            self.grid[py][px].visited = True

    def remove_wall(self, cell_a, cell_b) -> None:
        dx: int = cell_b.x - cell_a.x
        dy: int = cell_b.y - cell_a.y

        if dx == 1 and dy == 0:
            cell_a.east = False
            cell_b.west = False
        elif dx == -1 and dy == 0:
            cell_a.west = False
            cell_b.east = False
        elif dx == 0 and dy == 1:
            cell_a.south = False
            cell_b.north = False
        elif dx == 0 and dy == -1:
            cell_a.north = False
            cell_b.south = False

    def print_grid(self) -> None:
        for y in range(self.height):
            top: str = ""
            mid: str = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                top += "+" + ("---" if cell.north else "   ")
                mid += ("|" if cell.west else " ")
                if (x, y) == self.entry:
                    mid += " E "
                elif (x, y) == self.exit_pos:
                    mid += " X "
                elif (cell.x, cell.y) in self.pattern_cells:
                    mid += " # "
                else:
                    mid += "   "
            top += "+"
            mid += "|" if self.grid[y][self.width - 1].east else " "
            print(top)
            print(mid)
        bottom: str = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            bottom += "+" + ("---" if cell.south else "   ")
        bottom += "+"
        print(bottom)
