import pathlib
from typing import Tuple
from binary_image import BinaryImage
import itertools as itt

input_path = pathlib.Path(__file__).parent / "input.txt"
# input_path = pathlib.Path(__file__).parent / "test.txt"
lookup_table = ""
initial_image = BinaryImage(100, 100, 0)

with open(input_path) as input_file:
    lookup_table = next(input_file).strip()
    next(input_file)
    for row, line in enumerate(input_file):
        for column, character in enumerate(line.strip()):
            initial_image[column, row] = character == "#"

print("first star:")


def neighborhood_to_index(source: Tuple) -> int:
    retval = 0
    for num in source:
        retval = retval << 1
        retval += num
    return retval


def improve_image(base_image: BinaryImage) -> BinaryImage:
    bg_index = neighborhood_to_index(base_image.get_neighborhood(-10, -10))
    new_background = lookup_table[bg_index] == "#"
    retval = BinaryImage(base_image.height + 2, base_image.width + 2, new_background)
    for x, y in itt.product(range(-1, base_image.width + 1), repeat=2):
        neigh = base_image.get_neighborhood(x, y)
        value = neighborhood_to_index(neigh)
        pixel = lookup_table[value] == "#"
        retval[x + 1, y + 1] = pixel
    return retval


middle_image = improve_image(initial_image)
final_image = improve_image(middle_image)
print(
    f"After running the improvement algo twice, there are {sum(final_image)} lit pixels."
)

print("second star:")
# Oh hey, wonder why there suddenly are so many lanternfish around...
result = initial_image
for i in range(50):
    result = improve_image(result)

print(
    f"After running the improvement algo fifty times, there are {sum(result)} lit pixels."
)
