import pathlib
import re
from collections import namedtuple
import itertools as itt

input_path = pathlib.Path(__file__).parent / "input.txt"
# Test input should yield 45 for star 1, 112 for star 2.
# input_path = pathlib.Path(__file__).parent / "test-input.txt"
target_area = None
target_floor = 0
Point = namedtuple("Point", "x y")
Point.__annotations__ = {"x": int, "y": int}


def sign(num):
    if num == 0:
        return 0
    if num > 0:
        return 1
    return -1


with open(input_path) as input_file:
    # It's a single-line file, so just read the line.
    string_in = input_file.readline().strip()
    ranges = re.findall(r"-?\d+\.\.-?\d+", string_in)
    x_range = ranges[0].split("..")
    x_range = [int(r) for r in x_range]
    y_range = ranges[1].split("..")
    y_range = [int(r) for r in y_range]
    target_area = (range(x_range[0], x_range[1] + 1), range(y_range[0], y_range[1] + 1))
    target_floor = min(y_range)
    print("Target area:", target_area)

print("first star:")
# Start by shooting with velocities 0,0. If the target
# area is never hit and the first position *below* the
# target is to the left or in the x range of the target,
# increase x velocity. if the first position below the
# target is to the right, reduce x velocity and increase y.
# If the target is hit, increase y velocity.
# Repeat until one shot has a sequence that is in the x
# range of the target, but with one point above and the
# next point below target.

# Iterator that yields all the "scanned points" starting
# from (0,0) and following the rules for the trajectory
# calculations.
def trajectory(x_velocity: int, y_velocity: int):
    previous = Point(0, 0)
    yield previous
    while previous.y > target_floor:
        previous = Point(previous.x + x_velocity, previous.y + y_velocity)
        x_velocity = sign(x_velocity) * (abs(x_velocity) - 1)
        y_velocity -= 1
        yield previous


def float_range(start: float, stop: float, step: float):
    if step == 0:
        yield start
        return
    length = abs(start - stop)
    steps = abs(int(length / step))
    if stop < start and step > 0:
        step = -step
    for s in range(steps):
        yield start + (s * step)


# Iterator that yields all the points in a straight line from
# start to end, as integers. Adapted from the wikipedia page for
# Bresenham's line algorithm (https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#All_cases)
def line_itr(start: Point, end: Point):
    if start == end:
        return
    x_delta = end.x - start.x
    x_direction = 1 if start.x < end.x else -1
    y_delta = end.y - start.y
    y_direction = 1 if start.y < end.y else -1
    err_val = x_delta + y_delta
    x_now = start.x
    y_now = start.y
    while True:
        if x_now == end.x and y_now == end.y:
            break
        if (err_val * 2) >= y_delta:
            err_val += y_delta
            x_now += x_direction
        if (err_val * 2) <= x_delta:
            err_val += x_delta
            y_now += y_direction
        yield Point(x_now, y_now)


# Convenience function to check if the given point hits the target.
def target_hit(current: Point) -> bool:
    return current.x in target_area[0] and current.y in target_area[1]


# check if the point is to the left, right or in the target range.
def target_h_sign(current: Point):
    if current.x < min(target_area[0]):
        return -1
    if current.x > max(target_area[0]):
        return 1
    return 0


def target_v_sign(current: Point):
    if current.y < min(target_area[1]):
        return -1
    if current.y > max(target_area[1]):
        return 1
    return 0


# Function to check if the target was passed, but not hit.
def target_passed(first: Point, second: Point) -> bool:
    # The trajectory passes through the target, if any point in the
    # trajectory hits the target except the starting- or ending point.
    if target_hit(first) or target_hit(second):
        return False
    for pt in line_itr(first, second):
        if target_hit(pt):
            return True
    return False


# over-thought step one. A few things to keep in mind:
# -a shot with starting vertical velocity 3 (for instance) will pass
# through heights 0,3,5,6,6,5,3,0
# -If the vertical velocity vv starts positive, after 2*(vv+1) ticks, the
# probe is back at the starting height but with vv == initial_vv*-1
# -Horizontal velocity is irrellevant for high shots; drag will reduce
# it to 0 well before entering the target area.


def sum_to(input: int):
    return int(input * ((input / 2) + 0.5))


max_height = sum_to(target_floor)
print(f"Highest height reached before hitting the target: {max_height}")

print("second star:")
# Calculate *all* attacks that hit the target. Hoo boy.
# First thing to keep in mind: all courses where the forward velocity
# hits zero will have matching sets of upward velocities.
# Step 1: Figure out the horizontal velocities that could hit.
h_velocities = set()
# Any shot that starts with a horizontal velocity greater than the
# distance to the far end of the target is guaranteed to miss, giving
# me a quite reasonable upper bound.
for h_velocity in range(max(target_area[0]) + 1):
    for step in trajectory(h_velocity, 0):
        if target_h_sign(step) == 0:
            h_velocities.add(h_velocity)
            break

# Step 2: Figure out the vertical velocities that could hit.
v_velocities = set()
# Vertical velocity is a little trickier. However, a shot will vertically
# always miss if either the velocity is greater than the one used in the
# first star solution, and it will always miss if a negative value lower
# than the floor of the target is used. Hence the upper- and lower bound.
for v_velocity in range(target_floor - 1, -target_floor + 2):
    for step in trajectory(0, v_velocity):
        if target_v_sign(step) == 0:
            v_velocities.add(v_velocity)

print(
    "horizontal velocities: " + str(len(h_velocities)),
    "vertical velocities: " + str(len(v_velocities)),
    sep="\n",
)
print(
    f"total potential hits: {len(h_velocities)}*{len(v_velocities)} {len(h_velocities)*len(v_velocities)}"
)

# Step 3: trace out the paths from those velocities that hit the target.
Shot = namedtuple("Shot", "h v")
hits = []
for h_velocity, v_velocity in itt.product(h_velocities, v_velocities):
    for point in trajectory(h_velocity, v_velocity):
        if target_hit(point):
            hits.append(Shot(h_velocity, v_velocity))
            break

print(f"Total hits: {len(hits)}")
# sanity check for the test values.
def run_test():
    with open(pathlib.Path(__file__).parent / "test-output.txt") as test_values:
        for line in test_values:
            line = line.strip().split(",")
            miss = Shot(int(line[0]), int(line[1]))
            if miss not in hits:
                print(f"Couldn't find {miss} in the results.")
            else:
                hits.remove(miss)
    if len(hits) != 0:
        print(f"Found the following 'ghost hit':")
        print(",".join(str(x) for x in hits))
    else:
        print("Zero ghost hits.")


# run_test()
