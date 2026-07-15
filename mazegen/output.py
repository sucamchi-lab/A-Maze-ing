from typing import List, Tuple


def hex_converter(walls: List[List[int]]) -> List[str]:
    """
    Turns the map lines into hexadecimal.
    """
    lines: List[str] = []

    for row in walls:
        line = ""
        for tile in row:
            line += format(tile, "x")
        lines.append(line)
    return lines


def output_file(
    filename: str,
    walls: List[List[int]],
    entry: Tuple[int, int],
    map_exit: Tuple[int, int],
    path: str
) -> None:
    """
    Uses 'hex_converter' function to turn the map, line by line, to hexadecimal
    and saving the result of each line in the 'filename' variable
    """
    lines = hex_converter(walls)
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
        file.write("\n")
        file.write(f"{entry[0]}, {entry[1]}\n")
        file.write(f"{map_exit[0]}, {map_exit[1]}\n")
        file.write(path + "\n")
