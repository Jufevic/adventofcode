from collections import deque
from pathlib import Path
import numpy as np

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

points = set()
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        x, y, z = map(int, line.split(','))
        points.add((x, y, z))

def neighbours(point):
    x, y, z = point
    for dx, dy, dz in (
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)
    ):
        yield (x + dx, y + dy, z + dz)

# Compute exterior by BFS from a point we're sure is outside
np_points = np.array([list(point) for point in points])
min_x, min_y, min_z = np.amin(np_points, axis=0) - 1
max_x, max_y, max_z = np.amax(np_points, axis=0) + 1
start_pos = (min_x, min_y, min_z)
exterior = {start_pos}
frontier = deque([start_pos])
while frontier:
    current = frontier.popleft()
    for neighbour in neighbours(current):
        nx, ny, nz = neighbour
        if (neighbour not in exterior and neighbour not in points and 
                min_x <= nx <= max_x and min_y <= ny <= max_y
                and min_z <= nz <= max_z):
            frontier.append(neighbour)
            exterior.add(neighbour)

# Sum all faces facing exterior
total = 0
for point in points:
    for neighbour in neighbours(point):
        if neighbour not in points and neighbour in exterior:
            total += 1

print(total)
