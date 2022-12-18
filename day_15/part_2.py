from itertools import combinations
from pathlib import Path
from parse import parse
from sympy import (
    Eq,
    Abs,
    And,
    solve,
    symbols,
    piecewise_fold,
    Piecewise,
)

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

LOWER_COORD = 0
HIGHER_COORD = 4_000_000

x, y = symbols('x y', integer=True)

# Parse input data
sensors = {}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = parse(
            'Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', line)
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y) + 1
        sensors[sensor_x, sensor_y] = distance

# Select candidates based on the assumption that there is only one position
# where the beacon could possibly be: it must be somewhere at the intersection
# between at least four sensor exclusion zones.
candidates = set()
for ((s1_x, s1_y), d1), ((s2_x, s2_y), d2) in combinations(sensors.items(), 2):
    distance = abs(s1_x - s2_x) + abs(s1_y - s1_y)
    if abs(d1 - d2) < distance < d1 + d2 and (
        (s1_x + s1_y + d1 + s2_x + s2_y + d2) % 2 == 0):
        eq1 = Eq(Abs(x - s1_x) + Abs(y - s1_y), d1)
        eq2 = Eq(Abs(x - s2_x) + Abs(y - s2_y), d2)
        pw = piecewise_fold(And(eq1.rewrite(Piecewise), eq2.rewrite(Piecewise)))
        for e, co in pw.args:
            s = solve(e.args)
            if co.subs(s) and s and y in s:
                if (LOWER_COORD <= s[x] < HIGHER_COORD and
                        LOWER_COORD <= s[y] < HIGHER_COORD):
                    candidates.add((s[x], s[y]))

# Exclude impossible candidates
solution = None
for candidate in candidates:
    for (sensor_x, sensor_y), distance in sensors.items():
        if abs(candidate[0] - sensor_x) + abs(candidate[1] - sensor_y) < distance:
            break
    else:
        solution = candidate
        break

print(4_000_000 * solution[0] + solution[1])
