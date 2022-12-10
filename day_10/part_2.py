from pathlib import Path
import numpy as np

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
HEIGHT = 6
WIDTH = 40

x = 1
register = []

with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        if line.startswith('noop'):
            register.append(x)
        else:
            value = int(line.split()[1])
            register.append(x)
            register.append(x)
            x += value

sprite = np.reshape(register, (HEIGHT, WIDTH))
column = np.indices((HEIGHT, WIDTH))[1]
screen = np.full_like(sprite, ' ', dtype=str)
screen[np.abs(sprite - column) <= 1] = '#'
print('\n'.join(''.join(line) for line in screen))
