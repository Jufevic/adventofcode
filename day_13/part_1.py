from pathlib import Path

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

total = 0
with open(INPUT_FILE) as f:
    for i, block in enumerate(f.read().split('\n\n'), start=1):
        lines = block.splitlines()
        left = eval(lines[0])
        right = eval(lines[1])
        if compare(left, right) == -1:
            total += i

print(total)
