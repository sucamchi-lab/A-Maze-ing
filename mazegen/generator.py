"""Maze generator using recursive backtracker (DFS).

This module provides the MazeGenerator class that creates
mazes in two modes:

- **Perfect** (``PERFECT=True``): exactly one path between any two
  cells — produced by a standard recursive backtracker.
- **Playable / Pac-Man board** (``PERFECT=False``): a maze with
  loops, open corners and centre, and minimal dead-ends, suitable
  for a Pac-Man-like game.  *(Not yet implemented.)*
"""

import random
from typing import List, Tuple


class MazeGenerator:
    """Generates a maze using the recursive backtracker algorithm.

    The maze is represented internally as a 2D grid where each cell
    stores a bitmask of its **closed** walls:

    - Bit 0 (1): North wall
    - Bit 1 (2): East wall
    - Bit 2 (4): South wall
    - Bit 3 (8): West wall

    A bit set to 1 means the wall is **closed** (present).
    This format matches the hexadecimal output specified in the subject.

    Two generation modes are supported:

    - **Perfect** (``True``): recursive backtracker produces exactly
      one path between any two cells.
    - **Playable** (``False``): Pac-Man-style board with loops, open
      corners/centre, and minimal dead-ends.  *(Not yet implemented.)*

    Attributes:
        width: Number of cells horizontally.
        height: Number of cells vertically.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        seed: Random seed for reproducible generation, or ``None``.
        perfect: Whether to generate a perfect maze (default ``True``).
    """

    # Direction constants: (dx, dy, wall_bit, opposite_wall_bit)
    _DIRECTIONS: List[Tuple[int, int, int, int]] = [
        (0, -1, 1, 4),   # North: my north wall, neighbor's south wall
        (1, 0, 2, 8),    # East:  my east wall,  neighbor's west wall
        (0, 1, 4, 1),    # South: my south wall, neighbor's north wall
        (-1, 0, 8, 2),   # West:  my west wall,  neighbor's east wall
    ]

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = (0, 0),
        seed: int | None = None,
        perfect: bool = True,
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Number of cells horizontally (must be >= 2).
            height: Number of cells vertically (must be >= 2).
            entry: (x, y) coordinates of the entry cell.
            exit: (x, y) coordinates of the exit cell.
            seed: Random seed for reproducible generation.
                Pass ``None`` for a random (non-reproducible) maze.
            perfect: If ``True`` (default), generate a perfect maze
                (exactly one path between any two cells).  If
                ``False``, generate a Pac-Man-style playable board
                with loops.  *(Non-perfect mode is not yet
                implemented.)*

        Raises:
            ValueError: If dimensions are too small or entry/exit
                are out of bounds.
        """
        if width < 2 or height < 2:
            raise ValueError(
                f"Maze must be at least 2x2, got {width}x{height}"
            )
        ex, ey = entry
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(
                f"Entry {entry} is outside maze bounds "
                f"(0..{width - 1}, 0..{height - 1})"
            )
        xx, xy = exit
        if not (0 <= xx < width and 0 <= xy < height):
            raise ValueError(
                f"Exit {exit} is outside maze bounds "
                f"(0..{width - 1}, 0..{height - 1})"
            )
        if entry == exit:
            raise ValueError("Entry and exit must be different cells")

        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.seed: int | None = seed
        self.perfect: bool = perfect

        # walls[y][x] — bitmask of closed walls (0–15)
        self._walls: List[List[int]] = []

    def generate(self) -> None:
        """Run the maze generation algorithm.

        Clears any previously generated maze and creates a new one.
        All walls start closed; the recursive backtracker carves
        passages by removing walls between visited cells.
        """
        w = self.width
        h = self.height

        # Start with all walls closed (0xF = 1111 binary)
        self._walls = [[0xF for _ in range(w)] for _ in range(h)]

        rng = random.Random(self.seed)
        visited: List[List[bool]] = [
            [False for _ in range(w)] for _ in range(h)
        ]

        # Use an explicit stack instead of recursion to avoid
        # hitting Python's recursion limit on large mazes.
        stack: List[Tuple[int, int]] = [(0, 0)]
        visited[0][0] = True

        while stack:
            cx, cy = stack[-1]
            # Gather unvisited neighbors
            neighbors: List[Tuple[int, int, int]] = []
            for dx, dy, my_wall, their_wall in self._DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                    neighbors.append((nx, ny, my_wall))

            if neighbors:
                nx, ny, my_wall = rng.choice(neighbors)
                # Find the direction to get the opposite wall bit
                for dx, dy, mw, tw in self._DIRECTIONS:
                    if (nx - cx, ny - cy) == (dx, dy):
                        # Remove walls between current and neighbor
                        self.open_wall(cx, cy, nx, ny, mw, tw)
                        break
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()
            if not self.perfect:
                self.pac_man_maze(rng)

    def get_walls(self) -> List[List[int]]:
        """Return the maze wall grid.

        Returns:
            A 2D list ``walls[y][x]`` where each value is a 4-bit
            bitmask of closed walls (North=1, East=2, South=4, West=8).
        """
        return [row[:] for row in self._walls]

    def get_dimensions(self) -> Tuple[int, int]:
        """Return the maze dimensions as ``(width, height)``."""
        return (self.width, self.height)

    def get_entry(self) -> Tuple[int, int]:
        """Return the entry coordinates as ``(x, y)``."""
        return self.entry

    def get_exit(self) -> Tuple[int, int]:
        """Return the exit coordinates as ``(x, y)``."""
        return self.exit

    def open_wall(self, x: int, y: int, nx: int, ny: int, my_wall: int,
                  their_wall: int) -> None:
        """Remove walls between current and neighbor"""
        self._walls[y][x] &= ~my_wall
        self._walls[ny][nx] &= ~their_wall

    def closed_neighbours(self, x: int, y: int
                          ) -> List[Tuple[int, int, int, int]]:
        neighbours: List[Tuple[int, int, int, int]] = []
        for dx, dy, my_wall, their_wall in self._DIRECTIONS:
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if self._walls[y][x] & my_wall:
                neighbours.append((nx, ny, my_wall, their_wall))
        return neighbours

    def passage_count(self, x: int, y: int) -> int:
        """Return the amount of paths to one cell."""
        count = 0

        for dx, dy, my_wall, _ in self._DIRECTIONS:
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if not self._walls[y][x] & my_wall:
                count += 1
        return count

    def open_key_cells(self, rng: random.Random) -> None:
        """Ensure corners and centre have, at least, two open passages."""
        key_cells: List[Tuple[int, int]] = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
            (self.width // 2, self.height // 2),
        ]
        for x, y in key_cells:
            while self.passage_count(x, y) < 2:
                candidates = self.closed_neighbours(x, y)
                if not candidates:
                    break
                nx, ny, my_wall, their_wall = rng.choice(candidates)
                self.open_wall(x, y, nx, ny, my_wall, their_wall)

    def choose_dead_end_connection(self, rng: random.Random,
                                   candidates: List[Tuple[int, int, int, int]],
                                   dead_ends: List[Tuple[int, int]],
                                   ) -> Tuple[int, int, int, int]:
        """Literally, choose a closed wall"""
        dead_end_set = set(dead_ends)
        dead_end_candidates = [
            candidate
            for candidate in candidates
            if (candidate[0], candidate[1]) in dead_end_set
        ]
        if dead_end_candidates:
            return rng.choice(dead_end_candidates)
        return rng.choice(candidates)

    def reduce_dead_ends(self, rng: random.Random, maxi: int = 2) -> None:
        """Open internal walls until only a few dead-ends remain."""
        dead_ends = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.passage_count(x, y) == 1
        ]
        while len(dead_ends) > maxi:
            rng.shuffle(dead_ends)
            x, y = dead_ends[0]
            candidates = self.closed_neighbours(x, y)
            selected = self.choose_dead_end_connection(rng, candidates,
                                                       dead_ends)
            nx, ny, my_wall, their_wall = selected
            self.open_wall(x, y, nx, ny, my_wall, their_wall)
            dead_ends = [
                (x, y)
                for y in range(self.height)
                for x in range(self.width)
                if self.passage_count(x, y) == 1
            ]

    def pac_man_maze(self, rng: random.Random) -> None:
        """Transform a perfect maze into a pac-man maze"""
        self.open_key_cells(rng)
        self.reduce_dead_ends(rng, maxi=2)
