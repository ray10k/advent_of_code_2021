import pathlib

input_path = pathlib.Path(__file__).parent / "input.txt"

# Things to consider: I need some format of bingo card that is:
# - easy to scan for the occurrence of one number
# - can scan both columns and rows.
# Initial idea: lists, track drawn numbers in a set.


class BingoCard:
    def __init__(self, width, height, values) -> None:
        self.card_numbers = [val for val in values]
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        # TODO: format the card nicely.
        return "{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}".format(
            *self.card_numbers
        )

    def check_bingo(self, previous_numbers, latest_number) -> bool:
        if latest_number not in self.card_numbers:
            return False
        index = self.card_numbers.index(latest_number)
        # find the row start; on a 5x5 card, that is 0,5,10,15 or 20
        row_start = self.height * (index // self.width)
        # find the column start; on a 5x5 card, that is 0,1,2,3 or 4
        column_start = index % self.width
        # find the column end; on a 5x5 card, that is 20,21,22,23 or 24
        column_end = column_start + (self.width * (self.height - 1)) + self.width
        win = True

        # check if the row with the new number is a win.
        for cell in self.card_numbers[row_start : row_start + self.width]:
            if cell not in previous_numbers and cell != latest_number:
                win = False
                break
        if win:
            return True

        # check if the column is a win
        for cell in self.card_numbers[column_start : column_end : self.width]:
            if cell not in previous_numbers and cell != latest_number:
                return False

        # if the previous loop didn't return False, there must be a winner.
        return True

    def calculate_score(self, drawn_numbers):
        sum_total = 0
        for cell in self.card_numbers:
            if cell not in drawn_numbers:
                sum_total += int(cell)
        return sum_total

    def show_marked(self, drawn_numbers):
        marked_card = [
            "**" if num in drawn_numbers else num for num in self.card_numbers
        ]
        return "{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}\n{:>2} {:>2} {:>2} {:>2} {:>2}".format(
            *marked_card
        )

    def card_total(self):
        return sum(int(num) for num in self.card_numbers)


print("quick checks:")
test_card = BingoCard(5, 5, range(26))
row_drawn = set([0, 1, 2, 3, 4])
col_drawn = set([0, 5, 10, 15, 20])
print(
    f"row test:\n{test_card.show_marked(row_drawn)}\n{'winner' if test_card.check_bingo(row_drawn,0) else 'loser'}\n",
    f"column test:\n{test_card.show_marked(col_drawn)}\n{'winner' if test_card.check_bingo(col_drawn,0) else 'loser'}\n",
)

print("first star:")
playing_cards = []
pulled_numbers = None

with open(input_path, "r") as input_file:
    # First line is all the numbers drawn, as a comma-separated string.
    # Store as a string for now.
    pulled_numbers = next(input_file).split(",")
    # Strip the /n off the last item.
    pulled_numbers[-1] = pulled_numbers[-1][:-1]

    # Python does not give an easy way to tell if a file has more lines remaining.
    # Python *does* have a way to tell you that you went past the end of the file.
    # Blindly grope ahead until something breaks, then.
    try:
        while True:
            # Format of a single bingo card: 1 empty line, then 5 lines of space-separated numbers
            # that *may* start with a space if the first number is a single digit.
            next(
                input_file
            )  # Will raise the StopIteration error if the file is exhausted.
            # make a single string containing the entire bingo card. zip() terminates if any
            # of the iterators provided is exhausted, so I use that to pull five lines in one go.
            card_string = " ".join(line for _, line in zip(range(5), input_file))
            card_numbers = []
            # next step: read the numbers in order, discarding anything that is not a number.
            temp_number = ""
            for character in card_string:
                if not character.isdigit() and temp_number != "":
                    card_numbers.append(temp_number.strip(" \n"))
                    temp_number = ""
                elif character.isdigit():
                    temp_number += character
            playing_cards.append(BingoCard(5, 5, card_numbers))
    except StopIteration:
        print(f"Last card read. Total cards: {len(playing_cards)}")

# Time to start playing the game. Draw numbers one by one, add them to the set of drawn
# numbers, and check each card for a bingo.
previous_numbers = set()
last_drawn = None
winner = None
for drawn in pulled_numbers:
    for card in playing_cards:
        if card.check_bingo(previous_numbers, drawn):
            winner = card
            last_drawn = drawn
            break
    previous_numbers.add(drawn)
    if winner is not None:
        break
print(
    f"Winning card:\n{winner!r}\nWinner, marked:\n{winner.show_marked(previous_numbers)}"
)
print(
    f"Won after drawing {len(previous_numbers)} numbers. Winning card scored {int(last_drawn) * winner.calculate_score(previous_numbers)}. Last number drawn {last_drawn}\n"
)


print("second star:")
# Since the above search for a winning card does not *change* the cards, there's no need
# to rebuild the cards from the file.
# Loop over the list of cards and discard winners, until one card remains.
drawing_iterator = pulled_numbers.__iter__()
previous_numbers = set()
while len(playing_cards) > 1:
    last_drawn = next(drawing_iterator)
    playing_cards = [
        card
        for card in filter(
            lambda x: not x.check_bingo(previous_numbers, last_drawn), playing_cards
        )
    ]
    previous_numbers.add(last_drawn)
winner = playing_cards[0]
# At this point, there is one card left but it may not yet have won. Keep going until a win.
while not winner.check_bingo(previous_numbers, last_drawn):
    last_drawn = next(drawing_iterator)
    previous_numbers.add(last_drawn)


print(f'"winning" card: \n{winner!r}\nmarked:\n{winner.show_marked(previous_numbers)}')
print(
    f'"won" after drawing {len(previous_numbers)} numbers. "winning" card scored {int(last_drawn) * winner.calculate_score(previous_numbers)}'
)
