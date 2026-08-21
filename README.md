*This project has been created as part of the 42 curriculum by \<login1\>, \<luli2\>*

# A-Maze-ing

# Description
- 项目是做什么的
- 支持 PERFECT / non-PERFECT maze
- 主要功能简单概括

# Instructions

### Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
````

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
make install
```

### Run

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Build reusable package

```bash
make build
```


# Configuration

配置文件格式：

```text
WIDTH=30
HEIGHT=30
ENTRY=0,0
EXIT=19,24
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
...
```

说明每个字段：

* `WIDTH`
* `HEIGHT`
* `ENTRY`
* `EXIT`
* `OUTPUT_FILE`
* `PERFECT`
* optional parameters...

# Maze Generation Algorithm

### Perfect Maze

* 使用什么算法（你们现在是 randomized DFS）
* 大概执行流程
* 为什么选择它

### Imperfect Maze

* PERFECT=False 后做了什么
* 如何增加 loop / 减少 dead end

### Solver

* BFS
* 为什么可以得到 shortest path

## Program Architecture

```text
a_maze_ing.py
    ↓
Config
    ↓
Maze
    ↓
MazeGenerator
    ↓
MazeSolver
    ↓
render / save output
```

然后简单解释：

* `a_maze_ing.py`
* `config.py`
* `maze.py`
* `generator.py`
* `solver.py`
* `directions.py`

# Reusable Maze Generator

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import ...
```

### Custom size / seed

写 example。

### Access generated maze

写 example。

### Access a solution

写 example。

> 这一部分同时也是 `mazegen/USAGE.md` 里要有的 short documentation。

## Output Format

说明：

* 每个 cell 一个 hexadecimal digit
* N / E / S / W 对应哪些 bit
* blank line
* ENTRY
* EXIT
* shortest path

## Controls

例如：

* regenerate maze
* show/hide path
* change wall color
* toggle generation animation
* quit

# Team Work

### Roles

* Member A:
* Member B: luli2

### Planning and evolution

* 最开始怎么分工
* 后来有没有调整
* 为什么调整

### What worked / what did not

简短写开发过程中有效和无效的方案。

# Resources

* Python documentation
* setuptools / packaging documentation
* algorithm references
* 其他资料

### AI Usage

写你们在哪些地方用了 AI，以及最终代码/设计如何验证。

## License

This project is licensed under the MIT License.
See `LICENSE.md`.

# Bonus

* --max-dead-ends 0
* nimation during maze generation