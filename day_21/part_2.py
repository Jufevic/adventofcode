from pathlib import Path
from sympy import Eq, symbols, sympify, solve

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

monkeys = {}
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        monkey, job = line.split(': ')
        if monkey == 'root':
            left_member, operation, right_member = job.split()
        elif monkey == 'humn':
            continue
        else:
            monkeys[monkey] = job.strip()

def solve_monkey(monkeys, left, right, variable='humn'):

    def monkey_eq(monkey):
        job = monkeys[monkey]
        if job.isdecimal():
            return int(job)
        left, _, right = job.split()
        eq = Eq(sympify(monkey), sympify(job))
        if left != variable:
            left_eq = monkey_eq(left)
            eq = eq.subs(left, left_eq)
        if right != variable:
            right_eq = monkey_eq(right)
            eq = eq.subs(right, right_eq)
        return solve(eq, symbols(monkey))[0]

    eq = Eq(sympify(left_member), sympify(right_member))
    eq = eq.subs(left_member, monkey_eq(left_member))
    eq = eq.subs(right_member, monkey_eq(right_member))
    humn = symbols(variable)
    print(solve(eq, humn)[0])

solve_monkey(monkeys, left_member, right_member)