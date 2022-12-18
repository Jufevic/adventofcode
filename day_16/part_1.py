from pathlib import Path
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

print(flows)
print()
print(connections)