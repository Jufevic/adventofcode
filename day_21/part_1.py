from pathlib import Path
from operator import add, sub, mul, truediv

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

monkeys = {}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        monkey, job = line.split(': ')
        monkeys[monkey] = job.strip()

def monkey_yell(monkey, monkeys):
    job = monkeys[monkey]
    if job.isdecimal():
        return int(job)
    left, operation, right = job.split()
    func = {'+': add, '-': sub, '*': mul, '/': truediv}[operation]
    return func(monkey_yell(left, monkeys), monkey_yell(right, monkeys))

print(monkey_yell('root', monkeys))