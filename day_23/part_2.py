from pathlib import Path
from collections import defaultdict

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'
ELF = '#'
EMPTY = '.'

# North, South, West, East
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

elves = set()
with open(DEMO_INPUT_FILE) as f:
    for row, line in enumerate(f.read().splitlines()):
        for col, tile in enumerate(line):
            if tile == ELF:
                elves.add((row, col))

round = 1
while True:
    # First half: propositions
    propositions = {}
    contestants = defaultdict(int)
    for elf in elves:
        row, col = elf
        neighbours = set()
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                if (drow, dcol) != (0, 0):
                    if (row + drow, col + dcol) in elves:
                        neighbours.add((drow, dcol))
        # No neighbour: do not move
        if not neighbours:
            propositions[elf] = elf
        # If possible, propose to move in the wanted direction.
        else:
            for drow, dcol in DIRECTIONS:
                if drow == 0:
                    for new_row in range(-1, 2):
                        if (new_row, dcol) in neighbours:
                            break
                    else:
                        propositions[elf] = (row + drow, col + dcol)
                        contestants[row + drow, col + dcol] += 1
                        break
                else:
                    for new_col in range(-1, 2):
                        if (drow, new_col) in neighbours:
                            break
                    else:
                        propositions[elf] = (row + drow, col + dcol)
                        contestants[row + drow, col + dcol] += 1
                        break
        # Finally, if the elf is completely surrounded, do not move
        if elf not in propositions:
            propositions[elf] = elf

    # Second half: conflict(s) resolution(s)
    new_elves = set()
    for elf, proposition in propositions.items():
        if contestants[proposition] <= 1:
            new_elves.add(proposition)
        else:
            new_elves.add(elf)

    if new_elves == elves:
        print(f'{round=}')
        break
    elves = new_elves
    round += 1
    DIRECTIONS = DIRECTIONS[1:] + [DIRECTIONS[0]]
