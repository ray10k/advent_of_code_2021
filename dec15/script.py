import pathlib
from collections import namedtuple
import itertools as itt
from typing import List

input_path = pathlib.Path(__file__).parent / "input.txt"
Point = namedtuple("Point", "x y cost")
Route = namedtuple("Route", "points total_cost")
grid = []

with open(input_path, "r") as input_file:
    for line in input_file:
        line = line.strip()
        line_list = [int(num) for num in line]
        grid.append(line_list)


def get_neighborhood(x, y, values):
    # Get the 3x3 area, remove diagonals, remove center,
    # remove out-of-scope coordinates.
    width = range(len(values[0]))
    height = range(len(values))
    itr = (
        (x_, y_) for x_, y_ in itt.product(range(x - 1, x + 2), range(y - 1, y + 2))
    )  # 3x3 area
    itr = filter(lambda x_: x_[0] == x or x_[1] == y, itr)  # eliminate diagonals
    itr = filter(lambda x_: x_[0] != x or x_[1] != y, itr)  # eliminate center
    itr = filter(
        lambda x_: x_[0] in width and x_[1] in height, itr
    )  # eliminate outliers
    return tuple(Point(x_, y_, values[y_][x_]) for x_, y_ in itr)


# The usual sanity checks on the neighborhood.
print(get_neighborhood(3, 3, grid))  # Should print 2,3; 3,2; 4,3; 3,4;
print(get_neighborhood(0, 10, grid))  # Should print 0,9; 0,11; 1,10;
print(get_neighborhood(0, 0, grid))

START = Point(0, 0, 0)  # The challenge explicitly states that the
# danger of the starting position is ignored.
end = Point(len(grid[0]) - 1, len(grid) - 1, grid[-1][-1])
# print(f"going from ({START.x},{START.y})<{START.cost}> to ({end.x},{end.y})<{end.cost}>")


def a_star(start: Point, end: Point, values: List[List[int]]):
    print(f"Finding route from ({start.x},{start.y}) to ({end.x},{end.y})")
    previous_points = {(start.x, start.y): None}
    unchecked_points = [start]
    full_grid_value = sum(sum(line) for line in values)
    cost_to = [
        [full_grid_value for _ in range(len(values[0]))] for _ in range(len(values))
    ]
    cost_to[start.y][start.x] = start.cost
    while len(unchecked_points) > 0:
        unchecked_points.sort(key=lambda x_: cost_to[x_.y][x_.x], reverse=True)
        next_candidate = unchecked_points.pop()
        if next_candidate == end:
            # Re-construct the route taken to here
            constructed_route = []
            current_route_point = end
            while current_route_point != start:
                constructed_route.append(
                    previous_points[(current_route_point.x, current_route_point.y)]
                )
                current_route_point = previous_points[
                    (current_route_point.x, current_route_point.y)
                ]
            constructed_route.reverse()
            return Route(tuple(constructed_route), cost_to[end.y][end.x])
        neighbors = get_neighborhood(next_candidate.x, next_candidate.y, values)
        path_cost = cost_to[next_candidate.y][next_candidate.x]
        for neigh in neighbors:
            if path_cost + neigh.cost < cost_to[neigh.y][neigh.x]:
                # Better candidate found to that location.
                previous_points[(neigh.x, neigh.y)] = next_candidate
                cost_to[neigh.y][neigh.x] = path_cost + neigh.cost
                if neigh not in unchecked_points:
                    unchecked_points.append(neigh)
    print("Somehow, I ran out of points to check.")
    if cost_to[end.y][end.x] < full_grid_value:
        print("Cost to end is", cost_to[end.y][end.x])
    else:
        print("No path to end found.")


print("first star:")
first_route = a_star(START, end, grid)
print(
    f"Found a route with total danger value {first_route.total_cost}. The route is {len(first_route.points)} steps long."
)

print("second star:")
# Need to expand the grid to a whopping 500x500. Doable, but... Good grief.
mult_x = len(grid[0])
mult_y = len(grid)
expanded_grid = [[0 for _ in range(mult_x * 5)] for _ in range(mult_y * 5)]
# For a given location x,y in the original grid, I must set the following locations:
# x_:[x,x+100,x+200,x+300,x+400]
# y_:[y,y+100,y+200,y+300,y+400]
for off_x, off_y in itt.product(range(mult_x), range(mult_y)):
    for step_x, step_y in itt.product(range(5), range(5)):
        # Calculate the coordinates.
        coord_x = off_x + (mult_x * step_x)
        coord_y = off_y + (mult_y * step_y)
        # Calculate the value
        adj_value = grid[off_y][off_x] + step_x + step_y
        if adj_value > 9:
            adj_value -= 9
        expanded_grid[coord_y][coord_x] = adj_value
# Sanity check.
for c_x, c_y in itt.product(range(len(expanded_grid[0])), range(len(expanded_grid))):
    if expanded_grid[c_y][c_x] == 0:
        print(f"WARNING! Expanded grid location {c_x},{c_y} has not been set!")
end = Point(len(expanded_grid[0]) - 1, len(expanded_grid) - 1, expanded_grid[-1][-1])
second_route = a_star(START, end, expanded_grid)
print(
    f"Found a longer route with total danger value {second_route.total_cost}. The route is {len(second_route.points)} steps long."
)
