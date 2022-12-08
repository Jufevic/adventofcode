import numpy as np
from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

array = []
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        line_array = [int(n) for n in line]
        array.append(line_array)
data = np.array(array)

def row_score(line, tree):
    visibility = 0
    max_tree = -1
    for el in line:
        visibility += 1
        max_tree = max(el, max_tree)
        if el >= tree:
            break
    return visibility

def scenic_score(row, col):
    tree = data[row, col]
    total = 1
    for line in (data[row, col+1:], reversed(data[row, :col]), data[row+1:, col], reversed(data[:row, col])):
        total *= row_score(line, tree)
    return total

running_max = 0
height, width = data.shape
for row in range(height):
    for col in range(width):
        running_max = max(running_max, scenic_score(row, col))
print(running_max)
