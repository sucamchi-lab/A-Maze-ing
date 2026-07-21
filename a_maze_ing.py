#!/usr/bin/env python3
"""A-Maze-ing — Maze generator with terminal visualization.
Reads and parses config file and launches an interactive terminal
display of the generated maze.

Usage:
    python3 a_maze_ing.py config.txt
"""

import sys
from typing import Dict

from mazegen.generator import MazeGenerator
from mazegen.display import MazeDisplay
from mazegen import output_file, shortest_path


def parse_config(path: str) -> Dict[str, str]:
    """Parse a KEY=VALUE configuration file.

    Each line must contain exactly one '=' character.

    path: Path to the configuration file.

    Returns:
        A dictionary mapping keys (uppercased) to values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line has invalid syntax.
    """
    config: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line_number, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(
                    f"{path}:{line_number}: invalid line (missing '='): "
                    f"'{raw.rstrip()}'"
                )
            key, value = line.split("=", 1)
            config[key.strip().upper()] = value.strip()
    return config


def _parse_coords(raw: str) -> tuple[int, int]:
    """Parse a comma-separated coordinate pair."""
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid coordinates '{raw}': expected 'x,y'"
        )
    return (int(parts[0].strip()), int(parts[1].strip()))


def main() -> None:
    """Entry point: parse config, generate maze, launch display."""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config.txt>",
              file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        cfg = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: file not found: '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate required keys
    required = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                "OUTPUT_FILE", "PERFECT"}
    missing = required - set(cfg.keys())
    if missing:
        print(
            f"Error: missing required config keys: "
            f"{', '.join(sorted(missing))}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        width = int(cfg["WIDTH"])
        height = int(cfg["HEIGHT"])
        entry = _parse_coords(cfg["ENTRY"])
        exit_coords = _parse_coords(cfg["EXIT"])
    except ValueError as e:
        print(f"Error: invalid config value — {e}", file=sys.stderr)
        sys.exit(1)

    perfect = cfg["PERFECT"].upper() == "TRUE"

    try:
        generator = MazeGenerator(
            width=width,
            height=height,
            entry=entry,
            exit=exit_coords,
            seed=None,
            perfect=perfect,
        )
        generator.generate()

        walls = generator.get_walls()
        path = shortest_path(walls, entry, exit_coords)
        output_file(cfg["OUTPUT_FILE"], walls, entry, exit_coords, path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    display = MazeDisplay(generator, cfg["OUTPUT_FILE"])
    display.run()


if __name__ == "__main__":
    main()
