import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"
BRACE_PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
ERROR_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}

print("first star and second star:")
error_score = 0
autocomplete_scores = []
errors = 0
autocompletes = 0
with open(input_path, "r") as input_file:
    for line in input_file:
        stack = []
        for character in line.strip():
            if character in BRACE_PAIRS.keys():
                stack.append(BRACE_PAIRS[character])
                continue
            if len(stack) == 0 or stack.pop() != character:
                print(f"Error: unexpected {character}")
                errors += 1
                error_score += ERROR_SCORES[character]
                stack.clear()
                break
        if len(stack) != 0:
            print(f"Error: {len(stack)} chunks not closed. ", end="")
            autocompletes += 1
            line_score = 0
            while len(stack) > 0:
                character = stack.pop()
                print(character, end="")
                line_score *= 5
                line_score += AUTOCOMPLETE_SCORES[character]
            print("")
            autocomplete_scores.append(line_score)
autocomplete_scores.sort()
median_index = len(autocomplete_scores) // 2

print(
    f"\nTotal error score: {error_score}\nMedian autocorrect score: {autocomplete_scores[median_index]}"
)
print(
    f"Sanity check; found {errors} errors and needed to complete {autocompletes} lines, for a total of {autocompletes+errors} lines."
)
