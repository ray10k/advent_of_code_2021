import pathlib
from collections import namedtuple
from math import prod
from typing import List

input_path = pathlib.Path(__file__).parent / "input.txt"
hex_input, binary_input = "", ""

with open(input_path, "r") as input_file:
    # The entire file is a single line.
    hex_input = next(input_file).strip()
# Ensure that the padding is right.
if len(hex_input) % 2 == 1:
    hex_input += "0"
binary_input = bytes.fromhex(hex_input)

# Test input, should be a single literal of 2021
# binary_input = bytes.fromhex("D2FE28")

# Test input, should yield 3. Tests sum(1,2)
# binary_input = bytes.fromhex("C200B40A82")
# Test input, should yield 54. Tests prod(6,9)
# binary_input = bytes.fromhex("04005AC33890")
# Test input, should yield 7. Tests min(7,8,9)
# binary_input = bytes.fromhex("880086C3E88112")
# Test input, should yield 9. Tests max(7,8,9)
# binary_input = bytes.fromhex("CE00C43D881120")
# Test input, should yield 1. Tests 5 < 15
# binary_input = bytes.fromhex("D8005AC2A8F0")
# Test input, should yield 0. Tests 5 > 15
# binary_input = bytes.fromhex("F600BC2D8F")
# Test input, should yield 0. Tests 5 == 15
# binary_input = bytes.fromhex("9C005AC2F8F0")
# Test input, should yield 1. Tests 1 + 3 == 2 * 2
# binary_input = bytes.fromhex("9C0141080250320F1802104A08")

# Format: 3-bit version field, 3-bit type field.
# type 4 is a literal value, any other is an operator.
# if the first bit in an operator is 0:
# 15 bits of data length.
# if the first bit in an operator is 1:
# 11 bits of segment count.
# a literal value is represented as following:
# 0+ literal segments starting with 1 plus 4 bits of data
# 1 literal segment starting with 0 plus 4 bits of data.
# Trailing zeroes can be ignored.
# Investigate: Are there ever more than 3 trailing zeroes?
# The message is encoded to bytes, so at worst there are 7
# bits padding needed :(
# Worst case, the padding gets interpreted as a v0, t0 header
# and an operator of bit-encoded length, but without actual length.
# Best case, there is 0 padding and the total message length is a
# multiple of 8 bits.

# a package header. Always six bits long, 3 bit version and 3 bit type.
Head = namedtuple("Header", "ver type_")
# An operator. 1 bit type (bit stride or package count) and 11/15 bit length.
Oper = namedtuple("Operator", "type_ length bit_length head")
# A number literal. bit length is some multiple of 5.
Numb = namedtuple("Number_literal", "value bit_length head")

# Need the MSB each time!
def bit_iterator(byte_source: bytes):
    for byte in byte_source:
        for _ in range(8):
            yield 1 if (byte & 0x80) == 0x80 else 0
            byte = byte << 1


def decode_header(bit_source):
    try:
        version = 0
        for _ in range(3):
            version = version << 1
            version += next(bit_source)
        type_ = 0
        for _ in range(3):
            type_ = type_ << 1
            type_ += next(bit_source)
        # Might still be end-of-message padding,
        # but that can be handled elsewhere.
        return Head(version, type_)
    except StopIteration:
        # Definitely end-of-message padding.
        return None


def decode_operator(bit_source, header):
    # Small chance, but still a chance, of encountering
    # the end-of-message padding. Either when fetching
    # the type bit, or when fetching the first bit of
    # the length.
    try:
        len_type = next(bit_source)
        if len_type == 1:
            seg_count = 0
            for _ in range(11):
                seg_count = seg_count << 1
                seg_count += next(bit_source)
            return Oper(1, seg_count, 18, header)
        bit_count = 0
        for _ in range(15):
            bit_count = bit_count << 1
            bit_count += next(bit_source)
        return Oper(0, bit_count, 22, header)
    except StopIteration:
        # Hit the end-of-message padding.
        return None


def decode_int_literal(bit_source, header):
    # No way for an int literal to encounter the
    # end-of-message padding.
    more_segments = True
    segments = []
    while more_segments:
        more_segments = next(bit_source) == 1
        seg = 0
        for _ in range(4):
            seg = seg << 1
            seg += next(bit_source)
        segments.append(seg)
    value = 0
    for seg in segments:
        value = value << 4
        value += seg
    return Numb(value, (5 * len(segments)) + 6, header)


decoded = []
byte_source = bit_iterator(binary_input)

while True:
    head = decode_header(byte_source)
    if head == None:
        break
    if head.type_ == 4:
        num = decode_int_literal(byte_source, head)
        decoded.append(num)
    else:
        opr = decode_operator(byte_source, head)
        if opr == None:
            break
        decoded.append(opr)

print(f"Finished reading the bytes. {len(decoded)} parts identified.")

print("first star:")
version_sum = 0
for part in decoded:
    version_sum += part.head.ver
print("Sum of versions:", version_sum)

print("second star:")
mnemonics = ["sum", "pro", "min", "max", "lit", "grt", "lss", "equ"]
for part in decoded:
    print(mnemonics[part.head.type_], end=" ")
print()

# I have a series of operations. I need a result for some complicated
# calculation. Solution: Work backwards from the end, putting stuff
# on a stack and pop back off as needed. Just reverse-Polish it.

operand_functions = [sum, prod, min, max]

Ival = namedtuple("Intermediary_value", "value bitlength")

operand_stack: List[Ival] = []
for part in decoded[::-1]:
    if part.head.type_ == 4:
        # numerical value; guaranteed to require no further thought.
        operand_stack.append(Ival(part.value, part.bit_length))
        continue
    if part.head.type_ < 4:
        # sum, product, minimum or maximum. All of these take at least 1
        # operand. Additionally, any of these can have two representations
        # of the operands needed: a number of packages, or a number of bits
        # Make a list of operands, then run the calculation.
        temp_stack: List[Ival] = []
        bitcount = 0
        if part.type_ == 0:
            # length in bits.
            while bitcount < part.length:
                temp = operand_stack.pop()
                bitcount += temp.bitlength
                temp_stack.append(temp)
        else:
            # length in packages
            for _ in range(part.length):
                temp_stack.append(operand_stack.pop())
                bitcount += temp_stack[-1].bitlength
        # Order is irrelevant for these operations.
        res_value = operand_functions[part.head.type_](t.value for t in temp_stack)
        operand_stack.append(Ival(res_value, bitcount + part.bit_length))
        continue
    # Finally, 5, 6 and 7 are comparisons that always take two operands.
    left = operand_stack.pop()
    right = operand_stack.pop()
    res_value = 0
    if part.head.type_ == 5 and left.value > right.value:
        res_value = 1
    if part.head.type_ == 6 and left.value < right.value:
        res_value = 1
    if part.head.type_ == 7 and left.value == right.value:
        res_value = 1
    operand_stack.append(
        Ival(res_value, left.bitlength + right.bitlength + part.bit_length)
    )

print(
    f"Final result: {operand_stack[0].value}. {len(operand_stack)} item(s) left on the operand stack"
)
