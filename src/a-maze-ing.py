import sys
import random
from dataclasses import dataclass
from typing import Optional
from maze_parser import MazeParser

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

@dataclass
class Cell:
    x: int
    y: int
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    visited: bool = False

Pattern_width: int = 9
Pattern_height: int = 7

class MazeGrid:
    def __init__(self, config: MazeParser) -> None:
        self.width: int = config.width
        self.height: int = config.height
        self.entry: tuple[int, int] = config.entry
        self.exit: tuple[int, int] = config.exit
        self.pattern_cells: set[tuple[int, int]] = set()

        self.grid: list[list[Cell]] = [
            [Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]
        self._place_pattern_42()
        if config.seed is not None:
            self.seed: int = config.seed
        else:
            self.seed = random.randint(0, 2**32 - 1)

        def get_cell(self, x: int, y: int) -> Cell:
            return self.grid[y][x]

        def _place_pattern_42(self, x: int, y: int) -> Cell:
            if self.width < Pattern_width or self.height < Pattern_height:
                print("Warning: maze too small for 42 pattern, skipping")
                return

            offset_x: int = (self.width - Pattern_width) // 2
            offset_y: int = (self.height - Pattern_height) // 2
            for px, py in Digit_4:
                self.pattern_cells.add((offset_x + px, offset_y + py))
            for px, py in Digit_2:
                self.pattern_cells.add((offset_x + 5 + px, offset_y + py))

            if self.entry in self.pattern_cells:
                print("Warning: entry overlaps 42 pattern, skipping pattern")
                self.pattern_cells.clear()
                return
            if self.exit in self.pattern_cells:
                print("Warning: exit overlaps 42 pattern, skipping pattern")
                self.pattern_cells.clear()
                return
            for px, py, in self.pattern_cells:
                self.grid[py][px].visited = True

        def remove_wall_between(self, cell_a: Cell, cell_b: Cell) -> None: