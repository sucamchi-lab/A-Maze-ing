"""Terminal ASCII maze display with interactive menu.

Provides the MazeDisplay class that renders a maze to the
terminal using box-drawing characters and ANSI color codes.
"""

import sys
from typing import List

from mazegen.generator import MazeGenerator

# ── ANSI escape codes ──────────────────────────────────────────────

_CLEAR = "\033[2J\033[H"
_RESET = "\033[0m"

# Rotating color palette for walls (foreground colors, bold)
_COLORS: List[str] = [
    "\033[1;37m",   # bold white
    "\033[1;31m",   # bold red
    "\033[1;32m",   # bold green
    "\033[1;33m",   # bold yellow
    "\033[1;34m",   # bold blue
    "\033[1;35m",   # bold magenta
    "\033[1;36m",   # bold cyan
]


class MazeDisplay:
    """Renders a :class:`MazeGenerator` maze to the terminal.

    Supports an interactive menu loop with four actions:
    1. Re-generate a new maze
    2. Show/hide the shortest path (placeholder — pathfinding not yet
       implemented)
    3. Rotate wall colors
    4. Quit

    Attributes:
        generator: The :class:`MazeGenerator` instance to display.
        color_index: Index into the color palette for wall rendering.
        show_path: Whether to highlight the solution path (currently
            a no-op).
    """

    # Each maze cell is rendered as 3 chars wide × 1 char tall
    # (the interior is 3 spaces).  Corners are '+' and walls are
    # '---' (horizontal) or '|' (vertical).
    _CELL_W = 3  # interior width in characters
    _CELL_H = 1  # interior height in characters

    def __init__(self, generator: MazeGenerator) -> None:
        """Initialize the display with a maze generator.

        Args:
            generator: A configured (but not necessarily generated)
                :class:`MazeGenerator`.
        """
        self.generator: MazeGenerator = generator
        self.color_index: int = 0
        self.show_path: bool = False

    # ── Public helpers ─────────────────────────────────────────

    def regen(self) -> None:
        """Re-generate the maze with a new random seed."""
        self.generator.seed = None
        self.generator.generate()

    def rotate_color(self) -> None:
        """Advance to the next wall color in the palette."""
        self.color_index = (self.color_index + 1) % len(_COLORS)

    def toggle_path(self) -> None:
        """Toggle the solution path overlay.
        Pathfinding is not yet implemented
        TODO: implement pathfinding and overlay rendering.
        """
        self.show_path = not self.show_path

    # ── Rendering ──────────────────────────────────────────────

    def render(self) -> str:
        """Build the ASCII representation of the current maze.

        Returns:
            A multi-line string ready to print to the terminal.
        """
        w = self.generator.width
        h = self.generator.height
        walls = self.generator.get_walls()
        entry = self.generator.get_entry()
        exit_cell = self.generator.get_exit()

        cw = self._CELL_W   # 3
        ch = self._CELL_H   # 1

        # Canvas size: (2*h + 1) rows, (2*cw*w + 1) columns …
        # horizontal walls span cw chars between corners,
        # so the full width is  cw*w + (w+1)  for corners.
        canvas_w = (cw + 1) * w + 1
        canvas_h = (ch + 1) * h + 1

        # Start with all spaces
        canvas: List[List[str]] = [
            [" " for _ in range(canvas_w)] for _ in range(canvas_h)
        ]

        # Place corners (every (cw+1) columns, every (ch+1) rows)
        for cy in range(0, canvas_h, ch + 1):
            for cx in range(0, canvas_w, cw + 1):
                canvas[cy][cx] = "+"

        # For each cell, draw its north and west walls
        # (south and east are drawn by neighboring cells)
        for y in range(h):
            for x in range(w):
                cell = walls[y][x]
                # top-left corner of this cell in canvas coords
                tx = x * (cw + 1)
                ty = y * (ch + 1)

                # North wall
                if cell & 1:   # north closed
                    for i in range(1, cw + 1):
                        canvas[ty][tx + i] = "-"
                else:
                    for i in range(1, cw + 1):
                        canvas[ty][tx + i] = " "

                # West wall
                if cell & 8:   # west closed
                    for i in range(1, ch + 1):
                        canvas[ty + i][tx] = "|"
                else:
                    for i in range(1, ch + 1):
                        canvas[ty + i][tx] = " "

                # Cell interior: mark entry / exit
                interior = "   "
                if (x, y) == entry:
                    interior = " E "
                elif (x, y) == exit_cell:
                    interior = " X "

                for i, ch_char in enumerate(interior):
                    canvas[ty + 1][tx + 1 + i] = ch_char

        # Draw remaining south border (bottom row of cells)
        for x in range(w):
            cell = walls[h - 1][x]
            tx = x * (cw + 1)
            ty = (h - 1) * (ch + 1)
            if cell & 4:   # south closed
                for i in range(1, cw + 1):
                    canvas[ty + ch + 1][tx + i] = "-"
            else:
                for i in range(1, cw + 1):
                    canvas[ty + ch + 1][tx + i] = " "

        # Draw remaining east border (rightmost column of cells)
        for y in range(h):
            cell = walls[y][w - 1]
            tx = (w - 1) * (cw + 1)
            ty = y * (ch + 1)
            if cell & 2:   # east closed
                for i in range(1, ch + 1):
                    canvas[ty + i][tx + cw + 1] = "|"
            else:
                for i in range(1, ch + 1):
                    canvas[ty + i][tx + cw + 1] = " "

        # Apply color
        color = _COLORS[self.color_index]
        lines = []
        for row in canvas:
            line = "".join(row)
            lines.append(f"{color}{line}{_RESET}")
        return "\n".join(lines)

    # ── Interactive loop ───────────────────────────────────────

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
                if self.show_path:
                    print(
                        "\n(path display not yet implemented — "
                        "coming soon!)"
                    )
                    input("Press Enter to continue...")
            elif choice == "3":
                self.rotate_color()
            elif choice == "4":
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
        print("  4. Quit")
        print("─" * 40)
