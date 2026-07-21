"""Terminal ASCII maze display with interactive menu.

Provides the MazeDisplay class that renders a maze to the
terminal using ASCII characters and ANSI color codes.
"""

import sys
from typing import List, Set, Tuple

from mazegen.generator import MazeGenerator
from mazegen.solver import shortest_path
from mazegen.output import output_file
from mazegen.bonus_mazegen_animation import animate_dfs

# ANSI escape codes

_CLEAR = "\033[2J\033[H"
_RESET = "\033[0m"

# Rotating color palette for walls
_COLORS: List[str] = [
    "\033[1;37m",   # bold white
    "\033[1;31m",   # bold red
    "\033[1;32m",   # bold green
    "\033[1;33m",   # bold yellow
    "\033[1;34m",   # bold blue
    "\033[1;35m",   # bold magenta
    "\033[1;36m",   # bold cyan
]


# Cell rendering dimensions
_CELL_W = 3  # interior width in characters
_CELL_H = 1  # interior height in characters


def render_walls(
    walls: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path_cells: Set[Tuple[int, int]] | None = None,
    pattern_cells: Set[Tuple[int, int]] | None = None,
) -> str:
    """Render a maze walls grid as a plain ASCII string (no colors).

    Args:
        walls: 2D grid of 4-bit wall bitmasks.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry coordinates ``(x, y)``.
        exit_cell: Exit coordinates ``(x, y)``.
        path_cells: Optional cells to highlight with ``●``.
        pattern_cells: Fills in the 42 pattern cells with ``▓``

    Returns:
        Multi-line ASCII string.
    """
    cw = _CELL_W
    ch = _CELL_H

    canvas_w = (cw + 1) * width + 1
    canvas_h = (ch + 1) * height + 1

    canvas: List[List[str]] = [
        [" " for _ in range(canvas_w)] for _ in range(canvas_h)
    ]

    # Place corners
    for cy in range(0, canvas_h, ch + 1):
        for cx in range(0, canvas_w, cw + 1):
            canvas[cy][cx] = "█"
    # Fill in walls and interiors
    for y in range(height):
        for x in range(width):
            cell = walls[y][x]
            tx = x * (cw + 1)
            ty = y * (ch + 1)

            # North wall
            if cell & 1:
                for i in range(1, cw + 1):
                    canvas[ty][tx + i] = "█"
            else:
                for i in range(1, cw + 1):
                    canvas[ty][tx + i] = " "

            # West wall
            if cell & 8:
                for i in range(1, ch + 1):
                    canvas[ty + i][tx] = "█"
            else:
                for i in range(1, ch + 1):
                    canvas[ty + i][tx] = " "

            # Special markers: entry, exit, path, and pattern fill
            interior = "   "
            if (x, y) == entry:
                interior = " E "
            elif (x, y) == exit_cell:
                interior = " X "
            elif path_cells and (x, y) in path_cells:
                interior = " ● "
            elif pattern_cells and (x, y) in pattern_cells:
                interior = "▓▓▓"
            # Fill in the interior of the cell
            for i, ch_char in enumerate(interior):
                canvas[ty + 1][tx + 1 + i] = ch_char

    # South border
    for x in range(width):
        cell = walls[height - 1][x]
        tx = x * (cw + 1)
        ty = (height - 1) * (ch + 1)
        if cell & 4:
            for i in range(1, cw + 1):
                canvas[ty + ch + 1][tx + i] = "█"
        else:
            for i in range(1, cw + 1):
                canvas[ty + ch + 1][tx + i] = " "

    # East border
    for y in range(height):
        cell = walls[y][width - 1]
        tx = (width - 1) * (cw + 1)
        ty = y * (ch + 1)
        if cell & 2:
            for i in range(1, ch + 1):
                canvas[ty + i][tx + cw + 1] = "█"
        else:
            for i in range(1, ch + 1):
                canvas[ty + i][tx + cw + 1] = " "

    return "\n".join("".join(row) for row in canvas)


