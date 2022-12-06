from string import ascii_letters as alphabet
from itertools import islice

total = 0
with open('input.txt') as f:
    while (batch := list(islice(f, 3))):
        r1, r2, r3 = map(str.strip, batch)
        common = set.intersection(set(r1), set(r2), set(r3))
        total += alphabet.index(list(common)[0]) + 1
print(total)
