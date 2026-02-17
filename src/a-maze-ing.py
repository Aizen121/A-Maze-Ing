import sys
from typing import Optional
from maze_parser import MazeParser
from maze_grid import MazeGrid


@dataclass
class Cell:
    x: int
    y: int
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    visited: bool = False


class MazeGrid:
    def __init__(self, config: MazeParser) -> None:
        self.width: int = config.width
        self.height: int = config.height
        self.entry: tuple[int, int] = config.entry
        self.exit: tuple[int, int] = config.exit
        self.seed: Optional[int] = config.seed

        self.grid: list[list[Cell]] = [
            [Cell(x=x, y=y) for x in range(self.width)]
             for y in range(self.height)]
        ]
