from typing import Set, Tuple


PATTERN_42: Tuple[str, ...] = (
    "10001110",
    "10000010",
    "11101110",
    "00101000",
    "00101110",
)


def get_pattern(
    maze_width: int,
    maze_height: int,
) -> Set[Tuple[int, int]]:
    """Return tiles occupied by the fixed 42 pattern."""
    pattern_height = len(PATTERN_42)
    pattern_width = len(PATTERN_42[0])

    if maze_width < pattern_width or maze_height < pattern_height:
        return set()
    elif maze_width <= 8 or maze_height <= 6:
        return set()

    start_x = (maze_width - pattern_width) // 2
    start_y = (maze_height - pattern_height) // 2

    if start_x + pattern_width < maze_width:
        start_x += 1

    cells: Set[Tuple[int, int]] = set()

    for pattern_y, row in enumerate(PATTERN_42):
        for pattern_x, value in enumerate(row):
            if value == "1":
                cells.add((start_x + pattern_x, start_y + pattern_y))
    return cells
