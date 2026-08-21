"""Core maze data structure: grid, walls, encoding, and rendering.

Defines the Maze class, which stores the wall state of every cell in
a grid as well as entry/exit coordinates and the mandatory "42"
pattern. Provides methods to encode the maze as hexadecimal (for the
output file format) and to render it as an ANSI-coloured ASCII string
for terminal display.
"""


class Maze:

    """Represents a grid-based maze and its wall state.

    Stores the maze dimensions, entry/exit points, the "42" pattern
    cells, and a per-cell dictionary of wall states (True = closed,
    False = open) for each cardinal direction.
    """

    def __init__(
            self, height: int, width: int, start: tuple[int, int],
            end: tuple[int, int]
            ) -> None:
        """Initialize an empty maze grid with all walls closed.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            start: (row, col) coordinates of the entry cell.
            end: (row, col) coordinates of the exit cell.
        """
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self._42 = set()
        if self.height >= 6 and self.width >= 9:
            (r, c) = (self.height//2, self.width//2)
            self._42 = {(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2),
                        (r + 2, c + 3)}
        self.maze = [
            [
                {"N": True, "E": True, "S": True, "W": True}
                for col in range(width)
            ]
            for row in range(height)
        ]

    def cell_to_int(self, r: int, c: int) -> int:
        """Encode a cell's wall configuration as an integer (0-15).

        Args:
            r: Row index of the cell.
            c: Column index of the cell.

        Returns:
            Integer where each bit represents a closed wall
            (N=1, E=2, S=4, W=8), following the direction bit mapping.
        """
        return (
            self.maze[r][c]["N"] * 1
            + self.maze[r][c]["E"] * 2
            + self.maze[r][c]["S"] * 4
            + self.maze[r][c]["W"] * 8
        )

    def maze_to_hex(self) -> str:
        """Encode the entire maze as a hexadecimal grid string.

        Returns:
            A string with one row per line, each cell represented by
            a single hexadecimal digit (0-f) describing its walls.
        """
        return (
            "\n".join(
                [
                    "".join(
                        [
                            "0123456789abcdef"[self.cell_to_int(r, c)]
                            for c in range(self.width)
                        ]
                    )
                    for r in range(self.height)
                ]
            )
        )

    def render_maze(
        self, stack: list[tuple[int, int]], R: int = 0, G: int = 150,
        B: int = 225
    ) -> str:
        """Render an ASCII/ANSI-coloured text representation of the maze.

        Args:
            stack: Ordered list of cells to highlight as a path
                (e.g. the solution path or the generation stack).
                Pass an empty list to render with no path highlighted.
            R: Red component of the wall colour (0-255).
            G: Green component of the wall colour (0-255).
            B: Blue component of the wall colour (0-255).

        Returns:
            A multi-line string containing the ANSI-coloured maze,
            including the start, end, walls, the "42" pattern, and
            the highlighted path if provided.
        """

        WALL = f"\033[38;2;{R};{G};{B}m"
        GREEN = "\033[38;2;0;255;0m"
        YELLOW = "\033[38;2;255;255;0m"
        RESET = "\033[0m"

        stack_index = {cell: i for i, cell in enumerate(stack)}

        print(WALL, end="")
        whole_maze = "+" + "---+" * self.width + "\n"
        for r in range(self.height):
            row_str = "|"
            for c in range(self.width):
                if (r, c) in self._42:
                    row_str += f"{GREEN}███{WALL}|"
                elif (r, c) in stack_index:
                    index = stack_index[(r, c)]
                    if (r, c) == self.start:
                        if self.maze[r][c]["E"]:
                            row_str += f"{GREEN} S {WALL}|"
                        elif (index + 1 < len(stack) and
                              stack[index + 1] == (r, c + 1)):
                            row_str += f"{GREEN} S {YELLOW}."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"{GREEN} S {YELLOW}."
                        else:
                            row_str += f"{GREEN} S  "
                    elif (r, c) == self.end:
                        if self.maze[r][c]["E"]:
                            row_str += f"{GREEN} E {WALL}|"
                        elif (index + 1 < len(stack) and
                              stack[index + 1] == (r, c + 1)):
                            row_str += f"{GREEN} E {YELLOW}."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"{GREEN} E {YELLOW}."
                        else:
                            row_str += f"{GREEN} E  "
                    else:
                        if self.maze[r][c]["E"]:
                            row_str += f" {YELLOW}.{WALL} |"
                        elif (index + 1 < len(stack) and
                              stack[index + 1] == (r, c + 1)):
                            row_str += f"{YELLOW} . ."
                        elif (index - 1 >= 0 and
                              stack[index - 1] == (r, c + 1)):
                            row_str += f"{YELLOW} . ."
                        else:
                            row_str += f"{YELLOW} .  "
                else:
                    if (r, c) == self.start:
                        if self.maze[r][c]["E"]:
                            row_str += f"{GREEN} S {WALL}|"
                        else:
                            row_str += f"{GREEN} S  "
                    elif (r, c) == self.end:
                        if self.maze[r][c]["E"]:
                            row_str += f"{GREEN} E {WALL}|"
                        else:
                            row_str += f"{GREEN} E  "
                    else:
                        if self.maze[r][c]["E"]:
                            row_str += f"{WALL}   |"
                        else:
                            row_str += "    "
            whole_maze += row_str + "\n"
            row_str = "+"
            for c in range(self.width):
                if (r, c) in stack_index:
                    index = stack_index[(r, c)]
                    if self.maze[r][c]["S"]:
                        row_str += f"{WALL}---+"
                    elif (index + 1 < len(stack) and
                          stack[index + 1] == (r + 1, c)):
                        row_str += f" {YELLOW}.{WALL} +"
                    elif index - 1 >= 0 and stack[index - 1] == (r + 1, c):
                        row_str += f" {YELLOW}.{WALL} +"
                    else:
                        row_str += f"{WALL}   +"
                else:
                    if self.maze[r][c]["S"]:
                        row_str += f"{WALL}---+"
                    else:
                        row_str += f"{WALL}   +"
            whole_maze += row_str + "\n"
        return (whole_maze + RESET)
