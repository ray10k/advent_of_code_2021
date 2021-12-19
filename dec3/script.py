import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

print("first star:")

#approach: count the 1s per position plus the number of lines.
occurrences_of_one = []
report_values = []
linecount = 0
#got to read one item to figure out how long data is.
with open(input_path,"r") as input_file:
    first_line = next(input_file)
    #strip off the trailing linefeed.
    occurrences_of_one = [0]* (len(first_line)-1)

with open(input_path,"r") as input_file:
    for entry in input_file:
        linecount += 1
        entry = entry[:-1]
        report_values.append(entry)
        for position, value in enumerate(entry):

            occurrences_of_one[position] += 1 if value == "1" else 0

gamma = ""
epsilon = ""
threshold = linecount/2
print(",".join(str(one) for one in occurrences_of_one))

for character in occurrences_of_one:
    if character > threshold:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"
print(f"{gamma=}, {epsilon=}, result = {int(gamma,2) * int(epsilon,2)}")
 
print("second star:")
#The hard part starts here. Good thing you can filter()
oxygen = [val for val in report_values]
scrubber = [val for val in report_values]

def most_occurring(iterable,position,tiebreaker):
    occurrences = [0,0]
    for item in iterable:
        letter = int(item[position])
        occurrences[letter] += 1
    if occurrences[0] == occurrences[1]:
        return tiebreaker
    return occurrences.index(max(occurrences))

def final_check(the_list,position,tiebreaker):
    if len(the_list) > 2:
        return the_list
    if len(the_list) == 2:
        if the_list[0][position+1] == tiebreaker:
            return the_list[0]
        return the_list[1]
    return the_list[0]

for position in range(len(report_values[0])+1):
    #approach: Scan the list for the most (and least) occurring value, then filter based on that.
    if not isinstance(oxygen,str):
        most_oxy = str(most_occurring(oxygen,position,1))
        oxygen = [item for item in filter(lambda x: x[position] == most_oxy,oxygen)]
        oxygen = final_check(oxygen,position,"1")

    if not isinstance(scrubber,str):
        least_scr = "0" if most_occurring(scrubber,position,1) == 1 else "1"
        scrubber = [item for item in filter(lambda x: x[position] == least_scr,scrubber)]
        scrubber = final_check(scrubber,position,"0")
    
    if isinstance(oxygen,str) and isinstance(scrubber,str):
        break

print(f"{oxygen=} ({int(oxygen,2)}). {scrubber=} ({int(scrubber,2)}). Life support rating = {int(oxygen,2)*int(scrubber,2)}")
