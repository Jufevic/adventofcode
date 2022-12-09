from pathlib import Path
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
# Demo input 2 file answer is 35, not 36 as indicated in the problem description
DEMO_INPUT_2_FILE = Path(CURRENT_FILE.parent, 'demo_input_2.txt')

DIRECTIONS = {
    'L': (-1, 0),
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1)
}

knots = [(0, 0) for _ in range(10)]
visited = {knots[-1]}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        direction, steps = parse('{} {:d}', line)
        dx, dy = DIRECTIONS[direction]
        for _ in range(steps):
            new_knots = []
            for knot in knots:
                # Head knot
                if not new_knots:
                    new_knots.append((knot[0] + dx, knot[1] + dy))
                    continue
                prev_knot = new_knots[-1]
                if max(abs(prev_knot[0] - knot[0]), abs(prev_knot[1] - knot[1])) > 1:
                    if prev_knot[0] == knot[0] or prev_knot[1] == knot[1]:
                        # Move horizontally or vertically towards knot
                        step_x = (prev_knot[0] - knot[0]) // 2
                        step_y = (prev_knot[1] - knot[1]) // 2
                        new_knots.append((knot[0] + step_x, knot[1] + step_y))
                    else:
                        # Move diagonally towards knot
                        diag_x = 1 if prev_knot[0] > knot[0] else -1
                        diag_y = 1 if prev_knot[1] > knot[1] else -1
                        new_knots.append((knot[0] + diag_x, knot[1] + diag_y))
                # Do not move
                else:
                    new_knots.append(knot)
            visited.add(knots[-1])
            knots = new_knots

print(len(visited))
