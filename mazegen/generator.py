from .maze import Maze
from .directions import DIRECTIONS
import random
import time
import os


class MazeGenerator:
    def __init__(self, maze: Maze, perfect: bool = True) -> None:
        self.maze_object = maze
        self.stack: list[tuple[int, int]] = []
        self.visited = set(maze._42)
        self.perfect = perfect

    def independent_path(self) -> int:
        maze = self.maze_object
        V = maze.height * maze.width - len(maze._42)
        E = sum(
            1 if not maze.maze[r][c][d] else 0
            for r in range(maze.height)
            for c in range(maze.width)
            for d in "NESW")//2
        C = 1
        L = E - V + C
        return L

    def large_open_region(self, r: int, c: int, direction: str | None) -> bool:
        maze = self.maze_object

        if r == 0 and maze.height > 2:
            if direction is None:
                return False
            maze.maze[r][c][direction] = False
            result = any(
                self.large_open_region(r + 1, c - 1 + i, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            return result

        if r == maze.height - 1 and maze.height > 2:
            if direction is None:
                return False
            maze.maze[r][c][direction] = False
            result = any(
                self.large_open_region(r - 1, c - 1 + i, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            return result

        if c == 0 and maze.width > 2:
            if direction is None:
                return False
            maze.maze[r][c][direction] = False
            result = any(
                self.large_open_region(r - 1 + i, c + 1, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            return result

        if c == maze.width - 1 and maze.width > 2:
            if direction is None:
                return False
            maze.maze[r][c][direction] = False
            result = any(
                self.large_open_region(r - 1 + i, c - 1, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            return result

        if not (0 < c < maze.width - 1 and 0 < r < maze.height - 1):
            return False
        left = maze.maze[r][c - 1]
        bottom_left = maze.maze[r + 1][c - 1]
        bottom = maze.maze[r + 1][c]
        bottom_right = maze.maze[r + 1][c + 1]
        right = maze.maze[r][c + 1]
        top_right = maze.maze[r - 1][c + 1]
        top = maze.maze[r - 1][c]
        top_left = maze.maze[r - 1][c - 1]
        if direction is None:
            is_center_open = maze.cell_to_int(r, c) == 0
        else:
            is_center_open = maze.cell_to_int(r, c) == (
                1 << int(DIRECTIONS[direction]["bit"])
            )
        return (
            is_center_open
            and not any(left[d] for d in "NES")
            and not any(bottom_left[d] for d in "NE")
            and not any(bottom[d] for d in "WNE")
            and not any(bottom_right[d] for d in "WN")
            and not any(right[d] for d in "SWN")
            and not any(top_right[d] for d in "SW")
            and not any(top[d] for d in "ESW")
            and not any(top_left[d] for d in "ES"))

    def valid_wall_removal(self, r: int, c: int, direction: str) -> bool:
        maze = self.maze_object
        if (
            not 0 <= r + int(DIRECTIONS[direction]["dr"]) < maze.height
            or not 0 <= c + int(DIRECTIONS[direction]["dc"]) < maze.width
        ):
            return False
        if not maze.maze[r][c][direction]:
            return False
        if self.large_open_region(r, c, direction):
            return False
        if self.large_open_region(
                r + int(DIRECTIONS[direction]["dr"]),
                c + int(DIRECTIONS[direction]["dc"]),
                str(DIRECTIONS[direction]["opposite"])):
            return False
        if ((r, c) in maze._42 or
            (r + int(DIRECTIONS[direction]["dr"]),
                c + int(DIRECTIONS[direction]["dc"])) in maze._42):
            return False
        return True

    def make_imperfect(
        self, R: int = 0, G: int = 150, B: int = 225,
        delay: float = 0.01, display_generation: bool = False
    ) -> None:
        maze = self.maze_object

        def is_dead_end(r: int, c: int) -> bool:
            cell = maze.cell_to_int(r, c)
            return (cell != (1 << 4) - 1 and
                    ((cell | cell + 1) == (1 << 4) - 1))

        dead_ends = [
            (r, c) for r in range(maze.height)
            for c in range(maze.width)
            if is_dead_end(r, c)]
        dead_ends = [
                (0, 0), (0, maze.width - 1),
                (maze.height - 1, 0),
                (maze.height - 1, maze.width - 1),
                (maze.height//2, maze.width//2)
        ] + dead_ends
        i = 0
        while i < len(dead_ends):
            if display_generation:
                frame = maze.render_maze([], R, G, B)
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(delay)
            r, c = dead_ends[i]
            if not is_dead_end(r, c):
                i += 1
                continue
            neighbour_dirs = []
            for direction in DIRECTIONS:
                if self.valid_wall_removal(r, c, direction):
                    neighbour_dirs.append(direction)

            if neighbour_dirs:
                neighbour_dir = random.choice(neighbour_dirs)
                opposite = str(DIRECTIONS[neighbour_dir]["opposite"])
                maze.maze[r][c][neighbour_dir] = False
                maze.maze[
                        r + int(DIRECTIONS[neighbour_dir]["dr"])
                ][
                        c + int(DIRECTIONS[neighbour_dir]["dc"])
                ][
                        opposite
                ] = False
            i += 1
        L = self.independent_path()
        for (r, c) in (
                (row, col) for row in range(maze.height)
                for col in range(maze.width)):
            if display_generation:
                frame = maze.render_maze([], R, G, B)
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(delay)
            if L >= 2:
                break
            neighbour_dirs = []
            for direction in DIRECTIONS:
                if self.valid_wall_removal(r, c, direction):
                    neighbour_dirs.append(direction)

            if neighbour_dirs:
                neighbour_dir = random.choice(neighbour_dirs)
                opposite = str(DIRECTIONS[neighbour_dir]["opposite"])
                maze.maze[r][c][neighbour_dir] = False
                maze.maze[
                        r + int(DIRECTIONS[neighbour_dir]["dr"])
                ][
                        c + int(DIRECTIONS[neighbour_dir]["dc"])
                ][
                        opposite
                ] = False
                L = self.independent_path()

    def generate_maze(
        self, R: int = 0, G: int = 150, B: int = 225,
        delay: float = 0.1, display_generation: bool = False
    ) -> None:
        maze = self.maze_object
        start = maze.start
        self.stack.append(start)
        self.visited.add(start)
        while self.stack:
            if display_generation:
                frame = maze.render_maze(self.stack, R, G, B)
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(delay)
            r, c = self.stack[-1]
            neighbour = []
            for direction in DIRECTIONS:
                if (
                    0 <= r + int(DIRECTIONS[direction]["dr"]) < maze.height
                    and 0 <= c + int(DIRECTIONS[direction]["dc"]) < maze.width
                    and
                    (
                        r + int(DIRECTIONS[direction]["dr"]),
                        c + int(DIRECTIONS[direction]["dc"])
                    )
                    not in self.visited
                ):
                    neighbour.append(
                            ((r + int(DIRECTIONS[direction]["dr"]),
                              c + int(DIRECTIONS[direction]["dc"])), direction)
                    )

            if neighbour:
                next_point, neighbour_dir = random.choice(neighbour)
                self.stack.append(next_point)
                self.visited.add(next_point)
                opposite = str(DIRECTIONS[neighbour_dir]["opposite"])
                maze.maze[r][c][neighbour_dir] = False
                maze.maze[
                    r + int(DIRECTIONS[neighbour_dir]["dr"])
                ][
                    c + int(DIRECTIONS[neighbour_dir]["dc"])
                ][
                    opposite
                ] = False
            else:
                self.stack.pop(-1)

        if not self.perfect:
            self.make_imperfect(R, G, B, delay, display_generation)
