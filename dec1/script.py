import pathlib

input_file_path = pathlib.Path(__file__).parent / "input.txt"


def grab(handle):
    temp = handle.strip()
    return int(temp)


with open(input_file_path, "r") as input_file:
    inc_count = 0
    current_depth = grab(next(input_file))
    depth_measurements = 0
    for depth in input_file:
        i_depth = grab(depth)
        inc_count += 1 if i_depth > current_depth else 0
        current_depth = i_depth
        depth_measurements += 1
    print(inc_count, "\\", depth_measurements)

depth_list = []
with open(input_file_path, "r") as input_file:
    for depth in input_file:
        depth_list.append(grab(depth))

previous_depth = depth_list[0] + depth_list[1] + depth_list[2]
inc_count = 0
for window in zip(depth_list, depth_list[1:], depth_list[2:]):
    current_depth = sum(window)
    inc_count += 1 if current_depth > previous_depth else 0
    previous_depth = current_depth

print(inc_count)
