from pathlib import Path

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')


dir_sizes = {}
current_funcs = [dir_sizes.update]
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        # Command line
        if line.startswith('$'):
            command = line[2:]
            # change directory
            if command.startswith('cd'):
                content = command[3:]
                if content == '..':
                    current_funcs.pop()
                else:
                    subdict = {}
                    current_funcs[-1]({content: subdict})
                    current_funcs.append(subdict.update)

        # Output line(s)
        else:
            # new directory
            if line.startswith('dir'):
                dirname = line.split(' ')[1]
                current_funcs[-1]({dirname: {}})
            # new file
            else:
                size, name = line.split(' ')
                size = int(size)
                current_funcs[-1]({name: size})


def total_size(directory, maxsize=100_000):
    """Compute the total size of a directory."""
    # True total
    total = 0
    # Cumulated total, excluding directories > maxsize
    cum_total = 0
    for val in directory.values():
        if isinstance(val, dict):
            subtotal, cum_subtotal = total_size(val)
            total += subtotal
            cum_total += cum_subtotal
        else:
            total += val
    if total <= maxsize:
        return total, cum_total + total
    return total, cum_total

print(total_size(dir_sizes)[1])

# Demo input expected filestructure
expected = {
    '/': {
        'a': {
            'e': {
                'i': 584
            },
            'f': 29116,
            'g': 2557,
            'h.lst': 62596
        },
        'b.txt': 14848514,
        'c.dat': 8504156,
        'd': {
            'j': 4060174,
            'd.log': 8033020,
            'd.ext': 5626152,
            'k': 7214296
        }
    }
}
