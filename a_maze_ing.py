import random
import time
import os
import sys


DIRECTIONS: dict[str, dict[str, str | int]] = {
    "N": {"dr": -1, "dc": 0, "opposite": "S", "bit": 0},
    "E": {"dr": 0, "dc": 1, "opposite": "W", "bit": 1},
    "S": {"dr": 1, "dc": 0, "opposite": "N", "bit": 2},
    "W": {"dr": 0, "dc": -1, "opposite": "E", "bit": 3},
}


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
        return sum(
            1 << int(DIRECTIONS[direction]["bit"])
            for direction in DIRECTIONS if self.maze[r][c][direction]
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

        print(WALL, end="")
        whole_maze = "+" + "---+" * self.width + "\n"
        for r in range(self.height):
            row_str = "|"
            for c in range(self.width):
                if (r, c) in self._42:
                    row_str += f"{GREEN}███{WALL}|"
                elif (r, c) in stack:
                    index = stack.index((r, c))
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
                if (r, c) in stack:
                    index = stack.index((r, c))
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


class Maze_Generator:
    def __init__(self, maze: Maze, perfect: bool = True) -> None:
        self.maze_object = maze
        self.stack: list[tuple[int, int]] = []
        self.visited = set(maze._42)
        self.perfect = perfect

    def large_open_region(self, r: int, c: int, direction: str) -> bool:
        maze = self.maze_object
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
        return (
            maze.cell_to_int(r, c) == (1 << int(DIRECTIONS[direction]["bit"]))
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
        if ((r + int(DIRECTIONS[direction]["dr"]),
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
        maze = self.maze_object

        def is_dead_end(r: int, c: int) -> bool:
            cell = maze.cell_to_int(r, c)
            return (cell != (1 << 4) - 1 and
                    ((cell | cell + 1) == (1 << 4) - 1))

        dead_ends = [
            (r, c) for r in range(maze.height)
            for c in range(maze.width)
            if is_dead_end(r, c)]
        i = 0
        while i < len(dead_ends):
            if display_generation:
                frame = maze.render_maze([], R, G, B)
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(delay)
            r, c = dead_ends[i]
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
                dead_ends = [(r, c) for (r, c) in dead_ends
                             if is_dead_end(r, c)]
                i = 0
            else:
                i += 1

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


class Maze_Solver:
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


class Config:
    def __init__(self, filename: str) -> None:
        self.required = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "OUTPUT_FILE", "PERFECT", "DELAY", "SEED"]
        self.config = self.load_config(filename)
        self.parse_config()
        self.validate_config_format()

    def load_config(self, filename: str = "config.txt") -> dict[str, str]:
        config = {}

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                config[key] = value

        return config

    def parse_config(self) -> None:
        for key in self.required:
            value = self.config.get(key)
            if value is None:
                raise Exception(f"Missing key: {key}")

    def validate_config_format(self) -> None:
        self.WIDTH = int(self.config["WIDTH"])
        self.HEIGHT = int(self.config["HEIGHT"])
        r, c = tuple(int(x) for x in self.config["ENTRY"].split(",", 1))
        self.ENTRY = (r, c)
        r, c = tuple(int(x) for x in self.config["EXIT"].split(",", 1))
        self.EXIT = (r, c)
        self.OUTPUT_FILE = self.config["OUTPUT_FILE"].strip("\"'")
        self.PERFECT = self.config["PERFECT"].strip("\"'").lower() == "true"
        self.DELAY = float(self.config["DELAY"])
        self.SEED = int(self.config["SEED"])
        _42 = set()
        if self.HEIGHT >= 6 and self.WIDTH >= 9:
            (r, c) = (self.HEIGHT//2, self.WIDTH//2)
            _42 = {
                    (r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                    (r, c - 1), (r + 1, c - 1), (r + 2, c - 1),
                    (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                    (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                    (r + 1, c + 1), (r + 2, c + 1),
                    (r + 2, c + 2), (r + 2, c + 3)}
        if self.ENTRY in _42:
            raise Exception("Entry Cant be in 42 pattern")
        if self.EXIT in _42:
            raise Exception("Exit Cant be in 42 pattern")
        if self.ENTRY == self.EXIT:
            raise Exception("Entry and Exit cant be the same")
        if not (0 <= self.ENTRY[0] < self.HEIGHT and
                0 <= self.ENTRY[1] < self.WIDTH):
            raise Exception("Entry is out of bound")
        if not (0 <= self.EXIT[0] < self.HEIGHT and
                0 <= self.EXIT[1] < self.WIDTH):
            raise Exception("Exit is out of bound")
        if self.HEIGHT <= 0:
            raise Exception("Height must be positive integer")
        if self.WIDTH <= 0:
            raise Exception("Width must be positive integer")
        if ((self.HEIGHT == 1 or self.WIDTH == 1) and not self.PERFECT):
            raise Exception("No non-perfect maze can be generated")

    def save_output(
        self, maze_hex: str,
        solution_path: list[tuple[tuple[int, int], str | None]]
    ) -> None:
        with open(self.OUTPUT_FILE, "w") as file:
            file.write(
                maze_hex + "\n\n" +
                f"{self.ENTRY[0]},{self.ENTRY[1]}" +
                "\n" + f"{self.EXIT[0]},{self.EXIT[1]}"
                + "\n" +
                "".join(
                    [item[1] for item in solution_path
                     if item[1] is not None])
                + "\n"
            )


def main() -> None:

    if len(sys.argv) != 2:
        print("wrong format, usage: python3 a_maze_ing.py [config file name]")
        return

    disp_gen = False
    show_path = True
    i = 0
    colours = [
            (0, 150, 225), (255, 0, 0), (0, 255, 0),
            (0, 0, 255), (255, 255, 0), (255, 0, 255)]

    try:
        config = Config(sys.argv[1])
    except Exception as e:
        print(e)
        return

    while True:
        try:
            print("\033[?25l", end="")
            maze = Maze(config.HEIGHT, config.WIDTH, config.ENTRY, config.EXIT)
            maze_gen = Maze_Generator(maze, config.PERFECT)
            maze_gen.generate_maze(*colours[i], config.DELAY, disp_gen)
            maze_sol = Maze_Solver(maze)
            maze_sol.solver()
            while True:
                path = [
                        item[0] for item in maze_sol.solution_path
                ] if show_path else []
                frame = maze.render_maze(path, *colours[i])
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                print("=== A-Maze_ing ===")
                print("1. Re-generate a new maze")
                print("2. Show / Hide the shortest path")
                print("3. Rotate the wall colours")
                print(f"4. Toggle animation of generation of the "
                      f"maze (Status : {'On' if disp_gen else 'Off'})")
                print("5. Quit")

                config.save_output(maze.maze_to_hex(), maze_sol.solution_path)
                choice = input("Choice? (1-5): ")
                if choice == "1":
                    break
                if choice == "2":
                    show_path = not show_path
                    continue
                if choice == "3":
                    i += 1
                    i %= len(colours)
                    continue
                if choice == "4":
                    disp_gen = not disp_gen
                if choice == "5":
                    return

        except Exception as e:
            print(e)
            return

        finally:
            print("\033[?25h", end="")


if __name__ == "__main__":
    main()
