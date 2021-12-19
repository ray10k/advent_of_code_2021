import pathlib
import itertools as itt
from collections import Counter

input_path = pathlib.Path(__file__).parent / "input.txt"
initial_state = ""
poly_rules = {}
with open(input_path, "r") as input_file:
    initial_state = next(input_file).strip()
    next(input_file)  # Skip the empty line
    for line in input_file:
        rule = line.strip().split(" -> ")
        poly_rules[rule[0]] = rule[1]

# sanity check
bases = set(initial_state)
print(f"Initial state has {len(bases)} unique bases and {len(poly_rules)} rules.")
for one, two in itt.product(bases, repeat=2):
    pr = one + two
    print(f"{pr}->{poly_rules[pr]}|", end="")
print("\n")


def polymerize_once(pattern):
    to_insert = []
    # Trick I used before. To get every pair of letters, iterate
    # over the string plus the string offset by one.
    for a, b in zip(pattern, pattern[1:]):
        to_insert.append(poly_rules[a + b])
    retval = []
    for a, b in zip(pattern, to_insert):
        retval.append(a)
        retval.append(b)
    retval.append(pattern[-1])
    return retval


print("first star:")
result = initial_state
for _ in range(10):
    result = polymerize_once(result)
print(
    f"After 10 steps, the polymer went from length {len(initial_state)} to {len(result)}"
)
result_counter = Counter(result)
result = result_counter.most_common()
print(
    f"Most common base: {result[0][0]} ({result[0][1]}). Least common base: {result[-1][0]} ({result[-1][1]})"
)
print(f"Element delta: {result[0][1] - result[-1][1]}")

print("second star:")
projected_length = len(initial_state)
for _ in range(40):
    projected_length += projected_length - 1
print(f"Warning: will need to make a polymer chain of {projected_length} length. Ouch.")

# Stepping through each chain in its entirety is *not* an option. Requires too much memory.
# Instead, make a lookup table turning a pair of bases AB -> C to return AC, then build a
# generator going 40 layers deep. Fingers crossed it will end within this century.
# Spoiler alert: it's going to take a damn century. New approach.
# The order only matters per-pair. So, break the structure down to counts of pairs, and
# generate a new count-of-pairs based on that. Keep in mind, a pair AB will generate pairs
# AC and CB.
# It's the lanternfish all over again. Had to cheat and look at solutions :(

second_result = {}
for a, b in zip(initial_state, initial_state[1:]):
    pair = a + b
    second_result[pair] = second_result.get(pair, 0) + 1

for step in range(40):
    temp_result = {}
    for pair, amount in second_result.items():
        middle = poly_rules[pair]
        first_pair = pair[0] + middle
        second_pair = middle + pair[1]
        temp_result[first_pair] = temp_result.get(first_pair, 0) + amount
        temp_result[second_pair] = temp_result.get(second_pair, 0) + amount
    second_result = temp_result
# I now have the pairs; time to count individual instances of elements.
final_counter = {base: 0 for base in bases}
for pair, amount in second_result.items():
    final_counter[pair[0]] += amount
    final_counter[pair[1]] += amount
# Every base has been counted double, except the very first and very last.
# However, since the very first and last *do not change* from the original
# input, this can be adjusted for.
final_counter[initial_state[0]] += 1
final_counter[initial_state[-1]] += 1
for pair in final_counter:
    final_counter[pair] = final_counter[pair] // 2


final_length = sum(x for x in final_counter.values())
final_counter = Counter(final_counter).most_common()

print(
    f"After 40 steps, the polymer went from length {len(initial_state)} to {final_length}."
)
print(
    f"Sanity check: calculated length {projected_length}. Sanity check pass: {projected_length==final_length}"
)

print(
    f"Most common base: {final_counter[0][0]} ({final_counter[0][1]}). Least common base: {final_counter[-1][0]} ({final_counter[-1][1]})"
)
print(f"Element delta: {final_counter[0][1] - final_counter[-1][1]}")
