from pathlib import Path
import numpy as np

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
DECRYPTION_KEY = 811589153
MIXINGS = 10

listing = []
with open(INPUT_FILE) as f:
    for number in f.read().splitlines():
        listing.append(int(number) * DECRYPTION_KEY)

length = len(listing)
indexes = np.arange(length)

def mix(listing, indexes):
    """Mix the listing"""
    for order, index in enumerate(indexes):
        current = listing.pop(index)
        new_index = (index + current) % (length - 1)
        listing.insert(new_index, current)
        min_idx = min(index, new_index)
        max_idx = max(index, new_index)
        offset = np.sign(index - new_index)
        indexes[(min_idx <= indexes) & (indexes <= max_idx)] += offset
        indexes[order] = new_index
    return listing, indexes

for _ in range(MIXINGS):
    listing, indexes = mix(listing, indexes)

# Compute grove coordinates
zero_index = listing.index(0)
total = 0
for coordinate in (1000, 2000, 3000):
    coordinate_index = (zero_index + coordinate) % length
    total += listing[coordinate_index]

print(total)