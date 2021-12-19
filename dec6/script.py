import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

# Don't be dumb. Order of the fish does NOT matter in the slightest,
# what matters is "how many fish have this much time left?"

print("first star:")
fish_timers = []
with open(input_path, "r") as input_:
    line = input_.readline().split(",")
    print(line)
    fish_timers = [int(i) for i in line]

# Leaving this in for posteriety; And because I did the first star
# this way.
print(f"Initially, there are {len(fish_timers)} fish.")
for day in range(1, 81):
    new_fish = 0
    for fish in range(len(fish_timers)):
        fish_timers[fish] -= 1
        if fish_timers[fish] == -1:
            new_fish += 1
            fish_timers[fish] = 6
    fish_timers.extend([8] * new_fish)
    print(f"After day {day}, there are {len(fish_timers)} fish.")

print("second star:")
fish_timers = []
with open(input_path, "r") as input_:
    line = input_.readline().split(",")
    fish_timers = [int(i) for i in line]

fish_per_time = [0] * 9
for fish in fish_timers:
    fish_per_time[fish] += 1

for day in range(1, 257):
    new_fish = [0] * 9
    new_fish[8] = fish_per_time[0]
    new_fish[6] = fish_per_time[0]
    for i in range(1, 9):
        new_fish[i - 1] += fish_per_time[i]
    fish_per_time = new_fish
    if day % 16 == 0:
        print(f"day {day} done with {sum(fish_per_time)} fish alive.")

print(f"Initially, there are {len(fish_timers)} fish.")
