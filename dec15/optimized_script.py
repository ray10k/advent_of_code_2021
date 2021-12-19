import pathlib
from collections import namedtuple
import itertools as itt
from typing import Dict, List
import heapq as hq

input_path = pathlib.Path(__file__).parent / "input.txt"
#An x,y coordinate pair.
Coordinate = namedtuple("Coordinate", "x y")
#A single point in the grid, plus its associated cost.
Point = namedtuple("Point", "cost coord")
#A single step along a route, along with the total cost to that point.
Step = namedtuple("Step","path_cost coord")
#The total cost for a series of steps, plus the steps taken.
Route = namedtuple("Route", "total_cost coords")
grid = []

with open(input_path, "r") as input_file:
    for line in input_file:
        line = line.strip()
        line_list = [int(num) for num in line]
        grid.append(line_list)


def get_neighborhood(coord:Coordinate, values):
    # Get the 3x3 area, remove diagonals, remove center,
    # remove out-of-scope coordinates.
    width = range(len(values[0]))
    height = range(len(values))
    itr = (
        Coordinate(x_, y_) for x_, y_ in itt.product(range(coord.x - 1, coord.x + 2), range(coord.y - 1, coord.y + 2))
    )  # 3x3 area
    itr = filter(lambda x_: x_.x == coord.x or x_[1] == coord.y, itr)  # eliminate diagonals
    itr = filter(lambda x_: x_ != coord, itr)  # eliminate center
    itr = filter(
        lambda x_: x_.x in width and x_.y in height, itr
    )  # eliminate outliers
    return tuple(Point(values[y_][x_],Coordinate(x_,y_)) for x_, y_ in itr)


# The usual sanity checks on the neighborhood.
print(get_neighborhood(Coordinate(3, 3), grid))  # Should print 2,3; 3,2; 4,3; 3,4;
print(get_neighborhood(Coordinate(0, 10), grid))  # Should print 0,9; 0,11; 1,10;
print(get_neighborhood(Coordinate(0, 0), grid))

START = Coordinate(0, 0) # The challenge explicitly states that the
# danger of the starting position is ignored.
end = Coordinate(len(grid[0]) - 1, len(grid) - 1)
# print(f"going from ({START.x},{START.y})<{START.cost}> to ({end.x},{end.y})<{end.cost}>")


def a_star(start: Coordinate, end: Coordinate, values: List[List[int]]):
    print(f"Finding route from ({start.x},{start.y}) to ({end.x},{end.y})")
    previous_points:Dict[Coordinate,Step] = {start: None}
    unchecked_points:List[Step] = [Step(0,start)]
    hq.heapify(unchecked_points)
    #Python integers do not have a formal maximum value. Use the sum total of
    #all absolute values of grid squares as a "sensible" maximum instead. 
    #Guaranteed to be higher than any partial sum of cells.
    full_grid_value = sum(sum(abs(num) for num in line) for line in values)
    cost_to:Dict[Coordinate,int] = {}
    cost_to[start] = 0
    while len(unchecked_points) > 0:
        next_candidate = unchecked_points[0]
        if next_candidate.coord == end:
            # Re-construct the route taken to here
            constructed_route = []
            current_route_point = end
            while current_route_point != start:
                constructed_route.append(
                    previous_points[current_route_point]
                )
                current_route_point = previous_points[current_route_point].coord
            constructed_route.reverse()
            return Route(cost_to[end],tuple(constructed_route))
        candidate_point = next_candidate.coord
        neighbors = get_neighborhood(candidate_point, values)
        path_cost = cost_to.get(candidate_point,full_grid_value)
        changed = False
        for neigh in neighbors:
            if path_cost + neigh.cost < cost_to.get(neigh.coord,full_grid_value):
                # Better candidate found to that location.
                previous_points[neigh.coord] = Step(path_cost+neigh.cost,candidate_point)
                cost_to[neigh.coord] = path_cost + neigh.cost
                neigh_step = Step(path_cost+neigh.cost,neigh.coord)
                if neigh_step not in unchecked_points:
                    if not changed:
                        hq.heappushpop(unchecked_points,neigh_step)
                        changed = True
                    else:
                        hq.heappush(unchecked_points,neigh_step)
        if not changed:
            hq.heappop(unchecked_points)
    print("Somehow, I ran out of points to check.")
    if cost_to[end.y][end.x] < full_grid_value:
        print("Cost to end is", cost_to[end.y][end.x])
    else:
        print("No path to end found.")


print("first star:")
first_route = a_star(START, end, grid)
print(
    f"Found a route with total danger value {first_route.total_cost}. The route is {len(first_route.coords)} steps long."
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
end = Coordinate(len(expanded_grid[0]) - 1, len(expanded_grid) - 1)
second_route = a_star(START, end, expanded_grid)
print(
    f"Found a longer route with total danger value {second_route.total_cost}. The route is {len(second_route.coords)} steps long."
)
