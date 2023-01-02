from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'

ROCK_TYPES = [
    [[1, 1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1, 1],
     [1, 1]]
]
WIDTH = 7

jets = []
with open(INPUT_FILE) as f:
    for jet in f.read().strip():
        if jet == '>':
            jets.append((0, 1))
        else:
            jets.append((0, -1))

jet_length = len(jets)
jet_index = 0
chamber = [[1] * (WIDTH + 2)]
for i in range(2022):
    rock = ROCK_TYPES[i % len(ROCK_TYPES)]
    def visualize():
        for line in chamber:
            str_line = ''
            for item in line:
                if item:
                    str_line = str_line + '#'
                else:
                    str_line = str_line + ' '
            print(str_line)
        print()

    # A new rock spawns
    max_height = next(i for i, line in enumerate(chamber) if any(line[1:-1]))
    rock_height = len(rock)
    empties = rock_height - max_height + 3
    if empties < 0:
        chamber = chamber[-empties:]
    for _ in range(empties):
        chamber = [[1] + [0] * WIDTH + [1]] + chamber
    position = 0, 3
    # visualize()

    def try_moving(position, direction):
        row, col = position
        drow, dcol = direction
        blocked = False
        for object_row, line in enumerate(rock):
            for object_col, is_full in enumerate(line):
                if is_full and chamber[object_row + row + drow][object_col + col + dcol]:
                    blocked = True
                    break
        if blocked:
            return position
        return (row + drow, col + dcol)

    # The rock falls until it comes to rest
    while True:
        jet = jets[jet_index]
        jet_index = (jet_index + 1) % jet_length
        position = try_moving(position, jet)
        new_position = try_moving(position, (1, 0))
        if new_position == position:
            break
        position = new_position
    
    # This rock is added to the obstacles
    row, col = position
    for object_row, line in enumerate(rock):
        for object_col, is_full in enumerate(line):
            if is_full:
                chamber[object_row + row][object_col + col] = 1

max_height = next(i for i, line in enumerate(chamber) if any(line[1:-1]))
print(len(chamber) - max_height - 1)