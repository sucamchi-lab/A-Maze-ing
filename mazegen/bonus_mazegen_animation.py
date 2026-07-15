"""DFS maze generation animation.
Renders the recursive backtracker algorithm step-by-step
"""
import sys
import time
import random
from typing import List, Tuple


_CLEAR = "\033[2J\033[H"

# Direction constants: (dx, dy, my_wall_bit, their_wall_bit)
_DIRECTIONS: List[Tuple[int, int, int, int]] = [
    (0, -1, 1, 4),   # North
    (1, 0, 2, 8),    # East
    (0, 1, 4, 1),    # South
    (-1, 0, 8, 2),   # West
]


def animate_dfs(
    walls: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int] = (0, 0),
    exit_cell: Tuple[int, int] = (0, 0),
    seed: int | None = None,
    delay: float = 0.02,
    color: str = "",
) -> None:
    """Animate the DFS maze generation algorithm in the terminal.

    Args:
        walls: 2D grid of wall bitmasks (modified in-place).
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates ``(x, y)``.
        exit_cell: Exit coordinates ``(x, y)``.
        seed: Random seed (``None`` for random).
        delay: Seconds to pause between frames.
        color: ANSI color code to wrap each frame.
    """
    from mazegen.display import render_walls
    reset = "\033[0m"
    rng = random.Random(seed)

    visited: List[List[bool]] = [
        [False for _ in range(width)] for _ in range(height)
    ]

    stack: List[Tuple[int, int]] = [(0, 0)]
    visited[0][0] = True

    def redraw() -> None:
        """Clear screen and render the current maze state."""
        sys.stdout.write(_CLEAR)
        frame = render_walls(walls, width, height, entry, exit_cell)
        sys.stdout.write(f"{color}{frame}{reset}\n")
        sys.stdout.flush()
        time.sleep(delay)

    redraw()

    while stack:
        cx, cy = stack[-1]
        neighbors: List[Tuple[int, int, int]] = []
        for dx, dy, my_wall, _ in _DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
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
