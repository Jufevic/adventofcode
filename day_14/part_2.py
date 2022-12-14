from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

SAND_SOURCE = (500, 0)


def coords(start, stop):
    """List coordinates between start and stop, inclusive."""
    step = 1 if start <= stop else -1
    return range(start, stop + step, step)

def points(line):
    """List all points making up a line."""
    match line:
        case (x1, y1, x2, y2) if x1 == x2:
            for y in coords(y1, y2):
                yield x1, y
        case (x1, y1, x2, y2) if y1 == y2:
            for x in coords(x1, x2):
                yield x, y1

# Create obstacle set, this includes rocks and sand
obstacles = set()
with open(INPUT_FILE) as f:
    for path_str in f.read().splitlines():
        path = []
        for coordinates in path_str.split(' -> '):
            x, y = map(int, coordinates.split(','))
            path.append((x, y))
        for (start_x, start_y), (end_x, end_y) in zip(path[:-1], path[1:]):
            for rock in points((start_x, start_y, end_x, end_y)):
                obstacles.add(rock)

void_limit = max(y for x, y in obstacles)
# Add infinite floor at y = void_limit + 2
for x in range(SAND_SOURCE[0] - void_limit - 2, SAND_SOURCE[0] + void_limit + 3):
    obstacles.add((x, void_limit + 2))

# Run the simulation
to_rest = 0
finished = False
while True:
    unit = SAND_SOURCE
    while True:
        x, y = unit
        # Try to fall down
        if (x, y + 1) not in obstacles:
            unit = (x, y + 1)

        # Try to fall one step down and to the left
        elif (x - 1, y + 1) not in obstacles:
            unit = (x - 1, y + 1)

        # Try to fall one step down and to the right
        elif (x + 1, y + 1) not in obstacles:
            unit = (x + 1, y + 1)
        
        # All movement possibilities exhausted, come to rest
        else:
            if unit in obstacles:
                finished = True
                break
            obstacles.add(unit)
            break
    if finished:
        break
    to_rest += 1

print(to_rest)
