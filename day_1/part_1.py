def read_elf(elf):
    return sum(int(calorie) for calorie in elf.split('\n'))

with open('input.txt') as f:
    elves = f.read().strip().split('\n\n')
    calories = map(read_elf, elves)
print(max(calories))
