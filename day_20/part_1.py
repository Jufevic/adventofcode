from collections import deque
from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')

listing = []
with open(INPUT_FILE) as f:
    for number in f.read().splitlines():
        listing.append(int(number))

# Mix the file
length = len(listing)
indexes = deque(range(length))
while indexes:
    index = indexes.popleft()
    current = listing.pop(index)
    new_index = (index + current) % (length - 1)
    listing.insert(new_index, current)
    # Insert number at a position before its current position
    if new_index > index:
        for i, update_index in enumerate(indexes):
            if update_index <= new_index:
                indexes[i] -= 1
            else:
                break

# Compute grove coordinates
zero_index = listing.index(0)
total = 0
for coordinate in (1000, 2000, 3000):
    coordinate_index = (zero_index + coordinate) % length
    total += listing[coordinate_index]

print(total)