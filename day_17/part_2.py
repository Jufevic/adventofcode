from collections import deque
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / 'input.txt'
DEMO_INPUT_FILE = CURRENT_FOLDER / 'demo_input.txt'
IMPRESS_ELEPHANTS = 1_000_000_000_000

SHAPES = (
    ((1, 1, 1, 1),),

    ((0, 1, 0),
     (1, 1, 1),
     (0, 1, 0)),

    ((0, 0, 1),
     (0, 0, 1),
     (1, 1, 1)),

    ((1,),
     (1,),
     (1,),
     (1,)),

    ((1, 1),
     (1, 1))
)
shapes_number = len(SHAPES)
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
cut_rows = 0
chamber = (tuple([True] * (WIDTH + 2)),)
cache = {}

def rock_fall(rock_type: int, jet_index: int, chamber: tuple[tuple[bool]]):
    """Run the simulation for one rock falling down, pushed by the jets until it
    comes to rest."""
    init_jet_index = jet_index
    init_chamber = chamber

    chamber = list(list(line) for line in chamber)

    # A new rock spawns: its left edge is two units away from the left wall and
    # its bottom edge is three units above the highest rock in the room.
    shape = SHAPES[rock_type]
    rock_height = len(shape)
    for _ in range(rock_height + 3):
        chamber = [[True] + [False] * WIDTH + [True]] + chamber
    position = 0, 3

    def can_move(position, direction):
        """Can the rock move from the given position, in the given direction?"""
        row, col = position
        drow, dcol = direction
        for object_row, line in enumerate(shape, start=row):
            for object_col, is_full in enumerate(line, start=col):
                if is_full and chamber[object_row + drow][object_col + dcol]:
                    return False
        return True

    # The rock falls until it comes to rest
    while True:
        jet = jets[jet_index]
        jet_index = (jet_index + 1) % jet_length
        if can_move(position, jet):
            position = position[0] + jet[0], position[1] + jet[1]
        if can_move(position, (1, 0)):
            position = position[0] + 1, position[1]
        else:
            break

    # This rock is added to the obstacles
    row, col = position
    for object_row, line in enumerate(shape, start=row):
        for object_col, is_full in enumerate(line, start=col):
            if is_full:
                chamber[object_row][object_col] = True

    # Simplify the chamber: transform unreachable positions at the bottom into
    # obstacles
    height = len(chamber)
    reachable = {(0, 1)}
    queue = deque([(0, 1)])
    while queue:
        row, col = queue.popleft()
        for drow, dcol in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbour = row + drow, col + dcol
            if (0 <= row + drow < height and not chamber[row + drow][col + dcol]
                    and neighbour not in reachable):
                reachable.add(neighbour)
                queue.append(neighbour)

    for row, line in enumerate(chamber):
        for col, is_full in enumerate(line):
            if not is_full and (row, col) not in reachable:
                chamber[row][col] = True

    # Delete excess rows at the top
    first_row = next(i for i, line in enumerate(chamber) if any(line[1:-1]))
    chamber = chamber[first_row:]

    # Delete excess rows at the bottom
    last_row = next(i for i, line in enumerate(chamber) if all(line[1:-1]))
    deleted_rows = len(chamber) - last_row - 1
    chamber = chamber[:last_row + 1]

    # Visualize the chamber
    # for line in chamber:
    #     str_line = ''
    #     for item in line:
    #         if item:
    #             str_line = str_line + '#'
    #         else:
    #             str_line = str_line + ' '
    #     print(str_line)
    # print()

    chamber = tuple(tuple(line) for line in chamber)
    pass
    for key, value in cache.items():
        cache[key] = value[0] + deleted_rows, value[1], value[2], value[3] + 1
    cache[rock_type, init_jet_index, init_chamber] = deleted_rows, jet_index, chamber, 1
    return deleted_rows, jet_index, chamber

i = 0
# Flag to indicate that the cached mode has already been used
used_cache = False
while i < IMPRESS_ELEPHANTS:
    rock_type = i % shapes_number
    # Cached mode: use the cache to speed up the calculation
    if not used_cache and (rock_type, jet_index, chamber) in cache:
        deleted_rows, jet_index, chamber, fallen_rocks = cache[rock_type, 
            jet_index, chamber]
        block_rows = (IMPRESS_ELEPHANTS - i) // fallen_rocks
        cut_rows += block_rows * deleted_rows
        i += block_rows * fallen_rocks + 1
        used_cache = True
    # Normal mode: rocks fall one by one
    else:
        deleted_rows, jet_index, chamber = rock_fall(rock_type, jet_index, chamber)
        cut_rows += deleted_rows
        i += 1


chamber_height = len(chamber) - 1
print(cut_rows + chamber_height)