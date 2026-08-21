# mazegen — Usage Guide

`mazegen` is a standalone, reusable Python package for generating, solving, and
rendering mazes. It can be installed with `pip` and imported into any future
project independently of the `a_maze_ing.py` CLI tool.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

or, from source, at the root of the repository:

```bash
pip install .
```

## Import

```python
from mazegen import Maze, MazeGenerator, MazeSolver
import random
```

---

## 1. Basic example

```python
import random
from mazegen import Maze, MazeGenerator, MazeSolver

# Reproducibility: seed the global random module before generating
random.seed(42)

# 1. Create an empty maze grid
maze = Maze(height=10, width=10, start=(0, 0), end=(9, 9))

# 2. Carve the maze (perfect = single unique path, no loops)
generator = MazeGenerator(maze, perfect=True)
generator.generate_maze()

# 3. Solve it (shortest path, breadth-first search)
solver = MazeSolver(maze)
solver.solver()

print("Solved:", solver.found_solution)
```

That's the minimal flow: **create → generate → solve**.

---

## 2. Passing custom parameters

### Maze size and entry/exit points

```python
maze = Maze(
    height=15,       # number of rows
    width=20,        # number of columns
    start=(0, 0),    # entry coordinates (row, col)
    end=(14, 19),    # exit coordinates (row, col)
)
```

### Reproducibility (seed)

`mazegen` uses Python's built-in `random` module internally, so reproducibility
is controlled by seeding it **before** calling `generate_maze()`:

```python
random.seed(1234)   # same seed -> same maze, every time
```

### Perfect vs. non-perfect maze

```python
# Perfect maze: exactly one path between start and end, no loops
generator = MazeGenerator(maze, perfect=True)

# Non-perfect maze: Pac-Man-style board with loops and open corners
generator = MazeGenerator(maze, perfect=False)

generator.generate_maze()
```

### Animation / display while generating (optional)

`generate_maze()` accepts optional parameters to preview the carving process
in the terminal (mainly intended for the CLI, but usable standalone too):

```python
generator.generate_maze(
    R=0, G=150, B=225,       # wall colour (RGB)
    delay=0.05,               # seconds between animation frames
    display_generation=True,  # print each step to the terminal
)
```

---

## 3. Accessing the generated structure

The `Maze` object exposes the maze data directly — this is **not** the same
format as the hexadecimal output file, but a Python-native structure that is
easier to work with programmatically.

```python
maze.height    # int, number of rows
maze.width     # int, number of columns
maze.start     # tuple[int, int], entry coordinates (row, col)
maze.end       # tuple[int, int], exit coordinates (row, col)
maze._42       # set[tuple[int, int]], cells forming the "42" pattern
```

Each cell is a dictionary keyed by cardinal direction, where `True` means the
wall is closed and `False` means it's open:

```python
maze.maze[row][col]
# -> {"N": True, "E": False, "S": True, "W": True}
```

Example: check whether you can move east from cell (2, 3):

```python
if not maze.maze[2][3]["E"]:
    print("Open path to the east")
```

Helper methods are also available on the `Maze` object:

```python
maze.cell_to_int(r, c)   # int, hexadecimal-style wall encoding (0-15) for one cell
maze.maze_to_hex()       # str, full maze encoded as a hex grid (one row per line)
```

---

## 4. Accessing the solution

`MazeSolver` computes the shortest path from `maze.start` to `maze.end` using
a breadth-first search.

```python
solver = MazeSolver(maze)
solver.solver()

solver.found_solution   # bool, True if a path exists
solver.solution_path    # list[tuple[tuple[int, int], str | None]]
```

`solution_path` is an ordered list of `(coordinates, direction_taken)` pairs,
from start to end. The very first entry has `direction_taken = None` since no
move was needed to reach the starting cell:

```python
for (r, c), direction in solver.solution_path:
    print(f"At ({r}, {c})", f"-> moved {direction}" if direction else "(start)")
```

To get just the ordered list of cells on the path:

```python
path_cells = [coord for coord, _ in solver.solution_path]
```

To get just the sequence of moves (e.g. `"NEESS"`):

```python
path_moves = "".join(
    direction for _, direction in solver.solution_path if direction is not None
)
```

---

## Summary

| Task | Call |
|---|---|
| Create a maze grid | `Maze(height, width, start, end)` |
| Set the seed for reproducibility | `random.seed(seed_value)` before generating |
| Generate a perfect maze | `MazeGenerator(maze, perfect=True).generate_maze()` |
| Generate a Pac-Man-style board | `MazeGenerator(maze, perfect=False).generate_maze()` |
| Read wall data for a cell | `maze.maze[r][c]["N"/"E"/"S"/"W"]` |
| Get hex-encoded maze | `maze.maze_to_hex()` |
| Solve the maze | `MazeSolver(maze).solver()` |
| Read the solution path | `solver.solution_path` |