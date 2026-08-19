import random
import time
import os


DIRECTIONS = {
    "N": {"dr": -1, "dc": 0, "opposite": "S", "bit": 0},
    "E": {"dr": 0, "dc": 1, "opposite": "W", "bit": 1},
    "S": {"dr": 1, "dc": 0, "opposite": "N", "bit": 2},
    "W": {"dr": 0, "dc": -1, "opposite": "E", "bit": 3},
}


class Maze:
    def __init__(self, height: int, width: int, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self._42 = []
        if self.height >= 6 and self.width >= 9:
            (r, c) = (self.height//2, self.width//2)
            self._42 = {(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1), 
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2), (r + 2, c + 3)}
        self.maze = [
            [
                {"N": True, "E": True, "S": True, "W": True}
                for col in range(width)
            ]   
            for row in range(height)
        ]


    def cell_to_int(self, r: int, c: int) -> int:
        return sum([1 << DIRECTIONS[direction]["bit"] for direction in DIRECTIONS if self.maze[r][c][direction]])

    def maze_to_hex(self) -> str:
        return "\n".join(["".join(["0123456789abcdef"[self.cell_to_int(r, c)] for c in range(self.width)]) for r in range(self.height)])
    
    def render_maze(self, stack, R=0, G=150,B=225) -> str:

        WALL      = f"\033[38;2;{R};{G};{B}m"   
        GREEN     = "\033[38;2;0;255;0m"        
        YELLOW    = "\033[38;2;255;255;0m"      
        RESET     = "\033[0m"

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
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"{GREEN} S {YELLOW}."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"{GREEN} S {YELLOW}."
                        else:
                            row_str += f"{GREEN} S  "
                    elif (r, c) == self.end:
                        if self.maze[r][c]["E"]:
                            row_str += f"{GREEN} E {WALL}|"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"{GREEN} E {YELLOW}."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"{GREEN} E {YELLOW}."
                        else:
                            row_str += f"{GREEN} E  "
                    else:
                        if self.maze[r][c]["E"]:
                            row_str += f" {YELLOW}.{WALL} |"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"{YELLOW} . ."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
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
                    elif index + 1 < len(stack) and stack[index + 1] == (r + 1, c):
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
    def __init__(self, maze: Maze, perfect = True) -> None:
        self.maze_object = maze
        self.stack = []
        self.visited = set(maze._42)
        self.perfect = perfect

    def large_open_region(self, r, c, direction) -> bool:
        maze = self.maze_object
        if not(0 < c < maze.width - 1 and 0 < r < maze.height - 1):
            return False
        left = maze.maze[r][c - 1]
        bottom_left = maze.maze[r + 1][c - 1]
        bottom = maze.maze[r + 1][c]
        bottom_right = maze.maze[r + 1][c + 1]
        right = maze.maze[r][c + 1]
        top_right = maze.maze[r - 1][c + 1]
        top = maze.maze[r - 1][c]
        top_left = maze.maze[r - 1][c - 1]
        return (maze.cell_to_int(r, c) == (1 << DIRECTIONS[direction]["bit"])
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
        if (not 0 <= r + DIRECTIONS[direction]["dr"] < maze.height
            or not 0 <= c + DIRECTIONS[direction]["dc"] < maze.width):
            return False
        if not maze.maze[r][c][direction]:
            return False
        if (r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]) in maze._42:
            return False
        if self.large_open_region(r, c, direction):
            return False
        if self.large_open_region(
                r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"],
                DIRECTIONS[direction]["opposite"]):
            return False
        

        return True



    def make_imperfect(self) -> None:
        maze = self.maze_object

        def is_dead_end(r, c) -> bool:
            return (maze.cell_to_int(r, c) != (1 << 4) - 1 and (maze.cell_to_int(r, c) | (maze.cell_to_int(r, c) + 1)) == (1 << 4) - 1)

        dead_ends = [(r, c) for r in range(maze.height) for c in range(maze.width) if is_dead_end(r, c)] 
        i = 0
        while i < len(dead_ends):
            frame = maze.render_maze([])
            os.system("cls" if os.name == "nt" else "clear")
            print(frame)
            time.sleep(0.03)
            r, c = dead_ends[i]
            neighbour_dir = []
            for direction in DIRECTIONS:
                if self.valid_wall_removal(r, c, direction):
                    neighbour_dir.append(direction)

            if neighbour_dir:
                neighbour_dir = random.choice(neighbour_dir)
                opposite = DIRECTIONS[neighbour_dir]["opposite"]
                maze.maze[r][c][neighbour_dir] = False
                maze.maze[r + DIRECTIONS[neighbour_dir]["dr"]][c + DIRECTIONS[neighbour_dir]["dc"]][opposite] = False
                dead_ends = [(r, c) for (r, c) in dead_ends if is_dead_end(r, c)] 
                i = 0
            else:
                i += 1


    def generate_maze(self, R=0, G=150,B=225) -> None:
        maze = self.maze_object
        start = maze.start
        end = maze.end
        self.stack.append(start)
        self.visited.add(start)
        while self.stack:
            frame = maze.render_maze(self.stack, R, G, B)
            os.system("cls" if os.name == "nt" else "clear")
            print(frame)
            time.sleep(0.005)
            r, c = self.stack[-1]
            neighbour = []
            for direction in DIRECTIONS:
                if (0 <= r + DIRECTIONS[direction]["dr"] < maze.height
                    and 0 <= c + DIRECTIONS[direction]["dc"] < maze.width
                    and (r + DIRECTIONS[direction]["dr"],
                         c + DIRECTIONS[direction]["dc"]) not in self.visited):
                    neighbour.append(
                            ((r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]), direction)
                    )

            if neighbour:
                next_point, neighbour_dir = random.choice(neighbour)
                self.stack.append(next_point)
                self.visited.add(next_point)
                opposite = DIRECTIONS[neighbour_dir]["opposite"]
                maze.maze[r][c][neighbour_dir] = False
                maze.maze[r + DIRECTIONS[neighbour_dir]["dr"]][c + DIRECTIONS[neighbour_dir]["dc"]][opposite] = False
            else:
                self.stack.pop(-1)


        if not self.perfect:
            self.make_imperfect()


