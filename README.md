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
5. Generates a solution using a BFS algorithm
6. Generates a output file that includes a hexadecimal version of the map, the entry ubication, the exit ubication and the shortest path to exit in cardinal points (North, N; East, E; South, S; West, W)

*(Output file writing to the hexadecimal format is not yet implemented.)*

## Algorithms used

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


### Breadth-First Search (BFS) - Shortest path to exit
The function `shortest_path` defined in **solver.py** uses a BFS algorithm to find the first path to the exit, which is also the shortest path because all tiles have the same **movement cost**. In this function:

- `Queue`: Represent the tiles pending to visit.
- `Visited`: The tiles that has been already visited.
- `Parent`: The tile used to reach the "key" value with the movement direction.

#### Why not use DFS here?
`DFS always tries to go as deep as posible` ('South' direction, ↓
) which is perfect to generate laberithms but almost never guarantee that the solution path is also the shortest path to the exit.

This is not the case of the BFS algorithm. BFS algorithm is pretty similar to `flood fill` algorithm. Both algorithms, `BFS and Flood Fill, roams all the tiles until find a condition to stop`. However the main difference is that BFS algorithm also save the `Parent` path to generate a coherent solution.

## Bonus
*Not implemented yet*


## Resources
- https://medium.com/@icodewithben/solving-a-maze-using-depth-first-search-and-backtracking-142228603d1b
- https://github.com/cu-sanjay/Maze-Solver/
- https://www.codecademy.com/article/breadth-first-search-bfs-algorithm
- https://www.hackerearth.com/practice/algorithms/graphs/flood-fill-algorithm/tutorial/

## Contributions
- `lupalomi`: Backend algorithms, output file, pathfinding, "42" pattern,
  Pac-Man board mode.
- `scamlett`: Project setup, maze generation core, terminal display,
  README & documentation, package build,visual polish.

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
  - shortest_path function — Implements BFS algorithm to find the shortest path to exit.
  - output_file function — Generates a .txt file version that includes an hexadecimal version of the map, the entry ubication, the exit ubication and the solution provided by 'shortest_path' function
- a_maze_ing.py — config file parser, CLI argument handling, error messages
- README.md — description, instructions, execution flow, algorithms,
  to-do list
- LICENSE.md


Luis 06/07 - 10/07:
- BFS maze solver (mazegen/solver.py ; function shortest_path)
- Output file with hexadecimal format map, entry, exit and solution using cardinal points (N, E, S, W).

Luis 11/07:
- README update
- Minor fixes: 'main' function deleted at solver.py 


/////// LUIS TO-DO /////
- Implement new output_file at maze.regen()
- Implement "show/hide shortest path"
- "42" pattern
- PERFECT=False Pac-Man board (v2.2 requirements)
- Optional: Unit tests (pytest)
- Bonus: extra algorithms or zero dead-end braided board (v2.2 bonus)

//// SUSI TO-DO /////
- Package build (.whl) - Chapter VI and VII
- Bonus: extra graphics / animations
- README.md final version:
  - Config file format documentation
  - Why the recursive backtracker was chosen
  - Reusable module docs (instantiation, parameters, accessing structure)
  - Team roles, planning evolution, what worked / could improve
  - Resources section
