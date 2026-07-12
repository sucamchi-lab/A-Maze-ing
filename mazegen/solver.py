from collections import deque
from typing import Deque, Dict, List, Tuple


DIRECTIONS = [
    ("N", 0, -1, 1),
    ("E", 1, 0, 2),
    ("S", 0, 1, 4),
    ("W", -1, 0, 8)
]


def shortest_path(
    walls: List[List[int]],
    entry: Tuple[int, int],
    map_exit: Tuple[int, int]
) -> str:
    """
    Roams the entire map searching the shortest path to the exit. When
    the exit is found, returns 'rebuild_path(parent, entry, exit)'.
    """
    height = len(walls)
    width = len(walls[0])
    queue: Deque[Tuple[int, int]] = deque([entry])
    visited: set[Tuple[int, int]] = {entry}
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

    while queue:
        x, y = queue.popleft()
        if (x, y) == map_exit:
            return rebuild_path(parent, entry, map_exit)
        for move, dx, dy, wall_bit in DIRECTIONS:
            nx = x + dx
            ny = y + dy
            # Avoids move on impossible tiles
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            # Avoids run walls through
            if walls[y][x] & wall_bit:
                continue
            # Avoid visit tiles that has been already visited
            if (nx, ny) in visited:
                continue
            # If no conditions are meet, the tile is added to the visited list,
            # the parent dictionary and the double ended queue
            visited.add((nx, ny))
            parent[(nx, ny)] = ((x, y), move)
            queue.append((nx, ny))
    raise ValueError("No valid path found from entry to exit")


def rebuild_path(
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]],
    entry: Tuple[int, int],
    map_exit: Tuple[int, int]
) -> str:
    """
    This function start at the end and recreates the solution returning
    a string that indicates, by order, the cardinal points from the begining
    to the end
    """
    current = map_exit
    path = ""

    # Literally, go back rebuilding the entire solution path and return it
    while current != entry:
        previous, move = parent[current]
        path = move + path
        current = previous
    return path
