from functools import cache
from pathlib import Path
from collections import defaultdict

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'

DIRECTIONS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

blizzards = defaultdict(list)

with open(INPUT_FILE) as f:
    lines = f.read().splitlines()
    height = len(lines)
    width = len(lines[0])
    for row, line in enumerate(lines):
        for col, tile in enumerate(line):
            if tile in DIRECTIONS:
                blizzards[(row, col)].append(DIRECTIONS[tile])

def move_blizzards(blizzards):
    """Move the blizzards in the grid"""
    new_blizzards = defaultdict(list)
    for (row, col), directions in blizzards.items():
        for (drow, dcol) in directions:
            new_row, new_col = row + drow, col + dcol
            if new_row == 0:
                new_row = height - 2
            elif new_row == height - 1:
                new_row = 1
            elif new_col == 0:
                new_col = width - 2
            elif new_col == width - 1:
                new_col = 1
            new_blizzards[new_row, new_col].append((drow, dcol))
    return new_blizzards

steps = 0
reachable_positions = {(0, 1)}
found_exit = False
while not found_exit:
    blizzards = move_blizzards(blizzards)
    reachable_next = set()
    for row, col in reachable_positions:
        for drow, dcol in (0, 0), (1, 0), (0, 1), (-1, 0), (0, -1):
            new_row, new_col = row + drow, col + dcol
            if (new_row, new_col) == (height - 1, width - 2):
                found_exit = True
                break
            if (new_row, new_col) == (0, 1):
                reachable_next.add((new_row, new_col))
            if ((new_row, new_col) not in blizzards
                    and 0 < new_row < height - 1
                    and 0 < new_col < width - 1):
                reachable_next.add((new_row, new_col))
    reachable_positions = reachable_next
    steps += 1

print(steps)
