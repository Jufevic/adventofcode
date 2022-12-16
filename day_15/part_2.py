from collections import Counter
from pathlib import Path
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

LOWER_COORD = 0
HIGHER_COORD = 4_000_000
# HIGHER_COORD = 20

def coords(start, stop):
    """List coordinates between start and stop, exclusive."""
    step = 1 if start <= stop else -1
    return range(start, stop, step)

def points(line):
    """List all points making up a line."""
    x1, y1, x2, y2 = line
    return [(x, y) for x, y in zip(coords(x1, x2), coords(y1, y2))]

frontier = Counter()
# sensor[pos] = minimum_distance
sensors = {}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = parse(
            'Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', line)
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y) + 1
        sensors[sensor_x, sensor_y] = distance
        path = [
            [sensor_x - distance, sensor_y],
            [sensor_x, sensor_y + distance],
            [sensor_x + distance, sensor_y],
            [sensor_x, sensor_y - distance],
            [sensor_x - distance, sensor_y],
        ]
        for start, end in zip(path[:-1], path[1:]):
            for point in points((*start, *end)):
                if all((LOWER_COORD <= coord <= HIGHER_COORD) for coord in point):
                    frontier[point] += 1

candidates = [position for position, count in frontier.items() if count >= 4]
solution = None
for candidate in candidates:
    for (sensor_x, sensor_y), distance in sensors.items():
        if abs(candidate[0] - sensor_x) + abs(candidate[1] - sensor_y) < distance:
            break
    else:
        solution = candidate
        break

print(4_000_000 * solution[0] + solution[1])
