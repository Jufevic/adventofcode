from parse import parse

fully_contained = 0
with open('input.txt') as f:
    for line in f:
        a, b, c, d = parse('{:d}-{:d},{:d}-{:d}', line.strip())
        starts = sorted((a, c))
        ends = sorted((b, d))
        if ends[0] >= starts[1]:
            fully_contained += 1
print(fully_contained)
