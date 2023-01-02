from pathlib import Path
from numpy import base_repr

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'

def SNAFU_to_int(number):
    transtab = str.maketrans({'2': '4', '1': '3', '0': '2', '-': '1', '=': '0'})
    offset = number.translate(transtab)
    return int(offset, base=5) - int('2' * len(offset), base=5)

def int_to_SNAFU(number):
    string = base_repr(number, base=5)
    width = len(string)
    if string[0] in '34':
        width += 1
    number += int('2' * width, base=5)
    string = base_repr(number, base=5)
    transtab = str.maketrans({'4': '2', '3': '1', '2': '0', '1': '-', '0': '='})
    string = string.translate(transtab)
    return string

total = 0
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        total += SNAFU_to_int(line)

SNAFU = int_to_SNAFU(total)
print(f'{total=}')
print(f'SNAFU total: {SNAFU}')
