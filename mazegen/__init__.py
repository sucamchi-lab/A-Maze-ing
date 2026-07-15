"""Mazegen package
Export the necessary classes and functions to
generate, display, and solve mazes.
Used in a-maze-ing.py script.
"""

from mazegen.generator import MazeGenerator
from mazegen.display import MazeDisplay
from .solver import shortest_path
from .output import output_file

__all__ = ["MazeGenerator", "MazeDisplay", "shortest_path", "output_file"]
