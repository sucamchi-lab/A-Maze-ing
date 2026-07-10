"""Mazegen package

Provides the MazeGenerator class for creating mazes and
MazeDisplay for terminal ASCII visualization.

Used in the a_maze_ing.py script.
"""

from mazegen.generator import MazeGenerator
from mazegen.display import MazeDisplay
from .solver import shortest_path
from .output import output_file

__all__ = ["MazeGenerator", "MazeDisplay", "shortest_path", "output_file"]
