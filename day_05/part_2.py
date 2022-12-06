from parse import parse

with open('input.txt') as f:
    input_lines = []
    for line in f:
        line = line.rstrip()
        if not line:
            break
        input_lines.append(line)
    # Construct initial stacks
    number_line = input_lines.pop().strip()
    stack_numbers = map(int, number_line.split('   '))
    stacks = []
    for number in stack_numbers:
        stack = []
        for line in input_lines:
            if len(line) >= 4 * number - 1 and (letter := line[4 * number - 3]).isalpha():
                stack.append(letter)
        stacks.append(stack)
    
    # Follow instructions
    for line in f:
        line = line.rstrip()
        amount, start, end = parse('move {:d} from {:d} to {:d}', line)
        temp = stacks[start - 1][:amount]
        stacks[start - 1] = stacks[start - 1][amount:]
        stacks[end - 1] = temp + stacks[end - 1]

print(''.join(stack[0] for stack in stacks))
