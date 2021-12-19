import argparse as ap
import os
import pathlib as pl

SCRIPT_TEXT = """import pathlib as pl

INPUT_PATH = pl.Path(__file__).parent / "input.txt"

print("first star:")
#Do the initialization for the first star challenge.
result = 0
with open(INPUT_PATH,"r") as input_file:
    for line in input_file:
        #parse the file in whatever way the first challenge requires here.
        pass
print(f"{result=}\\n")

print("second star:")
#Do the initialization for the second star challenge.
result = 0
with open(INPUT_PATH,"r") as input_file:
    for line in input_file:
        #parse the file in whatever way the second challenge requires here.
        pass
print(f"{result=}")

"""


def init_directory(path, mode):
    try:
        os.mkdir(path)
        print(f"Directory {path} made.")
    except:
        print(f"Directory {path} already exists.")

    try:
        open(path / "input.txt", mode).close()
        print(f"data file {path/'input.txt'} made.")
    except:
        print(f"could not make data file {path/'input.txt'}")

    try:
        with open(path / "script.py", mode) as file:
            file.write(SCRIPT_TEXT)
        print(f"script file {path/'script.py'} made.")
    except:
        print(f"could not make script file {path/'script.py'}")


if __name__ == "__main__":
    parser = ap.ArgumentParser(
        description="Set up a folder structure for the Advent of Code challenge."
    )
    parser.add_argument(
        "-d",
        "--starting-directory",
        default=os.getcwd(),
        nargs=1,
        type=str,
        dest="root",
        help="Base path in which the folder structure will be set up. If none is supplied, the current working directory will be used.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        default="x",
        const="w",
        dest="mode",
        help="Forcefully overwrite existing files and folders. By default, existing files and folders will be left intact.",
    )
    arguments = parser.parse_args()

    for day in range(1, 26):
        directory_path = pl.Path(arguments.root[0]) / ("day "+str(day))
        init_directory(directory_path, arguments.mode)
