# Why did you put all the characters into a string? The lines
# are syntactically relevant; you need to analyze the first character
# of each line, then the second character of each line, etc.
# Is this the original puzzle input, or did you pre-process it somehow?
Decims = [
    "1110110011101001001100110011101010000101100000001001010010110000001010000111100110001100111001000011001100110011000001001011100111111001010110001100001001101000011011100001011011111000011010000011100000000000011100000110010100001101110101000111100100100101000110110111100000000101010111100010100000011111101111100010100100010110111001011001110101001100111100110000001101000001100110001111000010110111000000010011101000000010000110100100111100000000100101111001110001011011011000011110101000110111101011110010110100110001000000001110100111010110000001010011110011000000010111000011000011001111010100011100101011001101101110101110110010101101100000100010111010011001000001000011011010111001001010001110010111101001011111011010110111110011101001000011000110100010010101001110101110010010011001010010100100111011100010111100111011111010101000101000100110111011011100000111111000101110111010000000111000111011000101011110110000101110100110101101000110100001000000110010111110011011010001000100000111111011",
    "0011000000100001010000100000000001011110001100110111111000011110111111100001110000010011110110111101101111010111101111100001101110001001011000111001011110111000101000001000101000101110110101010010110001011110100001101001011000011101000011100010111110000110001110011010111011100101000011000011001001111101100101100000011001110001110010011011110101100111111101010101101110100101001111000100000110110000001011001101111000010001101100010001011011000111010110011111010011011101010100111010111000111101110101101000101000100101011111101000001011101010011010011111111011110100011110100111001110010011000001000001111111101111000010010001100100111010100010011010110110001111011011101101111111011111010111011110001110001100010010010010101001010110110111000010110111000011101111001111100011000001001011001100001011110001000000011000001010010101101111110010001110011010001110111101001110110000110100011111110110001000111000100100100100010101110011011011000000001111100110000000000101101110101111011111100110001001",
    "1000011101011110010001010000101011100000110010011000101001001010011101110101111110101100000110101010100000110011001000110010110110101001010011100010100111001111000010101100110101001110011000001110001011010111010101011010100101010101000111111011110001110001000001001000011000010001001011000010111011000010011011110000110000001101101101010010011000010001001011111101000100101010111101001110100010111100100111110000010110011111100011011011000111000000110100010010001001110100111100111010001110100111010000100011011010110000101001101010111100110010011001110010110010001011110000001001110011111001101111011101100111000011000011101101001001010010100001010100110100110111000010011011100000011110100011001110011111101000110110101000010000011011110101110010000101111001001010011111000110100011011100110110011111101001111011001001110011010010101110011010011111011011100011001101110011011011110111110101011101110000011101101000111101111110010000110001001101001110101101101111100010001001101110101001101100100101",
    "0000110110001010101000001000000011000001001001100011100111011101110000010101001011000101101110101110110100111110011101110111110011011011011000111101011100110001011111010000011110110101001010111101110001110111100000110001101100001000000001000011010000010111011000010111111110110101011100010000011011001110011000010000011100111100101111001101000100011111100111001111000001011101000001111101011110000110011100101001100001101101101000111111001011110001000010111011001011000101111001000000010110010010010010111101011100010010111101011110111100000100010000111001011100100111010100110101110001010110010110010111110110100110001000010011000001001110111100010111110101000001001001000110101000000011000110000010010101011111000010101110010000111011011101000010011101001111100100011001001010110111001000111100001111001101101101111110011000010011011010000000011010001110011001011111110100101010110011010001111011001111111010110011001100110010011100011100111001111101101000000010010011011110010111010110110111101101",
    "0000111001101100000001011111011000101100110010101101110110101001001011100111011110000011011010110000000010001001111101111001100110111111000000010011010010001000001010011110010100011000111001101101011010110000111101101010110110110100101101000111101110001001000110111110101100000101000000100111011100101011101000010110010110000010011110111011100110010100001000111110000111110111110111110000010001001111101110011000011000100110001111011010010001100000110110101100011010101101111000001111101001000110101101111000011011111110100101100100111111100011011001011110110000111100010010001000010100000001011101010110111100111011100100111010101110110100000011010100111100011001101010111001001100110010010101101001101110000100000110000010000110101000010000100011110001011011100100010111100010101100001100010000011111111101001011001010011110011111100000110111101011011110011000011101010110101111100100101101101000111011100011100101010110010101010010011000000000001111000010100011111001011111100011010010000100110001",
    "1000100101100010011011000100011001000011111110110011100111110000000010110111100011100100000010100111001010101001010110101100110010000110011111000001010101110010010010011011100100111100100011000001110111000100000101010110111000001000111110011010010111001000001100011111001110100111010111000111100101100010010101010111011111001101101101011110011010011101110110011000101111101011110010110110101100010011011101001111101011111101111000000000101110010000011001011110110101000011001000110010010100110000010000000001100111100010000000011010010000001100111010011010111011111110111011110110111000101100001110001101101110101001110000011111100001001000001000101001001001010011011001001010101011010001100110010101010011101010100010100110111000001000110010011110101111000000001011001111100011000101101011101111111011000011001101010110110010110000010100111111010101110101110100110100100100110110000100010100000011001011011100001100100100111011110111111101110001001111110000100110011010000001011010110101010000100010",
    "0101101100110010010011001011111111010101001010100000101100011111010100100001101110001110110000100011100000011011001100001001110000111101010011100000111100000000110111000110011101100101110011001100001100001110101110010100011001111101010000001000110000001010110001000011110110111100100100000001000100110110011111101111010000110000110010111110000010000011010010001111101010001001110100111110101001000000001100010111110000010110000000110110101110111000100010110111011011111101000110001100001111010001000001010000011011110000111000100111111101010000100100100001010001000100111011111100010110011101011001010011011110110100110011011010000011101000011010101001100100000010110111101110110001111110110010011100001010100011101110001100010001010000110100001110101001111100111001110001010011111000100100111010100011001010001000011000111000000001001100001101000111001110110110011000101110111001100100101010110100000110000110011100010001100100101101001111111101111110111110111111111110110001111111110100101100111101",
    "1010001101111001110000011111110010111111111111010011110101100000011110111010011100101111001111101001011010111001110010100001110100010001001101100010101110111110011010110110110101000011100011000110100100111100111000110111010101110001111000100011111000111111110101101101111011010011010010001001100010011111101110101100100010000001010001101100111001011100010010101110001001110110001100001110000010110011101011011110101010100110100010011010001100111000011111011010001111100101111101010000110001000001111101000111101001010111011110110011111111000011111010001110001111100010100100101010001101000001111111001010000001100011101011010000010000110101100110101110111101100011101010010101001000000101100011101010100101101011100011011101000010000010001100011001000010010100000011101100101111101001100101000000001001011011000101001001100010001001011011011010100110111000011110111001010101111000101100110111111000110101011101100000000111100101101001001001011100101110011110111101111101100001111001100111000111000100",
    "1110101011001001110101100100001111100110100010000110010000000011111111100101010110111001010010010011001101010001011101000100010000100111111110011001100000011100001100101100110011010010101000010111001000010000111101111111010101101111001111011110011000000100110011010110111110101001000010101110100000101010111011001100101111110000001100011101000100001111000000101111011000100100000111111101100111001111110000101110111100011101110010100000111111001001001011001110010111010111011010110000110100111000010010001011111001001010110010001010111101101101101010001100011011010011101101000100001000100100011000001010100101100100010110100110101101000001011111010101011111100100100111001101010111101011000111011101010101110111010100110110010101001100111011011101001011101000010010101100111001111010001011011010011010111100000100010111101101000000100010010101100110111110000011111101001010010010000110111101110011000001101000001100101010001010011101011011100011111101110110011000010001010111010001010111100011011011",
    "0001100110100011000000110001101101111111000001111110111100000001100011110110111000011010010000010011100011101010011010010100000001100001111101000111001001011010010111111001000001101100100101011100110100110111011010101011110111100101110110100010000010000101010010001000011110010110001001100100110111000100111001001100111111101000010000011001000101000011011101101111100011101011011001110010011110110101010000111110101011110100001100010010101100101101101100001100000001101100011100011110001001010100101110000010010000100010101010000110100101110100110100111101101111101100010111000100001001101001001111100101011001001100110000111000101101011000101001011110100000100011011101001100011111101000011100000001100100010101110111010001101101011110100101000000101111001000111100001000000010011011111011100110110011100001111110000110011110101110001011111000001101100110001011001110000011101110011101101001111101010101111011110001110100100110101110101111010011010001011010000000010111100110100100010011101110111000",
    "0101101101011001000010110001110010111001000010111000111110101001010001000101001001000101000001011100110111000100101111101000110110101001000101110010101111010100101111000100010010001010001010011101000001000001001110000001110101011000011100101001001001000010000101110010100001111001000101001010000100011010001001100111101011110010111000100000111111100111011001101101011111100101101011010110101001100111011101100101101011100000000000011001110001111101011000110111000110100100111110111000110110011010111101110101101101010010101110111111110001100111110110000111001110110011110110100111110000110010100011110001010011100100001010011010100010111010011011110010101101111001101110101011000111111101110110100011110001000011001011101111111010011111010010101000010011011011101011111011100100010100111100110000001000000000110001100101101100100100000101000110000100110110111111100010000101111001000000010100101000100000010010111111100111001001010110001000100101101000100010000100110011110110111001000000001011111111",
    "0011000000101101011011100111101010101010010101010010011010010110001001010100110101110011101110101001000010010000100100100000101010101000110011111110110110100001110001110110100111010110110100100010000101100101111111000101011010001100110001001101011100100101111110111111110000010010101000011010011001101011100110001110001011110110010010111011011011101100011010111100100101101010101000101101010001101010100010100111100110101000111010011010101001001101110000000001011111011011000010001111010100000100000010011100001110000001000100110000111101000110001010011101011110111111100001101011110111100101111001111000110010011000011001001100101101100010111110011001011000011010100011110011100111011110100100111001001000101101000000101100011101010100101100001101101101111100001011001001110000111110101001100000111110010111001110010011100111100001110111000001011111110100111010000100110101111011110110011011000000100001001101100010001111100010000001000100000100011110110101101000000111100111010100110011001110111010",
]
# Don't use sinlge-character variables, makes your code harder to understand.
b = 0
#Since you're essentially iterating over each string in Decims, use "for input in Decims:" instead.
for x in range(12):
    input = Decims[b]
    # again, don't use single-character variables.
    D = {}
    # I recommend against using keywords and built-in function names like list
    # for variable names. And yes, that includes those words with a capital letter.
    List = []
    # This line makes the line above a no-op; The line above does effectively nothing.
    List = list(input)
    # don't use single-character variables, round 3.
    a = 0
    #'input' is already a string. You can iterate over a string without turning it
    # into a list first. Replace with "for character in input:"
    for character in List:
        #'List[a]' is a code smell in this case. Just use "character" instead.
        D[character] = D.get(List[a], 0) + 1
        # unnecessary in its entirety, remove.
        a += 1
    print(D)
    #Unnecesary. Remove.
    b += 1
