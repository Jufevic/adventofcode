from pathlib import Path
import numpy as np

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

def save_sizes():
    """Avoid declaring `sizes` as a global variable by nesting function."""
    sizes = []
    def total_size(directory):
        """Compute the total size of a directory."""
        total = 0
        for val in directory.values():
            if isinstance(val, dict):
                subtotal = total_size(val)
                total += subtotal
            else:
                total += val
        sizes.append(total)
        return total
    
    to_free = total_size(dir_sizes) - 40_000_000
    return min(size for size in sizes if size >= to_free)

print(save_sizes())
