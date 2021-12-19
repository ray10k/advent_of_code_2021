import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"


def is_big(cave: str):
    return cave.upper() == cave


paths = {}
with open(input_path, "r") as input_file:
    for line in input_file:
        bare_line = line.strip()
        connection = bare_line.split("-")
        if connection[0] not in paths:
            paths[connection[0]] = []
        if connection[1] not in paths:
            paths[connection[1]] = []
        paths[connection[0]].append(connection[1])
        paths[connection[1]].append(connection[0])

for start, ends in paths.items():
    print(
        f"From node [{start}], paths lead to nodes {ends}.{' This is a large cave' if is_big(start) else ''}"
    )

print("first star:")
# I checked. There are no large caves with a direct connection to another large cave.
exploration = [("start",)]
finite_paths = 0
while len(exploration) != 0:
    current_path = exploration.pop()
    current_cave = current_path[-1]
    next_caves = paths[current_cave]
    for cave in next_caves:
        if cave == "end":
            # Found a route to the end!
            # print("found path:",current_path+('end',))
            finite_paths += 1
            continue
        if is_big(cave) or cave not in current_path:
            # Found a potential route forward.
            exploration.append(current_path + (cave,))
            continue
        # ran into a dead end.
print(f"Found {finite_paths} paths leading to the end.")
print("second star:")
# Note to self: *one* small cave is to be visited twice.
# So, at most 1 small cave with two visits,
# any number of large caves with any number of visits,
# any number of small caves with one visit.
exploration = [("start",)]
finite_paths = 0
while len(exploration) != 0:
    if finite_paths % 15000 == 0:
        print(
            f"found {finite_paths} so far, got {len(exploration)} more paths to check."
        )
    current_path = exploration.pop()
    current_cave = current_path[-1]
    next_caves = paths[current_cave]
    # Check if one small cave is already visited twice.
    small_caves = tuple(filter(lambda x: not is_big(x), current_path))
    double_cave = (
        len(tuple(filter(lambda x: small_caves.count(x) > 1, small_caves))) > 0
    )
    for cave in next_caves:
        if cave == "end":
            finite_paths += 1
            continue
        if cave == "start":
            # Can't go back to the start.
            continue
        # We can explore a possible way forward if:
        # - the candidate cave is a big one.
        # - either the cave isn't in the path already, or
        # - no small cave has been visited twice yet.
        if is_big(cave) or cave not in current_path or not double_cave:
            exploration.append(current_path + (cave,))
            continue
print(f"Found {finite_paths} to the end that may visit small caves twice.")
