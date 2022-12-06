length = 14
with open('input.txt') as f:
    line = f.read().strip()
    for i in range(len(line) - length):
        if len(set(line[i:i + length])) == length:
            break

print(i + length)
