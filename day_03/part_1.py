from string import ascii_letters as alphabet

total = 0
with open('input.txt') as f:
    for rucksack in f.read().splitlines():
        n = len(rucksack) // 2
        left, right = rucksack[:n], rucksack[n:]
        common = set.intersection(set(left), set(right))
        total += alphabet.index(list(common)[0]) + 1
print(total)
