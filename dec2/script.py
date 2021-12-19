import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

print("first star:")
horizontal = 0
vertical = 0
with open(input_path,"r") as actions:
    for action in actions:
        direction,distance = action.split(" ")
        distance = int(distance)
        if direction == "forward":
            horizontal += distance
        elif direction == "down":
            vertical += distance
        elif direction == "up":
            vertical -= distance
print(f"ended at ({horizontal},{vertical}); answer is {horizontal*vertical}")

print("second star:")
aim = 0
horizontal = 0
vertical = 0
with open(input_path,"r") as actions:
    for action in actions:
        direction,distance = action.split(" ")
        distance = int(distance)
        if direction == "forward":
            horizontal += distance
            vertical += (aim * distance)
        elif direction == "down":
            aim += distance
        elif direction == "up":
            aim -= distance
print(f"ended at ({horizontal},{vertical}); answer is {horizontal*vertical} with an aim of {aim} at the end.")