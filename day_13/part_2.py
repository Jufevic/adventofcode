from pathlib import Path
from functools import cmp_to_key

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

def compare(left, right):
    """Return -1 if left and right are in the right order,
    1 if in the wrong order and 0 if they compare equally."""
    # Both integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0

    # Both lists
    if isinstance(left, list) and isinstance(right, list):
        for left_item, right_item in zip(left, right):
            result = compare(left_item, right_item)
            if result == 0:
                continue
            elif result == -1:
                return -1
            else:
                return 1
        if len(left) < len(right):
            return -1
        if len(left) > len(right):
            return 1
        else:
            return 0
    
    # Exactly one of (left, right) is an integer
    else:
        if isinstance(left, int):
            left = [left]
        else:
            right = [right]
        return compare(left, right)

with open(INPUT_FILE) as f:
    packets = []
    for line in f.read().splitlines():
        if line:
            packets.append(eval(line))

packets.append([[2]])
packets.append([[6]])
packets.sort(key=cmp_to_key(compare))

first_divider_index = packets.index([[2]]) + 1
second_divider_index = packets.index([[6]]) + 1

print(first_divider_index * second_divider_index)
