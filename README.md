*This project has been created as part of the 42 curriculum by lupalomi y scamlett.*

# A-maze-ing

## Description

A-Maze-ing is a maze generation tool written in Python. It reads a
configuration file, generates a random maze, and displays it interactively
in the terminal with ASCII art and ANSI colours.

Two generation modes are supported (controlled by the ``PERFECT`` config key):

- **Perfect maze** (``PERFECT=True``): exactly one path between any two
  cells — no loops, no unreachable areas.  Generated with a recursive
  backtracker (DFS).  *(Implemented.)*
- **Pac-Man board** (``PERFECT=False``): a playable maze with loops, open
  corners and centre, and minimal dead-ends — suitable for a Pac-Man-like
  game.  *(Not yet implemented.)*

The project is built around a reusable ``mazegen`` package that can be
installed via pip and imported into other projects.

## Instructions

```bash
make install     # create venv and install dependencies
make run         # launch the interactive maze display
make lint        # run flake8 + mypy type checks
make clean       # remove caches and temporary files
```

The program expects a config.txt file as its only argument.


### Interactive controls

| Key | Action |
|-----|--------|
| `1` | Re-generate a new random maze |
| `2` | Show / hide the shortest path (coming soon) |
| `3` | Cycle through wall colours |
| `4` | Quit |

## Execution flow

1. Parse `config.txt` — extract `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`,
   `OUTPUT_FILE`, and `PERFECT`.
2. Instantiate `MazeGenerator` with the parsed parameters.
3. Run the generation algorithm — all cells start with four walls; the
   recursive backtracker carves passages until every cell is reachable.
4. Hand the generated maze to `MazeDisplay`, which renders it as an ASCII
   grid and starts the interactive menu loop.

*(Output file writing to the hexadecimal format is not yet implemented.)*

## Algorithms used

*not yet implemented*

### Recursive backtracker (DFS) — PERFECT=True

