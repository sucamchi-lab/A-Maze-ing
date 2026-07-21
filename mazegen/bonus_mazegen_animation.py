"""
DFS maze generation animation.
Renders the recursive backtracker algorithm step-by-step.
This file reuses the maze generation logic from mazegen/generator.py,
but adds animation and respects the 42 pattern.
"""
import sys
import time
import random
from typing import List, Tuple

from mazegen.generator import MazeGenerator


_CLEAR = "\033[2J\033[H"

# Direction constants: (dx, dy, my_wall_bit, their_wall_bit)
_DIRECTIONS: List[Tuple[int, int, int, int]] = [
    (0, -1, 1, 4),   # North
    (1, 0, 2, 8),    # East
    (0, 1, 4, 1),    # South
    (-1, 0, 8, 2),   # West
]


def animate_dfs(
    generator: MazeGenerator,
    delay: float = 0.02,
    color: str = "",
) -> None:
    """Animate the active maze generation algorithm in the terminal.
    DFS carving is rendered first, then the Pac-Man post-processing
    is animated when perfect=False.
    """
    from mazegen.display import render_walls
    reset = "\033[0m"

    walls = generator._walls
    width = generator.width
    height = generator.height
    entry = generator.entry
    exit_cell = generator.exit
    rng = random.Random(generator.seed)
    pattern = set(generator._pattern)
    centre = (width // 2, height // 2)

    visited: List[List[bool]] = [
        [False for _ in range(width)] for _ in range(height)
    ]

    stack: List[Tuple[int, int]] = [entry]
    start_x, start_y = entry
    visited[start_y][start_x] = True

    def is_pattern_cell(x: int, y: int) -> bool:
        """Check if a cell is part of the 42 pattern and not the centre."""
        return (x, y) in pattern and (x, y) != centre

    def redraw() -> None:
        """Clear screen and render the current maze state."""
        sys.stdout.write(_CLEAR)
        frame = render_walls(walls, width, height, entry, exit_cell)
        sys.stdout.write(f"{color}{frame}{reset}\n")
        sys.stdout.flush()
        time.sleep(delay)

    redraw()
    # Main DFS loop for maze generation
    while stack:
        cx, cy = stack[-1]
        neighbors: List[Tuple[int, int, int]] = []
        for dx, dy, my_wall, _ in _DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < width
                and 0 <= ny < height
                and not visited[ny][nx]
                and not is_pattern_cell(nx, ny)
            ):
                neighbors.append((nx, ny, my_wall))

        if neighbors:
            nx, ny, my_wall = rng.choice(neighbors)
            for dx, dy, mw, tw in _DIRECTIONS:
                if (nx - cx, ny - cy) == (dx, dy):
                    walls[cy][cx] &= ~mw
                    walls[ny][nx] &= ~tw
                    break
            visited[ny][nx] = True
            stack.append((nx, ny))
            redraw()
        else:
            stack.pop()
    # Pac-Man post-processing if perfect=False
    if not generator.perfect:
        def open_wall(x: int, y: int, nx: int, ny: int,
                      my_wall: int, their_wall: int) -> bool:
            if is_pattern_cell(x, y) or is_pattern_cell(nx, ny):
                return False
            walls[y][x] &= ~my_wall
            walls[ny][nx] &= ~their_wall
            return True

        def passage_count(x: int, y: int) -> int:
            """Count the number of open passages for a cell."""
            count = 0
            for dx, dy, my_wall, _ in _DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if not walls[y][x] & my_wall:
                    count += 1
            return count

        def closed_neighbours(
            x: int, y: int
        ) -> List[Tuple[int, int, int, int]]:
            neighbours: List[Tuple[int, int, int, int]] = []
            """Get closed neighbouring cells that can be opened."""
            if is_pattern_cell(x, y):
                return neighbours
            for dx, dy, my_wall, their_wall in _DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if is_pattern_cell(nx, ny):
                    continue
                if walls[y][x] & my_wall:
                    neighbours.append((nx, ny, my_wall, their_wall))
            return neighbours

        def open_key_cells() -> None:
            """Open the four corners and the centre cell"""
            key_cells: List[Tuple[int, int]] = [
                (0, 0),
                (width - 1, 0),
                (0, height - 1),
                (width - 1, height - 1),
                centre,
            ]
            for x, y in key_cells:
                if is_pattern_cell(x, y):
                    continue
                while passage_count(x, y) < 2:
                    candidates = closed_neighbours(x, y)
                    if not candidates:
                        break
                    nx, ny, my_wall, their_wall = rng.choice(candidates)
                    if open_wall(x, y, nx, ny, my_wall, their_wall):
                        redraw()
                    else:
                        break

        def reduce_dead_ends(maxi: int) -> None:
            """Reduce dead ends in the maze while respecting the 42 pattern."""
            while True:
                dead_ends: List[Tuple[int, int]] = [
                    (x, y)
                    for y in range(height)
                    for x in range(width)
                    if not is_pattern_cell(x, y) and passage_count(x, y) == 1
                ]
                if len(dead_ends) <= maxi:
                    return
                rng.shuffle(dead_ends)
                changed = False
                dead_end_set = set(dead_ends)
                for x, y in dead_ends:
                    candidates = closed_neighbours(x, y)
                    if not candidates:
                        continue
                    dead_end_candidates = [
                        candidate
                        for candidate in candidates
                        if (candidate[0], candidate[1]) in dead_end_set
                    ]
                    selected = rng.choice(dead_end_candidates or candidates)
                    nx, ny, my_wall, their_wall = selected
                    if open_wall(x, y, nx, ny, my_wall, their_wall):
                        redraw()
                        changed = True
                        break
                if not changed:
                    return

        open_key_cells()
        reduce_dead_ends(maxi=0)
