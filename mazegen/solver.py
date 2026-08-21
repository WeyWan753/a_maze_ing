from .maze import Maze
from .directions import DIRECTIONS


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
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
