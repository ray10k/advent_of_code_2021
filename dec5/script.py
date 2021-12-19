import pathlib
from math import sqrt, pow
from collections import namedtuple

input_path = pathlib.Path(__file__).parent / "input.txt"

Point = namedtuple("Point", "x y")


class Line:
    def __init__(self, input: str):
        input = input.strip()  # Strip the trailing newline off
        coordinates = input.split(" -> ")  # two pairs of numbers
        start_coords = coordinates[0].split(",")
        end_coords = coordinates[1].split(",")
        self.start = Point(int(start_coords[0]), int(start_coords[1]))
        self.end = Point(int(end_coords[0]), int(end_coords[1]))

    def __str__(self):
        return (
            f"Line from ({self.start.x},{self.start.y}) to ({self.end.x},{self.end.y})"
            + f"{' (orth)' if self.is_orthogonal() else ''}{' (diag)' if self.is_diagonal() else ''}"
        )

    def is_orthogonal(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    def is_diagonal(self):
        delta_h = abs(self.end.x - self.start.x)
        delta_v = abs(self.end.y - self.start.y)
        return delta_h == delta_v

    def length(self):
        delta_h = abs(self.end.x - self.start.x)
        delta_v = abs(self.end.y - self.start.y)
        return sqrt(delta_h ** 2 + delta_v ** 2)

    def __iter__(self):
        return LineIterator(self)


class LineIterator:
    def __init__(self, parent: Line):
        self.parent = parent
        self.n = 0
        self.v_delta = parent.end.y - parent.start.y
        self.h_delta = parent.end.x - parent.start.x
        self.steps = max(abs(self.v_delta), abs(self.h_delta))

        self.v_delta /= self.steps
        self.h_delta /= self.steps

    def __next__(self):
        if self.n > self.steps:
            raise StopIteration
        next_x = self.parent.start.x + (self.h_delta * self.n)
        next_y = self.parent.start.y + (self.v_delta * self.n)
        self.n += 1
        return Point(int(next_x), int(next_y))


print("first star:")
all_lines = []
ort_lines = []
dia_lines = []
with open(input_path, "r") as source:
    for line in source:
        p = Line(line)
        all_lines.append(p)
        if p.is_orthogonal():
            ort_lines.append(p)
        if p.is_diagonal():
            dia_lines.append(p)

grid = [[0] * 1000 for _ in range(1000)]
for line in ort_lines:
    for point in line:
        grid[point.x][point.y] += 1

collisions = 0
for line in grid:
    collisions += sum(1 if x > 1 else 0 for x in line)

print(f"Among {len(ort_lines)} orthogonal lines, there were {collisions} collisions.")

print("second star:")
# Easy from here on out; Just need to overlay the diagonals.
for line in dia_lines:
    for point in line:
        grid[point.x][point.y] += 1

collisions = 0
for line in grid:
    collisions += sum(1 if x > 1 else 0 for x in line)

print(
    f"Adding in the {len(dia_lines)} diagonal lines, there are now {collisions} collisions."
)
