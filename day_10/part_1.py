from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')


register = []
x = 1

with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        if line.startswith('noop'):
            register.append(x)
        else:
            value = int(line.split()[1])
            register.append(x)
            register.append(x)
            x += value

print(sum(cycle * register[cycle - 1] for cycle in range(20, 221, 40)))
