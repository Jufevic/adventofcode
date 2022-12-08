from functools import reduce
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

height, width = data.shape
filler_row = np.full((1, width), -1)
top_visible = (data > np.concatenate((filler_row, np.maximum.accumulate(data[:-1, :]))))

bottom_visible = (data > np.flipud(np.concatenate((filler_row, np.maximum.accumulate(np.flipud(data[1:, :]))))))

filler_col = np.full((height, 1), -1)
left_visible = (data > np.concatenate((filler_col, np.maximum.accumulate(data[:, :-1], axis=1)), axis=1))

right_visible = (data > np.fliplr(np.concatenate((filler_col, np.maximum.accumulate(np.fliplr(data[:, 1:]), axis=1)), axis=1)))

any_visible = top_visible | bottom_visible | left_visible | right_visible
print(any_visible.sum())
