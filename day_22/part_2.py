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

# For demo input ONLY
# file = DEMO_INPUT_FILE
# SIDE = 4
# tongues = [
#     (11 + 4j, 1, 15 + 8j, -1j),
#     (8 + 3j, -1, 7 + 4j, -1j),
#     (7 + 7j, 1j, 8 + 8j, -1),
#     (3 + 7j, 1j, 8 + 11j, 1j),
#     (7j, -1, 12 + 11j, 1j),
#     (4j, -1j, 11, -1j),
#     (11, 1, 15 + 11j, 1)
# ]

# For real input ONLY
file = INPUT_FILE
SIDE = 50
tongues = [
    (2j * SIDE, -1j, SIDE + SIDE * 1j, -1),
    (3 * SIDE - 1 + (SIDE - 1) * 1j, 1j, 2 * SIDE - 1 + (2 * SIDE - 1) * 1j, 1),
    (2 * SIDE - 1 + (3 * SIDE - 1) * 1j, 1j, SIDE - 1 + (4 * SIDE - 1) * 1j, 1),
    ((3 * SIDE - 1) * 1j, -1, SIDE, -1),
    (3 * SIDE - 1, 1, 2 * SIDE - 1 + (3 * SIDE - 1) * 1j, 1),
    ((4 * SIDE - 1) * 1j, -1, 2 * SIDE - 1, -1j),
    (2 * SIDE, -1j, (4 * SIDE - 1) * 1j, 1j)
]

with open(file) as f:
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
wraps = {}
for start, start_o, end, end_o in tongues:
    for i in range(SIDE):
        wraps[start + i * start_o * 1j, start_o] = end + i * end_o * -1j, -end_o
        wraps[end + i * end_o * -1j, end_o] = start + i * start_o * 1j, -start_o

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
            next_pos, next_orientation = wraps.get((position, orientation),
                (position + orientation, orientation))
            if board[int(next_pos.imag), int(next_pos.real)] == WALL:
                break
            position = next_pos
            orientation = next_orientation

print(f'position={int(position.imag), int(position.real)}')
print(f'orientation={int(orientation.imag), int(orientation.real)}')

password = (1000 * (int(position.imag) + 1) 
    + 4 * (int(position.real) + 1) 
    + int(degrees(phase(orientation)) / 90) % 4)
print(f'{password=}')
