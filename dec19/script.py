import pathlib
from collections import namedtuple

Coordinate = namedtuple("Coordinate","x y z")
Scanner = namedtuple("Scanner","name coordinates")

input_path = pathlib.Path(__file__).parent / "input.txt"
scanners = []
with open(input_path) as input_file:
    current_coords = []
    scanner = None
    try:
        while True:
            scanner = next(input_file)
            scanner = scanner.strip("\n- ")
            print(f"<{scanner}>")
            while (line := next(input_file)) != "\n":
                nmbs = [int(x) for x in line.split(",")]
                
                current_coords.append(Coordinate(int(nmbs[0]),int(nmbs[1]),int(nmbs[2])))
            scanners.append(Scanner(scanner,tuple(current_coords)))
            print(f"{len(current_coords)} coordinates found.")
            current_coords.clear()
    except StopIteration:
        scanners.append(Scanner(scanner,tuple(current_coords)))
        print(f"Final scanner had {len(current_coords)} coordinates.")

print("first star:")

print("second star:")