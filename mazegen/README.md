## Reusable ``mazegen`` package

The ``mazegen/`` directory is a **self-contained, pip-installable Python
package** that can be imported and reused in a future project.  It
exposes the ``MazeGenerator`` class through a clean public API.


### Building the distributable paackage

The package is built with the standard ``build`` tool, producing a
``mazegen-1.0.0-py3-none-any.whl`` at the **root** of the
repository (the source archive ``.tar.gz`` stays in ``dist/``):

```bash
# 1. Create a virtualenv and install build dependencies
make install

# 2. Build the wheel + sdist, copy .whl to repo root
make build
```

``make build`` runs ``python -m build`` and then copies the ``.whl``
to the project root so it is available as a single distributable file
alongside the sources.

### Installing in another project

Once the .whl file is built, any project can install it with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

#### Instantiation & basic usage

```python
from mazegen import MazeGenerator

# Create a 20×10 perfect maze with random seed
gen = MazeGenerator(width=20, height=10)
gen.generate()                          # carve the passages

# Access the generated structure
walls = gen.get_walls()                 # 2D list of 4-bit wall bitmasks
w, h = gen.get_dimensions()             # (20, 10)
entry = gen.get_entry()                 # (0, 0) by default
exit_cell = gen.get_exit()              # (19, 9) e.g. bottom-right
```

#### Custom parameters

All constructor arguments are optional except ``width`` and ``height``:

| Parameter  | Type             | Default     | Description                                          |
|------------|------------------|-------------|------------------------------------------------------|
| ``width``  | ``int``          | *required*  | Cells horizontally (≥ 2).                            |
| ``height`` | ``int``          | *required*  | Cells vertically (≥ 2).                              |
| ``entry``  | ``(int, int)``   | ``(0, 0)``  | Coordinates of the entry cell.                       |
| ``exit``   | ``(int, int)``   | ``(0, 0)``  | Coordinates of the exit cell.                        |
| ``seed``   | ``int | None``   | ``None``    | Random seed for reproducible generation.             |
| ``perfect``| ``bool``         | ``True``    | ``True`` = perfect maze; ``False`` = Pac-Man board.  |

```python
# Reproducible maze with custom entry/exit
gen = MazeGenerator(
    width=30,
    height=15,
    entry=(0, 0),
    exit=(29, 14),
    seed=None,
    perfect=True,
)
gen.generate()
```


#### Accessing the maze structure

The internal representation is a **2D grid of 4-bit wall bitmasks**,
where each cell stores which walls are *closed* (present):

| Bit | Value | Wall  |
|-----|-------|-------|
| 0   | 1     | North |
| 1   | 2     | East  |
| 2   | 4     | South |
| 3   | 8     | West  |

A bit set to ``1`` means the wall is **closed**.  A cell with all four
walls closed has value ``0xF`` (15); a fully open cell has value ``0``.

```python
walls = gen.get_walls()         
```

### Complete usage example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=15, height=10, entry=(0, 0), exit=(14, 9), seed=42)
gen.generate()

print(f"Maze: {gen.get_dimensions()}")
print(f"Entry: {gen.get_entry()}, Exit: {gen.get_exit()}")

walls = gen.get_walls()
print(f"Cell (0,0) walls: {walls[0][0]:04b}")
```