"""mazegen — a reusable maze generation, solving, and rendering package.

Exposes the core building blocks needed to generate mazes (perfect or
Pac-Man-style looped boards), solve them with breadth-first search,
render them to the terminal, and load generation parameters from a
configuration file.

Classes:
    Maze: Represents the grid, walls, and metadata of a maze.
    MazeGenerator: Carves maze walls using randomized DFS backtracking.
    MazeSolver: Finds the shortest path via breadth-first search.
    Config: Loads and validates settings from a configuration file.

Constants:
    DIRECTIONS: Mapping of cardinal directions to movement deltas,
        opposite direction, and wall-encoding bit position.
"""


from .maze import Maze
from .generator import MazeGenerator
from .solver import MazeSolver
from .config import Config
from .directions import DIRECTIONS

__all__ = ["Maze", "MazeGenerator", "MazeSolver", "Config", "DIRECTIONS"]
