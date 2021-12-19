import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

print("first star:")
# First star is simple. Look for outputs with lengths 2, 3, 4 or 7.
# Ignore everything before the pipe character, also.
digits_known = 0
valid_lengths = {2, 3, 4, 7}
with open(input_path, "r") as input_file:
    for line in input_file:
        # Split on the pipe.
        pipe_index = line.index(" | ") + 3
        output_section = line[pipe_index:].strip()
        displays = output_section.split(" ")
        digits_known += sum(1 if len(d) in valid_lengths else 0 for d in displays)
print(f"Managed to find {digits_known} 'easy' digits.")

print("second star:")
# Once more, but this time I have to find a proper mapping
# from "unknown garbage" to "legible numbers."
proper_numbers = [
    "abcdeg",
    "ab",
    "acdfg",
    "abcdf",
    "abef",
    "bcdef",
    "bcdefg",
    "abd",
    "abcdefg",
    "abcdef",
]
# When a proper mapping is known, then every input should match one of the above.

with open(input_path, "r") as input_file:
    sum_total = 0
    for line in input_file:
        # do the same prepwork as before, but this time only extract the
        # leading digits. More known-good values increases the chances getting
        # a weird collision especially when the numbers 0 through 9 are provided.
        wire_mapping = {letter: "X" for letter in "abcdefg"}
        pipe_index = line.index("|")
        test_pattern = line[:pipe_index].strip()
        test_numbers = [set(num.strip()) for num in test_pattern.split(" ")]

        segment_count = {letter: 0 for letter in "abcdefg"}
        for nums in test_numbers:
            for num in nums:
                segment_count[num] += 1
        # Next, find samples for the easy digits: 1, 7, 4 and 8. These have
        # recognisable lengths.
        known_numbers = [
            num for num in filter(lambda x: len(x) in valid_lengths, test_numbers)
        ]
        known_numbers.sort(key=len)
        # Segment d is easiest to find: take 1 and 7. The difference between
        # the two is segment d.
        s_one = known_numbers[0]
        s_seven = known_numbers[1]
        s_four = known_numbers[2]
        s_eight = known_numbers[3]
        diff_one_seven = s_seven - s_one
        seg_d = diff_one_seven.pop()
        wire_mapping[seg_d] = "d"

        # Next, we can determine segments b, e and g by how many numbers set those.
        # b is the only segment that gets set 9 times; e the only one that gets set 6 times
        # and g only 4 times. Both segments a and d get set for 8 numbers, and segments
        # c and f get set for 7 numbers.
        seg_b = next(filter(lambda value: value[1] == 9, segment_count.items()))[0]
        seg_e = next(filter(lambda value: value[1] == 6, segment_count.items()))[0]
        seg_g = next(filter(lambda value: value[1] == 4, segment_count.items()))[0]
        all_set_9_times = [
            i for i in filter(lambda value: value[1] == 9, segment_count.items())
        ]
        all_set_6_times = [
            i for i in filter(lambda value: value[1] == 6, segment_count.items())
        ]
        all_set_4_times = [
            i for i in filter(lambda value: value[1] == 4, segment_count.items())
        ]

        wire_mapping[seg_b] = "b"
        wire_mapping[seg_e] = "e"
        wire_mapping[seg_g] = "g"
        # segments d and a both get set 8 times. Segment d is known. Segment a has to
        # be the only unknown segment set 8 times.
        seg_a_candidates = [
            i
            for i in filter(
                lambda value: value[1] == 8 and seg_d not in value[0],
                segment_count.items(),
            )
        ]
        seg_a = next(
            filter(
                lambda value: value[1] == 8 and seg_d not in value[0],
                segment_count.items(),
            )
        )[0]
        wire_mapping[seg_a] = "a"

        # segment f is the only unknown segment in 4 at this point.
        seg_f_candidates = s_four - set([seg_a, seg_b, seg_e])
        seg_f = seg_f_candidates.pop()
        wire_mapping[seg_f] = "f"

        # segment c is the only unknown segment in 8 at this point.
        seg_c_candidates = s_eight - set([seg_a, seg_b, seg_d, seg_e, seg_f, seg_g])
        seg_c = (s_eight - set([seg_a, seg_b, seg_d, seg_e, seg_f, seg_g])).pop()
        wire_mapping[seg_c] = "c"

        # All wire mappings are now known.

        # extract the display numbers from the line.
        display_string = line[pipe_index + 1 :].strip()
        display_numbers = display_string.split(" ")

        def sort_and_map(original: str):
            mapped_letters = [n for n in map(lambda x: wire_mapping[x], original)]
            mapped_letters.sort()
            return proper_numbers.index("".join(mapped_letters))

        fixed_numbers = [n for n in map(sort_and_map, display_numbers)]
        final_number = int("".join(str(n) for n in fixed_numbers))
        sum_total += final_number
        print(final_number)
        print()
    print(f"sum total of all displayed numbers: {sum_total}")
