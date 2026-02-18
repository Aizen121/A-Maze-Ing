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
        return self.grid[x][y]

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

    def print_grid(self):
        """"""
        for row in self.grid:
            for cell in row:
                if (cell.x, cell.y) in self.pattern_cells:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
