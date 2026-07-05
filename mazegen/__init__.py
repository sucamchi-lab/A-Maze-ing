"""Mazegen package

Provides the MazeGenerator class for creating mazes and
MazeDisplay for terminal ASCII visualization.

Used in the a_maze_ing.py script.
"""

from mazegen.generator import MazeGenerator
from mazegen.display import MazeDisplay

__all__ = ["MazeGenerator", "MazeDisplay"]
