import pathlib
from itertools import product
from PIL import Image
from numpy import asarray

input_path = pathlib.Path(__file__).parent / "input.txt"


class GridIterator:
    def __init__(self):
        self.iterator = product(range(100), range(100))

    def __iter__(self):
        return self.iterator


print("first star:")
grid = [[0] * 100 for _ in range(100)]
with open(input_path, "r") as input_file:
    for row, line in enumerate(input_file):
        for column, number in enumerate(line.strip()):
            grid[column][row] = int(number)

print(grid[0])
total_danger = 0
EDGES = {0, 99}
for row, column in GridIterator():
    left = max(0, column - 1)
    right = min(99, column + 1)
    up = max(0, row - 1)
    down = min(99, row + 1)
    middle = grid[column][row]
    greaters = 0
    if row in EDGES:
        greaters += 1
    if column in EDGES:
        greaters += 1
    if grid[column][up] > middle:
        greaters += 1
    if grid[column][down] > middle:
        greaters += 1
    if grid[left][row] > middle:
        greaters += 1
    if grid[right][row] > middle:
        greaters += 1
    if greaters == 4:
        total_danger += middle + 1
print(f"total danger: {total_danger}")

print("second star:")
# turn the table into a binary grid; replace all 9s with high values,
# everything else with 0.
HIGH = 100000
for row, column in GridIterator():
    grid[column][row] = HIGH if grid[column][row] == 9 else 0

# "paint" in the areas with 2s, keeping count of how many cells
# were filled in per connected area.
def get_neighbors(column, row):
    retval = []
    if column > 0:
        retval.append((column - 1, row))
    if column < 99:
        retval.append((column + 1, row))
    if row > 0:
        retval.append((column, row - 1))
    if row < 99:
        retval.append((column, row + 1))
    return retval


paint = 1
stack = []

for row, column in GridIterator():
    if grid[column][row] != 0:
        continue
    stack.append((column, row))
    while len(stack) > 0:
        current_c, current_r = stack.pop()
        if grid[current_c][current_r] == 0:
            grid[current_c][current_r] = paint
            stack.extend(get_neighbors(current_c, current_r))
    paint += 1
    print(f" done painting {paint-1}")

# Grid is now painted in; time to see which color "won."
counts = {}

for row, column in GridIterator():
    val = grid[column][row]
    if val != HIGH:
        counts[val] = counts.get(val, 0) + 1

paints = counts.keys()
cell_count = counts.values()
sorted_counts = [
    (paint_, count)
    for (paint_, count) in sorted(
        zip(paints, cell_count), key=lambda x: x[1], reverse=True
    )
]
print(f"Top three: {sorted_counts[0]}, {sorted_counts[1]}, {sorted_counts[2]}.")
print(
    f"Product of top three: {sorted_counts[0][1] * sorted_counts[1][1] * sorted_counts[2][1]}"
)

# Silly extra thing that is really not needed but scratch
# it, I'm doing it anyway.
output_image = Image.new("HSV", (100, 100))
editable_image = asarray(output_image)
for row, column in GridIterator():
    val = grid[column][row]
    if val != HIGH:
        hue = (val / paint) * 255
        editable_image[column, row] = (hue, 250, 250)
output_path = pathlib.Path(__file__).parent / "out.png"
Image.fromarray(editable_image, mode="HSV").convert(mode="RGB").save(output_path)
