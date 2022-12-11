from pathlib import Path
from parse import parse
from collections import deque
from heapq import nlargest
from math import lcm

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
TURNS = 10_000

monkeys = {}

# Parse input file
with open(INPUT_FILE) as f:
    for block in f.read().split('\n\n'):
        lines = iter(block.splitlines())
        monkey_number = parse('Monkey {:d}:', next(lines))[0]
        monky = {
            'items': parse('  Starting items: {}', next(lines))[0],
            'operation': parse('  Operation: new = {}', next(lines))[0],
            'divisor': parse('  Test: divisible by {:d}', next(lines))[0],
            'if_true': parse('    If true: throw to monkey {:d}', next(lines))[0],
            'if_false': parse('    If false: throw to monkey {:d}', next(lines))[0],
        }
        monky['items'] = deque([int(item) for item in monky['items'].split(', ')])
        monkeys[monkey_number] = monky

least_common_multiple = lcm(*[monkey['divisor'] for monkey in monkeys.values()])

# Make the items turn and count the number of inspections
inspections = {monkey: 0 for monkey in monkeys}
for turn in range(TURNS):
    for monkey_number, specs in monkeys.items():
        while specs['items']:
            old = specs['items'].popleft()
            # Trick to avoid dealing with huge numbers: modulo
            new = eval(specs['operation']) % least_common_multiple
            # Is the current worry level divisible by `divisor` ?
            if (new % specs['divisor']) == 0:
                monkeys[specs['if_true']]['items'].append(new)
            else:
                monkeys[specs['if_false']]['items'].append(new)
            inspections[monkey_number] += 1

total = nlargest(2, inspections.values())
print(total[0] * total[1])