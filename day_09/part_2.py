from pathlib import Path
from parse import parse
from itertools import chain
import numpy as np

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
DEMO_INPUT_2_FILE = Path(CURRENT_FILE.parent, 'demo_input_2.txt')

DIRECTIONS = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
}

knots = [(0, 0) for _ in range(10)]
visited = {knots[-1]}

def visualize(knots, visited):
    """Add helper visualization"""
    min_row = float('inf')
    min_col = float('inf')
    max_row = -float('inf')
    max_col = -float('inf')
    for knot_row, knot_col in chain(knots, visited):
        min_row = min(knot_row, min_row)
        min_col = min(knot_col, min_col)
        max_row = max(knot_row, max_row)
        max_col = max(knot_col, max_col)
    grid = np.full((max_row - min_row + 1, max_col - min_col + 1), '.')
    for pos_row, pos_col in visited:
        grid[min_row - pos_row - 1, pos_col - min_col] = '#'
    grid[min_row - 1, - min_col] = 's'
    for i, (pos_row, pos_col) in reversed(list(enumerate(knots[1:], start=1))):
        grid[min_row - pos_row - 1, pos_col - min_col] = str(i)
    head_row, head_col = knots[0]
    grid[min_row - head_row - 1, head_col - min_col] = 'H'
    grid = np.flipud(grid)
    print('\n'.join(''.join(line) for line in grid))
    print()

with open(DEMO_INPUT_2_FILE) as f:
    for line in f.read().splitlines():
        direction, steps = parse('{} {:d}', line)
        drow, dcol = DIRECTIONS[direction]
        for _ in range(steps):
            new_knots = []
            for knot in knots:
                # Head knot
                if not new_knots:
                    new_knots.append((knot[0] + drow, knot[1] + dcol))
                    continue
                prev_knot = new_knots[-1]
                if max(abs(prev_knot[0] - knot[0]), abs(prev_knot[1] - knot[1])) > 1:
                    if prev_knot[0] == knot[0] or prev_knot[1] == knot[1]:
                        # Move horizontally or vertically towards knot
                        step_row = (prev_knot[0] - knot[0]) // 2
                        step_col = (prev_knot[1] - knot[1]) // 2
                    else:
                        # Move diagonally towards knot
                        step_row = 1 if prev_knot[0] > knot[0] else -1
                        step_col = 1 if prev_knot[1] > knot[1] else -1
                    new_knots.append((knot[0] + step_row, knot[1] + step_col))
                # Do not move
                else:
                    new_knots.append(knot)
            visited.add(new_knots[-1])
            knots = new_knots
        visualize(knots, visited)

print(len(visited))
