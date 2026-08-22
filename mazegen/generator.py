"""Randomized maze generation via DFS backtracking.

Carves maze walls in place on a Maze instance using an iterative
depth-first-search backtracker. Supports both perfect mazes (single
path, no loops) and non-perfect, Pac-Man-style boards (looped, with
open corners and centre) while respecting the "42" pattern and the
no-large-open-area constraint.
"""

from .maze import Maze
from .directions import DIRECTIONS
import random
import time
import os


class MazeGenerator:
    """Generates a maze's wall layout using a randomized DFS backtracker.

    Carves passages into a Maze object either as a perfect maze
    (single unique path, no loops) or, if not perfect, converts it
    afterwards into a Pac-Man-style board with loops and open corners.
    """
    def __init__(self, maze: Maze, perfect: bool = True) -> None:
        """Initialize the generator for a given maze.

        Args:
            maze: The Maze instance whose walls will be carved.
            perfect: If True, generate a perfect maze (no loops).
                If False, generate a maze and then loosen it into a
                Pac-Man-style board with multiple routes.
        """
        self.maze_object = maze
        self.stack: list[tuple[int, int]] = []
        self.visited = set(maze._42)
        self.perfect = perfect

    def independent_path(self) -> int:
        """Compute the maze's cyclomatic number (number of independent loops).

        Returns:
            The number of independent cycles in the maze graph,
            computed as edges - vertices + connected_components.
        """
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
        """Check whether opening a wall would create an oversized open area.

        Args:
            r: Row index of the cell being evaluated.
            c: Column index of the cell being evaluated.
            direction: Direction of the wall to test opening, or None
                to test the cell's current open state directly.

        Returns:
            True if opening this wall would create a corridor wider
            than the allowed 2-cell maximum, False otherwise.
        """
        maze = self.maze_object

        if r == 0 and maze.height > 2:
            if direction is None:
                return False
            dr = int(DIRECTIONS[direction]["dr"])
            dc = int(DIRECTIONS[direction]["dc"])
            opp = str(DIRECTIONS[direction]["opposite"])
            maze.maze[r][c][direction] = False
            maze.maze[r + dr][c + dc][opp] = False
            result = any(
                self.large_open_region(r + 1, c - 1 + i, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            maze.maze[r + dr][c + dc][opp] = True
            return result

        if r == maze.height - 1 and maze.height > 2:
            if direction is None:
                return False
            dr = int(DIRECTIONS[direction]["dr"])
            dc = int(DIRECTIONS[direction]["dc"])
            opp = str(DIRECTIONS[direction]["opposite"])
            maze.maze[r][c][direction] = False
            maze.maze[r + dr][c + dc][opp] = False
            result = any(
                self.large_open_region(r - 1, c - 1 + i, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            maze.maze[r + dr][c + dc][opp] = True
            return result

        if c == 0 and maze.width > 2:
            if direction is None:
                return False
            dr = int(DIRECTIONS[direction]["dr"])
            dc = int(DIRECTIONS[direction]["dc"])
            opp = str(DIRECTIONS[direction]["opposite"])
            maze.maze[r][c][direction] = False
            maze.maze[r + dr][c + dc][opp] = False
            result = any(
                self.large_open_region(r - 1 + i, c + 1, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            maze.maze[r + dr][c + dc][opp] = True
            return result

        if c == maze.width - 1 and maze.width > 2:
            if direction is None:
                return False
            dr = int(DIRECTIONS[direction]["dr"])
            dc = int(DIRECTIONS[direction]["dc"])
            opp = str(DIRECTIONS[direction]["opposite"])
            maze.maze[r][c][direction] = False
            maze.maze[r + dr][c + dc][opp] = False
            result = any(
                self.large_open_region(r - 1 + i, c - 1, None)
                for i in range(3)
            )
            maze.maze[r][c][direction] = True
            maze.maze[r + dr][c + dc][opp] = True
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
        if direction is not None:
            dr = int(DIRECTIONS[direction]["dr"])
            dc = int(DIRECTIONS[direction]["dc"])
            opp = str(DIRECTIONS[direction]["opposite"])
            maze.maze[r][c][direction] = False
            maze.maze[r + dr][c + dc][opp] = False
            is_center_open = maze.cell_to_int(r, c) == 0
            result = (
                is_center_open
                and not any(left[d] for d in "NES")
                and not any(bottom_left[d] for d in "NE")
                and not any(bottom[d] for d in "WNE")
                and not any(bottom_right[d] for d in "WN")
                and not any(right[d] for d in "SWN")
                and not any(top_right[d] for d in "SW")
                and not any(top[d] for d in "ESW")
                and not any(top_left[d] for d in "ES"))
            maze.maze[r][c][direction] = True
            maze.maze[r + dr][c + dc][opp] = True

        else:
            is_center_open = maze.cell_to_int(r, c) == 0
            result = (
                is_center_open
                and not any(left[d] for d in "NES")
                and not any(bottom_left[d] for d in "NE")
                and not any(bottom[d] for d in "WNE")
                and not any(bottom_right[d] for d in "WN")
                and not any(right[d] for d in "SWN")
                and not any(top_right[d] for d in "SW")
                and not any(top[d] for d in "ESW")
                and not any(top_left[d] for d in "ES"))

        return result

    def valid_wall_removal(self, r: int, c: int, direction: str) -> bool:
        """Check whether a wall can be safely removed.

        Args:
            r: Row index of the cell.
            c: Column index of the cell.
            direction: Direction of the wall to remove.

        Returns:
            True if removing this wall stays in bounds, doesn't touch
            the "42" pattern, and doesn't create an oversized open
            region; False otherwise.
        """
        maze = self.maze_object
        if (
            not 0 <= r + int(DIRECTIONS[direction]["dr"]) < maze.height
            or not 0 <= c + int(DIRECTIONS[direction]["dc"]) < maze.width
        ):
            return False
        if not maze.maze[r][c][direction]:
            return False
        if ((r, c) in maze._42 or
            (r + int(DIRECTIONS[direction]["dr"]),
                c + int(DIRECTIONS[direction]["dc"])) in maze._42):
            return False
        if self.large_open_region(r, c, direction):
            return False
        if self.large_open_region(
                r + int(DIRECTIONS[direction]["dr"]),
                c + int(DIRECTIONS[direction]["dc"]),
                str(DIRECTIONS[direction]["opposite"])):
            return False

        return True

    def make_imperfect(
        self, R: int = 0, G: int = 150, B: int = 225,
        delay: float = 0.01, display_generation: bool = False
    ) -> None:
        """Convert a perfect maze into a Pac-Man-style playable board.

        Removes walls at dead ends and, if needed, additional walls
        to guarantee at least two independent routes (loops) while
        opening the four corners and the centre cell.

        Args:
            R: Red component of the wall colour, used only for
                optional live-rendering during the process.
            G: Green component of the wall colour.
            B: Blue component of the wall colour.
            delay: Seconds to wait between rendered animation frames.
            display_generation: If True, print each intermediate step
                to the terminal.
        """
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
        """Carve the maze's walls in place using randomized DFS backtracking.

        Starts from maze.start and performs an iterative depth-first
        search, removing walls between the current cell and a
        randomly chosen unvisited neighbour, backtracking when no
        unvisited neighbours remain. If self.perfect is False,
        make_imperfect is called afterwards to add loops.

        Args:
            R: Red component of the wall colour, used only when
                display_generation is True.
            G: Green component of the wall colour, used only when
                display_generation is True.
            B: Blue component of the wall colour, used only when
                display_generation is True.
            delay: Seconds to pause between animation frames when
                display_generation is True.
            display_generation: If True, print each intermediate step
                to the terminal as an animation.
        """
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
