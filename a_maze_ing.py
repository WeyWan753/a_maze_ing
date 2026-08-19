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
            self._42 = [(r - 2, c - 3), (r - 1, c - 3), (r, c - 3), (r, c - 2),
                        (r, c - 1), (r + 1, c - 1), (r + 2, c - 1), 
                        (r - 2, c + 1), (r - 2, c + 2), (r - 2, c + 3),
                        (r - 1, c + 3), (r, c + 3), (r, c + 2), (r, c + 1),
                        (r + 1, c + 1), (r + 2, c + 1), (r + 2, c + 2), (r + 2, c + 3)]
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
    



    def render_maze(self, stack) -> None:
        R, G, B = 0, 150, 225
    
        print(f"\033[38;2;{R};{G};{B}m", end="")
        whole_maze = "+" + "---+" * self.width + "\n"
        for r in range(self.height):
            row_str = "|"
            for c in range(self.width):
                if (r, c) in self._42:
                    row_str += f"\033[38;2;0;255;0m███\033[38;2;{R};{G};{B}m|"
                elif (r, c) in stack:
                    index = stack.index((r, c))
                    if (r, c) == self.start:
                        if self.maze[r][c]["E"]:
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m|"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m\033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m"
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m\033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m"
                        else:
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m "
                    elif (r, c) == self.end:
                        if self.maze[r][c]["E"]:
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m|"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m\033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m"
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m\033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m"
                        else:
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m "
                    else:
                        if self.maze[r][c]["E"]:
                            row_str += f" \033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m |"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += f"\033[38;2;255;255;0m . .\033[38;2;{R};{G};{B}m"
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += f"\033[38;2;255;255;0m . .\033[38;2;{R};{G};{B}m"
                        else:
                            row_str += f"\033[38;2;255;255;0m .  \033[38;2;{R};{G};{B}m"
                else:
                    if (r, c) == self.start:
                        if self.maze[r][c]["E"]:
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m|"
                        else:
                            row_str += f"\033[38;2;0;255;0m S \033[38;2;{R};{G};{B}m "
                    elif (r, c) == self.end:
                        if self.maze[r][c]["E"]:
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m|"
                        else:
                            row_str += f"\033[38;2;0;255;0m E \033[38;2;{R};{G};{B}m "
                    else:
                        if self.maze[r][c]["E"]:
                            row_str += "   |"
                        else:
                            row_str += "    "
            whole_maze += row_str + "\n"
            row_str = "+"
            for c in range(self.width):
                if (r, c) in stack:
                    index = stack.index((r, c))
                    if self.maze[r][c]["S"]:
                        row_str += "---+"
                    elif index + 1 < len(stack) and stack[index + 1] == (r + 1, c):
                        row_str += f" \033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m +"
                    elif index - 1 >= 0 and stack[index - 1] == (r + 1, c):
                        row_str += f" \033[38;2;255;255;0m.\033[38;2;{R};{G};{B}m +"
                    else:
                        row_str += "   +"
                else:
                    if self.maze[r][c]["S"]:
                        row_str += "---+"
                    else:
                        row_str += "   +"

                    
            whole_maze += row_str + "\n"
        print(whole_maze)
        print("\033[0m", end="")


class Maze_Generator:
    def __init__(self, maze: Maze, perfect = True) -> None:
        self.maze_object = maze
        self.stack = []
        self.visited = [] + maze._42
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
        dead_ends = [(r, c) for r in range(maze.height) for c in range(maze.width) if maze.cell_to_int(r, c) != (1 << 4) - 1 and
                     (maze.cell_to_int(r, c) | (maze.cell_to_int(r, c) + 1)) == (1 << 4) - 1] 
        i = 0
        while i < len(dead_ends):
            r, c = dead_ends[i]
            neighbour_dir = []
            for direction in DIRECTIONS:
                if self.valid_wall_removal(r, c, direction):
                    neighbour_dir.append(direction)

            if neighbour_dir:
                neighbour_dir = random.choice(neighbour_dir)
                for direction in DIRECTIONS:
                    opposite = DIRECTIONS[direction]["opposite"]
                    if neighbour_dir == direction:
                        maze.maze[r][c][direction] = False
                        maze.maze[r + DIRECTIONS[direction]["dr"]][c + DIRECTIONS[direction]["dc"]][opposite] = False
                
                dead_ends = [(r, c) for r in range(maze.height) for c in range(maze.width) if maze.cell_to_int(r, c) != (1 << 4) - 1 and
                            (maze.cell_to_int(r, c) | (maze.cell_to_int(r, c) + 1)) == (1 << 4) - 1] 
                i = 0
            else:
                i += 1


    def generate_maze(self) -> None:
        maze = self.maze_object
        start = maze.start
        end = maze.end
        self.stack.append(start)
        self.visited.append(start)
        while self.stack:
            #maze.render_maze(self.stack)
            #time.sleep(0.05)
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
                self.visited.append(next_point)
                
                for direction in DIRECTIONS:
                    opposite = DIRECTIONS[direction]["opposite"]
                    if neighbour_dir == direction:
                        maze.maze[r][c][direction] = False
                        maze.maze[r + DIRECTIONS[direction]["dr"]][c + DIRECTIONS[direction]["dc"]][opposite] = False
            else:
                self.stack.pop(-1)

        maze.render_maze([])

        if not self.perfect:
            self.make_imperfect()
            maze.render_maze([])


class Maze_Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze_object = maze
        self.queue = []
        self.visited = []
        self.parent = {}
        self.queue_index = 0
        self.found_solution = False
        self.solution_path = []

    def solver(self) -> None:
        self.queue.append(self.maze_object.start)
        self.visited.append(self.maze_object.start)
        self.parent[self.maze_object.start] = None
        while self.queue_index < len(self.queue):
            r, c = self.queue[self.queue_index]
            #if (r, c) == self.maze_object.end:
            if self.maze_object.end in self.queue:
                self.found_solution = True
                break
            for direction in DIRECTIONS:
                if (not self.maze_object.maze[r][c][direction] and
                    (r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"])
                    not in self.visited):
                    self.queue.append((r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]))
                    self.parent[(r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"])] = ((r, c), direction)
                    self.visited.append((r + DIRECTIONS[direction]["dr"], c + DIRECTIONS[direction]["dc"]))
            self.queue_index += 1
            
        if self.found_solution:
            curr = (self.maze_object.end, None)
            while curr is not None:
                self.solution_path.append(curr)
                curr = self.parent[curr[0]]
            self.solution_path.reverse()



def main() -> None:
    for seed in [10]:#random.sample(range(1, 101), 1):
        random.seed(seed)
        maze = Maze(30, 30, (0, 0), (29, 29))
        maze.render_maze([])
        maze_gen = Maze_Generator(maze, perfect=False)
        maze_gen.generate_maze()
        maze_sol = Maze_Solver(maze)
        maze_sol.solver()
        maze.render_maze([item[0] for item in maze_sol.solution_path])
        print(maze.maze_to_hex())
        sol = [item[1] for item in maze_sol.solution_path if item[1] is not None]
        print("".join(sol))
        print("-" * 90)

if __name__ == "__main__":
    main()