class Maze_Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze_object = maze
        self.queue = []
        self.visited = set()
        self.parent = {}
        self.queue_index = 0
        self.found_solution = False
        self.solution_path = []


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
                if (not self.maze_object.maze[r][c][direction] and
                    (r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"])
                    not in self.visited):
                    self.queue.append((r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]))
                    self.parent[(r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"])] = ((r, c), direction)
                    self.visited.add((r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]))
            self.queue_index += 1
            
        if self.found_solution:
            curr = (self.maze_object.end, None)
            while curr is not None:
                self.solution_path.append(curr)
                curr = self.parent[curr[0]]
            self.solution_path.reverse()



def main() -> None:
    random.seed(42)
    show_path = True
    perfect = False
    i = 0
    colours = [(0, 150, 225), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    while True:
        try:
            print("\033[?25l", end="") #hide cursor
            maze = Maze(15, 15, (0, 0), (14, 14))
            maze_gen = Maze_Generator(maze, perfect)
            maze_gen.generate_maze(*colours[i])
            maze_sol = Maze_Solver(maze)
            maze_sol.solver()
            while True:
                path = [item[0] for item in maze_sol.solution_path] if show_path else []
                frame = maze.render_maze(path, *colours[i])
                os.system("cls" if os.name == "nt" else "clear")
                print(frame)
                time.sleep(0.005)
                print("=== A-Maze_ing ===")
                print("1. Re-generate a new maze")
                print("2. Show / Hide the shortest path")
                print("3. Rotate the wall colours")
                print("4. Quit")
                choice = input("Choice? (1-4): ")
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
                    return
        finally:
            print("\033[?25h", end="")#show cursor

if __name__ == "__main__":
    main()