The maze generator uses a **depth-first search with an explicit stack** (no
recursion, to avoid hitting Python's recursion limit on large mazes).

1. Initialise every cell with all four walls **closed** (bitmask `0xF`).
2. Push the starting cell `(0, 0)` onto the stack and mark it visited.
3. While the stack is not empty:
   - Look at the top cell. If it has any unvisited neighbours, pick one
     at random, remove the wall between them, mark it visited, and push
     it onto the stack.
   - If it has no unvisited neighbours, pop it (backtrack).
4. Open the border walls at the entry and exit coordinates.

This guarantees a **perfect maze** — exactly one path connects any two
cells, with no loops and no isolated areas. The algorithm is simple,
well-documented, and produces mazes with a characteristic long-corridor
texture.

### Pac-Man board — PERFECT=False (coming soon)


## Reusable ``mazegen`` package

The ``mazegen/`` directory is a **self-contained, pip-installable Python
package** that can be imported and reused in a future project.  It
exposes the ``MazeGenerator`` class through a clean public API.


### Building the distributable package

The package is built with the standard ``build`` tool, producing a
``mazegen-1.0.0-py3-none-any.whl`` at the **root** of the
repository (the source archive ``.tar.gz`` stays in ``dist/``):

```bash
# 1. Create a virtualenv and install build dependencies
make install

# 2. Build the wheel + sdist, copy .whl to repo root
make build
```

``make build`` runs ``python -m build`` and then copies the ``.whl``
to the project root so it is available as a single distributable file
alongside the sources.

### Installing in another project

Once the .whl file is built, any project can install it with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

#### Instantiation & basic usage

```python
from mazegen import MazeGenerator

# Create a 20×10 perfect maze with random seed
gen = MazeGenerator(width=20, height=10)
gen.generate()                          # carve the passages

# Access the generated structure
walls = gen.get_walls()                 # 2D list of 4-bit wall bitmasks
w, h = gen.get_dimensions()             # (20, 10)
entry = gen.get_entry()                 # (0, 0) by default
exit_cell = gen.get_exit()              # (19, 9) e.g. bottom-right
```

#### Custom parameters

All constructor arguments are optional except ``width`` and ``height``:

| Parameter  | Type             | Default     | Description                                          |
|------------|------------------|-------------|------------------------------------------------------|
| ``width``  | ``int``          | *required*  | Cells horizontally (≥ 2).                            |
| ``height`` | ``int``          | *required*  | Cells vertically (≥ 2).                              |
| ``entry``  | ``(int, int)``   | ``(0, 0)``  | Coordinates of the entry cell.                       |
| ``exit``   | ``(int, int)``   | ``(0, 0)``  | Coordinates of the exit cell.                        |
| ``seed``   | ``int | None``   | ``None``    | Random seed for reproducible generation.             |
| ``perfect``| ``bool``         | ``True``    | ``True`` = perfect maze; ``False`` = Pac-Man board.  |

```python
# Reproducible maze with custom entry/exit
gen = MazeGenerator(
    width=30,
    height=15,
    entry=(0, 0),
    exit=(29, 14),
    seed=None,
    perfect=True,
)
gen.generate()
```


#### Accessing the maze structure

The internal representation is a **2D grid of 4-bit wall bitmasks**,
where each cell stores which walls are *closed* (present):

| Bit | Value | Wall  |
|-----|-------|-------|
| 0   | 1     | North |
| 1   | 2     | East  |
| 2   | 4     | South |
| 3   | 8     | West  |

A bit set to ``1`` means the wall is **closed**.  A cell with all four
walls closed has value ``0xF`` (15); a fully open cell has value ``0``.

```python
walls = gen.get_walls()         
```

### Complete usage example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=15, height=10, entry=(0, 0), exit=(14, 9), seed=42)
gen.generate()

print(f"Maze: {gen.get_dimensions()}")
print(f"Entry: {gen.get_entry()}, Exit: {gen.get_exit()}")

walls = gen.get_walls()
print(f"Cell (0,0) walls: {walls[0][0]:04b}")
```


## Bonus


## Resources
- https://medium.com/@icodewithben/solving-a-maze-using-depth-first-search-and-backtracking-142228603d1b
- https://github.com/cu-sanjay/Maze-Solver/

## Contributions
- `lupalomi`: Backend algorithms, output file, pathfinding, "42" pattern,
  Pac-Man board mode.
- `scamlett`: Project setup, maze generation core, terminal display,
  README & documentation, package build, visual polish.

## Contribution diary
Susana 19/06:
- Initial file structure

Susana 04/07–05/07:
- venv, requirements.txt, Makefile, .gitignore
- setup.cfg for flake8 and mypy to ignore venv
- mazegen package structure:
  - init.py - exporting package
  - MazeGenerator class — recursive backtracker
  - MazeDisplay class — terminal ASCII rendering, ANSI colour rotation,
  interactive menu
- a_maze_ing.py — config file parser, CLI argument handling, error messages
- README.md — description, instructions, execution flow, algorithms,
  to-do list
- LICENSE.md

Susana 11/07:
- Fix Makefile
- Add .toml file for package generation 
- Add documentation for reusable package
- Test package generation (create .whl at repo root)


/////// LUIS TO-DO /////
- Output file maze.txt (hex format) with maze_analyzer.py validation
- Solution algorithm (shortest path BFS for example)
- "42" pattern
- PERFECT=False Pac-Man board (v2.2 requirements)
- Optional: Unit tests (pytest)
- Bonus: extra algorithms or zero dead-end braided board (v2.2 bonus)

//// SUSI TO-DO /////
- Rewrite and simplify generator algorithm
- Bonus: extra graphics / animations
- README.md final version:
  - Config file format documentation
  - Why the recursive backtracker was chosen
  - Reusable module docs (instantiation, parameters, accessing structure)
  - Team roles, planning evolution, what worked / could improve
  - Resources section
