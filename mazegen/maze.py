class Maze:
    def __init__(
            self, height: int, width: int, start: tuple[int, int],
            end: tuple[int, int]
            ) -> None:
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
        return (
            self.maze[r][c]["N"] * 1
            + self.maze[r][c]["E"] * 2
            + self.maze[r][c]["S"] * 4
            + self.maze[r][c]["W"] * 8
        )

    def maze_to_hex(self) -> str:
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
