from pathlib import Path
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

DIRECTIONS = {
    'L': (-1, 0),
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1)
}

head = (0, 0)
tail = (0, 0)
visited = {tail}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        direction, steps = parse('{} {:d}', line)
        dx, dy = DIRECTIONS[direction]
        for _ in range(steps):
            new_head = head[0] + dx, head[1] + dy
            if max(abs(new_head[0] - tail[0]), abs(new_head[1] - tail[1])) > 1:
                tail = head
                visited.add(tail)
            head = new_head

print(len(visited))