"""Breadth-first shortest-path solver for a Maze.

Defines the MazeSolver class, which explores a Maze's open walls from
its entry point using breadth-first search and reconstructs the
shortest path to the exit, expressed as an ordered sequence of
cardinal-direction moves.
"""

from .maze import Maze
from .directions import DIRECTIONS


class MazeSolver:
    """Finds the shortest path between a maze's entry and exit.

    Performs a breadth-first search over the maze's open walls,
    reconstructing the path once the exit cell is reached.

    Attributes:
        maze_object (Maze): The Maze instance to solve.
        queue (list[tuple[int, int]]): BFS frontier of cell
            coordinates.
        visited (set[tuple[int, int]]): Cells already enqueued/visited.
        parent (dict[tuple[int, int], tuple[tuple[int, int], str] | None]):
            Maps each visited cell to the (previous cell, direction
            moved) pair used to reach it, or None for the start cell.
        queue_index (int): Current read position in the BFS queue.
        found_solution (bool): Whether a path from start to end was found.
        solution_path (list[tuple[tuple[int, int], str | None]]):
            Ordered list of (coordinates, direction taken to reach
            them) from start to end, populated after solver() runs.
    """
    def __init__(self, maze: Maze) -> None:
        """Initialize the solver for a given maze.

        Args:
            maze: The Maze instance to solve. Its start and end
                attributes define the search endpoints.
        """
        self.maze_object = maze
        self.queue: list[tuple[int, int]] = []
        self.visited: set[tuple[int, int]] = set()
        self.parent: dict[
            tuple[int, int],
            tuple[tuple[int, int], str] | None
        ] = {}
        self.queue_index = 0
        self.found_solution = False
        self.solution_path: list[tuple[tuple[int, int], str | None]] = []

    def solver(self) -> None:
        """Run breadth-first search and populate the solution path.

        Explores the maze from maze_object.start until
        maze_object.end is reached or the search space is exhausted.
        On success, found_solution is set to True and solution_path
        is filled with the ordered (cell, direction) pairs from start
        to end.
        """
        self.queue.append(self.maze_object.start)
        self.visited.add(self.maze_object.start)
        self.parent[self.maze_object.start] = None
        while self.queue_index < len(self.queue):
            r, c = self.queue[self.queue_index]
            if (r, c) == self.maze_object.end:
                self.found_solution = True
                break
            for direction in DIRECTIONS:
                if (
                    not self.maze_object.maze[r][c][direction] and
                    (r + int(DIRECTIONS[direction]["dr"]),
                     c + int(DIRECTIONS[direction]["dc"]))
                    not in self.visited
                ):
                    self.queue.append(
                        (r + int(DIRECTIONS[direction]["dr"]),
                         c + int(DIRECTIONS[direction]["dc"])))
                    self.parent[
                        (r + int(DIRECTIONS[direction]["dr"]),
                         c + int(DIRECTIONS[direction]["dc"]))
                    ] = ((r, c), direction)
                    self.visited.add(
                        (r + int(DIRECTIONS[direction]["dr"]),
                         c + int(DIRECTIONS[direction]["dc"])))
            self.queue_index += 1
        if self.found_solution:
            curr: tuple[
                tuple[int, int], str | None
            ] | None = (self.maze_object.end, None)
            while curr is not None:
                self.solution_path.append(curr)
                curr = self.parent[curr[0]]
            self.solution_path.reverse()
