import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

print("first star:")

# Order of the crabs doesn't matter; regardless if the final crab in the line
# is told their target position first or last, it takes the same amount of fuel.
crabs = None
with open(input_path, "r") as input_file:
    line = input_file.readline()
    crabs = [int(num) for num in line.split(",")]
    crabs = sorted(crabs)
print(f"There are {len(crabs)} crabs in little submarines.")

# Shortest distance adding it all up is probably the median position; Most
# crabs should be close to this.
median_index = len(crabs) // 2
median_value = crabs[median_index]
fuel_used = 0

for crab in crabs:
    fuel_used += abs(median_value - crab)

print(
    f"Fuel usage to align on median: {fuel_used}. Median position is {median_index} -> {median_value}"
)

print("second star:")

# I keep coming back to this, huh?
def series_sum(last_value):
    return int(last_value * ((last_value / 2) + 0.5))


# The median alignment may not be best. Brute-force? ...Brute-force.
# No point checking past the outer-most crabs; will take at least
# 1 more distance than the best possible solution.
usage_per_position = {}
for position in range(min(crabs), max(crabs) + 1):
    sum_usage = 0
    for crab in crabs:
        sum_usage += series_sum(abs(position - crab))
    usage_per_position[position] = sum_usage

all_usages = tuple(usage_per_position.values())
all_positions = tuple(usage_per_position.keys())
best_usage = all_usages.index(min(all_usages))
best_position = all_positions[best_usage]

print(f"With {all_usages[best_usage]} fuel used, position {best_position} is best.")
