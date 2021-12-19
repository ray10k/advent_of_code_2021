import pathlib
import itertools
from types import prepare_class

input_path = pathlib.Path(__file__).parent / "input.txt"

VALID_RANGE = range(10)


def get_neighborhood(column, row):
    # Making an iterator nested 3 layers deep. First time doing that kind of thing!
    # Get the 3x3 area around the given coordinates.
    retval = itertools.product(range(column - 1, column + 2), range(row - 1, row + 2))
    # Filter out the positions past the grid boundaries.
    retval = filter(lambda x: x[0] in VALID_RANGE and x[1] in VALID_RANGE, retval)
    # filter out the central position.
    retval = filter(lambda x: x != (column, row), retval)
    return tuple(retval)


def get_empty_grid():
    return [[0] * 10 for _ in range(10)]


def iterate_grid():
    return itertools.product(range(10), repeat=2)


def grid_to_string(grid):
    # I'm sure that someone smarter than me can do this with nested iterators.
    # I'm not smarter than myself.
    retval = ""
    for y in range(10):
        for x in range(10):
            retval += str(grid[x][y])
        retval += "\n"
    return retval


def grid_compare(left, right):
    for x, y in iterate_grid():
        if left[x][y] != right[x][y]:
            return False
    return True


def grid_diff(left, right):
    retval = get_empty_grid()
    for x, y in iterate_grid():
        retval[x][y] = abs(left[x][y] - right[x][y])
    return retval


def single_step_one(grid):
    # First, increment the octopi and track which ones flash because
    # of the increment.
    flashes = 0
    middle_grid = get_empty_grid()
    final_grid = get_empty_grid()
    for x, y in iterate_grid():
        final_grid[x][y] = grid[x][y] + 1
        if final_grid[x][y] > 9:
            middle_grid[x][y] = 1
    # Then, construct a new grid that will contain the cells that
    # flash during this step due to the increment.
    stable = False
    while not stable:
        stable = True
        for x, y in iterate_grid():
            if middle_grid[x][y] == 1:
                # If a cell has flashed already, it's stable.
                continue
            # Cell has not flashed yet; check if neighboring cells flashing
            # will cause *this* cell to flash.
            flashes_around = sum(
                middle_grid[n_x][n_y] for n_x, n_y in get_neighborhood(x, y)
            )
            if flashes_around + final_grid[x][y] > 9:
                # A new flash happened.
                stable = False
                middle_grid[x][y] = 1
    # Finally, count the flashes and update the grid.
    for x, y in iterate_grid():
        if middle_grid[x][y] == 1:
            flashes += 1
            final_grid[x][y] = 0
        else:
            flashes_around = sum(
                middle_grid[n_x][n_y] for n_x, n_y in get_neighborhood(x, y)
            )
            final_grid[x][y] = flashes_around + final_grid[x][y]
    return (final_grid, flashes)


print("TESTING TESTING TESTING")

print(get_neighborhood(3, 6))  # should give x=2..4, y=5..7
print(get_neighborhood(4, 0))  # should give x=3..5, y=0..1

test_path = pathlib.Path(__file__).parent / "test_input.txt"
known_good = [get_empty_grid() for _ in range(6)]
with open(test_path, "r") as test_input:
    current = 0
    try:
        while True:
            for y in range(10):
                line = next(test_input)
                for x, num in enumerate(line.strip()):
                    known_good[current][x][y] = int(num)
            current += 1
            next(test_input)
    except StopIteration:
        print("done loading test data.")
# Single-step tests.
for i in range(len(known_good) - 1):
    result, _ = single_step_one(known_good[i])
    print(f"Step {i} to {i+1}, result: ", end="")
    if grid_compare(result, known_good[i + 1]):
        print("good!")
    else:
        print(f"BAD! Difference:\n{grid_to_string(grid_diff(result,known_good[i+1]))}")
        print(
            f"grid inputs:\n{grid_to_string(result)}\n{grid_to_string(known_good[i+1])}"
        )
# entire progression test.
result = known_good[0]
for i in range(1, len(known_good)):
    result, _ = single_step_one(result)
    if grid_compare(result, known_good[i]):
        print(f"step {i} OK.")
    else:
        print(f"step {i} fail.")
        print(grid_to_string(result), "", grid_to_string(known_good[i]), sep="\n")
if grid_compare(result, known_good[5]):
    print("Long test OK.")
else:
    print("Back to the drawing board.")


print("first star:")
# Make a 10x10 grid (in the form of nested lists)
initial_grid = get_empty_grid()
with open(input_path) as input_file:
    for row, line in enumerate(input_file):
        for column, character in enumerate(line.strip()):
            initial_grid[row][column] = int(character)
print("initial grid:\n", grid_to_string(initial_grid), sep="")

flashes = 0
step_grid = initial_grid
for step in range(1, 101):
    step_grid, flash = single_step_one(step_grid)
    flashes += flash

print(
    "Final state of the grid:\n",
    grid_to_string(initial_grid),
    f"{flashes} flashes counted.",
    sep="",
)

print("second star:")
# When all octopuses flash, they all end up at 0 energy.
# So, when the grid after a step is all 0s, they all flashed.
generation_count = 0
target_grid = get_empty_grid()
step_grid = initial_grid
while not grid_compare(target_grid, step_grid):
    generation_count += 1
    step_grid, _ = single_step_one(step_grid)
print(f"after {generation_count} steps, all octopuses are syched.")
