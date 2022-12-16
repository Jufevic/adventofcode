from pathlib import Path
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

ROW_OF_INTEREST = 2_000_000
# ROW_OF_INTEREST = 10

no_beacon = set()
beacon = set()
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = parse(
            'Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', line)
        if beacon_y == ROW_OF_INTEREST:
            beacon.add(beacon_x)
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        width = distance - abs(ROW_OF_INTEREST - sensor_y)
        for x in range(sensor_x - width, sensor_x + width + 1):
            no_beacon.add(x)

print(len(no_beacon - beacon))