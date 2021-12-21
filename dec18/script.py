import pathlib
from typing import List
from math import floor,ceil
from tree import LeafNode,TreeNode
import snailfish as sf
    
def parse_string(to_parse:str):
    iterator = iter(to_parse)
    next(iterator)
    current_node = TreeNode(None)
    current_leaf = LeafNode(0)
    build_stack = [current_node]
    for character in iterator:
        if character == "[":
            #New layer to add.
            new_layer = TreeNode(current_node)
            current_node.insert(new_layer)
            build_stack.append(current_node)
            current_node = new_layer
            continue
        if character == ",":
            if current_leaf >= 0:
                current_node.insert(current_leaf)
            current_leaf = LeafNode(0)
            continue
        if character == "]":
            #Drop down a layer.
            current_node.insert(current_leaf)
            current_leaf = LeafNode(-1)
            current_node = build_stack.pop()
            continue
        current_leaf.append(character)
        
    return current_node

input_path = pathlib.Path(__file__).parent / "input.txt"

snail_numbers:List[TreeNode] = []



print("\n\nparsing input file\n")

with open(input_path,"r") as input_file:
    for line in input_file:
        print(line.strip(),end = " -> ")
        root_node = parse_string(line.strip())
        print(str(root_node))
        snail_numbers.append(root_node)
print("first star:")



def test_battery():
    errors = 0

    big_boom = parse_string('[[[[[1,1],[2,2]],[[3,3],[4,4]]],[[[5,5],[6,6]],[[7,7],[8,8]]]],[[[[1,1],[2,2]],[[3,3],[4,4]]],[[[5,5],[6,6]],[[7,7],[8,8]]]]]')
    print(big_boom.depth())
    print(big_boom.get_leaves())
    for i in range(30):
        print(f"Step {i}: {str(big_boom)}")
        sf.explode_number(big_boom)

    #Test if the magnitude calculations are correct.
    my_directory = pathlib.Path(__file__).parent
    with open(my_directory/"mag_tests.txt") as tests:
        for line in tests:
            line = line.strip()
            print(line)
            magnitude = sf.calculate_magnitude(parse_string(line.split("->")[0]))
            expected = int(line.split("->")[1])
            print(f"{magnitude} == {expected}")
            if expected != magnitude:
                print("ERR")
                errors += 1
    #Explosion tests next.
    with open(my_directory/"exp_tests.txt") as tests:
        for line in tests:
            trees = line.strip().split("->")
            print(f"Exploding <{trees[0]}> to get <{trees[1]}>")
            trees[0] = parse_string(trees[0])
            trees[1] = parse_string(trees[1])
            sf.explode_number(trees[0])
            print(f"<{str(trees[0])}>==<{str(trees[1])}>")
            if str(trees[0]) != str(trees[1]):
                print("ERR")
                errors+=1
    #Reduction tests
    with open(my_directory/"reduction_tests.txt") as tests:
        for line in tests:
            line = line.strip()
            q_and_a = line.split("=")
            expected = q_and_a[1]
            to_add = q_and_a[0].split("+")
            current_result = parse_string(to_add[0])
            print(f"\nAdding together {len(to_add)} numbers.")
            for num in to_add[1:]:
                current_result = current_result + parse_string(num)
                sf.reduce(current_result)
            print(f"Expected result: {expected}\nactual result:   {str(current_result)}")
            if expected != str(current_result):
                print("ERR")
                errors+=1
                #start from the top, but go single-step this time.
                current_result = parse_string(to_add[0])
                for num in to_add[1:]:
                    current_result = current_result + parse_string(num)
                    curr_str = str(current_result)
                    prev_str = ""
                    while curr_str != prev_str:
                        prev_str = curr_str
                        print(prev_str)
                        sf.reduce(current_result,True)
                        curr_str = str(current_result)

    #Finally, addition-with-reduction tests.
    

    print("Encountered",errors,"mis-matches between expected and given values.")
    pass

test_battery()
exit()

result = snail_numbers[0]

for current in snail_numbers[1:]:
    print(f"{str(result)} + {str(current)} = ",end="")
    result = result + current
    sf.reduce(result)
    

print(repr(result))

print(f"Final snail number: {result}. Magnitude: {sf.calculate_magnitude(result)}")

print("second star:")