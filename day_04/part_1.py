from parse import parse

fully_contained = 0
with open('input.txt') as f:
    for line in f:
        a, b, c, d = parse('{:d}-{:d},{:d}-{:d}', line.strip())
        if (a >= c and b <= d) or (a <= c and b >= d):
            fully_contained += 1
print(fully_contained)
