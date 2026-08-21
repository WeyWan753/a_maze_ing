from mazegen import Maze, MazeGenerator, MazeSolver, Config
import random
import os
import sys


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
        random.seed(config.SEED)
    except Exception as e:
        print(e)
        return

    while True:
        try:
            print("\033[?25l", end="")
            maze = Maze(config.HEIGHT, config.WIDTH, config.ENTRY, config.EXIT)
            maze_gen = MazeGenerator(maze, config.PERFECT)
            maze_gen.generate_maze(*colours[i], config.DELAY, disp_gen)
            maze_sol = MazeSolver(maze)
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
