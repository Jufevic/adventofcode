from collections import defaultdict
from pathlib import Path
from copy import copy
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

START_VALVE = 'AA'

connections = {}
flows = {}
with open(INPUT_FILE) as f:
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

# BFS to find out all distances between pairs of edges
distances = defaultdict(dict)
working_valve = [valve for valve, flow in flows.items() if flow > 0]
for start in ['AA'] + working_valve:
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
                    if neighbour in working_valve:
                        distances[start][neighbour] = steps
        frontier = new_frontier
        steps += 1

def max_flow(minutes, flows, current_pos, distances):
    if minutes <= 0 or not flows:
        return 0

    max_so_far = 0
    for valve in flows:
        distance = distances[current_pos][valve]
        if distance + 1 >= minutes:
            continue
        # Try to open this valve next
        new_flows = copy(flows)
        flow = new_flows.pop(valve)
        result = max_flow(minutes - distance - 1, new_flows, valve, distances)
        result += (minutes - distance - 1) * flow
        max_so_far = max(max_so_far, result)

    return max_so_far

working_flows = {valve: flow for valve, flow in flows.items() if flow > 0}
print(max_flow(30, working_flows, 'AA', distances))