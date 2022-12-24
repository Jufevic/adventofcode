from collections import defaultdict, namedtuple
from pathlib import Path
from functools import cache
from itertools import chain, product
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

START_VALVE = 'AA'

connections = {}
flows = {}
with open(DEMO_INPUT_FILE) as f:
    for line in f.read().splitlines():
        if result := parse(
            'Valve {} has flow rate={:d}; tunnel leads to valve {}',
            line
        ):
            valve, flow, tunnel = result
            flows[valve] = flow
            connections[valve] = [tunnel]
        else:
            valve, flow, tunnels = parse(
                'Valve {} has flow rate={:d}; tunnels lead to valves {}',
                line
            )
            flows[valve] = flow
            connections[valve] = tunnels.split(', ')

# BFS to find out all distances between pairs of working valves
distances = defaultdict(dict)
working_flows = {valve: flow for valve, flow in flows.items() if flow > 0}
for start in chain(['AA'], working_flows.keys()):
    distance = 0
    frontier = [start]
    visited = set()
    steps = 1
    while frontier:
        new_frontier = []
        for current in frontier:
            for neighbour in connections[current]:
                if neighbour not in visited:
                    new_frontier.append(neighbour)
                    visited.add(neighbour)
                    if neighbour in working_flows:
                        distances[start][neighbour] = steps
        frontier = new_frontier
        steps += 1

@cache
def max_flow(minutes, current_pos, closed):
    if minutes <= 0 or not any(closed):
        return 0

    max_so_far = 0
    for valve, flow in working_flows.items():
        # Check if valve is already opened
        if not(getattr(closed, valve)):
            continue
        distance = distances[current_pos][valve]
        remaining_time = minutes - distance - 1
        # Check if we can get to this valve in time
        if remaining_time <= 0:
            continue
        # Try to open this valve next
        new_closed = closed._replace(**{valve: False})
        result = max_flow(remaining_time, valve, new_closed)
        result += remaining_time * flow
        max_so_far = max(max_so_far, result)

    return max_so_far

# Namedtuples can be cached, dicts cannot. 
ClosedValves = namedtuple('ClosedValves', working_flows.keys())
max_score = 0
for partition in product((True, False), repeat=len(working_flows)):
    partition_score = 0
    you = ClosedValves(**{valve: state for valve, state in zip(working_flows, partition)})
    elephant = ClosedValves(**{valve: not state for valve, state in zip(working_flows, partition)})
    max_score = max(max_score, max_flow(26, 'AA', you) + max_flow(26, 'AA', elephant))

print(max_score)
