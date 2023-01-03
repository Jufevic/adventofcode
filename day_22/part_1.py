from pathlib import Path
from cmath import phase
from math import degrees
import numpy as np

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'
VOID = ' '
OPEN = '.'
WALL = '#'

with open(DEMO_INPUT_FILE) as f:
    board_str, instr_str = f.read().split('\n\n')

# Build the instructions list
instructions = []
buffer = ''
for letter in instr_str:
    if letter in 'LR':
        if buffer:
            instructions.append(int(buffer))
            buffer = ''
        instructions.append(letter)
    else:
        buffer = buffer + letter
if buffer:
    instructions.append(int(buffer))

# Build the board, filling up with void to get a rectangular board.
lines = board_str.splitlines()
height = len(lines)
width = max(len(line) for line in lines)
board = np.full((height, width), VOID)
for row, line in enumerate(lines):
    board[row, :] = list(line.ljust(width, VOID))

# Construct wrap around map
not_void = (board != VOID)
first_col = not_void.argmax(axis=1)
last_col = width - 1 - np.fliplr(not_void).argmax(axis=1)
first_row = not_void.argmax(axis=0)
last_row = height - 1 - np.flipud(not_void).argmax(axis=0)
wraps = {}
for row, (start, end) in enumerate(zip(first_col, last_col)):
    wraps[1j * row + start, -1] = end + 1j * row
    wraps[1j * row + end, 1] = start + 1j * row
for col, (start, end) in enumerate(zip(first_row, last_row)):
    wraps[1j * start + col, -1j] = col + 1j * end
    wraps[1j * end + col, 1j] = col + 1j * start

# Initialization
position = complex(np.argmax(board[0, :] == OPEN), 0)
orientation = 1

# Follow the instructions one by one
for instruction in instructions:
    if isinstance(instruction, str):
        # Rotate left
        if instruction == 'L':
            orientation *= -1j
        # Rotate right
        else:
            orientation *= 1j
    # Move forward
    else:
        for _ in range(instruction):
            next_pos = wraps.get((position, orientation),
                                 position + orientation)
            if board[int(next_pos.imag), int(next_pos.real)] == WALL:
                break
            position = next_pos

print(f'position={int(position.imag), int(position.real)}')
print(f'orientation={int(orientation.imag), int(orientation.real)}')

password = (1000 * (int(position.imag) + 1) 
    + 4 * (int(position.real) + 1) 
    + int(degrees(phase(orientation)) / 90) % 4)
print(f'{password=}')
