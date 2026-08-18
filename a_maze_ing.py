import random
import time
import os


class Maze:
    def __init__(self, height: int, width: int, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self.maze = [
            [
                {"N": True, "E": True, "S": True, "W": True}
                for col in range(width)
            ]   
            for row in range(height)
        ]


    def cell_to_int(self, r: int, c: int) -> int:
        result = 0
        if self.maze[r][c]["N"]:
            result += (1 << 0)
        if self.maze[r][c]["E"]:
            result += (1 << 1)
        if self.maze[r][c]["S"]:
            result += (1 << 2)
        if self.maze[r][c]["W"]:
            result += (1 << 3)
        return result

    def maze_to_hex(self) -> str:
        return "\n".join(["".join(["0123456789abcdef"[self.cell_to_int(r, c)] for c in range(self.width)]) for r in range(self.height)])
    



        
    def render_maze(self) -> None:
        whole_maze = "+" + "---+" * self.width + "\n"
        for r in range(self.height):
            row_str = "|"
            for c in range(self.width):
                if (r, c) == self.start:
                    row_str += " S |"
                elif (r, c) == self.end:
                    row_str += " E |"
                elif self.maze[r][c]["E"]:
                    row_str += "   |"
                else:
                    row_str += "    "
            whole_maze += row_str + "\n"
            row_str = "+"
            for c in range(self.width):
                if self.maze[r][c]["S"]:
                    row_str += "---+"
                else:
                    row_str += "   +"
            whole_maze += row_str + "\n"
        print(whole_maze)




class Maze_Generator:
    def __init__(self, maze: Maze, perfect = True) -> None:
        self.maze_object = maze
        self.stack = []
        self.visited = []
        self.perfect = perfect

    def valid_wall_removal(self, r: int, c: int, direction: str) -> bool:
        maze = self.maze_object
        if direction == "N":
            if r == 0:
                return False
            if not maze.maze[r][c]["N"]:
                return False
    
        if direction == "E":
            if c == maze.width - 1:
                return False
            if not maze.maze[r][c]["E"]:
                return False

        if direction == "S":
            if r == maze.height - 1:
                return False
            if not maze.maze[r][c]["S"]:
                return False

        if direction == "W":
            if c == 0:
                return False
            if not maze.maze[r][c]["W"]:
                return False
        return True



    def make_imperfect(self) -> None:
        maze = self.maze_object
        dead_ends = [(r, c) for r in range(maze.height) for c in range(maze.width) if maze.cell_to_int(r, c) != (1 << 4) - 1 and
                     (maze.cell_to_int(r, c) | (maze.cell_to_int(r, c) + 1)) == (1 << 4) - 1] 
        i = 0
        while dead_ends:
            r, c = dead_ends[i]
            neighbour = []
            if self.valid_wall_removal(r, c, "N"):
                neighbour.append(((r - 1, c), "N"))
            if self.valid_wall_removal(r, c, "E"):
                neighbour.append(((r, c + 1), "E"))
            if self.valid_wall_removal(r, c, "S"):
                neighbour.append(((r + 1, c), "S"))
            if self.valid_wall_removal(r, c, "W"):
                neighbour.append(((r, c - 1), "W"))

            if neighbour:
                next_point, wall_dir = random.choice(neighbour)
                if wall_dir == "N":
                    maze.maze[r][c]["N"] = False
                    maze.maze[r - 1][c]["S"] = False
                elif wall_dir == "S":
                    maze.maze[r][c]["S"] = False
                    maze.maze[r + 1][c]["N"] = False
                elif wall_dir == "W":
                    maze.maze[r][c]["W"] = False
                    maze.maze[r][c - 1]["E"] = False
                else:
                    maze.maze[r][c]["E"] = False
                    maze.maze[r][c + 1]["W"] = False
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
            self.render_maze()
            time.sleep(0.05)
            r, c = self.stack[-1]
            neighbour = []
            if r > 0 and (r - 1, c) not in self.visited:
                neighbour.append(((r - 1, c), "N"))
            if r < maze.height - 1 and (r + 1, c) not in self.visited:
                neighbour.append(((r + 1, c), "S"))
            if c > 0 and (r, c - 1) not in self.visited:
                neighbour.append(((r, c - 1), "W"))
            if c < maze.width - 1 and (r, c + 1) not in self.visited:
                neighbour.append(((r, c + 1), "E"))

            if neighbour:
                next_point, direction = random.choice(neighbour)
                self.stack.append(next_point)
                self.visited.append(next_point)
                
                if direction == "N":
                    maze.maze[r][c]["N"] = False
                    maze.maze[r - 1][c]["S"] = False
                elif direction == "S":
                    maze.maze[r][c]["S"] = False
                    maze.maze[r + 1][c]["N"] = False
                elif direction == "W":
                    maze.maze[r][c]["W"] = False
                    maze.maze[r][c - 1]["E"] = False
                else:
                    maze.maze[r][c]["E"] = False
                    maze.maze[r][c + 1]["W"] = False

            else:
                self.stack.pop(-1)

        #if not self.perfect:
            #self.make_imperfect()


    def render_maze(self) -> None:
        whole_maze = "+" + "---+" * self.maze_object.width + "\n"
        for r in range(self.maze_object.height):
            row_str = "|"
            for c in range(self.maze_object.width):
                if (r, c) in self.stack:
                    index = self.stack.index((r, c))
                    if (r, c) == self.maze_object.start:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " S |"
                        elif index + 1 < len(self.stack) and self.stack[index + 1] == (r, c + 1):
                            row_str += " S ."
                        elif index - 1 >= 0 and self.stack[index - 1] == (r, c + 1):
                            row_str += " S ."
                        else:
                            row_str += " S  "
                    elif (r, c) == self.maze_object.end:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " E |"
                        elif index + 1 < len(self.stack) and self.stack[index + 1] == (r, c + 1):
                            row_str += " E ."
                        elif index - 1 >= 0 and self.stack[index - 1] == (r, c + 1):
                            row_str += " E ."
                        else:
                            row_str += " E  "
                    else:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " . |"
                        elif index + 1 < len(self.stack) and self.stack[index + 1] == (r, c + 1):
                            row_str += " . ."
                        elif index - 1 >= 0 and self.stack[index - 1] == (r, c + 1):
                            row_str += " . ."
                        else:
                            row_str += " .  "
                else:
                    if (r, c) == self.maze_object.start:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " S |"
                        else:
                            row_str += " S  "
                    elif (r, c) == self.maze_object.end:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " E |"
                        else:
                            row_str += " E  "
                    else:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += "   |"
                        else:
                            row_str += "    "
            whole_maze += row_str + "\n"
            row_str = "+"
            for c in range(self.maze_object.width):
                if (r, c) in self.stack:
                    index = self.stack.index((r, c))
                    if self.maze_object.maze[r][c]["S"]:
                        row_str += "---+"
                    elif index + 1 < len(self.stack) and self.stack[index + 1] == (r + 1, c):
                        row_str += " . +"
                    elif index - 1 >= 0 and self.stack[index - 1] == (r + 1, c):
                        row_str += " . +"
                    else:
                        row_str += "   +"
                else:
                    if self.maze_object.maze[r][c]["S"]:
                        row_str += "---+"
                    else:
                        row_str += "   +"

                    
            whole_maze += row_str + "\n"
        print(whole_maze)


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
            if (r, c) == self.maze_object.end:
                self.found_solution = True
                break
            if not self.maze_object.maze[r][c]["N"] and (r - 1, c) not in self.visited:
                self.queue.append((r - 1, c))
                self.parent[(r - 1, c)] = ((r, c), "N")
                self.visited.append((r - 1, c))
            if not self.maze_object.maze[r][c]["S"] and (r + 1, c) not in self.visited:
                self.queue.append((r + 1, c))
                self.parent[(r + 1, c)] = ((r, c), "S")
                self.visited.append((r + 1, c))
            if not self.maze_object.maze[r][c]["W"] and (r, c - 1) not in self.visited:
                self.queue.append((r, c - 1))
                self.parent[(r, c - 1)] = ((r, c), "W")
                self.visited.append((r, c - 1))
            if not self.maze_object.maze[r][c]["E"] and (r, c + 1) not in self.visited:
                self.queue.append((r, c + 1))
                self.parent[(r, c + 1)] = ((r, c), "E")
                self.visited.append((r, c + 1))
            self.queue_index += 1
            
        if self.found_solution:
            curr = (self.maze_object.end, None)
            while curr is not None:
                self.solution_path.append(curr)
                curr = self.parent[curr[0]]
            self.solution_path.reverse()

    def render_maze(self) -> None:
        stack = [item[0] for item in self.solution_path]
        solution_direction = "".join([item[1] for item in self.solution_path if item[1] is not None])
        whole_maze = "+" + "---+" * self.maze_object.width + "\n"
        for r in range(self.maze_object.height):
            row_str = "|"
            for c in range(self.maze_object.width):
                if (r, c) in stack:
                    index = stack.index((r, c))
                    if (r, c) == self.maze_object.start:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " S |"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += " S ."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += " S ."
                        else:
                            row_str += " S  "
                    elif (r, c) == self.maze_object.end:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " E |"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += " E ."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += " E ."
                        else:
                            row_str += " E  "
                    else:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " . |"
                        elif index + 1 < len(stack) and stack[index + 1] == (r, c + 1):
                            row_str += " . ."
                        elif index - 1 >= 0 and stack[index - 1] == (r, c + 1):
                            row_str += " . ."
                        else:
                            row_str += " .  "
                else:
                    if (r, c) == self.maze_object.start:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " S |"
                        else:
                            row_str += " S  "
                    elif (r, c) == self.maze_object.end:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += " E |"
                        else:
                            row_str += " E  "
                    else:
                        if self.maze_object.maze[r][c]["E"]:
                            row_str += "   |"
                        else:
                            row_str += "    "
            whole_maze += row_str + "\n"
            row_str = "+"
            for c in range(self.maze_object.width):
                if (r, c) in stack:
                    index = stack.index((r, c))
                    if self.maze_object.maze[r][c]["S"]:
                        row_str += "---+"
                    elif index + 1 < len(stack) and stack[index + 1] == (r + 1, c):
                        row_str += " . +"
                    elif index - 1 >= 0 and stack[index - 1] == (r + 1, c):
                        row_str += " . +"
                    else:
                        row_str += "   +"
                else:
                    if self.maze_object.maze[r][c]["S"]:
                        row_str += "---+"
                    else:
                        row_str += "   +"

                    
            whole_maze += row_str + "\n"
        print(whole_maze)
        print(solution_direction)


def main() -> None:
    seed = 1048
    random.seed(seed)
    maze = Maze(10, 10, (0, 0), (3, 6))
    maze.render_maze()
    maze_gen = Maze_Generator(maze, perfect=True)
    maze_gen.generate_maze()
    maze_gen.render_maze()
    maze_sol = Maze_Solver(maze)
    maze_sol.solver()
    maze_sol.render_maze()

if __name__ == "__main__":
    main()

