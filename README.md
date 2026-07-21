*This project has been created as part of the 42 curriculum by lupalomi y scamlett.*

# A-maze-ing

## Description

A-Maze-ing is a maze generation tool written in Python. It reads a
configuration file, generates a random maze, and displays it interactively
in the terminal with ASCII art and ANSI colours.

Two generation modes are supported (controlled by the ``PERFECT`` config key):

- **Perfect maze** (``PERFECT=True``): exactly one path between any two
  cells — no loops, no unreachable areas.  Generated with a recursive
  backtracker (DFS).
- **Pac-Man board** (``PERFECT=False``): a playable maze with loops, open
  corners and centre, and minimal dead-ends — suitable for a Pac-Man-like
  game.

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
| `2` | Show / hide the shortest path |
| `3` | Cycle through wall colours |
| `4` | Show DFS generation animation |
| `5` | Quit |

## Config file format

The program reads a single configuration file (default: ``config.txt``).
Every line follows the ``KEY=VALUE`` pattern:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=True
```

| Key            | Format              | Description                              |
|----------------|---------------------|------------------------------------------|
| ``WIDTH``      | positive integer    | Maze width in cells (≥ 2).               |
| ``HEIGHT``     | positive integer    | Maze height in cells (≥ 2).              |
| ``ENTRY``      | ``x,y``             | Coordinates of the entry cell.           |
| ``EXIT``       | ``x,y``             | Coordinates of the exit cell.            |
| ``OUTPUT_FILE``| filename            | Path where the hex output is written.    |
| ``PERFECT``    | ``True`` / ``False``| ``True`` = perfect maze; ``False`` = Pac‑Man board. |

All keys are **mandatory**.  Entry and exit must be different cells
and must lie within the maze bounds.  The parser strips whitespace and
ignores empty lines.

## Execution flow

1. Parse `config.txt` — extract `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`,
   `OUTPUT_FILE`, and `PERFECT`.
2. Instantiate `MazeGenerator` with the parsed parameters.
3. Run the generation algorithm — all cells start with four walls; the
   recursive backtracker carves passages until every cell is reachable.
4. Hand the generated maze to `MazeDisplay`, which renders it as an ASCII
   grid and starts the interactive menu loop.
5. Generates a solution using a BFS algorithm
6. Generates a output file that includes a hexadecimal version of the map, the entry ubication, the exit ubication and the shortest path to exit in cardinal points (North, N; East, E; South, S; West, W)

## Algorithms used


### DFS maze generator — PERFECT=True

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

#### Why DFS?

- **Guaranteed connectivity** — every cell is reachable from every other
  cell, with no isolated areas.  The maze is always solvable.
- **Simplicity** — the algorithm is easy to understand, implement, and
  debug.  Using an explicit stack avoids Python's recursion limit on
  large mazes while keeping the logic clear.
- **Well-studied** — recursive backtracker is one of the most common
  maze generation algorithms, with abundant documentation and examples
  available for reference.
- **Perfect maze** — exactly one path connects any two
  cells, with no loops and no isolated areas.

### Pac-Man board — PERFECT=False 
Generates a DFS maze and then:

1. **Search and secures open corners and the center of the maze.**
2. **Search and eliminate almost every the dead-end of the maze, leaving only 2 intact.**

The algorithm used here is exactly the same that the **`PERFECT=TRUE`** uses (DFS) but with a few extra steps.

### Breadth-First Search (BFS) - Shortest path to exit
The function `shortest_path` defined in **solver.py** uses a BFS algorithm to find the first path to the exit, which is also the shortest path because all tiles have the same **movement cost**. In this function:

- `Queue`: Represent the tiles pending to visit.
- `Visited`: The tiles which have already been visited.
- `Parent`: The tile used to reach the "key" value with the movement direction.

#### Why not use DFS here?
`DFS always tries to go as deep as posible` ('South' direction, ↓) which is perfect for generating mazes but almost never guarantees that the solution path is also the shortest path to the exit.

This is not the case of the BFS algorithm, which is pretty similar to `flood fill` algorithm. Both algorithms roam all the tiles until they find a condition to stop. However, the main difference is that BFS algorithm also saves the `Parent` path to generate a coherent solution with the shortest possible path.


## Reusable ``mazegen`` package

The ``mazegen/`` directory is a **self-contained, pip-installable Python
package** that can be imported and reused in a future project.  It
exposes the ``MazeGenerator`` class through a clean public API.

### What is reusable and how

| Module                        | Reusable component         | How to reuse it                                          |
|-------------------------------|----------------------------|----------------------------------------------------------|
| ``mazegen/generator.py``      | ``MazeGenerator`` class    | Import to create and generate mazes in any Python project. |
| ``mazegen/solver.py``         | ``shortest_path()``        | Pass any valid walls grid to get a BFS solution string.    |
| ``mazegen/display.py``        | ``MazeDisplay`` class      | Embed the interactive terminal viewer.    |
| ``mazegen/display.py``        | ``render_walls()``         | Render any walls grid to a plain ASCII string (no colours).|
| ``mazegen/output.py``         | ``output_file()``          | Write a maze + solution to disk in the project's hex format.|
| ``mazegen/output.py``         | ``hex_converter()``        | Convert a walls grid to hex strings line by line.          |
| ``mazegen/bonus_mazegen_animation.py`` | ``animate_dfs()`` | Show a step-by-step DFS generation animation for any walls grid. |



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

- **DFS generation animation** — option `4` in the interactive menu
  replays the recursive-backtracker algorithm step by step, showing how
  walls are carved in real time.  Implemented in
  ``mazegen/bonus_mazegen_animation.py``.

- **Dead-end braided board** — As you possibly noticed, `PERFECT=FALSE` mazes doesn't have any dead-end. This is archived thanks to the `reduce_dead_ends` function. This function can be set with a `maximun` of any `int` value, **including 0**. This, also, doesn't work with a `PERFECT=TRUE` maze. This way, the bonus part is archived.


## Resources
- https://medium.com/@icodewithben/solving-a-maze-using-depth-first-search-and-backtracking-142228603d1b
- https://github.com/cu-sanjay/Maze-Solver/
- https://www.codecademy.com/article/breadth-first-search-bfs-algorithm
- https://www.hackerearth.com/practice/algorithms/graphs/flood-fill-algorithm/tutorial/
- https://medium.com/@ja.harr91/exploring-the-pacman-maze-understanding-optimizing-breadth-first-search-depth-first-search-in-5e354b5d149b
- https://stackoverflow.com/questions/12225981/how-to-create-a-random-pacman-maze

AI was used in a responsible manner as a tutor and to assist in algorithm generation, error handling and README.md formatting.
All code has been fully reviewed and is understood by both partners.

## Team and project management

### Contribution

- **lupalomi (Luis)** — Backend algorithms: BFS solver, output file
  generation, hex conversion, and Pac-Man board mode design.
- **scamlett (Susana)** — Project setup and architecture: maze generation
  core, terminal display, DFS animation bonus, package build, README and documentation.

### Planning and how it evolved

Our initial plan was to split the work along two tracks: **generation & display** (Susana) and **algorithms & output** (Luis).

### What worked well

- **Clear separation of work** - Work and responsabilities were divided in a way that we would avoid affecting our partner's progress.
- **Git management** — we used different branches to develop our code,which kept the codebase in a working state at all times.
- **Linting from day one** — flake8 and mypy were configured in the
  Makefile from the start, catching issues early and avoiding a painful
  cleanup at the end.

### What could be improved
- **Pac-Man board mode** — we underestimated the complexity and it took     more time than expected, and involved heavy code refactoring.

### Tools used

| Tool              | Purpose                                        |
|-------------------|------------------------------------------------|
| ``venv``          | Isolated virtual environment.                  |
| ``flake8``        | Code style linting (PEP 8).                    |
| ``mypy``          | Static type checking.                          |
| ``build``         | PEP 517 package builder (wheel + sdist).       |
| ``make``          | Task runner (install, lint, build, run, clean).|
| Git / GitHub      | Version control and collaboration.             |
| VS Code           | Editor, with flake8 + mypy integrated.         |

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

Luis 06/07 - 10/07:
- BFS maze solver (mazegen/solver.py ; function shortest_path)
- Output file with hexadecimal format map, entry, exit and solution using cardinal points (N, E, S, W).

Luis 11/07:
- README update
- Minor fixes: 'main' function deleted at solver.py 

Luis 12/07:
- Show/Hide solution implementation in display

Luis 13/07:
- Merge with main branch.
- Adjustments in output.py and display.py
- Missing Entry/Exit wall borders problem solved

Susana 13/07:
- Fix README
- Different colours at show/hide solution path

Susana 15/07:
- Rewrite and comment display.py and generator.py
- BONUS = Full animation for DFS maze generation
- Polish README.md, add extra sections
- Ran multiple unit tests to catch bugs
- Fix empty line parsing in config.txt

Luis 16/07:
- PERFECT=False Pac-Man board (*With a lot of suffering*).

Luis 20/07:
- "42" pattern implemented successfully.
- Dead-end braided board implemented (BONUS PART)
- Multiple fixes due to small mazes and some edge cases.

Susana 21/07:
- Fix animation code for Perfect = True and Perfect = False with "42" pattern
- Improve code comments
- Add colour INSIDE 42 pattern.

/////// LUIS TO-DO /////
- Optional: Unit tests (pytest)
- Fix dead-ends when 42 pattern is not generated correctly.

//// SUSI TO-DO /////
- README.md final version:
  - Polish README.md

