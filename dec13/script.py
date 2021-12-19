import pathlib
from collections import namedtuple

input_path = pathlib.Path(__file__).parent / "input.txt"

Point = namedtuple("Point", "x y")
Fold = namedtuple("Fold", "axis value")
initial_points = []
folding_instructions = []


def fold_point(p: Point, f: Fold):
    relevant_coordinate = getattr(p, f.axis)
    # If the relevant coordinate of the point is to
    # the left or above the folding line, return
    # the point unchanged.
    if relevant_coordinate < f.value:
        return p
    # Otherwise, subtract the difference from the
    # folding line's value and make a new Point.
    diff = abs(relevant_coordinate - f.value)
    if f.axis == "x":
        return Point(f.value - diff, p.y)
    return Point(p.x, f.value - diff)


with open(input_path, "r") as input_file:
    # read lines with points until an empty line comes up
    line = next(input_file).strip()
    while line != "":
        coords = line.split(",")
        p = Point(int(coords[0]), int(coords[1]))
        initial_points.append(p)
        line = next(input_file).strip()
    # The remaining lines are now folding instructions.
    for line in input_file:
        line = line.strip()
        instr = line.split(" ")[-1]
        instr = instr.split("=")
        f = Fold(instr[0], int(instr[1]))
        folding_instructions.append(f)

# test with a pair of folds.
test_folds = [Fold("x", 5), Fold("y", 7)]
test_point = Point(10, 10)
end_point = fold_point(fold_point(test_point, test_folds[0]), test_folds[1])
print(f"folded {test_point}, ended at {end_point}")


print("first star:")
result_one = set()
first_fold = folding_instructions[0]
for p in initial_points:
    result_one.add(fold_point(p, first_fold))
print(
    f"After the first fold, {len(result_one)} points out of {len(initial_points)} are still visible."
)

print("second star:")
# First, do all the folds. Use sets since that gives the unique values "for free."
final_result = set(initial_points)
for instruction in folding_instructions:
    step_result = set()
    for point in final_result:
        step_result.add(fold_point(point, instruction))
    final_result = step_result
print(
    f"After folding {len(folding_instructions)} times, {len(final_result)} points remain."
)

# second, determine the point furthest down and the point furthest to the right.
down, right = 0, 0
for point in final_result:
    if point.x > right:
        right = point.x
    if point.y > down:
        down = point.y
print(f"The final result is {right} by {down} large.")

# third, turn the points in the set into marked spots in the buffer.
print_buffer = [["░"] * (right + 1) for _ in range(down + 1)]
for point in final_result:
    print_buffer[point.y][point.x] = "█"

# finally, print the lines out.
for line in print_buffer:
    print("".join(str(char) for char in line))