class MazeDisplay:
    """Renders a :class:`MazeGenerator` maze to the terminal.

    Supports an interactive menu loop with five actions:
    1. Re-generate a new maze
    2. Show/hide the shortest path
    3. Rotate wall colors
    4. Show DFS animation
    5. Quit

    Attributes:
        generator: The :class:`MazeGenerator` instance to display.
        color_index: Index into the color palette
        show_path: Highlight the solution path
    """

    def __init__(self, generator: MazeGenerator,
                 output_name: str = "output_maze.txt") -> None:
        """Initialize the display with a maze generator."""
        self.generator: MazeGenerator = generator
        self.color_index: int = 0
        self.output_name = output_name
        self.show_path: bool = False
        self.path: str = shortest_path(
            self.generator.get_walls(),
            self.generator.get_entry(),
            self.generator.get_exit(),
        )
        self.path_cells: Set[Tuple[int, int]] = self.get_path_cells(self.path)

    def regen(self) -> None:
        """Re-generate the maze with a new random seed."""
        self.generator.seed = None
        self.generator.generate()
        self.path = shortest_path(
            self.generator.get_walls(),
            self.generator.get_entry(),
            self.generator.get_exit()
        )
        self.path_cells = self.get_path_cells(self.path)
        output_file(
            self.output_name,
            self.generator.get_walls(),
            self.generator.get_entry(),
            self.generator.get_exit(),
            self.path
        )

    def rotate_color(self) -> None:
        """Advance to the next wall color in the palette."""
        self.color_index = (self.color_index + 1) % len(_COLORS)

    def get_path_cells(self, path: str) -> Set[Tuple[int, int]]:
        """Convert a path string into a set of (x, y) coordinates. """
        x, y = self.generator.get_entry()
        path_cells: Set[Tuple[int, int]] = {(x, y)}

        for movement in path:
            if movement == "N":
                y -= 1
            elif movement == "E":
                x += 1
            elif movement == "S":
                y += 1
            elif movement == "W":
                x -= 1
            path_cells.add((x, y))
        return path_cells

    def toggle_path(self) -> None:
        """Toggle the solution path overlay."""
        self.show_path = not self.show_path

    def animate_dfs(self) -> None:
        """Run the DFS maze generation animation in the terminal."""
        # Reset walls so the animation starts from a fully closed maze.
        self.generator._walls = [
            [0xF for _ in range(self.generator.width)]
            for _ in range(self.generator.height)
        ]
        animate_dfs(
            self.generator,
            color=_COLORS[self.color_index],
        )
        # Recalculate path for the maze the animation just built
        self.path = shortest_path(
            self.generator.get_walls(),
            self.generator.get_entry(),
            self.generator.get_exit(),
        )
        self.path_cells = self.get_path_cells(self.path)
        output_file(
            self.output_name,
            self.generator.get_walls(),
            self.generator.get_entry(),
            self.generator.get_exit(),
            self.path,
        )

    def render(self) -> str:
        """Build the ASCII representation of the current maze.
        Returns a multi-line string ready to print to the terminal.
        """
        path_cells = self.path_cells if self.show_path else None
        result = render_walls(
            self.generator.get_walls(),
            self.generator.width,
            self.generator.height,
            self.generator.get_entry(),
            self.generator.get_exit(),
            path_cells,
            self.generator.get_pattern(),
        )

        # Apply ANSI colors
        wall_color = _COLORS[self.color_index]
        path_color = _COLORS[(self.color_index + 1) % len(_COLORS)]
        lines = []
        for line in result.split("\n"):
            if self.show_path:
                line = line.replace("●", f"{path_color}●{wall_color}")
            lines.append(f"{wall_color}{line}{_RESET}")
        return "\n".join(lines)

    def run(self) -> None:
        """Start the interactive terminal menu loop."""
        while True:
            self._clear()
            print(self.render())
            print()
            self._print_menu()

            try:
                choice = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if choice == "1":
                self.regen()
            elif choice == "2":
                self.toggle_path()
            elif choice == "3":
                self.rotate_color()
            elif choice == "4":
                self.animate_dfs()
            elif choice == "5":
                break
            else:
                print(f"\nUnknown option: '{choice}'")
                input("Press Enter to continue...")

        self._clear()

    @staticmethod
    def _clear() -> None:
        """Clear the terminal screen."""
        sys.stdout.write(_CLEAR)
        sys.stdout.flush()

    @staticmethod
    def _print_menu() -> None:
        """Print the interactive menu."""
        print("─" * 40)
        print("  1. Re-generate a new maze")
        print("  2. Show / Hide path from entry to exit")
        print("  3. Rotate maze colors")
        print("  4. Show DFS animation")
        print("  5. Quit")
        print("─" * 40)
